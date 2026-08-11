# College AI Assistant

An interactive assistant for managing and querying college student information (profiles, marks, attendance) using an MCP-based tool server and Google Gemini.

## Overview

College AI Assistant demonstrates a small local system with:
- an MCP tool server (`server.py`) exposing student data and helper tools
- a CLI assistant (`ai_agent.py`) that uses Gemini plus MCP tools
- a FastAPI wrapper (`api.py`) for the browser UI
- a simple static frontend in `web/`
- a local SQLite database managed by `database.py`

## Features

- Search student profiles by name
- Retrieve detailed student information by ID
- View subject-wise marks, average marks, and academic performance
- View subject-wise attendance and attendance analysis
- Find students with attendance below a threshold
- Run the assistant from CLI, HTTP API, or web UI

## Repository Structure

- `ai_agent.py` — CLI client that starts an interactive assistant session
- `api.py` — FastAPI app exposing `/chat` and health endpoints
- `server.py` — MCP tool server with student data tools and prompts
- `database.py` — SQLite helpers, schema creation, and sample data seeding
- `config/settings.py` — Gemini and MCP server configuration
- `agent/` — shared adapter code for integrating Gemini and MCP tools
- `web/` — static frontend: `index.html`, `script.js`, `style.css`
- `requirements.txt` — Python dependencies

## Requirements

- Python 3.9+
- A valid Gemini API key

Install dependencies with:

```bash
pip install -r requirements.txt
```

## Configuration

Create a `.env` file in the project root with:

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

Default Gemini model and MCP settings are configured in `config/settings.py`:
- `GEMINI_MODEL = "gemini-2.5-flash"`
- `MCP_SERVER_COMMAND = "python"`
- `MCP_SERVER_FILE = "server.py"`

## Setup & Run

1. Initialize the database and seed sample data:

```bash
python database.py
```

2. Start the MCP tool server:

```bash
python server.py
```

3a. Run the CLI assistant:

```bash
python ai_agent.py
```

3b. Or start the HTTP API for the web UI:

```bash
uvicorn api:app --reload --host 127.0.0.1 --port 8000
```

4. Open `web/index.html` in your browser. The UI sends chat requests to `http://127.0.0.1:8000/chat` by default.

## API Endpoints

- `GET /` — basic health check
- `GET /health` — service status
- `POST /chat` — chat endpoint

Request body:

```json
{ "message": "Hello", "session_id": "optional-session-id" }
```

Response body:

```json
{ "session_id": "...", "response": "..." }
```

## Notes

- The local SQLite database file is `college.db`.
- The web UI is a static front end and requires the FastAPI server to be running.
- `database.py` can be re-run to recreate tables and insert sample rows.

## Troubleshooting

- If the web UI cannot connect, verify the API is running at `127.0.0.1:8000`.
- If Gemini fails due to quota or authentication, check `GEMINI_API_KEY` and your Gemini account settings.

## Optional Improvements

- Add `docker-compose.yml` for streamlined startup
- Add a `Makefile` or PowerShell script for common commands
- Add tests for the API and MCP tools
