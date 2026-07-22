import json
from collections.abc import Callable

from mcp.server.fastmcp import FastMCP

from ..api_client import AcronisClient, AcronisError
from ._common import NO_TOKEN


def register(mcp: FastMCP, client_factory: Callable[[], AcronisClient | None]) -> None:

    @mcp.tool()
    async def acronis_get_tenant(
        tenant_id: str,
        embed_path: bool | None = None,
        allow_deleted: bool | None = None,
    ) -> str:
        """Fetch a tenant by ID.

        API: GET /api/2/tenants/{tenant_id} (Account Management v2)

        Args:
            tenant_id: Required tenant UUID.
            embed_path: If true, embed the tenant path in the result.
            allow_deleted: If true, a deleted tenant may be returned.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        params = {"embed_path": embed_path, "allow_deleted": allow_deleted}
        try:
            result = await client.get(f"/api/2/tenants/{tenant_id}", params=params)
            return json.dumps(result, indent=2)
        except AcronisError as e:
            return f"Error: {e}"
