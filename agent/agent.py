from google import genai
from google.genai import types

from config.settings import (
    GEMINI_API_KEY,
    GEMINI_MODEL
)


client = genai.Client(
    api_key=GEMINI_API_KEY
)
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

async def run_agent(
    session,
    gemini_tools,
    conversation,
    user_query
):

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

            if "429" in error_message or "RESOURCE_EXHAUSTED" in error_message:
                print(
                    "\nCollege Assistant:"
                    "\n⚠️ Gemini API quota has been reached."
                    "\nPlease try again later."
                )
            else:
                print(
                    "\nCollege Assistant:"
                    f"\n⚠️ An error occurred: {error}"
                )

            return

        # Gemini has produced the final answer
        if not response.function_calls:

            if response.text:
                print("\nCollege Assistant:")
                print(response.text)

            if response.candidates:
                conversation.append(
                    response.candidates[0].content
                )

            break

        # Save Gemini's tool-call response
        if response.candidates:
            conversation.append(
                response.candidates[0].content
            )

        # Execute MCP tools
        for function_call in response.function_calls:

            tool_name = function_call.name

            tool_arguments = (
                function_call.args
                if function_call.args
                else {}
            )

            try:

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

            except Exception as error:

                conversation.append(
                    types.Content(
                        role="user",
                        parts=[
                            types.Part.from_function_response(
                                name=tool_name,
                                response={
                                    "error": str(error)
                                }
                            )
                        ]
                    )
                )

SYSTEM_INSTRUCTION = """
You are the College Assistant.

You have access to MCP tools for student information.

When a user asks about a student by name:

1. If you do not know the student's ID, first call search_students.
2. Use the returned student ID with the appropriate student tool.
3. Never ask the user for a student ID when the student's name is available.
4. If exactly one student matches the name, use that student's ID automatically.
5. If multiple students match, ask the user to clarify which student they mean.
6. For academic summary requests, retrieve the student's academic information using the available MCP tools and provide a clear natural-language answer.
"""