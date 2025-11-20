from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from pathlib import Path
from stubResponse import buildContract
from jsonschema import Draft7Validator

SCHEMA = json.loads(Path('../../docs/ai_contract.schema.json').read_text(encoding='utf-8'))
VALIDATOR = Draft7Validator(SCHEMA)

class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path != '/generate':
            self.send_error(404)
            return
        length = int(self.headers.get('content-length', '0'))
        body = self.rfile.read(length)
        test_case = json.loads(body)
        contract = buildContract(test_case)
        errors = sorted(VALIDATOR.iter_errors(contract), key=lambda e: e.path)
        if errors:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(json.dumps({ 'error': 'invalid contract' }).encode('utf-8'))
            return
        self.send_response(200)
        self.end_headers()
        self.wfile.write(json.dumps(contract).encode('utf-8'))

def run(port=4000):
    server = HTTPServer(('', port), Handler)
    print(f'Stub listening on port {port}')
    server.serve_forever()

if __name__ == '__main__':
    run()
