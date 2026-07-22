import json
from collections.abc import Callable

from mcp.server.fastmcp import FastMCP

from ..api_client import AcronisClient, AcronisError
from ._common import NO_TOKEN


def register(mcp: FastMCP, client_factory: Callable[[], AcronisClient | None]) -> None:

    @mcp.tool()
    async def acronis_get_agents(
        hostname: str | None = None,
        online: bool | None = None,
        os_family: str | None = None,
        tenant_id: str | None = None,
        up_to_date: bool | None = None,
        limit: int | None = None,
        after: str | None = None,
        before: str | None = None,
    ) -> str:
        """Fetch registered Acronis agents.

        API: GET /agents (Agent Manager v2)

        Args:
            hostname: Filter by host name; supports "hlike(x)"/"like(x)"/"tlike(x)"
                for starts-with/contains/ends-with matching.
            online: If true, only responsive agents; if false, only irresponsive.
            os_family: Filter by OS family (UNKNOWN/WINDOWS/LINUX/MACOSX/SOLARIS).
            tenant_id: Only return agents under this tenant subtree.
            up_to_date: Filter by whether agent software is current.
            limit: Max number of agents to return.
            after: Pagination cursor for the next page.
            before: Pagination cursor for the previous page.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        params = {
            "hostname": hostname,
            "online": online,
            "os_family": os_family,
            "tenant_id": tenant_id,
            "up_to_date": up_to_date,
            "limit": limit,
            "after": after,
            "before": before,
        }
        try:
            result = await client.get("/api/agent_manager/v2/agents", params=params)
            return json.dumps(result, indent=2)
        except AcronisError as e:
            return f"Error: {e}"
