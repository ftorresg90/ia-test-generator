import argparse
from pathlib import Path
import json

from src.parser import parse_cases
from src.generator import generate_artifacts
from src.history import save_contracts
from src.validator import validate_contract
from src.ai_client import request_contract
from locator_validator import validate_locators
from locator_harvester import harvest_locators


def cmd_parse(args):
    cases = parse_cases(Path(args.file))
    print(json.dumps(cases, indent=2, ensure_ascii=False))


def cmd_generate(args):
    cases = parse_cases(Path(args.file))
    if args.cases:
        requested = {case_id.strip() for case_id in args.cases if case_id.strip()}
        filtered = [case for case in cases if case.get("id") in requested]
        missing = sorted(requested - {case.get("id") for case in filtered})
        if missing:
            raise ValueError(f"Casos no encontrados en {args.file}: {', '.join(missing)}")
        if not filtered:
            raise ValueError("No se seleccionó ningún caso válido para generar.")
        cases = filtered
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


def cmd_validate(args):
    cases = parse_cases(Path(args.file))
    if args.cases:
        requested = {case_id.strip() for case_id in args.cases if case_id.strip()}
        filtered = [case for case in cases if case.get("id") in requested]
        missing = sorted(requested - {case.get("id") for case in filtered})
        if missing:
            raise ValueError(f"Casos no encontrados en {args.file}: {', '.join(missing)}")
        if not filtered:
            raise ValueError("No se seleccionó ningún caso válido para validar.")
        cases = filtered
    contracts = []
    for case in cases:
        contract = request_contract(case, args.service_url)
        valid, errors = validate_contract(contract)
        if not valid:
            raise ValueError(f"Contrato inválido {case.get('id')}: {errors}")
        contracts.append(contract)
    validate_locators(
        contracts,
        browser=args.browser,
        headless=not args.no_headless,
        timeout=args.timeout,
        remote_url=args.remote_url,
    )


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
    p_generate.add_argument(
        "--case",
        dest="cases",
        action="append",
        help="Filtra por ID de caso. Repite esta bandera para múltiples valores.",
    )
    p_generate.set_defaults(func=cmd_generate)

    p_validate = sub.add_parser("validate", help="Valida los locators usando Selenium")
    p_validate.add_argument("file")
    p_validate.add_argument("--service-url", default="local")
    p_validate.add_argument("--browser", choices=["chrome", "firefox", "edge"], default="chrome")
    p_validate.add_argument("--timeout", type=int, default=5, help="Timeout de búsqueda (segundos)")
    p_validate.add_argument("--case", dest="cases", action="append",
                            help="ID de caso a validar (repetir bandera para múltiples).")
    p_validate.add_argument("--no-headless", action="store_true", help="Ejecuta el navegador visible.")
    p_validate.add_argument("--remote-url", help="URL de Selenium Grid/Remote WebDriver (opcional).")
    p_validate.set_defaults(func=cmd_validate)

    p_harvest = sub.add_parser("harvest", help="Obtiene locators automáticamente con Selenium headless")
    p_harvest.add_argument("file")
    p_harvest.add_argument("--output", default="locator_suggestions.json")
    p_harvest.add_argument("--browser", choices=["chrome", "firefox", "edge"], default="chrome")
    p_harvest.add_argument("--timeout", type=int, default=5, help="Timeout de búsqueda (segundos)")
    p_harvest.add_argument("--case", dest="cases", action="append", help="ID de caso a procesar (repetible)")
    p_harvest.add_argument("--no-headless", action="store_true", help="Ejecuta el navegador visible.")
    p_harvest.add_argument("--remote-url", help="URL de Selenium Grid/Remote WebDriver (opcional).")
    p_harvest.add_argument("--update-hints", action="store_true",
                           help="Actualiza el archivo ai/stub/locator_hints.json con los resultados.")
    p_harvest.add_argument("--hints-file", default="ai/stub/locator_hints.json",
                           help="Ruta del archivo de hints a actualizar.")
    p_harvest.set_defaults(func=harvest_locators)

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
