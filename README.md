# College AI Assistant

A compact assistant for exploring and querying student records (profiles, marks, attendance). This repository provides a small local demo using an MCP-style tool server plus a Gemini-based assistant and a simple web UI.

## Quick Start

1. Create and activate a Python virtual environment (recommended):

```bash
python -m venv venv
# Windows PowerShell
venv\Scripts\Activate.ps1
# Windows CMD
venv\Scripts\activate.bat
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Add your Gemini API key to a `.env` file at the project root:

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

4. Initialize the local database (creates `college.db` and seeds sample data):

```bash
python database.py
```

5. Start the MCP tool server (tooling used by the assistant):

```bash
python server.py
```

6a. Run the CLI assistant:

```bash
python ai_agent.py
```

6b. Or run the HTTP API and use the web UI:

```bash
uvicorn api:app --reload --host 127.0.0.1 --port 8000
```

Then open `web/index.html` in a browser (or visit the API at `http://127.0.0.1:8000`).

## Configuration

Key settings are in `config/settings.py` and can be overridden via environment variables. Notable defaults:

- `GEMINI_MODEL` — default Gemini model
- `MCP_SERVER_COMMAND` / `MCP_SERVER_FILE` — command used to launch the MCP server

The project reads `GEMINI_API_KEY` from `.env`.

## Project Layout

- `ai_agent.py` — CLI client that starts an interactive assistant session
- `api.py` — FastAPI app exposing `/chat` and health endpoints
- `server.py` — MCP-style tool server with student data tools and prompts
- `database.py` — SQLite helpers, schema creation, and sample data seeding
- `config/settings.py` — Gemini and MCP server configuration
- `agent/` — adapter code that integrates Gemini and MCP tools
- `web/` — static frontend: `index.html`, `script.js`, `style.css`
- `requirements.txt` — Python dependencies

## API Endpoints

- `GET /` — basic health check
- `GET /health` — service status
- `POST /chat` — chat endpoint (JSON `{ "message": "...", "session_id": "..." }`)

Response format is `{ "session_id": "...", "response": "..." }`.

## Development Notes

- Re-run `python database.py` to recreate the sample database.
- For local development, use the `.env` file and `uvicorn --reload` for live reloads.
- Consider adding `docker-compose.yml` and a `Makefile` to simplify startup.

## Troubleshooting

- If the web UI cannot connect, confirm `uvicorn api:app` is running and reachable at `127.0.0.1:8000`.
- If Gemini authentication fails, verify `GEMINI_API_KEY` and account quotas.

## Contributing

Contributions are welcome. Open an issue or submit a pull request with a clear description of changes and steps to reproduce.

## License

This project is provided as-is for demonstration and learning purposes. Add a license file if you plan to publish or redistribute.
