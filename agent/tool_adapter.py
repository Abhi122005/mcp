from google.genai import types


def convert_mcp_tools_to_gemini(mcp_tools):

    gemini_tools = []

    for tool in mcp_tools:

        function_declaration = types.FunctionDeclaration(
            name=tool.name,
            description=tool.description or "",
            parameters=tool.input_schema
        )

        gemini_tools.append(
            function_declaration
        )

    return gemini_tools