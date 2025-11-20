import re


def to_camel(text: str) -> str:
    segments = re.findall(r"[a-z0-9]+", text, re.I)
    if not segments:
        return "element"
    first, *rest = segments
    return first.lower() + ''.join(segment.capitalize() for segment in rest)


def to_pascal(text: str) -> str:
    segments = re.findall(r"[a-z0-9]+", text, re.I)
    if not segments:
        return "Case"
    return ''.join(segment.capitalize() for segment in segments)


def detect_parameters(text: str):
    return re.findall(r'"([^\"]+)"', text)


def suggest_locator(text: str, idx: int):
    if re.search(r"usuario|user", text, re.I):
        return {"strategy": "id", "value": "username", "confidence": 0.85}
    if re.search(r"password|clave", text, re.I):
        return {"strategy": "id", "value": "password", "confidence": 0.85}
    if re.search(r"buscar|search", text, re.I):
        return {"strategy": "css", "value": "input[type='search']", "confidence": 0.7}
    if re.search(r"validar|verificar|asegurar", text, re.I):
        return {"strategy": "css", "value": f"div[data-test='resultado-{idx + 1}']", "confidence": 0.6}
    return {"strategy": "css", "value": f"[data-test='step-{idx + 1}']", "confidence": 0.3}


def detect_interaction(text: str, has_params: bool):
    if re.search(r"validar|verificar|asegurar", text, re.I):
        return "assertText" if has_params else "assertVisible"
    return "input" if has_params else "click"


def buildContract(test_case: dict):
    steps = test_case.get("steps", [])
    class_base = to_pascal(test_case.get("title") or test_case.get("id") or "Case")
    page_class = f"com.autogen.pages.{class_base}Page"
    notes = []
    seen = {}
    for text in steps:
        key = text.lower()
        seen[key] = seen.get(key, 0) + 1
    for text, count in seen.items():
        if count > 1:
            notes.append(f"El paso '{text}' aparece {count} veces.")

    contracts = {
        "meta": {
            "caseId": test_case.get("id"),
            "title": test_case.get("title"),
            "url": test_case.get("url"),
            "tags": test_case.get("tags", [])
        },
        "gherkin": {
            "featureName": test_case.get("title"),
            "featureDescription": f"Feature generado para {test_case.get('title')}",
            "background": [],
            "scenarios": [
                {
                    "name": test_case.get("title"),
                    "tags": test_case.get("tags", []),
                    "steps": [
                        {
                            "keyword": "Given" if idx == 0 else "Then" if idx == len(steps) - 1 else "When",
                            "text": text
                        }
                        for idx, text in enumerate(steps)
                    ]
                }
            ]
        },
        "stepDefinitions": [],
        "pageObjects": [
            {
                "className": page_class,
                "methods": []
            }
        ],
        "notes": notes,
    }

    for idx, text in enumerate(steps):
        params = detect_parameters(text)
        regex_text = re.sub(r'"([^\"]+)"', '"(.*)"', text)
        interaction = detect_interaction(text, bool(params))
        base_name = to_camel(text)
        contracts["stepDefinitions"].append({
            "stepText": regex_text,
            "glueClass": f"com.autogen.steps.{class_base}Steps",
            "methodName": f"step{idx + 1}",
            "parameters": [f"String param{i + 1}" for i in range(len(params))],
            "body": None,
            "action": {
                "pageObjectClass": page_class,
                "baseName": base_name,
                "interaction": interaction
            },
            "reusesExisting": False
        })
        contracts["pageObjects"][0]["methods"].append({
            "name": base_name,
            "locator": suggest_locator(text, idx)
        })
    return contracts
