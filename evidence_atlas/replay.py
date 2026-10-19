"""Only registered demos run, after pinned source checks; no manifest shell commands."""
from datetime import datetime,timezone
import hashlib
import json
import os
import re
from pathlib import Path
import subprocess
import sys
from .evidence import repo_name,commit_id

REGISTRY={
 'mission-intent-repair':('mission_repair',0),
 'fab-discovery-loop':('fab_discovery',0),
 'sql-meaning-mutator':('sql_meaning',1),
 'robot-dataset-crash-lab':('robot_crash',0),
 'synthcase-forge':('synthcase',0),
 'invoice-acceptance-contracts':('invoice_contract',0),
 'agent-compensation-map':('compensation_map',0),
 'resource-outage-explorer':('outage_explorer',0),
 'emotion-lens-lab':('emotion_lens',0),
 'brain-breakers':('brain_breakers',0),
 'hedge-counterexample':('hedge_counterexample',0),
 'semantic-plan-compiler':('semantic_plan',0),
}
EXPECTATIONS={
 'mission-intent-repair':[(('outage','utility'),8),(('outage','replay','valid'),True),(('outage','plan','calibrate'),0)],
 'fab-discovery-loop':[(('recommendation',),'p3-d2'),(('hardware_executed',),False)],
 'sql-meaning-mutator':[(('status',),'counterexample'),(('seed_equal',),True),(('row_count',),4)],
 'robot-dataset-crash-lab':[(('real_process_kills',),8),(('safe_protocol_passed',),True),(('broken_control_detected',),True)],
 'synthcase-forge':[(('dataset','status'),'complete'),(('dataset','synthetic'),True)],
 'invoice-acceptance-contracts':[(('audit','status'),'blocked'),(('proposal','after_line_subtotal'),'12.50'),(('proposal','audit','status'),'ready_for_review')],
 'agent-compensation-map':[(('verification','valid'),True),(('verification','worlds_checked'),3),(('worst_case_cost',),9)],
 'resource-outage-explorer':[(('baseline','worst','shortfall'),6),(('baseline','worst','flow','certificate','valid'),True),(('best_single_catalog_upgrade',),'independent-backup')],
 'emotion-lens-lab':[(('observed_reader_cells',),7),(('possible_reader_cells',),8),(('human_accuracy_measured',),False)],
 'brain-breakers':[(('paired_trials',),4),(('injected_detected',),4),(('repaired_passed',),4)],
 'hedge-counterexample':[(('worst','payoff','settled_net_cents'),-924),(('witness_replay','valid'),True)],
 'semantic-plan-compiler':[(('provider_calls',),4),(('questions_sent',),6),(('status',),'completed')],
}
def assertions(slug,payload):
    results=[]
    for path,expected in EXPECTATIONS[slug]:
        actual=payload
        try:
            for part in path:actual=actual[part]
        except (KeyError,TypeError):actual=None
        results.append({'path':list(path),'expected':expected,'actual':actual,'passed':type(actual)is type(expected) and actual==expected})
    return results
def git(path,*args):return subprocess.check_output(['git','-C',str(path),*args],text=True,timeout=10).strip()
def replay(card,checkout,python=None,kind='demo'):
    repository=repo_name(card['repository']);commit=commit_id(card['commit']);slug=repository.split('/')[1]
    if repository!='gbesse/'+slug or slug not in REGISTRY:raise ValueError('unregistered_demo')
    path=Path(checkout).resolve()
    if git(path,'rev-parse','HEAD')!=commit:raise ValueError('checkout_commit_mismatch')
    if git(path,'status','--porcelain','--untracked-files=normal'):raise ValueError('checkout_not_clean')
    remote=git(path,'remote','get-url','origin').removesuffix('.git')
    if remote not in ('https://github.com/'+repository,'git@github.com:'+repository):raise ValueError('checkout_remote_mismatch')
    module,expected_exit=REGISTRY[slug]
    if kind not in ('demo','unit','browser'):raise ValueError('unregistered_check_kind')
    env={k:v for k,v in os.environ.items() if k in ('PATH','LANG','LC_ALL','TMPDIR','SYSTEMROOT')};env['PYTHONDONTWRITEBYTECODE']='1'
    env['PYTHON']=python or sys.executable
    command=[python or sys.executable,'-m',module,'demo'] if kind=='demo' else [python or sys.executable,'-m','unittest','discover','-s','tests','-q'] if kind=='unit' else ['node','tests/browser.mjs']
    if kind!='demo':expected_exit=0
    result=subprocess.run(command,cwd=path,env=env,capture_output=True,timeout=120)
    if len(result.stdout)>2000000:raise ValueError('demo_output_budget')
    try:payload=json.loads(result.stdout)
    except (ValueError,UnicodeError):payload=None
    checks=assertions(slug,payload) if kind=='demo' and isinstance(payload,dict) else []
    unit_count=re.search(r'Ran (\d+) tests?',result.stderr.decode(errors='replace'));skipped=re.search(r'skipped=(\d+)',result.stderr.decode(errors='replace'))
    substantive=all(c['passed'] for c in checks) and bool(checks) if kind=='demo' else unit_count is not None and int(unit_count.group(1))>0 and skipped is None if kind=='unit' else True
    return {'repository':repository,'commit':commit,'check_id':'registered_'+kind,'passed':result.returncode==expected_exit and substantive,'expected_exit':expected_exit,'exit_code':result.returncode,'stdout_sha256':hashlib.sha256(result.stdout).hexdigest(),'json_object':isinstance(payload,dict),'assertions':checks,'tests_run':int(unit_count.group(1)) if unit_count else None,'tests_skipped':int(skipped.group(1)) if skipped else 0,'observed_at':datetime.now(timezone.utc).isoformat(),'external_provider_credentials_forwarded':False}

def coverage(requirements,cards,receipts):
    if not isinstance(requirements,list) or not 1<=len(requirements)<=500 or len({r.get('id') for r in requirements})!=len(requirements):raise ValueError('unique_nonempty_requirements_required')
    if len({c['repository'] for c in cards})!=len(cards):raise ValueError('duplicate_repository_card')
    for card in cards:
        pin=card['commit']
        if not isinstance(pin,str) or not (re.fullmatch(r'[0-9a-f]{40}',pin) or card['repository']=='gbesse/oss-evidence-atlas' and re.fullmatch(r'package-sha256:[0-9a-f]{64}',pin)):raise ValueError('invalid_source_pin')
    if len({(r['repository'],r['commit'],r['check_id']) for r in receipts})!=len(receipts):raise ValueError('duplicate_receipt')
    by_repo={c['repository']:c for c in cards};by_receipt={(r['repository'],r['commit'],r['check_id']):r for r in receipts};rows=[]
    for requirement in requirements:
        card=by_repo.get(requirement['repository']);receipt=by_receipt.get((card['repository'],card['commit'],'registered_demo')) if card else None
        required=requirement.get('required_checks',['demo','unit','browser']);checks=[by_receipt.get((card['repository'],card['commit'],'registered_'+kind)) if card else None for kind in required]
        if not isinstance(required,list) or not required or set(required)-{'demo','unit','browser'} or len(set(required))!=len(required):raise ValueError('invalid_required_checks')
        rows.append({**requirement,'status':'reproduced' if all(r and r['passed'] for r in checks) else 'not_reproduced','receipts':checks})
    return {'requirements':rows,'total':len(rows),'reproduced':sum(r['status']=='reproduced' for r in rows),'all_reproduced':all(r['status']=='reproduced' for r in rows),'note':'A demo replay is a smoke check; per-capability unit/browser evidence remains linked separately.'}
