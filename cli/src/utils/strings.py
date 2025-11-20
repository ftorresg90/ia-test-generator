import re


def slugify(text: str) -> str:
    return re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", text.lower())).strip('-')[:80]


def camel_case(text: str) -> str:
    segments = re.findall(r"[a-z0-9]+", text, re.I)
    if not segments:
        return "generated"
    return segments[0].lower() + ''.join(segment.capitalize() for segment in segments[1:])


def extract_url(text: str) -> str | None:
    match = re.search(r"https?://\S+", text)
    if not match:
        return None
    return match.group(0).rstrip('"\'.,')


def sanitize_json_text(text: str) -> str:
    if not text:
        return ""
    cleaned = text.strip()
    fence = re.search(r"```(?:json)?\s*([\s\S]+?)```", cleaned, re.I)
    if fence:
        cleaned = fence.group(1).strip()
    start = cleaned.find('{')
    end = cleaned.rfind('}')
    if start != -1 and end != -1 and end > start:
        cleaned = cleaned[start:end + 1]
    return cleaned.strip()
