from google import genai
from google.genai import types

from config.settings import (
    GEMINI_API_KEY,
    GEMINI_MODEL
)


client = genai.Client(
    api_key=GEMINI_API_KEY
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