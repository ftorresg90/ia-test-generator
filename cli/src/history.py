from pathlib import Path
import json

HISTORY_DIR = Path('.iatg_history')


def save_contracts(results):
    HISTORY_DIR.mkdir(exist_ok=True)
    for item in results:
        case_id = item.get('caseId')
        contract = item.get('contract')
        if not case_id or not contract:
            continue
        path = HISTORY_DIR / f"{case_id}.json"
        path.write_text(json.dumps(contract, ensure_ascii=False, indent=2), encoding='utf-8')
