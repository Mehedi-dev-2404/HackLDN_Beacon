import html
import json
from pathlib import Path

from app.core.config import Settings
from app.models.schemas.health import HealthResponse


PAGES = {
    "dashboard": "Dashboard",
    "health": "Health",
    "scrape": "Scrape",
    "llm": "LLM",
    "socratic": "Socratic",
    "workflow": "Workflow",
}


def build_health_response(settings: Settings) -> HealthResponse:
    return HealthResponse(
        service=settings.app_name,
        version=settings.app_version,
        status="ok",
        environment=settings.environment,
        dependencies=settings.dependency_status(),
    )


def _load_html(path: Path) -> str:
    if not path.exists():
        return "<html><body><h1>UI file not found</h1></body></html>"
    return path.read_text(encoding="utf-8")


def build_ui_shell() -> str:
    buttons = "".join(
        [
            (f"<button class='tab-btn' data-page='{key}'>{value}</button>")
            for key, value in PAGES.items()
        ]
    )

    return f"""
<!DOCTYPE html>
<html lang='en'>
<head>
  <meta charset='utf-8' />
  <meta name='viewport' content='width=device-width, initial-scale=1' />
  <title>Beacon Panel</title>
  <style>
    body {{ margin: 0; font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, sans-serif; background: #0f172a; }}
    .layout {{ display: grid; grid-template-columns: 260px 1fr; min-height: 100vh; }}
    .sidebar {{ background: #111827; color: #e5e7eb; padding: 20px; border-right: 1px solid #1f2937; }}
    .sidebar h1 {{ margin: 0 0 16px; font-size: 1.1rem; }}
    .tab-btn {{ width: 100%; text-align: left; margin-bottom: 8px; border: 0; padding: 10px 12px; border-radius: 8px; background: #1f2937; color: #e5e7eb; cursor: pointer; font-weight: 600; }}
    .tab-btn:hover {{ background: #374151; }}
    .tab-btn.active {{ background: #2563eb; }}
    .quick-links a {{ display: block; color: #93c5fd; margin-top: 6px; font-size: 0.87rem; text-decoration: none; }}
    .quick-links a:hover {{ text-decoration: underline; }}
    iframe {{ width: 100%; height: 100vh; border: 0; background: #ffffff; }}
    @media (max-width: 900px) {{
      .layout {{ grid-template-columns: 1fr; }}
      .sidebar {{ border-right: 0; border-bottom: 1px solid #1f2937; }}
    }}
  </style>
</head>
<body>
  <div class='layout'>
    <aside class='sidebar'>
      <h1>Beacon Page Switcher</h1>
      {buttons}
      <div class='quick-links'>
        <a href='/docs' target='_blank' rel='noreferrer'>Open API Docs</a>
        <a href='/api/v1/health' target='_blank' rel='noreferrer'>Open Health JSON</a>
      </div>
    </aside>
    <main>
      <iframe id='panelFrame' src='/api/v1/health/ui/page/dashboard'></iframe>
    </main>
  </div>

  <script>
    const frame = document.getElementById('panelFrame');
    const buttons = Array.from(document.querySelectorAll('.tab-btn'));
    const activate = (page) => {{
      buttons.forEach((btn) => btn.classList.toggle('active', btn.dataset.page === page));
    }};
    buttons.forEach((button) => {{
      button.addEventListener('click', () => {{
        activate(button.dataset.page);
        frame.src = `/api/v1/health/ui/page/${{button.dataset.page}}`;
      }});
    }});
    activate('dashboard');
  </script>
</body>
</html>
"""


