# College AI Assistant

A local AI assistant for exploring student profiles, marks, attendance, and academic performance. The project combines a Gemini-powered agent, an MCP-style tool server backed by SQLite, a FastAPI API, and a lightweight browser interface.

## Features

- Search students by name and retrieve profile details.
- Review subject marks, averages, strongest and weakest subjects.
- Review subject attendance and find students below a threshold.
- Add students and marks through assistant requests.
- Use the same agent through either the CLI or the web application.

## Requirements

- Python 3.10 or later
- A Gemini API key
- PowerShell, Command Prompt, or another Python-compatible shell

## Setup

From the project root, create and activate a virtual environment:

```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

On Windows Command Prompt, use `venv\Scripts\activate.bat` instead. Install the pinned dependencies:

```powershell
pip install -r requirements.txt
```

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

Initialize the sample SQLite database:

```powershell
python database.py
```

This creates `college.db` and seeds the sample student records.

## Run The CLI

Start an interactive assistant session:

```powershell
python ai_agent.py
```

The CLI starts the MCP tool server as needed. You do not need to run `server.py` separately.

## Run The Web App

Start the API in one terminal:

```powershell
uvicorn api:app --reload --host 127.0.0.1 --port 8000
```

Serve the static frontend from the `web` directory in a second terminal. Serving it on port `5500` matches the API's local CORS configuration:

```powershell
python -m http.server 5500 --directory web
```

Open <http://127.0.0.1:5500> in your browser. The API and interactive documentation are available at <http://127.0.0.1:8000> and <http://127.0.0.1:8000/docs>.

## Configuration

Configuration defaults are defined in `config/settings.py`:

- `GEMINI_API_KEY` — loaded from the environment or root `.env` file.
- `GEMINI_MODEL` — Gemini model name, defaulting to `gemini-2.5-flash`.
- `MCP_SERVER_COMMAND` — command used to start the tool server, defaulting to `python`.
- `MCP_SERVER_FILE` — tool server entry point, defaulting to `server.py`.

## API

### Health check

```http
GET /health
```

Example response:

```json
{"status":"ok","service":"College AI Assistant"}
```

### Chat

```http
POST /chat
Content-Type: application/json

{"message":"What are Abhishek's marks?"}
```

The response includes a session ID that can be sent with subsequent messages to preserve conversation context:

```json
{"session_id":"session-uuid","response":"..."}
```

## Project Layout

| Path | Purpose |
| --- | --- |
| `ai_agent.py` | Interactive CLI client |
| `api.py` | FastAPI application and chat endpoints |
| `server.py` | MCP-style student data tools |
| `database.py` | SQLite schema, queries, and sample data |
| `agent/` | Gemini agent and MCP integration |
| `config/settings.py` | Environment-backed configuration |
| `web/` | Static browser interface |
| `requirements.txt` | Pinned Python dependencies |

## Troubleshooting

- **Web UI cannot connect:** Confirm both servers are running, then open the UI at `http://127.0.0.1:5500` rather than opening `index.html` directly.
- **Gemini authentication fails:** Check `GEMINI_API_KEY` in `.env` and confirm the key has access to the configured model.
- **Database records are missing:** Run `python database.py` from the project root to recreate and reseed `college.db`.
- **MCP startup fails:** Run commands from the project root and verify that the virtual environment is active.

## License

This project is provided as-is for demonstration and learning purposes.
