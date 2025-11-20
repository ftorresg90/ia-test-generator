from pathlib import Path

import re

import re

import re

from .utils.strings import slugify, camel_case, extract_url

STEP_PACKAGE = 'com.autogen.steps'
PAGE_PACKAGE = 'com.autogen.pages'
HOOKS_PACKAGE = 'com.autogen.hooks'
RUNNER_PACKAGE = 'com.autogen.runners'


def compute_step_keywords(count: int):
    if count <= 0:
        return []
    if count == 1:
        return ['Given']
    if count == 2:
        return ['Given', 'Then']
    keywords = ['Given', 'When']
    if count > 3:
        keywords.extend(['And'] * (count - 3))
    keywords.append('Then')
    return keywords


def indent(body: str, spaces: int = 8) -> str:
    pad = ' ' * spaces
    return '\n'.join(f"{pad}{line.rstrip()}" for line in body.split('\n'))


def write_file(path: Path, content: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding='utf-8')


### Features

def render_feature(contract, index):
    gherkin = contract.get('gherkin', {})
    feature_name = gherkin.get('featureName') or contract['meta']['title']
    lines = [f"Feature: {feature_name}"]
    if desc := gherkin.get('featureDescription'):
        lines.append(f"  {desc}")
    if background := gherkin.get('background'):
        lines.extend(['', '  Background:'])
        lines.extend(f"    {step}" for step in background)
    for scenario in gherkin.get('scenarios', []):
        lines.append('')
        if scenario.get('tags'):
            lines.append('  ' + ' '.join(scenario['tags']))
        lines.append(f"  Scenario: {scenario.get('name', f'Escenario {index + 1}')}")
        steps = scenario.get('steps', [])
        keyword_flow = compute_step_keywords(len(steps))
        for idx, step in enumerate(steps):
            keyword = keyword_flow[idx] if idx < len(keyword_flow) else step.get('keyword', 'When')
            lines.append(f"    {keyword} {step.get('text', '')}")
    lines.append('')
    return '\n'.join(lines)


def write_features(contracts, output_dir):
    feature_dir = Path(output_dir) / 'test/resources/features'
    feature_dir.mkdir(parents=True, exist_ok=True)
    for idx, contract in enumerate(contracts):
        meta = contract.get('meta', {})
        preferred_name = meta.get('title') or meta.get('caseId') or f"feature-{idx + 1}"
        slug = slugify(preferred_name) or f"feature-{idx + 1}"
        write_file(feature_dir / f"{slug}.feature", render_feature(contract, idx))


### Step Definitions

def build_step_body(step, page_infos):
    action = step.get('action') or {}
    po_class = action.get('pageObjectClass')
    base_name = camel_case(action.get('baseName', 'element'))
    params = [param.split()[-1] for param in step.get('parameters', [])]
    if not po_class:
        url = extract_url(step.get('stepText', ''))
        return f'driver.get("{url}");' if url else '// TODO'
    target = next((info for info in page_infos if info['fqcn'] == po_class), None)
    if not target:
        return '// TODO'
    interaction = (action.get('interaction') or 'click').lower()
    if interaction == 'input' and params:
        return f"{target['var']}.{base_name}SendKeys({params[0]});"
    if interaction == 'asserttext' and params:
        return f"Assert.assertEquals({target['var']}.{base_name}GetText(), {params[0]});"
    if interaction == 'assertvisible':
        return f"Assert.assertTrue({target['var']}.{base_name}IsVisible());"
    return f"{target['var']}.{base_name}Click();"


def normalize_step_text(text: str) -> str:
    if not text:
        return ''
    normalized = re.sub(r'"[^"]*"', '""', text)
    normalized = re.sub(r'<[^>]+>', '""', normalized)
    normalized = ' '.join(normalized.split())
    return normalized.lower()


def build_keyword_map(contract):
    mapping = {}
    for scenario in contract.get('gherkin', {}).get('scenarios', []):
        steps = scenario.get('steps', [])
        keyword_flow = compute_step_keywords(len(steps))
        for idx, step in enumerate(steps):
            normalized = normalize_step_text(step.get('text', ''))
            keyword = keyword_flow[idx] if idx < len(keyword_flow) else step.get('keyword', 'When')
            mapping.setdefault(normalized, keyword)
    return mapping


