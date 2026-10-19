"""Keep observable declarations separate from people, execution and adoption."""
from datetime import datetime,timezone
import hashlib
import json
from pathlib import PurePosixPath
import re
import ssl
import tomllib
from urllib.error import HTTPError,URLError
from urllib.parse import urlparse,quote
from urllib.request import Request,build_opener,HTTPSHandler,HTTPRedirectHandler

ALLOWED_HOSTS={'api.github.com','raw.githubusercontent.com','github.com','release-assets.githubusercontent.com','objects.githubusercontent.com'}
def sha(data):return hashlib.sha256(data).hexdigest()
def repo_name(value):
    if not isinstance(value,str) or not re.fullmatch(r'[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+',value):raise ValueError('invalid_repository')
    return value
def commit_id(value):
    if not isinstance(value,str) or not re.fullmatch(r'[0-9a-f]{40}',value):raise ValueError('pinned_commit_required')
    return value
def safe_path(value):
    if not isinstance(value,str) or not value or PurePosixPath(value).is_absolute() or '..' in PurePosixPath(value).parts or '\\' in value:raise ValueError('invalid_manifest_path')
    return value
def checked_url(url):
    parsed=urlparse(url)
    if parsed.scheme!='https' or parsed.hostname not in ALLOWED_HOSTS or parsed.username or parsed.password or parsed.port not in (None,443):raise ValueError('public_github_https_required')
    return url
class PublicRedirect(HTTPRedirectHandler):
    max_redirections=4
    def redirect_request(self,req,fp,code,msg,headers,newurl):
        checked_url(newurl);return super().redirect_request(req,fp,code,msg,headers,newurl)
def fetch_public(url,max_bytes=2000000):
    import certifi
    checked_url(url);request=Request(url,headers={'User-Agent':'oss-evidence-atlas/0.1 public-evidence'})
    try:
        with build_opener(PublicRedirect(),HTTPSHandler(context=ssl.create_default_context(cafile=certifi.where()))).open(request,timeout=20) as stream:
            data=stream.read(max_bytes+1)
            if len(data)>max_bytes:raise ValueError('public_artifact_size_limit')
            return data
    except HTTPError as error:raise ValueError('public_http_'+str(error.code)) from None
    except (URLError,TimeoutError):raise ValueError('public_fetch_failed') from None

def normalize_python(name):return re.sub(r'[-_.]+','-',name).lower()
def declared_dependencies(path,raw):
    if not isinstance(raw,bytes) or len(raw)>2000000:raise ValueError('invalid_manifest')
    text=raw.decode('utf-8');name=PurePosixPath(safe_path(path)).name;rows=[]
    if name=='package.json':
        data=json.loads(text)
        for section,scope in [('dependencies','runtime'),('devDependencies','development'),('optionalDependencies','optional'),('peerDependencies','peer')]:
            items=data.get(section,{})
            if not isinstance(items,dict):raise ValueError('invalid_npm_section')
            for package,version in items.items():
                if not isinstance(version,str):raise ValueError('invalid_npm_version')
                rows.append({'ecosystem':'npm','name':package,'declared_version':version,'scope':scope,'section':section})
    elif name=='pyproject.toml':
        data=tomllib.loads(text).get('project',{});groups=[('dependencies',data.get('dependencies',[]),'runtime')]
        groups.extend(('optional-dependencies.'+group,values,'optional') for group,values in data.get('optional-dependencies',{}).items())
        for section,values,scope in groups:
            if not isinstance(values,list):raise ValueError('invalid_python_dependencies')
            for value in values:
                if not isinstance(value,str) or not re.match(r'^[A-Za-z0-9][A-Za-z0-9_.-]*',value):raise ValueError('unsupported_python_requirement')
                package=re.match(r'^([A-Za-z0-9][A-Za-z0-9_.-]*)',value).group(1)
                rows.append({'ecosystem':'pypi','name':normalize_python(package),'declared_version':value[len(package):].strip(),'scope':scope,'section':section})
    else:raise ValueError('unsupported_manifest_format')
    return rows

def manifest_evidence(repo,commit,path,raw,ecosystem,target,publisher_owner,fork=False):
    repo_name(repo);commit_id(commit);safe_path(path)
    if ecosystem not in ('npm','pypi') or not isinstance(target,str) or not target or not isinstance(publisher_owner,str) or not publisher_owner or type(fork)is not bool:raise ValueError('invalid_target')
    expected=normalize_python(target) if ecosystem=='pypi' else target
    claims=[]
    for entry in declared_dependencies(path,raw):
        if entry['ecosystem']!=ecosystem or entry['name']!=expected:continue
        claim={'repository':repo,'commit':commit,'manifest_path':path,'manifest_sha256':sha(raw),'dependency':entry,'same_github_owner':repo.split('/')[0].lower()==publisher_owner.lower(),'fork':fork,'evidence_kind':'direct_manifest_declaration','runtime_execution_proven':False,'human_adoption_proven':False,'source_url':f'https://github.com/{repo}/blob/{commit}/{quote(path,safe="/")}'}
        claim['id']=sha(json.dumps({k:claim[k] for k in ('repository','commit','manifest_path','dependency')},sort_keys=True).encode());claims.append(claim)
    return {'repository':repo,'commit':commit,'manifest_path':path,'manifest_sha256':sha(raw),'target':{'ecosystem':ecosystem,'name':target},'claims':claims,'absence_is_not_proof_of_nonuse':True}

