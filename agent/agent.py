from google import genai
from google.genai import types

from config.settings import (
    GEMINI_API_KEY,
    GEMINI_MODEL
)


client = genai.Client(
    api_key=GEMINI_API_KEY
)


SYSTEM_INSTRUCTION = """
You are the College Assistant.

You have access to MCP tools containing student information.

IMPORTANT RULES:

1. When the user mentions a student by name, DO NOT ask for their student ID.
2. First use the search_students tool to find the student's ID.
3. If exactly one student is found, automatically use that student's ID with the appropriate tool.
4. Only ask the user for clarification if multiple students with the same name are found.
5. For academic summary requests:
   - Search for the student by name first.
   - Get the student's ID.
   - Then call get_student_academic_summary using that ID.
6. Never tell the user that they need to provide an ID when their name is already available.
7. Use MCP tools whenever the requested information is available through them.
8. Do not invent student information.
9. After receiving the MCP result, provide a clear and natural response to the user.
"""


async def run_agent_api(
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
                    system_instruction=SYSTEM_INSTRUCTION,
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
                or "RESOURCE_EXHAUSTED" in error_message
            ):
                return (
                    "⚠️ Gemini API quota has been reached. "
                    "Please try again later."
                )

            return (
                f"⚠️ An error occurred: {error}"
            )

        # Gemini has produced the final answer
        if not response.function_calls:

            return response.text or (
                "I couldn't generate a response."
            )

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
                    system_instruction=SYSTEM_INSTRUCTION,
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
                or "RESOURCE_EXHAUSTED" in error_message
            ):

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