def collect_glue_data(contracts):
    glue_map = {}
    for contract in contracts:
        keyword_map = build_keyword_map(contract)
        for step in contract.get('stepDefinitions', []):
            glue = step.get('glueClass') or STEP_PACKAGE
            entry = glue_map.setdefault(glue, {'steps': [], 'pages': set()})
            enriched = dict(step)
            normalized = normalize_step_text(step.get('stepText'))
            enriched['_keyword'] = keyword_map.get(normalized, 'When')
            entry['steps'].append(enriched)
            po_class = step.get('action', {}).get('pageObjectClass')
            if po_class:
                entry['pages'].add(po_class)
    return glue_map


def write_step_classes(contracts, output_dir):
    base_dir = Path(output_dir) / 'test/java'
    glue_map = collect_glue_data(contracts)
    for glue, data in glue_map.items():
        method_names = set()
        package_parts = glue.split('.')
        package = '.'.join(package_parts[:-1])
        class_name = package_parts[-1]
        dir_path = base_dir / '/'.join(package_parts[:-1])
        dir_path.mkdir(parents=True, exist_ok=True)

        imports = {
            'io.cucumber.java.en.*',
            'org.openqa.selenium.WebDriver',
            f'{HOOKS_PACKAGE}.Hooks'
        }
        page_infos = []
        for fqcn in data['pages']:
            parts = fqcn.split('.')
            info = {'fqcn': fqcn, 'class': parts[-1], 'var': camel_case(parts[-1])}
            page_infos.append(info)
            imports.add(fqcn)
        if any(step.get('action', {}).get('interaction', '').lower().startswith('assert') for step in data['steps']):
            imports.add('org.testng.Assert')

        methods = []
        for idx, step in enumerate(data['steps']):
            annotation = (step.get('_keyword') or 'When').capitalize()
            text = step.get('stepText') or ''
            params = ', '.join(step.get('parameters', []))
            body = build_step_body(step, page_infos)
            base_name = camel_case(text or f"step{idx + 1}") or f"step{idx + 1}"
            name_candidate = base_name
            counter = 1
            while name_candidate in method_names:
                name_candidate = f"{base_name}{counter}"
                counter += 1
            method_names.add(name_candidate)
            escaped = text.replace('\\', '\\\\').replace('"', '\\"')
            method_lines = [f"    @{annotation}(\"{escaped}\")",
                            f"    public void {name_candidate}({params}) {{",
                            indent(body if body else '// TODO'),
                            '    }']
            methods.append('\n'.join(method_lines))

        import_block = '\n'.join(f'import {imp};' for imp in sorted(imports))
        field_lines = ['    private final WebDriver driver;'] + [f"    private final {info['class']} {info['var']};" for info in page_infos]
        ctor_lines = ['    public {0}() {{'.format(class_name), '        this.driver = Hooks.getDriver();']
        ctor_lines.extend(f"        this.{info['var']} = new {info['class']}(this.driver);" for info in page_infos)
        ctor_lines.append('    }')

        class_lines = [f"package {package};", '', import_block, '', f"public class {class_name} {{", *field_lines, '', *ctor_lines, '', '\n\n'.join(methods), '}']
        write_file(dir_path / f"{class_name}.java", '\n'.join(class_lines))


### Page Objects

def render_find_by(locator, fallback, idx):
    default_value = f"[data-test='{fallback or idx}']"
    if not locator:
        return f"@FindBy(css = \"{default_value}\")"
    value = locator.get('value', '') or default_value
    value = value.replace('"', '\\"')
    strategy = locator.get('strategy', 'css')
    mapping = {
        'id': f"@FindBy(id = \"{value}\")",
        'name': f"@FindBy(name = \"{value}\")",
        'xpath': f"@FindBy(xpath = \"{value}\")",
        'class': f"@FindBy(className = \"{value}\")",
        'aria': f"@FindBy(css = \"[aria-label='{value}']\")",
        'css': f"@FindBy(css = \"{value}\")",
    }
    return mapping.get(strategy, mapping['css'])


