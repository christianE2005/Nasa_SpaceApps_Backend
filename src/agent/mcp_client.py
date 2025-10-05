from typing import Any, Dict, List, Optional

from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client
from langchain_mcp_adapters.tools import load_mcp_tools
from src.core.settings import Settings

settings = Settings()

class MCPClient:
    def __init__(self, host: Optional[str] = None):
        self.host = host or settings.mcp_host
        self.tools = []
        self.prompts: List[Dict[str, Any]] = []
        self.templates: List[Dict[str, Any]] = []
        self.resources: List[Dict[str, Any]] = []

    async def get_server_attributes(self) -> Dict[str, Any]:
        async with streamablehttp_client(self.host) as (read, write, _):
            async with ClientSession(read, write) as session:
                await session.initialize()

                # Tools
                self.tools = await load_mcp_tools(session)

                # Prompts
                p = await session.list_prompts()
                self.prompts = [
                    {"name": getattr(x, "name", ""), "description": getattr(x, "description", "")}
                    for x in getattr(p, "prompts", [])
                ]

                # Resource templates
                t = await session.list_resource_templates()
                self.templates = [
                    {
                        "name": getattr(rt, "name", None),
                        "uri_template": getattr(rt, "uri_template", None),
                        "description": getattr(rt, "description", None),
                    }
                    for rt in getattr(t, "resource_templates", [])
                ]

                # Resources
                r = await session.list_resources()
                self.resources = [
                    {"uri": getattr(x, "uri", ""), "name": getattr(x, "name", "")}
                    for x in getattr(r, "resources", [])
                ]

                return {
                    "tools": self.tools,
                    "prompts": self.prompts,
                    "resource_templates": self.templates,
                    "resources": self.resources,
                }
