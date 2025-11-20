import importlib.util
from pathlib import Path

repo_root = Path(__file__).resolve().parents[2]
stub_file = repo_root / 'ai/stub/stubResponse.py'

spec = importlib.util.spec_from_file_location('stubResponse', stub_file)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)  # type: ignore
build_contract = module.buildContract