def build_element_blocks(methods):
    used = set()
    blocks = []
    for idx, method in enumerate(methods or []):
        base = camel_case(method.get('name') or method.get('description', '') or f'element{idx + 1}')
        name = base or f'element{idx + 1}'
        field_name = name
        counter = 1
        while field_name in used:
            field_name = f"{name}{counter}"
            counter += 1
        used.add(field_name)
        annotation = render_find_by(method.get('locator'), name, idx)
        field_line = f"    {annotation}\n    private WebElement {field_name};"
        actions = [
            f"    public void {field_name}Click() {{\n        clickElement({field_name});\n    }}",
            f"    public void {field_name}SendKeys(String text) {{\n        typeText({field_name}, text);\n    }}",
            f"    public boolean {field_name}IsVisible() {{\n        return isVisible({field_name});\n    }}",
            f"    public String {field_name}GetText() {{\n        return getText({field_name});\n    }}",
        ]
        blocks.append({'field': field_line, 'actions': '\n\n'.join(actions)})
    return blocks


def write_page_objects(contracts, output_dir):
    base_dir = Path(output_dir) / 'test/java'
    for contract in contracts:
        for po in contract.get('pageObjects', []):
            package_parts = po['className'].split('.')
            package = '.'.join(package_parts[:-1])
            class_name = package_parts[-1]
            dir_path = base_dir / '/'.join(package_parts[:-1])
            dir_path.mkdir(parents=True, exist_ok=True)
            blocks = build_element_blocks(po.get('methods'))
            class_lines = [f"package {package};", '',
                           'import org.openqa.selenium.WebDriver;',
                           'import org.openqa.selenium.WebElement;',
                           'import org.openqa.selenium.support.FindBy;',
                           'import org.openqa.selenium.support.PageFactory;',
                           '',
                           f"public class {class_name} extends WebBasePage {{",
                           '    private static WebDriver driver;',
                           '']
            if blocks:
                for block in blocks:
                    class_lines.append(block['field'])
                    class_lines.append('')
            class_lines.extend([
                f"    public {class_name}(WebDriver driver) {{",
                '        super(driver);',
                f"        {class_name}.driver = driver;",
                '        PageFactory.initElements(driver, this);',
                '    }',
                ''
            ])
            for block in blocks:
                class_lines.append(block['actions'])
                class_lines.append('')
            class_lines.append('}')
            write_file(dir_path / f"{class_name}.java", '\n'.join(class_lines))


