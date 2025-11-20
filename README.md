# IA Test Generator (Python)

Lee casos desde un `.txt`, solicita a una IA (stub local o Gemini) el contrato y genera artefactos Java (features, steps, PageObjects con PageFactory, hooks y runner).

## Comandos
- `python3 cli/main.py parse sample_input.txt`
- `python3 cli/main.py generate sample_input.txt --output generator/src --service-url local`
- `python3 cli/main.py generate sample_input.txt --output generator/src --service-url gemini`

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
