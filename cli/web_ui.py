import json
import subprocess
from pathlib import Path
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs

from src.parser import parse_cases


class CaseServer(BaseHTTPRequestHandler):
    CASES = []
    BASE_ARGS = {}
    history = {"generate": "", "validate": "", "harvest": ""}

    def do_GET(self):
        if self.path == "/":
            html = self.build_page()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(html.encode("utf-8"))
        elif self.path.startswith("/history"):
            case_id = self.path.split("/")[-1]
            log = self.history.get(case_id, "")
            self.send_response(200)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.end_headers()
            self.wfile.write(log.encode("utf-8"))
        else:
            self.send_error(404)

    def do_POST(self):
        if self.path == "/generate":
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length).decode("utf-8")
            payload = parse_qs(body)
            selected = payload.get("case", [])
            service_url = payload.get("service_url", [self.BASE_ARGS["service_url"]])[0]
            command = [
                "python3",
                "cli/main.py",
                "generate",
                self.BASE_ARGS["file"],
                "--output",
                self.BASE_ARGS["output"],
                "--service-url",
                service_url,
            ]
            for case_id in selected:
                command.extend(["--case", case_id])
            message = self.run_command(command, "generate", selected)
        elif self.path == "/validate":
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length).decode("utf-8")
            payload = parse_qs(body)
            selected = payload.get("case", [])
            service_url = payload.get("service_url", [self.BASE_ARGS["service_url"]])[0]
            browser = payload.get("browser", ["chrome"])[0]
            timeout = payload.get("timeout", ["5"])[0]
            remote_url = payload.get("remote_url", [""])[0]

            command = [
                "python3",
                "cli/main.py",
                "validate",
                self.BASE_ARGS["file"],
                "--service-url",
                service_url,
                "--browser",
                browser,
                "--timeout",
                timeout,
            ]
            if remote_url:
                command.extend(["--remote-url", remote_url])
            for case_id in selected:
                command.extend(["--case", case_id])
            message = self.run_command(command, "validate", selected)
        elif self.path == "/harvest":
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length).decode("utf-8")
            payload = parse_qs(body)
            selected = payload.get("case", [])
            output = payload.get("harvest_output", [self.BASE_ARGS["harvest_output"]])[0]
            browser = payload.get("browser", ["chrome"])[0]
            timeout = payload.get("timeout", ["5"])[0]
            remote_url = payload.get("remote_url", [""])[0]
            hints_file = payload.get("hints_file", [self.BASE_ARGS["hints_file"]])[0]
            show_browser = "no_headless" in payload
            update_hints = "update_hints" in payload

            command = [
                "python3",
                "cli/main.py",
                "harvest",
                self.BASE_ARGS["file"],
                "--output",
                output,
                "--browser",
                browser,
                "--timeout",
                timeout,
                "--hints-file",
                hints_file,
            ]
            if remote_url:
                command.extend(["--remote-url", remote_url])
            if show_browser:
                command.append("--no-headless")
            if update_hints:
                command.append("--update-hints")
            for case_id in selected:
                command.extend(["--case", case_id])
            message = self.run_command(command, "harvest", selected)
        else:
            self.send_error(404)
            return

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps({"message": message}).encode("utf-8"))

    def run_command(self, command, action, selected):
        if not selected:
            return "Debes seleccionar al menos un caso."
        try:
            result = subprocess.run(
                command,
                check=True,
                capture_output=True,
                text=True,
            )
            message = f"{action.capitalize()} completada:\n{result.stdout}"
        except subprocess.CalledProcessError as exc:
            message = f"Error en {action}:\n{exc.stderr or exc.stdout}"
        self.history[action] = message
        return message

    def build_page(self):
        rows = "\n".join(
            f"""
            <label class="case-item">
                <input type="checkbox" name="case" value="{case.get('id')}" />
                <div class="case-info">
                    <span class="case-title">{case.get('id')} · {case.get('title')}</span>
                    <span class="case-url">{case.get('url') or 'sin URL'}</span>
                </div>
            </label>
            """
            for case in self.CASES
        )
        return f"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="utf-8" />
    <title>IA Test Generator</title>
    <style>
        :root {{
            --bg: #fff2e2;
            --surface: #fffaf5;
            --card: #ffffff;
            --accent: #ff8c5c;
            --accent-dark: #f8743a;
            --text: #3b2f2f;
            --muted: #8c6b56;
            --border: #f2d7c3;
        }}
        * {{ box-sizing: border-box; }}
        body {{
            margin: 0;
            min-height: 100vh;
            font-family: "Inter", "Segoe UI", system-ui, sans-serif;
            background: var(--bg);
            color: var(--text);
            display: flex;
            flex-direction: column;
        }}
        header {{
            padding: 40px 16px 80px;
            text-align: center;
            background: linear-gradient(120deg, #ffe1c7, #ffd3ac);
        }}
        header h1 {{ margin: 0; font-size: 32px; }}
        header p {{ margin: 8px 0 0; color: var(--muted); }}
        main {{
            flex: 1;
            width: 100%;
            max-width: 1040px;
            margin: -60px auto 40px;
            padding: 0 20px;
        }}
        .panel {{
            background: var(--card);
            border-radius: 24px;
            border: 1px solid var(--border);
            box-shadow: 0 25px 60px rgba(255, 140, 92, 0.18);
            padding: 28px;
        }}
        .section {{
            margin-bottom: 28px;
        }}
        .section h2 {{ margin: 0 0 12px; font-size: 20px; }}
        .section p {{ margin: 0 0 16px; color: var(--muted); }}
        .cases-controls {{
            display: flex;
            gap: 12px;
            flex-wrap: wrap;
            margin-bottom: 16px;
        }}
        .cases-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(230px, 1fr));
            gap: 12px;
            max-height: 320px;
            overflow-y: auto;
            padding-right: 4px;
        }}
        .case-item {{
            display: flex;
            gap: 10px;
            padding: 12px;
            border-radius: 14px;
            border: 1px solid var(--border);
            background: var(--surface);
            cursor: pointer;
            transition: border-color 0.2s, transform 0.1s;
        }}
        .case-item:hover {{
            border-color: var(--accent);
            transform: translateY(-2px);
        }}
        .case-info {{
            display: flex;
            flex-direction: column;
            gap: 2px;
        }}
        .case-item input {{ margin-top: 3px; }}
        .case-title {{ font-weight: 600; font-size: 14px; }}
        .case-url {{ font-size: 12px; color: var(--muted); }}
        .form-row {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 16px;
            margin-bottom: 18px;
        }}
        label span {{
            display: block;
            font-size: 13px;
            color: var(--muted);
            margin-bottom: 4px;
        }}
        input[type='text'],
        input[type='number'],
        select {{
            width: 100%;
            padding: 10px 12px;
            border-radius: 12px;
            border: 1px solid var(--border);
            font-size: 14px;
        }}
        .actions {{ display: flex; flex-wrap: wrap; gap: 12px; }}
        .btn {{
            border: none;
            border-radius: 999px;
            padding: 10px 22px;
            background: var(--accent);
            color: #fff;
            font-size: 14px;
            cursor: pointer;
            transition: background 0.2s, transform 0.1s;
        }}
        .btn:hover {{ background: var(--accent-dark); }}
        .btn:active {{ transform: scale(0.98); }}
        .btn-secondary {{
            background: transparent;
            color: var(--accent);
            border: 1px solid var(--accent);
        }}
        #log {{
            white-space: pre-wrap;
            background: var(--surface);
            border-radius: 18px;
            border: 1px dashed var(--border);
            padding: 18px;
            min-height: 120px;
            color: var(--muted);
        }}
        @media (max-width: 720px) {{
            header h1 {{ font-size: 26px; }}
            .cases-grid {{ grid-template-columns: repeat(auto-fill, minmax(180px, 1fr)); }}
            .panel {{ padding: 20px; }}
        }}
    </style>
    <script>
        async function runAction(event, endpoint) {{
            event.preventDefault();
            const form = event.target.closest("form");
            const data = new FormData(form);
            const response = await fetch(endpoint, {{
                method: "POST",
                body: new URLSearchParams(data)
            }});
            const result = await response.json();
            document.getElementById("log").textContent = result.message;
        }}
        function toggleSelection(value) {{
            document.querySelectorAll("input[name='case']").forEach(cb => cb.checked = value);
        }}
    </script>
