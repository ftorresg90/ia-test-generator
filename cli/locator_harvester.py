import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional
from urllib.parse import urlparse

from src.parser import parse_cases

try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.common.exceptions import TimeoutException
except ImportError as exc:  # pragma: no cover
    webdriver = None
    By = WebDriverWait = EC = TimeoutException = None


def ensure_selenium_available():
    if webdriver is None:
        raise RuntimeError(
            "Selenium no está instalado. Ejecuta `pip install selenium` "
            "y asegúrate de que el driver del navegador esté disponible."
        )


def build_driver(browser: str, headless: bool, remote_url: Optional[str]) -> "webdriver.Remote":
    ensure_selenium_available()
    browser = browser.lower()
    if browser == "chrome":
        options = webdriver.ChromeOptions()
        if headless:
            options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        if remote_url:
            return webdriver.Remote(command_executor=remote_url, options=options)
        return webdriver.Chrome(options=options)
    if browser == "firefox":
        options = webdriver.FirefoxOptions()
        if headless:
            options.add_argument("--headless")
        if remote_url:
            return webdriver.Remote(command_executor=remote_url, options=options)
        return webdriver.Firefox(options=options)
    if browser == "edge":
        options = webdriver.EdgeOptions()
        if headless:
            options.add_argument("--headless=new")
        if remote_url:
            return webdriver.Remote(command_executor=remote_url, options=options)
        return webdriver.Edge(options=options)
    raise ValueError(f"Navegador no soportado: {browser}")


def detect_action(text: str) -> str:
    lowered = text.lower()
    if any(keyword in lowered for keyword in ("validar", "verificar", "asegurar", "visualizar", "comprobar")):
        return "assert"
    if any(keyword in lowered for keyword in ("presionar", "hacer click", "clic", "seleccionar", "abrir", "navegar")):
        return "click"
    if "buscar" in lowered:
        return "search"
    if any(keyword in lowered for keyword in ("ingresar", "introducir", "escribir", "completar")):
        return "input"
    return "generic"


def extract_tokens(text: str) -> List[str]:
    base_tokens = re.findall(r"[\\wáéíóúñü]+", text.lower())
    quoted = re.findall(r'"([^"]+)"', text)
    for chunk in quoted:
        base_tokens.extend(re.findall(r"[\\wáéíóúñü]+", chunk.lower()))
    filtered = [token for token in base_tokens if len(token) > 2]
    return list(dict.fromkeys(filtered))


def element_descriptor(element) -> str:
    parts = [
        element.text,
        element.get_attribute("placeholder"),
        element.get_attribute("aria-label"),
        element.get_attribute("title"),
        element.get_attribute("name"),
        element.get_attribute("id"),
        element.get_attribute("value"),
        element.get_attribute("data-test"),
        element.get_attribute("data-testid"),
    ]
    return " ".join(part for part in parts if part).lower()


def element_to_locator(driver, element) -> Dict[str, str]:
    element_id = element.get_attribute("id")
    if element_id:
        return {"strategy": "css", "value": f"#{element_id}"}
    data_test = element.get_attribute("data-test") or element.get_attribute("data-testid")
    if data_test:
        return {"strategy": "css", "value": f"[data-test='{data_test}']"}
    name = element.get_attribute("name")
    if name:
        return {"strategy": "css", "value": f"[name='{name}']"}
    aria_label = element.get_attribute("aria-label")
    if aria_label:
        return {"strategy": "css", "value": f"[aria-label='{aria_label}']"}
    classes = (element.get_attribute("class") or "").strip()
    if classes:
        cls = ".".join(part for part in classes.split() if part)
        if cls:
            return {"strategy": "css", "value": f".{cls}"}
    css_path = driver.execute_script(
        """
        function cssPath(el) {
            if (!(el instanceof Element)) return null;
            const path = [];
            while (el.nodeType === Node.ELEMENT_NODE) {
                let selector = el.nodeName.toLowerCase();
                if (el.id) {
                    selector += '#' + el.id;
                    path.unshift(selector);
                    return path.join(' > ');
                }
                let sibling = el;
                let nth = 1;
                while (sibling = sibling.previousElementSibling) {
                    if (sibling.nodeName.toLowerCase() === selector) {
                        nth++;
                    }
                }
                if (nth > 1) {
                    selector += `:nth-of-type(${nth})`;
                }
                path.unshift(selector);
                el = el.parentNode;
            }
            return path.join(' > ');
        }
        return cssPath(arguments[0]);
        """,
        element,
    )
    if css_path:
        return {"strategy": "css", "value": css_path}
    return {"strategy": "xpath", "value": element.xpath}  # type: ignore[attr-defined]


