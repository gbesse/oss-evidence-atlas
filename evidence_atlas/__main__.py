import json
import hashlib
from pathlib import Path
import sys
import subprocess
from .evidence import collect_manifest,summarize_claims,freshness,audit_release
from .replay import replay,coverage
ROOT=Path(__file__).resolve().parent
MESSAGES={'fr':{'help':'Utilisation : python -m evidence_atlas demo|collect propriétaire/dépôt manifeste écosystème paquet propriétaire-publicateur|audit fiche.json|freshness contrat.json source receipt.json|replay fiche.json checkout [demo|unit|browser]|serve [port] [--lang fr|en|es]','error':'Entrée non valide, preuve absente ou accès public indisponible','ready':'Atlas de preuves local'},'en':{'help':'Usage: python -m evidence_atlas demo|collect owner/repo manifest ecosystem package publisher-owner|audit card.json|freshness contract.json source receipt.json|replay card.json checkout [demo|unit|browser]|serve [port] [--lang fr|en|es]','error':'Invalid input, missing evidence or unavailable public access','ready':'Local evidence atlas'},'es':{'help':'Uso: python -m evidence_atlas demo|collect propietario/repo manifiesto ecosistema paquete propietario-publicador|audit ficha.json|freshness contrato.json fuente receipt.json|replay ficha.json checkout [demo|unit|browser]|serve [puerto] [--lang fr|en|es]','error':'Entrada no válida, prueba ausente o acceso público no disponible','ready':'Atlas local de pruebas'}}
def package_fingerprint():
    files=sorted([*ROOT.glob('*.py'),*ROOT.joinpath('web').glob('*.js'),*ROOT.joinpath('web').glob('*.html'),*ROOT.joinpath('web').glob('*.css')])
    return hashlib.sha256(b''.join(str(p.relative_to(ROOT)).encode()+b'\0'+p.read_bytes()+b'\0' for p in files)).hexdigest()
def portfolio():
    data=json.loads((ROOT/'examples/portfolio.json').read_text());expected='package-sha256:'+package_fingerprint()
    for card in data['cards']:
        if card['repository']=='gbesse/oss-evidence-atlas' and card['commit']!=expected:
            for receipt in data['receipts']:
                if receipt['repository']==card['repository']:receipt.update(passed=False,source_pin_changed=True)
    return data
def summary(data):return {'coverage':coverage(data['requirements'],data['cards'],data['receipts']),'declarations':summarize_claims(data.get('manifest_records',[])),'anonymous_audits':data.get('anonymous_audits',[]),'sota_or_human_adoption_proven':False}
def main(argv=None):
    args=list(sys.argv[1:] if argv is None else argv);lang='en'
    try:
        if '--lang' in args:i=args.index('--lang');lang=args[i+1];del args[i:i+2]
        if lang not in MESSAGES:raise ValueError('language')
        if not args or args[0] in ('help','--help'):print(MESSAGES[lang]['help']);return 0
        cmd=args.pop(0)
        if cmd=='serve':
            from .server import serve
            port=int(args[0]) if args else 8775;print(f'{MESSAGES[lang]["ready"]}: http://127.0.0.1:{port}/?lang={lang}',flush=True);serve(port);return 0
        if cmd=='demo':result=summary(portfolio())
        elif cmd=='collect':result=collect_manifest(*args)
        elif cmd=='audit':result=audit_release(json.loads(Path(args[0]).read_text()))
        elif cmd=='freshness':result=freshness(json.loads(Path(args[0]).read_text()),Path(args[1]).read_bytes(),json.loads(Path(args[2]).read_text()) if len(args)>2 else None)
        elif cmd=='replay':result=replay(json.loads(Path(args[0]).read_text()),args[1],kind=args[2] if len(args)>2 else 'demo')
        else:raise ValueError('command')
        print(json.dumps(result,ensure_ascii=False,indent=2));return 1 if result.get('passed') is False else 0
    except (ValueError,TypeError,KeyError,IndexError,OSError,subprocess.SubprocessError):print(json.dumps({'error':'invalid_input','message':MESSAGES.get(lang,MESSAGES['en'])['error']}),file=sys.stderr);return 2
if __name__=='__main__':raise SystemExit(main())
