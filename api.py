import asyncio

from uuid import uuid4
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from mcp import ClientSession
from mcp.client.stdio import stdio_client

from agent.mcp_client import create_server_parameters
from agent.tool_adapter import convert_mcp_tools_to_gemini
from agent.agent import run_agent


app = FastAPI(
    title="College AI Assistant API"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    message: str
    session_id: str | None = None


@app.get("/")
def home():
    return {
        "message": "College AI Assistant API is running"
    }

conversations = {}

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

async def run_agent_api(
    session,
    gemini_tools,
    conversation,
    user_query
):

    from google import genai
    from google.genai import types

    from config.settings import (
        GEMINI_API_KEY,
        GEMINI_MODEL
    )

    client = genai.Client(
        api_key=GEMINI_API_KEY
    )

    conversation.append(
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(
                    text=user_query
                )
            ]
        )
    )

    while True:

        try:

            response = client.models.generate_content(
                model=GEMINI_MODEL,
                contents=conversation,
                config=types.GenerateContentConfig(
                    tools=[
                        types.Tool(
                            function_declarations=gemini_tools
                        )
                    ]
                )
            )

        except Exception as error:

            error_message = str(error)

            if (
                "429" in error_message
                or "RESOURCE_EXHAUSTED"
                in error_message
            ):

                return (
                    "⚠️ Gemini API quota has been reached. "
                    "Please try again later."
                )

            return (
                f"⚠️ An error occurred: {error}"
            )

        if not response.function_calls:

            return response.text or (
                "I couldn't generate a response."
            )

        conversation.append(
            response.candidates[0].content
        )

        for function_call in response.function_calls:

            tool_name = function_call.name

            tool_arguments = (
                function_call.args
                if function_call.args
                else {}
            )

            tool_result = await session.call_tool(
                tool_name,
                arguments=tool_arguments
            )

            result_text = ""

            for content in tool_result.content:

                if hasattr(content, "text"):
                    result_text += content.text

            conversation.append(
                types.Content(
                    role="user",
                    parts=[
                        types.Part.from_function_response(
                            name=tool_name,
                            response={
                                "result": result_text
                            }
                        )
                    ]
                )
            )