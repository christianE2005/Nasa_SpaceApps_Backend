import asyncio
from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client
from langchain_mcp_adapters.tools import load_mcp_tools

class MCPClient:
    def __init__(self, host: str):
        self.host = host
        self.tools = []
        self.prompts = []
        self.templates = []

    async def get_tools(self):
        async with streamablehttp_client(self.host) as (read, write, _):
            async with ClientSession(read, write) as session:
                await session.initialize()
                self.tools = await load_mcp_tools(session)
                return self.tools
