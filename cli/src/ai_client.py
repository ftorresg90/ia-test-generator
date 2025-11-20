import json
import urllib.request

from .local_stub import build_contract
from .gemini_client import request_contract_from_gemini


def request_contract(test_case, service_url='local'):
    if service_url == 'local':
        return build_contract(test_case)
    if service_url == 'gemini':
        return request_contract_from_gemini(test_case)
    if service_url.startswith('http://') or service_url.startswith('https://'):
        data = json.dumps(test_case).encode('utf-8')
        req = urllib.request.Request(service_url, data=data, headers={'Content-Type': 'application/json'})
        with urllib.request.urlopen(req, timeout=30) as resp:
            if resp.status >= 400:
                raise RuntimeError(f"IA service {resp.status}")
            return json.loads(resp.read().decode('utf-8'))
    raise ValueError(f"Servicio IA no soportado: {service_url}")
