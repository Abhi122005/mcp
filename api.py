from uuid import uuid4

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from mcp import ClientSession
from mcp.client.stdio import stdio_client

from agent.mcp_client import create_server_parameters
from agent.tool_adapter import convert_mcp_tools_to_gemini
from agent.agent import run_agent_api


app = FastAPI(
    title="College AI Assistant API"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
    "http://127.0.0.1:5500",
    "http://localhost:5500",
],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    message: str
    session_id: str | None = None


conversations = {}


@app.get("/")
def home():
    return {
        "message": "College AI Assistant API is running"
    }


@app.post("/chat")
async def chat(request: ChatRequest):

    session_id = request.session_id

    if not session_id:
        session_id = str(uuid4())

    if session_id not in conversations:
        conversations[session_id] = []

    conversation = conversations[session_id]

    server_params = create_server_parameters()

    async with stdio_client(server_params) as (read, write):

        async with ClientSession(
            read,
            write
        ) as session:

            await session.initialize()

            tools_result = await session.list_tools()

            gemini_tools = (
                convert_mcp_tools_to_gemini(
                    tools_result.tools
                )
            )

            response = await run_agent_api(
                session,
                gemini_tools,
                conversation,
                request.message
            )

            return {
                "session_id": session_id,
                "response": response
            }

@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "College AI Assistant"
    }