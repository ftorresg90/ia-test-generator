from typing import Dict, List, Tuple

try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.common.exceptions import TimeoutException, WebDriverException
except ImportError:  # pragma: no cover
    webdriver = None
    By = WebDriverWait = EC = TimeoutException = WebDriverException = None


def build_driver(browser: str, headless: bool, remote_url: str | None = None):
    if webdriver is None:
        raise RuntimeError(
            "Selenium no está instalado. Ejecuta `pip install selenium` y asegúrate "
            "de tener el driver adecuado (chromedriver/geckodriver/etc.) en tu PATH."
        )

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


def locator_to_by(locator: Dict[str, str]) -> Tuple[By, str]:
    strategy = (locator.get("strategy") or "css").lower()
    value = locator.get("value") or ""
    mapping = {
        "css": (By.CSS_SELECTOR, value),
        "xpath": (By.XPATH, value),
        "id": (By.ID, value),
        "name": (By.NAME, value),
        "class": (By.CLASS_NAME, value),
        "linktext": (By.LINK_TEXT, value),
        "partiallinktext": (By.PARTIAL_LINK_TEXT, value),
    }
    if strategy == "aria":
        return By.CSS_SELECTOR, f'[aria-label="{value}"]'
    if strategy not in mapping:
        stripped = value.strip()
        if stripped.startswith(("/", ".", "(")) or stripped.lower().startswith("xpath=") or "//" in stripped:
            return By.XPATH, stripped.replace("xpath=", "", 1) if stripped.lower().startswith("xpath=") else stripped
    return mapping.get(strategy, (By.CSS_SELECTOR, value))


def format_strategy(locator: Dict[str, str]) -> str:
    return f"{locator.get('strategy', 'css')}:{locator.get('value', '')}"


def validate_contract(driver, contract: Dict, timeout: int):
    meta = contract.get("meta", {})
    url = meta.get("url")
    if not url:
        print(f"[advertencia] Caso {meta.get('caseId')} no tiene URL.")
        return
    print(f"\nValidando {meta.get('caseId')} -> {url}")
    driver.get(url)
    wait = WebDriverWait(driver, timeout)
    for po in contract.get("pageObjects", []):
        for method in po.get("methods", []):
            by, value = locator_to_by(method.get("locator", {}))
            try:
                wait.until(EC.presence_of_element_located((by, value)))
                status = "✔"
            except TimeoutException:
                status = "✖"
            print(f"  {status} {method.get('name')} ({format_strategy(method.get('locator', {}))})")


def validate_locators(contracts: List[Dict], browser: str, headless: bool, timeout: int, remote_url: str | None = None):
    driver = build_driver(browser, headless, remote_url)

    try:
        for contract in contracts:
            validate_contract(driver, contract, timeout)
    finally:
        driver.quit()
