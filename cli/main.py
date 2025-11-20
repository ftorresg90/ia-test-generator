import argparse
from pathlib import Path
import json

from src.parser import parse_cases
from src.generator import generate_artifacts
from src.history import save_contracts
from src.validator import validate_contract
from src.ai_client import request_contract


def cmd_parse(args):
    cases = parse_cases(Path(args.file))
    print(json.dumps(cases, indent=2, ensure_ascii=False))


def cmd_generate(args):
    cases = parse_cases(Path(args.file))
    results = []
    for case in cases:
        contract = request_contract(case, args.service_url)
        valid, errors = validate_contract(contract)
        if not valid:
            raise ValueError(f"Contrato inválido {case.get('id')}: {errors}")
        results.append({"caseId": case.get("id"), "contract": contract})
    save_contracts(results)
    generate_artifacts([item["contract"] for item in results], Path(args.output))
    print(f"Se generaron {len(results)} casos en {args.output}")


def build_parser():
    parser = argparse.ArgumentParser(description="IA Test Generator CLI (Python)")
    sub = parser.add_subparsers(dest="command", required=True)

    p_parse = sub.add_parser("parse", help="Parsea el archivo de casos")
    p_parse.add_argument("file")
    p_parse.set_defaults(func=cmd_parse)

    p_generate = sub.add_parser("generate", help="Genera artefactos")
    p_generate.add_argument("file")
    p_generate.add_argument("--output", default="generator/src")
    p_generate.add_argument("--service-url", default="local")
    p_generate.set_defaults(func=cmd_generate)

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
