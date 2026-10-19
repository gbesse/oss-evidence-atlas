import json
import unittest
import tempfile
from pathlib import Path
from unittest.mock import patch
from evidence_atlas.evidence import manifest_evidence,summarize_claims,freshness,collect_manifest,checked_url,audit_release,sha
from evidence_atlas.replay import assertions,coverage,replay
COMMIT='a'*40
class EvidenceTests(unittest.TestCase):
    def test_npm_dependency_scopes_and_exact_target_not_substring(self):
        raw=json.dumps({'dependencies':{'tool':'^1','tool-extra':'2'},'devDependencies':{'tool':'1.2'}}).encode();r=manifest_evidence('outside/app',COMMIT,'package.json',raw,'npm','tool','publisher');self.assertEqual(len(r['claims']),2);self.assertEqual({c['dependency']['scope'] for c in r['claims']},{'runtime','development'});self.assertTrue(all(not c['human_adoption_proven'] for c in r['claims']))
    def test_python_pep503_names_and_optional_scope(self):
        raw=b'[project]\ndependencies = ["My_Tool>=1; python_version >= \'3.11\'"]\n[project.optional-dependencies]\ntest = ["my-tool==1.2"]\n';r=manifest_evidence('outside/app',COMMIT,'pyproject.toml',raw,'pypi','my.tool','publisher');self.assertEqual(len(r['claims']),2);self.assertEqual(r['claims'][1]['dependency']['scope'],'optional')
    def test_same_owner_forks_and_dedup_do_not_prove_human_use(self):
        raw=b'{"dependencies":{"tool":"1"}}';a=manifest_evidence('publisher/app',COMMIT,'package.json',raw,'npm','tool','publisher');b=manifest_evidence('outside/fork',COMMIT,'package.json',raw,'npm','tool','publisher',True);r=summarize_claims([a,a,b]);self.assertEqual(r['unique_declarations'],2);self.assertEqual(r['same_owner_declarations'],1);self.assertEqual(r['fork_declarations'],1);self.assertFalse(r['human_adoption_proven']);self.assertEqual(r['different_owner_nonfork_declarations'],0)
    def test_missing_manifest_declaration_is_not_nonuse_proof(self):
        r=manifest_evidence('outside/app',COMMIT,'package.json',b'{}','npm','tool','publisher');self.assertEqual(r['claims'],[]);self.assertTrue(r['absence_is_not_proof_of_nonuse'])
    def test_public_collection_pins_commit_before_fetch_and_uses_no_auth(self):
        urls=[]
        def fetch(url):
            urls.append(url)
            if '/commits/' in url:return json.dumps({'sha':COMMIT}).encode()
            if 'api.github' in url:return b'{"private":false,"fork":false,"default_branch":"main"}'
            return b'{"dependencies":{"tool":"1.2.3"}}'
        r=collect_manifest('outside/app','package.json','npm','tool','publisher',fetch=fetch);self.assertFalse(r['authenticated']);self.assertIn(COMMIT,urls[-1]);self.assertEqual(r['claims'][0]['dependency']['declared_version'],'1.2.3')
    def test_private_repository_is_not_collected(self):
        with self.assertRaises(ValueError):collect_manifest('outside/app','package.json','npm','tool','publisher',fetch=lambda _:b'{"private":true}')
    def test_ssrf_auth_urls_paths_and_unpinned_commits_rejected(self):
        for url in ['http://github.com/a','https://127.0.0.1/a','https://github.com.evil/a','https://user:pass@github.com/a','file:///tmp/a','https://github.com:8443/a']:
            with self.assertRaises(ValueError):checked_url(url)
        with self.assertRaises(ValueError):manifest_evidence('outside/app','main','package.json',b'{}','npm','tool','publisher')
        with self.assertRaises(ValueError):manifest_evidence('outside/app',COMMIT,'../package.json',b'{}','npm','tool','publisher')
    def contract(self):return {'source_sha256':sha(b'original'),'reproducer':{'repository':'gbesse/sql-meaning-mutator','commit':COMMIT,'check_id':'registered_demo'}}
    def test_fresh_source_does_not_claim_reproduction_without_receipt(self):self.assertEqual(freshness(self.contract(),b'original')['status'],'current_not_replayed')
    def test_stale_source_requires_review_even_when_demo_still_passes(self):
        c=self.contract();r=freshness(c,b'changed',{**c['reproducer'],'passed':True});self.assertEqual(r['status'],'source_changed_requires_review');self.assertFalse(r['novelty_or_sota_proven'])
    def test_failed_or_mismatched_reproduction_receipt(self):
        c=self.contract();self.assertEqual(freshness(c,b'original',{**c['reproducer'],'passed':False})['status'],'reproduction_failed')
        with self.assertRaises(ValueError):freshness(c,b'original',{**c['reproducer'],'commit':'b'*40,'passed':True})
    def test_release_requires_anonymous_source_and_matching_wheel_hash(self):
        source=b'source';wheel=b'wheel';card={'repository':'gbesse/tool','commit':COMMIT,'tag':'v1','source_sha256':sha(source),'wheel':{'name':'tool.whl','sha256':sha(wheel)}}
        self.assertTrue(audit_release(card,fetch=lambda url,**_:source if 'raw.' in url else wheel)['passed'])
        self.assertFalse(audit_release(card,fetch=lambda url,**_:source if 'raw.' in url else b'tampered')['passed'])
    def test_capability_assertions_reject_just_valid_but_wrong_json(self):self.assertFalse(all(c['passed'] for c in assertions('hedge-counterexample',{})))
    def test_coverage_exposes_missing_stale_and_failed_receipts(self):
        requirements=[{'id':'one','repository':'gbesse/tool'}];cards=[{'repository':'gbesse/tool','commit':COMMIT}];receipts=[{'repository':'gbesse/tool','commit':COMMIT,'check_id':'registered_'+kind,'passed':True} for kind in ('demo','unit','browser')]
        self.assertTrue(coverage(requirements,cards,receipts)['all_reproduced']);self.assertFalse(coverage(requirements,cards,receipts[:-1])['all_reproduced']);receipts[0]['commit']='b'*40;self.assertFalse(coverage(requirements,cards,receipts)['all_reproduced'])
    def test_duplicate_requirements_and_empty_checks_fail(self):
        r={'id':'one','repository':'gbesse/tool','required_checks':[]}
        with self.assertRaises(ValueError):coverage([r,r],[],[])
        with self.assertRaises(ValueError):coverage([r],[],[])
    def test_unregistered_replay_is_rejected_before_execution(self):
        with self.assertRaises(ValueError):replay({'repository':'outside/malicious','commit':COMMIT},'/tmp')
    def test_self_package_change_invalidates_recorded_self_receipts(self):
        from evidence_atlas.__main__ import portfolio
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);(root/'examples').mkdir();(root/'changed.py').write_text('changed implementation')
            (root/'examples/portfolio.json').write_text(json.dumps({'cards':[{'repository':'gbesse/oss-evidence-atlas','commit':'package-sha256:'+'0'*64}],'receipts':[{'repository':'gbesse/oss-evidence-atlas','passed':True}]}))
            with patch('evidence_atlas.__main__.ROOT',root):self.assertFalse(portfolio()['receipts'][0]['passed'])
if __name__=='__main__':unittest.main()
