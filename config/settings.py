import os

from dotenv import load_dotenv


load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

GEMINI_MODEL = "gemini-2.5-flash"

MCP_SERVER_COMMAND = "python"

MCP_SERVER_FILE = "server.py"