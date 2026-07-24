import json
from collections.abc import Callable

from mcp.server.fastmcp import FastMCP

from ..api_client import AcronisClient, AcronisError
from ._common import NO_TOKEN

_BASE = "/api/policy_management/v4"


def register(mcp: FastMCP, client_factory: Callable[[], AcronisClient | None]) -> None:

    @mcp.tool()
    async def acronis_get_policies(
        tenant_id: str | None = None,
        types: str | None = None,
        enabled: bool | None = None,
        policy_id: str | None = None,
        search: str | None = None,
        include_settings: bool | None = None,
        templates_only: bool | None = None,
        limit: int | None = None,
        after: str | None = None,
        before: str | None = None,
        extra_params: dict[str, object] | None = None,
    ) -> str:
        """Fetch a list of protection policies.

        API: GET /policy_management/v4/policies

        Args:
            tenant_id: Filter by one or more tenant IDs/UUIDs (max 100).
            types: Filter by one or more policy types (max 10).
            enabled: Filter only enabled or disabled policies.
            policy_id: Filter by one or more policy IDs (max 100).
            search: SQL-like search by name, type, and tags.
            include_settings: If true, include policy settings.
            templates_only: If true, filter out non-template policies.
            limit: Number of elements per page.
            after: Pagination cursor after the current page.
            before: Pagination cursor before the current page.
            extra_params: Additional raw query params (policy_selection_id,
                parent_ids, applicable_to_context_id,
                applicable_to_context_selection_id, dependency_namespace,
                dependency_path, os_type, include_settings_constraints,
                include_applied_context, include_templates, include_temporaries,
                favorite, default).
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        params = {
            "tenant_id": tenant_id,
            "types": types,
            "enabled": enabled,
            "policy_id": policy_id,
            "search": search,
            "include_settings": include_settings,
            "templates_only": templates_only,
            "limit": limit,
            "after": after,
            "before": before,
            **(extra_params or {}),
        }
        try:
            result = await client.get(f"{_BASE}/policies", params=params)
            return json.dumps(result, indent=2)
        except AcronisError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def acronis_get_policy_applications(
        tenant_id: str | None = None,
        policy_id: str | None = None,
        context_id: str | None = None,
        context_type: str | None = None,
        status: str | None = None,
        enabled_only: bool | None = None,
        limit: int | None = None,
        after: str | None = None,
        before: str | None = None,
        extra_params: dict[str, object] | None = None,
    ) -> str:
        """Fetch a list of policy applications (policy-to-resource bindings).

        API: GET /policy_management/v4/applications

        Args:
            tenant_id: Filter by one or more tenant IDs/UUIDs (max 100).
            policy_id: Filter by one or more policy IDs (max 100).
            context_id: Filter by one or more resource/context IDs (max 100).
            context_type: Filter by one or more resource types (max 10).
            status: Filter by one or more statuses (ExecutionStatus, max 10).
            enabled_only: If true, only return enabled applications.
            limit: Number of elements per page.
            after: Pagination cursor after the current page.
            before: Pagination cursor before the current page.
            extra_params: Additional raw query params (agent_id,
                context_selection_id, policy_selection_id, policy_type,
                deployment_state, execution_state, issue_types, direct_only,
                empty_link_only, include_deleted, include_temporaries).
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        params = {
            "tenant_id": tenant_id,
            "policy_id": policy_id,
            "context_id": context_id,
            "context_type": context_type,
            "status": status,
            "enabled_only": enabled_only,
            "limit": limit,
            "after": after,
            "before": before,
            **(extra_params or {}),
        }
        try:
            result = await client.get(f"{_BASE}/applications", params=params)
            return json.dumps(result, indent=2)
        except AcronisError as e:
            return f"Error: {e}"
