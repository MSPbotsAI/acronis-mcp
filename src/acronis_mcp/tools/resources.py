import json
from collections.abc import Callable

from mcp.server.fastmcp import FastMCP

from ..api_client import AcronisClient, AcronisError
from ._common import NO_TOKEN

_BASE = "/api/resource_management/v4"


def register(mcp: FastMCP, client_factory: Callable[[], AcronisClient | None]) -> None:

    @mcp.tool()
    async def acronis_get_resources(
        tenant_id: str | None = None,
        agent_id: str | None = None,
        parent_id: str | None = None,
        type: str | None = None,
        resource_id: str | None = None,
        search: str | None = None,
        include_attributes: bool | None = None,
        include_deleted: bool | None = None,
        is_group: bool | None = None,
        updated_at: str | None = None,
        limit: int | None = None,
        after: str | None = None,
        before: str | None = None,
        extra_params: dict[str, object] | None = None,
    ) -> str:
        """Fetch a list of all resources (managed workloads/devices/groups).

        API: GET /resource_management/v4/resources

        Args:
            tenant_id: Filter by one or more tenant IDs/UUIDs (max 100).
            agent_id: Filter by one or more agent UUIDs (max 100).
            parent_id: Filter by one or more parent UUIDs (max 100).
            type: Filter by resource type (ResourceType or cti.CTI), max 10.
            resource_id: Filter by one or more resource UUIDs (max 100).
            search: SQL-like search by type and tags.
            include_attributes: If true, include resources' attributes.
            include_deleted: If true, include deleted resources.
            is_group: If true, only groups; if false, only non-group resources.
            updated_at: Filter by update timestamp.
            limit: Number of elements per page.
            after: Pagination cursor after the current page.
            before: Pagination cursor before the current page.
            extra_params: Additional raw query params (has_member_id,
                include_attribute_namespaces, not_applied_only,
                applicable_to_policy_id, applicable_to_policy_selection_id,
                applied_only, applied_to_policy_id, applied_to_policy_selection_id,
                allowed_actions).
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        params = {
            "tenant_id": tenant_id,
            "agent_id": agent_id,
            "parent_id": parent_id,
            "type": type,
            "resource_id": resource_id,
            "search": search,
            "include_attributes": include_attributes,
            "include_deleted": include_deleted,
            "is_group": is_group,
            "updated_at": updated_at,
            "limit": limit,
            "after": after,
            "before": before,
            **(extra_params or {}),
        }
        try:
            result = await client.get(f"{_BASE}/resources", params=params)
            return json.dumps(result, indent=2)
        except AcronisError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def acronis_get_resource_statuses(
        tenant_id: str | None = None,
        agent_id: str | None = None,
        resource_id: str | None = None,
        search: str | None = None,
        include_deleted: bool | None = None,
        updated_at: str | None = None,
        order: str | None = None,
        limit: int | None = None,
        after: str | None = None,
        before: str | None = None,
        extra_params: dict[str, object] | None = None,
    ) -> str:
        """Fetch the protection status of resources.

        API: GET /resource_management/v4/resource_statuses

        Args:
            tenant_id: Filter by one or more tenant IDs/UUIDs (max 100).
            agent_id: Filter by one or more agent UUIDs (max 100).
            resource_id: Filter by one or more resource UUIDs (max 100).
            search: SQL-like search by type and tags.
            include_deleted: If true, include deleted resources.
            updated_at: Filter by update timestamp.
            order: e.g. "is_group" or "asc(updated_at)".
            limit: Number of elements per page.
            after: Pagination cursor after the current page.
            before: Pagination cursor before the current page.
            extra_params: Additional raw query params (parent_id, has_member_id,
                type, selection_id, include_attributes,
                include_attribute_namespaces).
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        params = {
            "tenant_id": tenant_id,
            "agent_id": agent_id,
            "resource_id": resource_id,
            "search": search,
            "include_deleted": include_deleted,
            "updated_at": updated_at,
            "order": order,
            "limit": limit,
            "after": after,
            "before": before,
            **(extra_params or {}),
        }
        try:
            result = await client.get(f"{_BASE}/resource_statuses", params=params)
            return json.dumps(result, indent=2)
        except AcronisError as e:
            return f"Error: {e}"