def collect_manifest(repo,path,ecosystem,target,publisher_owner,ref='HEAD',fetch=fetch_public):
    repo_name(repo);safe_path(path)
    if not isinstance(ref,str) or not re.fullmatch(r'[A-Za-z0-9_./-]{1,100}',ref):raise ValueError('invalid_ref')
    meta=json.loads(fetch(f'https://api.github.com/repos/{repo}'))
    if meta.get('private') is not False:raise ValueError('public_repository_required')
    if ref=='HEAD':ref=meta['default_branch']
    commit=json.loads(fetch(f'https://api.github.com/repos/{repo}/commits/{quote(ref,safe="")}'))['sha'];commit_id(commit)
    raw=fetch(f'https://raw.githubusercontent.com/{repo}/{commit}/{quote(path,safe="/")}')
    return {**manifest_evidence(repo,commit,path,raw,ecosystem,target,publisher_owner,meta.get('fork',False)),'observed_at':datetime.now(timezone.utc).isoformat(),'authenticated':False}

def summarize_claims(records):
    claims={claim['id']:claim for record in records for claim in record.get('claims',[])}
    return {'unique_declarations':len(claims),'same_owner_declarations':sum(c['same_github_owner'] for c in claims.values()),'different_owner_nonfork_declarations':sum(not c['same_github_owner'] and not c['fork'] for c in claims.values()),'fork_declarations':sum(c['fork'] for c in claims.values()),'human_adoption_proven':False,'runtime_execution_proven':False,'scope':'supplied_repositories_and_manifests_only','declarations':list(claims.values())}

def freshness(contract,current_bytes,replay=None):
    if not isinstance(contract,dict) or not re.fullmatch(r'[0-9a-f]{64}',contract.get('source_sha256','')) or not isinstance(current_bytes,bytes):raise ValueError('invalid_freshness_contract')
    same=sha(current_bytes)==contract['source_sha256']
    replayed=replay is not None
    if replayed and (not isinstance(replay,dict) or type(replay.get('passed'))is not bool):raise ValueError('invalid_replay_receipt')
    target=contract.get('reproducer',{});repo_name(target.get('repository'));commit_id(target.get('commit'))
    if not isinstance(target.get('check_id'),str) or not target['check_id']:raise ValueError('invalid_reproducer_contract')
    if replayed and any(replay.get(k)!=target[k] for k in ('repository','commit','check_id')):raise ValueError('receipt_does_not_match_reproducer')
    status='source_changed_requires_review' if not same else 'reproduction_failed' if replayed and not replay['passed'] else 'current_and_reproduced' if replayed else 'current_not_replayed'
    return {'status':status,'source_matches_snapshot':same,'source_sha256':sha(current_bytes),'replay_passed':replay['passed'] if replayed else None,'novelty_or_sota_proven':False}

def audit_release(card,fetch=fetch_public):
    repo=repo_name(card['repository']);commit=commit_id(card['commit']);path=safe_path(card.get('source_path','pyproject.toml'));asset=card['wheel']
    if not re.fullmatch(r'[A-Za-z0-9_.+-]+\.whl',asset['name']) or not re.fullmatch(r'[0-9a-f]{64}',asset['sha256']) or not re.fullmatch(r'[A-Za-z0-9_.-]+',card['tag']):raise ValueError('invalid_release_card')
    result={'repository':repo,'commit':commit,'authenticated':False,'human_adoption_proven':False}
    if not re.fullmatch(r'[0-9a-f]{64}',card.get('source_sha256','')):raise ValueError('source_hash_required')
    try:source=fetch(f'https://raw.githubusercontent.com/{repo}/{commit}/{quote(path,safe="/")}');result['source_anonymous']=True;result['source_sha256']=sha(source);result['source_hash_matches']=sha(source)==card['source_sha256']
    except ValueError as error:result['source_anonymous']=False;result['source_error']=str(error)
    try:
        data=fetch(f'https://github.com/{repo}/releases/download/{card["tag"]}/{asset["name"]}',max_bytes=32000000);result['wheel_anonymous']=True;result['wheel_hash_matches']=sha(data)==asset['sha256']
    except ValueError as error:result['wheel_anonymous']=False;result['wheel_hash_matches']=False;result['wheel_error']=str(error)
    result['passed']=result['source_anonymous'] and result.get('source_hash_matches',False) and result['wheel_anonymous'] and result['wheel_hash_matches'];return result