SELECTOR_MAP = {
    "input": [
        "input:not([type='hidden'])",
        "textarea",
    ],
    "search": [
        "input[type='search']",
        "input[name*='search' i]",
        "input[name*='buscar' i]",
        "input[placeholder*='buscar' i]",
        "input[aria-label*='buscar' i]",
    ],
    "click": [
        "button",
        "input[type='submit']",
        "a",
        "[role='button']",
    ],
    "assert": [
        "[data-test]",
        "[data-testid]",
        "h1, h2, h3",
        ".alert",
        ".card",
        "div",
        "span",
        "p",
    ],
    "generic": [
        "[data-test]",
        "[data-testid]",
        "*",
    ],
}


@dataclass
class StepSuggestion:
    text: str
    action: str
    locator: Optional[Dict[str, str]]
    confidence: float
    tokens: List[str]
    note: Optional[str] = None


def score_element(element, tokens: List[str]) -> int:
    if not tokens:
        return 0
    descriptor = element_descriptor(element)
    score = 0
    for token in tokens:
        if token in descriptor:
            score += 1
    return score


def find_best_element(driver, selectors: List[str], tokens: List[str]):
    best = (None, 0)
    for selector in selectors:
        try:
            candidates = driver.find_elements(By.CSS_SELECTOR, selector)
        except Exception:
            continue
        for candidate in candidates:
            if not candidate.is_displayed():
                continue
            hits = score_element(candidate, tokens)
            if hits > best[1]:
                best = (candidate, hits)
    return best


def harvest_step(driver, step_text: str, action: str, timeout: int) -> StepSuggestion:
    tokens = extract_tokens(step_text)
    selectors = SELECTOR_MAP.get(action, SELECTOR_MAP["generic"])
    if action == "assert":
        try:
            WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.CSS_SELECTOR, selectors[0])))
        except Exception:
            pass
    element, hits = find_best_element(driver, selectors, tokens)
    if element:
        locator = element_to_locator(driver, element)
        confidence = hits / len(tokens) if tokens else 0.5
        return StepSuggestion(step_text, action, locator, round(confidence, 2), tokens)
    return StepSuggestion(step_text, action, None, 0.0, tokens, note="No se encontró un elemento adecuado.")


def harvest_case(driver, case: Dict, timeout: int) -> Dict:
    url = case.get("url")
    if not url:
        return {"caseId": case.get("id"), "url": None, "steps": [], "note": "Caso sin URL"}
    driver.get(url)
    suggestions = []
    for step in case.get("steps", []):
        action = detect_action(step)
        suggestion = harvest_step(driver, step, action, timeout)
        suggestions.append(suggestion)
    return {
        "caseId": case.get("id"),
        "url": url,
        "steps": [s.__dict__ for s in suggestions],
    }


def merge_with_hints(hints_path: Path, case_results: List[Dict]):
    try:
        hints = json.loads(hints_path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        hints = {"global": [], "domains": {}}
    except json.JSONDecodeError:
        hints = {"global": [], "domains": {}}
    domains = hints.setdefault("domains", {})
    for result in case_results:
        url = result.get("url")
        if not url:
            continue
        hostname = urlparse(url).hostname
        if not hostname:
            continue
        key = hostname.lower()
        domain_hints = domains.setdefault(key, [])
        for step in result.get("steps", []):
            locator = step.get("locator")
            if not locator:
                continue
            pattern = f"(?i){re.escape(step.get('text', ''))}"
            entry = {"pattern": pattern, "locator": locator}
            if entry not in domain_hints:
                domain_hints.append(entry)
    hints_path.write_text(json.dumps(hints, indent=2, ensure_ascii=False), encoding="utf-8")


def harvest_locators(args):
    cases = parse_cases(Path(args.file))
    if args.cases:
        requested = {case_id.strip() for case_id in args.cases if case_id.strip()}
        cases = [case for case in cases if case.get("id") in requested]
    driver = build_driver(args.browser, not args.no_headless, args.remote_url)
    results: List[Dict] = []
    try:
        for case in cases:
            results.append(harvest_case(driver, case, args.timeout))
    finally:
        driver.quit()
    output = Path(args.output or "locator_suggestions.json")
    output.write_text(json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Se guardó el archivo con sugerencias en {output}")
    if args.update_hints:
        hints_path = Path(args.hints_file)
        merge_with_hints(hints_path, results)
        print(f"Se actualizaron los hints en {hints_path}")