</head>
<body>
    <header>
        <h1>IA Test Generator</h1>
        <p>Orquesta tus casos, genera artefactos y valida selectores sin salir del navegador.</p>
    </header>
    <main>
        <form class="panel">
            <section class="section">
                <h2>1. Selecciona los casos</h2>
                <p>Elige qué escenarios vas a generar o validar.</p>
                <div class="cases-controls">
                    <button type="button" class="btn btn-secondary" onclick="toggleSelection(true)">Seleccionar todos</button>
                    <button type="button" class="btn btn-secondary" onclick="toggleSelection(false)">Limpiar selección</button>
                </div>
                <div class="cases-grid">
                    {rows}
                </div>
            </section>
            <section class="section">
                <h2>2. Configuración</h2>
                <div class="form-row">
                    <label>
                        <span>Service URL</span>
                        <input type="text" name="service_url" value="{self.BASE_ARGS['service_url']}" />
                    </label>
                    <label>
                        <span>Remote WebDriver URL</span>
                        <input type="text" name="remote_url" placeholder="http://localhost:4444/wd/hub" />
                    </label>
                </div>
            </section>
            <section class="section">
                <h2>3. Genera artefactos</h2>
                <p>Page Objects, steps y features listos para compilar.</p>
                <div class="actions">
                    <button class="btn" onclick="runAction(event, '/generate')">Generar</button>
                </div>
            </section>
            <section class="section">
                <h2>4. Valida locators</h2>
                <p>Ejecuta Selenium local o remoto para comprobar los selectores.</p>
                <div class="form-row">
                    <label>
                        <span>Navegador</span>
                        <select name="browser">
                            <option value="chrome">Chrome</option>
                            <option value="firefox">Firefox</option>
                            <option value="edge">Edge</option>
                        </select>
                    </label>
                    <label>
                        <span>Timeout (segundos)</span>
                        <input type="number" name="timeout" value="5" min="1" />
                    </label>
                </div>
                <div class="actions">
                    <button class="btn" onclick="runAction(event, '/validate')">Validar</button>
                </div>
            </section>
            <section class="section">
                <h2>5. Harvest de locators</h2>
                <p>Abre cada URL en modo headless y sugiere selectores automáticamente.</p>
                <div class="form-row">
                    <label>
                        <span>Archivo de salida</span>
                        <input type="text" name="harvest_output" value="{self.BASE_ARGS['harvest_output']}" />
                    </label>
                    <label>
                        <span>Archivo de hints</span>
                        <input type="text" name="hints_file" value="{self.BASE_ARGS['hints_file']}" />
                    </label>
                </div>
                <div class="form-row">
                    <label>
                        <span>Remote WebDriver URL</span>
                        <input type="text" name="remote_url" placeholder="http://localhost:4444/wd/hub" />
                    </label>
                </div>
                <div class="form-row" style="grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));">
                    <label style="display:flex; align-items:center; gap:8px;">
                        <input type="checkbox" name="no_headless" />
                        <span>Mostrar navegador</span>
                    </label>
                    <label style="display:flex; align-items:center; gap:8px;">
                        <input type="checkbox" name="update_hints" checked />
                        <span>Actualizar hints</span>
                    </label>
                </div>
                <div class="actions">
                    <button class="btn" onclick="runAction(event, '/harvest')">Ejecutar harvest</button>
                </div>
            </section>
        </form>
        <section class="panel" style="margin-top:24px;">
            <h2>Historial y mensajes</h2>
            <div id="log">Selecciona casos y ejecuta una acción para ver el resultado aquí.</div>
        </section>
    </main>
</body>
</html>
"""


def run_server(args):
    cases = parse_cases(Path(args.file))
    CaseServer.CASES = cases
    CaseServer.BASE_ARGS = {
        "file": args.file,
        "output": args.output,
        "service_url": args.service_url,
        "harvest_output": args.harvest_output,
        "hints_file": args.hints_file,
    }
    server = HTTPServer(("0.0.0.0", args.port), CaseServer)
    print(f"UI web disponible en http://127.0.0.1:{args.port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServidor detenido por el usuario.")
    finally:
        server.server_close()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="UI web mínima para IA Test Generator")
    parser.add_argument("file")
    parser.add_argument("--output", default="generator/src")
    parser.add_argument("--service-url", default="local")
    parser.add_argument("--port", type=int, default=8000)
    parser.add_argument("--harvest-output", default="locator_suggestions.json")
    parser.add_argument("--hints-file", default="ai/stub/locator_hints.json")
    args = parser.parse_args()
    run_server(args)
