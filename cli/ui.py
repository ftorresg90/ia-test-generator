import argparse
import subprocess
from pathlib import Path

from src.parser import parse_cases


def build_command(base_args, selected_ids):
    command = [
        "python3",
        "cli/main.py",
        "generate",
        base_args.file,
        "--output",
        base_args.output,
        "--service-url",
        base_args.service_url,
    ]
    for case_id in selected_ids:
        command.extend(["--case", case_id])
    return command


def prompt_selection(cases):
    print("\nCasos disponibles:\n")
    for idx, case in enumerate(cases, start=1):
        print(f"[{idx}] {case.get('id')}  -  {case.get('title')}")
    print("\nIngresa los números separados por coma (ej: 1,3).")
    print("Presiona Enter o escribe 'all' para generar todos.\n")

    selection = input("Selección: ").strip()
    if not selection or selection.lower() in {"all", "a"}:
        return [case.get("id") for case in cases]

    try:
        indexes = {int(part) for part in selection.split(",")}
    except ValueError:
        raise ValueError("La selección contiene valores no numéricos.")

    invalid = [idx for idx in indexes if idx < 1 or idx > len(cases)]
    if invalid:
        raise ValueError(f"Números fuera de rango: {invalid}")

    return [cases[idx - 1].get("id") for idx in sorted(indexes)]


def main():
    parser = argparse.ArgumentParser(
        description="UI mínima para seleccionar casos y ejecutar el generador."
    )
    parser.add_argument("file", help="Archivo de casos (ej: sample_input.txt)")
    parser.add_argument("--output", default="generator/src")
    parser.add_argument("--service-url", default="local")
    args = parser.parse_args()

    cases = parse_cases(Path(args.file))
    if not cases:
        print("No se encontraron casos en el archivo proporcionado.")
        return

    try:
        selected_ids = prompt_selection(cases)
    except ValueError as exc:
        print(f"[error] {exc}")
        return

    command = build_command(args, selected_ids)
    print("\nSe ejecutará:\n", " ".join(command))
    confirm = input("¿Continuar? [s/N] ").strip().lower()
    if confirm not in {"s", "si", "sí"}:
        print("Operación cancelada.")
        return

    subprocess.run(command, check=True)


if __name__ == "__main__":
    main()
