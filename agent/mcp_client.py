from mcp import StdioServerParameters

from config.settings import (
    MCP_SERVER_COMMAND,
    MCP_SERVER_FILE
)


def create_server_parameters():

    return StdioServerParameters(
        command=MCP_SERVER_COMMAND,
        args=[MCP_SERVER_FILE]
    )