def write_base_page(output_dir):
    dir_path = Path(output_dir) / 'test/java' / '/'.join(PAGE_PACKAGE.split('.'))
    lines = [f"package {PAGE_PACKAGE};", '',
             'import org.openqa.selenium.*;',
             'import org.openqa.selenium.support.ui.ExpectedConditions;',
             'import org.openqa.selenium.support.ui.WebDriverWait;',
             '',
             'import java.time.Duration;',
             '',
             'public abstract class WebBasePage {',
             '    protected final WebDriver driver;',
             '    private final WebDriverWait wait;',
             '    private static final long DEFAULT_TIMEOUT = 30;',
             '',
             '    protected WebBasePage(WebDriver driver) {',
             '        this(driver, DEFAULT_TIMEOUT);',
             '    }',
             '',
             '    protected WebBasePage(WebDriver driver, long timeoutSeconds) {',
             '        this.driver = driver;',
             '        this.wait = new WebDriverWait(driver, Duration.ofSeconds(timeoutSeconds));',
             '    }',
             '',
             '    protected WebDriver getDriver() {',
             '        return driver;',
             '    }',
             '',
             '    protected void waitUntilElementIsVisible(WebElement element) {',
             '        wait.until(ExpectedConditions.visibilityOf(element));',
             '    }',
             '',
             '    protected void waitUntilElementIsVisible(By locator) {',
             '        wait.until(ExpectedConditions.visibilityOfElementLocated(locator));',
             '    }',
             '',
             '    protected void waitUntilElementIsVisibleNonThrow(WebElement element, long timeoutSeconds) {',
             '        try {',
             '            new WebDriverWait(driver, Duration.ofSeconds(timeoutSeconds))',
             '                    .until(ExpectedConditions.visibilityOf(element));',
             '        } catch (Exception ignored) {',
             '        }',
             '    }',
             '',
             '    protected void waitUntilElementIsVisibleNonThrow(By locator, long timeoutSeconds) {',
             '        try {',
             '            new WebDriverWait(driver, Duration.ofSeconds(timeoutSeconds))',
             '                    .until(ExpectedConditions.visibilityOfElementLocated(locator));',
             '        } catch (Exception ignored) {',
             '        }',
             '    }',
             '',
             '    protected void clickElement(WebElement element) {',
             '        waitUntilElementIsVisible(element);',
             '        element.click();',
             '    }',
             '',
             '    protected void typeText(WebElement element, String text) {',
             '        waitUntilElementIsVisible(element);',
             '        element.clear();',
             '        element.sendKeys(text);',
             '    }',
             '',
             '    protected boolean isVisible(WebElement element) {',
             '        try {',
             '            return element.isDisplayed();',
             '        } catch (Exception e) {',
             '            return false;',
             '        }',
             '    }',
             '',
             '    protected boolean isVisible(By locator) {',
             '        try {',
             '            return driver.findElement(locator).isDisplayed();',
             '        } catch (Exception e) {',
             '            return false;',
             '        }',
             '    }',
             '',
             '    protected boolean isInvisible(WebElement element) {',
             '        try {',
             '            return !element.isDisplayed();',
             '        } catch (NoSuchElementException | StaleElementReferenceException e) {',
             '            return true;',
             '        } catch (Exception e) {',
             '            return false;',
             '        }',
             '    }',
             '',
             '    protected boolean isInvisible(By locator) {',
             '        try {',
             '            return !driver.findElement(locator).isDisplayed();',
             '        } catch (NoSuchElementException | StaleElementReferenceException e) {',
             '            return true;',
             '        } catch (Exception e) {',
             '            return false;',
             '        }',
             '    }',
             '',
             '    protected String getText(WebElement element) {',
             '        return element.getText();',
             '    }',
             '}']
    write_file(dir_path / 'WebBasePage.java', '\n'.join(lines))


def write_hooks(output_dir):
    dir_path = Path(output_dir) / 'test/java' / '/'.join(HOOKS_PACKAGE.split('.'))
    lines = [f"package {HOOKS_PACKAGE};", '',
             'import io.cucumber.java.After;',
             'import io.cucumber.java.Before;',
             'import org.openqa.selenium.WebDriver;',
             'import org.openqa.selenium.chrome.ChromeDriver;',
             '',
             'public class Hooks {',
             '    private static WebDriver driver;',
             '',
             '    @Before',
             '    public void beforeScenario() {',
             '        driver = new ChromeDriver();',
             '    }',
             '',
             '    @After',
             '    public void afterScenario() {',
             '        if (driver != null) {',
             '            driver.quit();',
             '            driver = null;',
             '        }',
             '    }',
             '',
             '    public static WebDriver getDriver() {',
             '        return driver;',
             '    }',
             '}',]
    write_file(dir_path / 'Hooks.java', '\n'.join(lines))


def write_runner(output_dir):
    dir_path = Path(output_dir) / 'test/java' / '/'.join(RUNNER_PACKAGE.split('.'))
    lines = [f"package {RUNNER_PACKAGE};", '',
             'import org.junit.runner.RunWith;',
             'import io.cucumber.junit.Cucumber;',
             'import io.cucumber.junit.CucumberOptions;',
             '',
             '@RunWith(Cucumber.class)',
             '@CucumberOptions(',
             '        features = "src/test/resources/features",',
             f'        glue = {{"{STEP_PACKAGE}", "{HOOKS_PACKAGE}"}},',
             '        plugin = "pretty",',
             '        monochrome = true',
             ')',
             'public class RunCukesTest {',
             '}',]
    write_file(dir_path / 'RunCukesTest.java', '\n'.join(lines))


def generate_artifacts(contracts, output_dir):
    output_dir = Path(output_dir)
    write_features(contracts, output_dir)
    write_step_classes(contracts, output_dir)
    write_page_objects(contracts, output_dir)
    write_base_page(output_dir)
    write_hooks(output_dir)
    write_runner(output_dir)
