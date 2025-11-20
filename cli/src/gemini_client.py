import json
import os
import re
import urllib.request

from .utils.strings import sanitize_json_text

DEFAULT_MODEL = "gemini-pro"
DEFAULT_ENDPOINT = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"


def build_prompt(test_case: dict) -> str:
    title = test_case.get("title", "Caso sin título")
    case_id = test_case.get("id", "CASE-ID")
    url = test_case.get("url") or "N/A"
    tags = " ".join(test_case.get("tags", []))
    steps = "\n".join(f"- {step}" for step in test_case.get("steps", []))
    template = (
        "Eres un generador de contratos de automatización QA. "
        "Debes responder EXCLUSIVAMENTE con un JSON válido que cumpla el esquema descrito. "
        "No incluyas explicaciones fuera del JSON. "
        "Si necesitas escribir código, hazlo dentro del JSON.\n\n"
        "Contrato esperado:\n"
        "{\n"
        '  "meta": { "caseId": string, "title": string, "url": string, "tags": [string] },\n'
        '  "gherkin": {\n'
        '      "featureName": string,\n'
        '      "featureDescription": string,\n'
        '      "background": [string],\n'
        '      "scenarios": [ { "name": string, "tags": [string], "steps": [ { "keyword": string, "text": string } ] } ]\n'
        "  },\n"
        '  "stepDefinitions": [ {\n'
        '      "stepText": string,\n'
        '      "glueClass": "com.autogen.steps.{caseId}Steps",\n'
        '      "methodName": string,\n'
        '      "parameters": ["String param1", ...],\n'
        '      "action": {\n'
        '          "pageObjectClass": "com.autogen.pages.{caseId}Page",\n'
        '          "baseName": camelCase del paso,\n'
        '          "interaction": "click" | "input" | "assertVisible" | "assertText"\n'
        "      }\n"
        "  } ],\n"
        '  "pageObjects": [ {\n'
        '      "className": "com.autogen.pages.{caseId}Page",\n'
        '      "methods": [ {\n'
        '          "name": camelCase del paso,\n'
        '          "locator": { "strategy": "id|css|xpath|name", "value": string, "confidence": número 0-1 }\n'
        "      } ]\n"
        "  } ],\n"
        '  "notes": [string]\n'
        "}\n\n"
        "Datos del caso:\n"
        f"- caseId: {case_id}\n"
        f"- título: {title}\n"
        f"- url: {url}\n"
        f"- tags: {tags}\n"
        "Pasos:\n"
        f"{steps}\n"
        "Responde únicamente con el JSON."
    )
    return template


def extract_text_from_response(payload: dict) -> str:
    candidates = payload.get("candidates") or []
    for candidate in candidates:
        content = candidate.get("content") or {}
        parts = content.get("parts") or []
        for part in parts:
            if "text" in part:
                return part["text"]
    raise RuntimeError("Gemini no devolvió contenido utilizable")


def call_gemini_api(prompt: str) -> dict:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY no está configurado")
    model = os.getenv("GEMINI_MODEL", DEFAULT_MODEL)
    endpoint_tpl = os.getenv("GEMINI_API_URL", DEFAULT_ENDPOINT)
    endpoint = endpoint_tpl.format(model=model)
    url = f"{endpoint}?key={api_key}"
    payload = {
        "contents": [
            {
                "role": "user",
                "parts": [{"text": prompt}]
            }
        ],
        "generationConfig": {
            "temperature": 0.1,
            "topP": 0.9,
            "topK": 32,
            "maxOutputTokens": 2048
        }
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        if resp.status >= 400:
            raise RuntimeError(f"Gemini API error {resp.status}")
        return json.loads(resp.read().decode("utf-8"))


def request_contract_from_gemini(test_case: dict) -> dict:
    prompt = build_prompt(test_case)
    response = call_gemini_api(prompt)
    text = extract_text_from_response(response)
    cleaned = sanitize_json_text(text)
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"Gemini devolvió un JSON inválido: {exc}") from exc
