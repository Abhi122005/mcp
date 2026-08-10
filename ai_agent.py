import asyncio

from mcp import ClientSession
from mcp.client.stdio import stdio_client

from agent.agent import run_agent
from agent.mcp_client import create_server_parameters
from agent.tool_adapter import (
    convert_mcp_tools_to_gemini
)


async def main():

    print("\n======================================")
    print("       COLLEGE AI ASSISTANT")
    print("======================================")

    server_params = create_server_parameters()

    async with stdio_client(server_params) as (read, write):

        async with ClientSession(
            read,
            write
        ) as session:

            # Initialize MCP
            await session.initialize()

            # Discover tools
            tools_result = await session.list_tools()

            print("\nAvailable MCP tools:")

            for tool in tools_result.tools:
                print(f"  - {tool.name}")

            # Convert MCP tools → Gemini tools
            gemini_tools = convert_mcp_tools_to_gemini(
                tools_result.tools
            )

            # Conversation memory
            conversation = []

            print("\n--------------------------------------")
            print("College Assistant is ready!")
            print("Type 'exit' to quit.")
            print("--------------------------------------")

            while True:

                user_query = input("\nYou: ").strip()

                if not user_query:
                    continue

                if user_query.lower() == "exit":

                    print(
                        "\nCollege Assistant: Goodbye!"
                    )

                    break

                await run_agent(
                    session,
                    gemini_tools,
                    conversation,
                    user_query
                )


if __name__ == "__main__":

    asyncio.run(main())
