# Contrato IA (Python)

La IA debe responder un JSON con:
- `meta`: caseId, title, url, tags.
- `gherkin`: featureName, featureDescription, background, scenarios.
- `stepDefinitions`: glueClass, methodName, parámetros, body, acción.
- `pageObjects`: className, métodos, locators.
- `notes`: advertencias.

Este contrato se valida con `docs/ai_contract.schema.json`.
