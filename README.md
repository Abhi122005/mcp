# College AI Assistant

An interactive assistant for managing and querying college student information (profiles, marks, attendance) using an MCP-based tool server and the Google Gemini model.

**Project**: A small demo combining an MCP tool server (`server.py`) that exposes student data and tools, a CLI agent (`ai_agent.py`), a FastAPI wrapper (`api.py`) and a simple web UI (`web/`). Data is stored in a local SQLite database (`college.db`) managed by `database.py`.

**Features**
- **Search students** and view profiles.
- **View marks** and **attendance** per student.
- **Find low-attendance** students below a threshold.
- CLI agent, HTTP API, and a browser-based frontend.

**Repository Structure**
- [ai_agent.py](ai_agent.py) — CLI client that runs the interactive assistant.
- [api.py](api.py) — FastAPI server exposing `POST /chat` for the web UI and other clients.
- [server.py](server.py) — MCP tool server exposing student-related tools.
- [database.py](database.py) — SQLite helpers, schema creation and sample data.
- [config/settings.py](config/settings.py) — configuration (Gemini model, MCP command/file).
- [agent/](agent) — adapter code that integrates Gemini and MCP tools (`agent.py`, `mcp_client.py`, `tool_adapter.py`).
- [web/](web) — static web UI: `index.html`, `script.js`, `style.css`.
- [requirements.txt](requirements.txt) — Python dependencies.

**Requirements**
- Python 3.9+ (recommended)
- Add your dependencies and install with:

```bash
pip install -r requirements.txt
```

**Environment**
Create a `.env` file in the project root with at least:

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

The Gemini model used is configured in `config/settings.py` (default: `gemini-2.5-flash`).

**Setup & Run**
1. Initialize the database (creates schema and inserts sample data):

```bash
python database.py
```

2. Run the MCP tool server (exposes tools from `server.py`):

```bash
python server.py
```

3a. Run the CLI agent (connects to the MCP server and Gemini):

```bash
python ai_agent.py
```

3b. Or run the HTTP API (FastAPI) which the web UI uses:

```bash
uvicorn api:app --reload --host 127.0.0.1 --port 8000
```

4. Open the web UI: open [web/index.html](web/index.html) in your browser. The UI posts to `http://127.0.0.1:8000/chat` by default.

**API**
- `GET /` — health check returning a running message.
- `POST /chat` — accepts JSON `{ "message": "...", "session_id": "optional" }` and returns `{ "session_id": "...", "response": "..." }`.

**Configuration notes**
- MCP server command and file are defined in [config/settings.py](config/settings.py): `MCP_SERVER_COMMAND` and `MCP_SERVER_FILE`.
- The project uses a local SQLite database file named `college.db`.
- Gemini API quota errors are handled and surfaced to users when the model responds with quota/exhaustion errors.

**Development**
- To iterate quickly: run the MCP server and the API locally, then open the web UI. Use the sample buttons for example queries.
- To re-seed sample data: re-run `python database.py` (this will create tables and insert sample rows).

**Troubleshooting**
- If the web UI shows "Unable to connect", ensure the API is running at `127.0.0.1:8000`.
- If Gemini responses fail with quota errors, check your `GEMINI_API_KEY` and usage limits.

If you'd like, I can also: run tests (if added), create a `docker-compose` for easy local launches, or add a minimal `Makefile`/scripts to automate startup.