def _build_action_page(
    title: str,
    description: str,
    endpoint: str,
    method: str,
    payload: dict | None = None,
) -> str:
    has_payload = payload is not None
    payload_text = json.dumps(payload or {}, indent=2)
    escaped_payload = html.escape(payload_text)
    body_input = (
        f"""
      <label for='payload'>Request Body</label>
      <textarea id='payload'>{escaped_payload}</textarea>
        """
        if has_payload
        else ""
    )
    send_body = "body: payloadText,"
    if not has_payload:
        send_body = ""

    return f"""
<!DOCTYPE html>
<html lang='en'>
<head>
  <meta charset='utf-8' />
  <meta name='viewport' content='width=device-width, initial-scale=1' />
  <title>{title}</title>
  <style>
    body {{ margin: 0; font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, sans-serif; background: #f8fafc; color: #0f172a; }}
    .wrap {{ max-width: 900px; margin: 36px auto; padding: 24px; }}
    .card {{ border: 1px solid #e2e8f0; border-radius: 14px; padding: 20px; background: #ffffff; box-shadow: 0 8px 26px rgba(15, 23, 42, 0.06); }}
    h1 {{ margin-top: 0; margin-bottom: 8px; }}
    p {{ color: #475569; }}
    .links a {{ display: inline-block; margin-right: 14px; font-weight: 600; color: #2563eb; text-decoration: none; }}
    .links a:hover {{ text-decoration: underline; }}
    code {{ background: #e2e8f0; border-radius: 6px; padding: 2px 8px; }}
    label {{ display: block; margin: 14px 0 6px; font-weight: 600; font-size: 0.92rem; }}
    textarea {{ width: 100%; min-height: 170px; border: 1px solid #cbd5e1; border-radius: 10px; padding: 10px; font: 13px/1.5 ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; }}
    button {{ margin-top: 12px; border: 0; border-radius: 10px; padding: 10px 14px; background: #2563eb; color: #ffffff; font-weight: 700; cursor: pointer; }}
    button:hover {{ background: #1d4ed8; }}
    pre {{ margin-top: 14px; max-height: 320px; overflow: auto; background: #0f172a; color: #e2e8f0; border-radius: 10px; padding: 12px; font: 12px/1.5 ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; }}
  </style>
</head>
<body>
  <div class='wrap'>
    <div class='card'>
      <h1>{title}</h1>
      <p>{description}</p>
      <div class='links'>
        <a href='{endpoint}' target='_blank' rel='noreferrer'>Open Endpoint</a>
        <a href='/docs' target='_blank' rel='noreferrer'>Open Docs</a>
      </div>
      <p>Method: <code>{method}</code> | Path: <code>{endpoint}</code></p>
      {body_input}
      <button id='runAction'>Run Request</button>
      <pre id='responsePanel'>No response yet.</pre>
    </div>
  </div>
  <script>
    const runButton = document.getElementById('runAction');
    const panel = document.getElementById('responsePanel');
    runButton.addEventListener('click', async () => {{
      panel.textContent = 'Loading...';
      try {{
        let payloadText = '';
        const payloadEl = document.getElementById('payload');
        if (payloadEl) {{
          JSON.parse(payloadEl.value);
          payloadText = payloadEl.value;
        }}

        const response = await fetch('{endpoint}', {{
          method: '{method}',
          headers: {{ 'Content-Type': 'application/json' }},
          {send_body}
        }});

        const text = await response.text();
        let parsed = text;
        try {{
          parsed = JSON.parse(text);
        }} catch (_err) {{}}

        panel.textContent = JSON.stringify({{
          status: response.status,
          ok: response.ok,
          data: parsed
        }}, null, 2);
      }} catch (err) {{
        panel.textContent = JSON.stringify({{
          status: 'client_error',
          ok: false,
          error: String(err)
        }}, null, 2);
      }}
    }});
  </script>
</body>
</html>
"""


def get_ui_page(page_name: str, settings: Settings) -> str:
    page = page_name.lower().strip()

    if page == "dashboard":
        return _load_html(settings.ui_html_path)
    if page == "health":
        return _build_action_page(
            title="Health",
            description="Monitor API health and dependency status.",
            endpoint="/api/v1/health",
            method="GET",
            payload=None,
        )
    if page == "scrape":
        return _build_action_page(
            title="Scrape",
            description="Run scraping with inline HTML or URL source.",
            endpoint="/api/v1/scrape",
            method="POST",
            payload={
                "source_url": "",
                "mode": "http",
                "raw_html": "<html><body><ul><li>Math Coursework</li><li>Business Essay</li></ul></body></html>",
            },
        )
    if page == "llm":
        return _build_action_page(
            title="LLM",
            description="Run Gemini priority scoring and inspect normalized output.",
            endpoint="/api/v1/llm/rate",
            method="POST",
            payload={
                "tasks": [
                    {
                        "id": "task-1",
                        "title": "Math Homework",
                        "module": "Math",
                        "due_at": "2026-02-23T16:00:00Z",
                        "module_weight_percent": 40,
                        "estimated_hours": 6,
                        "notes": "Exam prep",
                    },
                    {
                        "id": "task-2",
                        "title": "Sport Session",
                        "module": "Sport",
                        "due_at": "2026-03-20T16:00:00Z",
                        "module_weight_percent": 10,
                        "estimated_hours": 2,
                        "notes": "",
                    },
                ],
                "custom_prompt": "",
                "temperature": 0.2,
            },
        )
    if page == "workflow":
        return _build_action_page(
            title="Workflow",
            description="Run scrape + llm + persistence in one endpoint call.",
            endpoint="/api/v1/workflow/run",
            method="POST",
            payload={
                "source_url": "",
                "raw_html": "<html><body><ul><li>Math Coursework</li><li>Business Essay</li></ul></body></html>",
                "scrape_mode": "http",
                "custom_prompt": "Prioritize most urgent coursework first.",
            },
        )
    if page == "socratic":
        return _build_action_page(
            title="Socratic Agent",
            description="Generate Socratic questions with integrity-aware behavior.",
            endpoint="/api/v1/socratic/question",
            method="POST",
            payload={
                "topic": "Recursion in Python",
                "previous_answer": "A function can call itself.",
                "student_query": "Can you help me understand this concept?",
            },
        )

    return _build_action_page(
        title="Unknown",
        description="Page not found. Use the left panel to switch between pages.",
        endpoint="/api/v1/health",
        method="GET",
        payload=None,
    )
