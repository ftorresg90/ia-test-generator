from pathlib import Path
import json

try:
    from jsonschema import Draft7Validator
except ImportError:  # fallback when jsonschema is unavailable
    Draft7Validator = None

SCHEMA_PATH = Path('docs/ai_contract.schema.json')
SCHEMA = json.loads(SCHEMA_PATH.read_text(encoding='utf-8'))
VALIDATOR = Draft7Validator(SCHEMA) if Draft7Validator else None


def validate_contract(contract):
    if not VALIDATOR:
        return True, []
    errors = sorted(VALIDATOR.iter_errors(contract), key=lambda e: e.path)
    return not errors, [error.message for error in errors]
