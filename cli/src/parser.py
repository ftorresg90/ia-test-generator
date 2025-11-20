from pathlib import Path

def parse_cases(path: Path):
    content = path.read_text(encoding="utf-8")
    lines = content.splitlines()
    cases = []
    current = None
    mode = None

    def push():
        nonlocal current
        if current:
            current["steps"] = [step for step in current.get("steps", []) if step.strip()]
            if not current.get("id"):
                current["id"] = f"case-{len(cases) + 1}"
            cases.append(current)
            current = None

    for raw in lines:
        line = raw.strip()
        if not line:
            continue
        if line.startswith("#"):
            push()
            current = {"title": line[1:].strip(), "steps": []}
            continue
        if current is None:
            continue
        lower = line.lower()
        if lower.startswith("id:"):
            current["id"] = line.split(":", 1)[1].strip()
            continue
        if lower.startswith("url:"):
            current["url"] = line.split(":", 1)[1].strip()
            continue
        if lower.startswith("tags:"):
            raw_tags = line.split(":", 1)[1].strip()
            current["tags"] = ([tag if tag.startswith('@') else f"@{tag}"
                                 for tag in raw_tags.split()] if raw_tags else [])
            continue
        if lower.startswith("pasos:"):
            mode = "steps"
            continue
        if mode == "steps":
            normalized = line.lstrip("0123456789-.) ").strip()
            current["steps"].append(normalized or line)

    push()
    return cases
