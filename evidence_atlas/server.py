import json
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
from urllib.parse import urlparse
from .__main__ import ROOT,portfolio,summary
from .evidence import freshness,sha
from .replay import coverage
class Handler(BaseHTTPRequestHandler):
    def log_message(self,*_):pass
    def reply(self,code,data,kind='application/json'):
        content=data if isinstance(data,bytes) else json.dumps(data).encode();self.send_response(code);self.send_header('Content-Type',kind+'; charset=utf-8');self.send_header('Content-Length',str(len(content)));self.send_header('Cache-Control','no-store');self.send_header('X-Content-Type-Options','nosniff');self.end_headers();self.wfile.write(content)
    def do_GET(self):
        path=urlparse(self.path).path
        if path=='/api/portfolio':
            data=portfolio();return self.reply(200,{**data,'summary':summary(data)})
        if path in ('/','/app.js','/style.css'):
            file='index.html' if path=='/' else path[1:];return self.reply(200,(ROOT/'web'/file).read_bytes(),{'index.html':'text/html','app.js':'text/javascript','style.css':'text/css'}[file])
        self.reply(404,{'error':'not_found'})
    def do_POST(self):
        if self.path not in ('/api/freshness-demo','/api/coverage-demo'):return self.reply(404,{'error':'not_found'})
        if self.headers.get('Origin') not in (None,f'http://127.0.0.1:{self.server.server_port}'):return self.reply(403,{'error':'origin_denied'})
        try:
            size=int(self.headers.get('Content-Length','0'))
            if not 0<size<=10000:raise ValueError('size')
            body=json.loads(self.rfile.read(size));data=portfolio();card=data['cards'][0]
            if self.path=='/api/coverage-demo':
                receipts=[r for r in data['receipts'] if r['repository']!=card['repository']] if body.get('remove_first') is True else data['receipts']
                return self.reply(200,coverage(data['requirements'],data['cards'],receipts))
            target={'repository':card['repository'],'commit':card['commit'],'check_id':'registered_demo'};source=b'synthetic source snapshot v1';contract={'source_sha256':sha(source),'reproducer':target};current=source+b' changed' if body.get('changed') is True else source;receipt={**target,'passed':body.get('replay_passed',True)};self.reply(200,freshness(contract,current,receipt))
        except (ValueError,TypeError,KeyError):self.reply(400,{'error':'invalid_input','messages':['Entrée non valide','Invalid input','Entrada no válida']})
def serve(port=8775):ThreadingHTTPServer(('127.0.0.1',port),Handler).serve_forever()
