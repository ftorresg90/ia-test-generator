# IA Test Generator (Python)

Lee casos desde un `.txt`, solicita a una IA (stub local o Gemini) el contrato y genera artefactos Java (features, steps, PageObjects con PageFactory, hooks y runner).

## Comandos
- `python3 cli/main.py parse sample_input.txt`
- `python3 cli/main.py generate sample_input.txt --output generator/src --service-url local`
- `python3 cli/main.py generate sample_input.txt --output generator/src --service-url gemini`
- Filtra casos específicos repitiendo `--case`, por ejemplo:
  `python3 cli/main.py generate sample_input.txt --case TC-001 --case TC-010`
- UI mínima para seleccionar casos de forma interactiva:
  `python3 cli/ui.py sample_input.txt`
- UI web básica:
  `python3 cli/web_ui.py sample_input.txt --port 8000`
- Validar locators con Selenium (local o remoto):
  1. Instala Selenium: `pip install selenium`.
  2. Si usarás navegador local, asegúrate de que el driver esté disponible (ChromeDriver/GeckoDriver/EdgeDriver) o usa Selenium Manager de Selenium 4.  
     Para Selenium Grid/BrowserStack/etc. pasa `--remote-url http://<grid>:4444/wd/hub`.
  3. Ejecuta `python3 cli/main.py validate sample_input.txt --service-url local --browser chrome --case TC-001`.

  Bandera opcional `--remote-url` (y en los tests `SELENIUM_REMOTE_URL`) permite validar sin instalar un driver local.

## Tests Java con Gradle

Se añadió un `build.gradle` que descarga automáticamente Selenium, Cucumber y TestNG.

1. Instala Gradle o genera el wrapper (`gradle wrapper`) y luego ejecuta `./gradlew test` (o `gradle test`) desde la raíz.  
2. El `sourceSet` apunta a `generator/src/test/java` y `generator/src/test/resources`, por lo que los artefactos generados se compilan y ejecutan con JUnit.

Variables útiles para los tests:
- `SELENIUM_BROWSER` (`chrome|firefox|edge`, por defecto `chrome`)
- `SELENIUM_HEADLESS` (`true/false`)
- `SELENIUM_REMOTE_URL` (URL de Selenium Grid; si está presente se usa `RemoteWebDriver`)

## Integración con Gemini
1. Crea una API Key en Google AI Studio y exporta la variable `GEMINI_API_KEY`.
2. Opcional: ajusta `GEMINI_MODEL` (default `gemini-pro`) o `GEMINI_API_URL` (default `https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent`).
3. Ejecuta el comando `generate` con `--service-url gemini`. El CLI construye el prompt en base al caso y espera un JSON válido según `docs/ai_contract.schema.json`.  
   - Las respuestas se almacenan en `.iatg_history/CASE-ID.json` antes de generar el código.

Si prefieres otra IA HTTP, entrega la URL vía `--service-url https://mi-servicio` y el CLI hará un POST con el caso.

## Estructura
- `docs/`: contrato IA y schema.
- `cli/`: parser, clientes de IA, generador y utilidades.
- `ai/stub/`: stub heurístico para desarrollo offline.
- `generator/src`: salida Java (se sobreescribe en cada `generate`).
