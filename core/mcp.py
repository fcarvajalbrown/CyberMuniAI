from strands.tools.mcp import MCPClient
from mcp import stdio_client, StdioServerParameters

def get_mcp_client() -> MCPClient:
    # serves ./data/ directory over MCP filesystem protocol
    params = StdioServerParameters(
        command="npx",
        args=["-y", "@modelcontextprotocol/server-filesystem", "./data"],
    )
    return MCPClient(lambda: stdio_client(params))