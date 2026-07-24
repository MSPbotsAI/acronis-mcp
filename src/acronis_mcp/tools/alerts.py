import json
from collections.abc import Callable

from mcp.server.fastmcp import FastMCP

from ..api_client import AcronisClient, AcronisError
from ._common import NO_TOKEN

_BASE = "/api/alert_manager/v1"


def register(mcp: FastMCP, client_factory: Callable[[], AcronisClient | None]) -> None:

    @mcp.tool()
    async def acronis_get_alerts(
        limit: int | None = None,
        severity: str | None = None,
        type: str | None = None,
        category: str | None = None,
        tenant: str | None = None,
        query: str | None = None,
        show_deleted: bool | None = None,
        order: str | None = None,
        updated_at: str | None = None,
        created_at: str | None = None,
        extra_params: dict[str, object] | None = None,
    ) -> str:
        """Fetch all alerts by optional filtering parameters.

        API: GET /alerts (Alert Manager v1)

        Args:
            limit: Max number of alerts to return.
            severity: Filter by severity (ok/information/warning/error/critical).
                Supports operators, e.g. "eq(warning)", "or(warning,critical)".
            type: Filter by alert type.
            category: Filter by alert category (e.g. "Backup", "Monitoring").
            tenant: Filter by alert tenant ID.
            query: Free-text search within planName/resourceName fields.
            show_deleted: If true, include dismissed alerts.
            order: Order results, e.g. "asc(updated_at)" or "desc(created_at)".
            updated_at: Filter by update timestamp (Unix ns). Supports operators
                like "ge(1711687981)".
            created_at: Filter by creation timestamp (Unix ns), same operator syntax.
            extra_params: Additional raw query params (e.g. id, skip, deleted_at,
                source, source_time_stamp, planId, resourceId, planName,
                resourceName, show_deleted_only).
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        params = {
            "limit": limit,
            "severity": severity,
            "type": type,
            "category": category,
            "tenant": tenant,
            "query": query,
            "show_deleted": show_deleted,
            "order": order,
            "updated_at": updated_at,
            "created_at": created_at,
            **(extra_params or {}),
        }
        try:
            result = await client.get(f"{_BASE}/alerts", params=params)
            return json.dumps(result, indent=2)
        except AcronisError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def acronis_get_customer_alerts(
        customer_id: list[str],
        severity: str | None = None,
        type: str | None = None,
        category: str | None = None,
        query: str | None = None,
        show_deleted: bool | None = None,
        extra_params: dict[str, object] | None = None,
    ) -> str:
        """Fetch alerts grouped per customer.

        API: GET /customer_alerts (Alert Manager v1)

        Args:
            customer_id: Required list of customer IDs whose alerts to return.
            severity: Filter by severity (ok/information/warning/error/critical).
            type: Filter by alert type.
            category: Filter by alert category.
            query: Free-text search within planName/resourceName fields.
            show_deleted: If true, include dismissed alerts.
            extra_params: Additional raw query params (id, source, updated_at,
                created_at, planId, resourceId, planName, resourceName,
                deleted_at, source_time_stamp, show_deleted_only).
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        params = {
            "customer_id": customer_id,
            "severity": severity,
            "type": type,
            "category": category,
            "query": query,
            "show_deleted": show_deleted,
            **(extra_params or {}),
        }
        try:
            result = await client.get(f"{_BASE}/customer_alerts", params=params)
            return json.dumps(result, indent=2)
        except AcronisError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def acronis_get_customer_alerts_count(
        severity: str | None = None,
        type: str | None = None,
        category: str | None = None,
        show_deleted: bool | None = None,
        extra_params: dict[str, object] | None = None,
    ) -> str:
        """Fetch count of alerts per customer (customers with no alerts are omitted).

        API: GET /customer_alerts_count (Alert Manager v1)

        Args:
            severity: Filter by severity (ok/information/warning/error/critical).
            type: Filter by alert type.
            category: Filter by alert category.
            show_deleted: If true, include dismissed alerts.
            extra_params: Additional raw query params (id, query, source,
                updated_at, created_at, planId, resourceId, planName,
                resourceName, deleted_at, source_time_stamp, show_deleted_only).
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        params = {
            "severity": severity,
            "type": type,
            "category": category,
            "show_deleted": show_deleted,
            **(extra_params or {}),
        }
        try:
            result = await client.get(f"{_BASE}/customer_alerts_count", params=params)
            return json.dumps(result, indent=2)
        except AcronisError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def acronis_get_alert_types(
        os_type: list[str],
        category: str | None = None,
        order: str | None = None,
    ) -> str:
        """Fetch all registered alert types.

        API: GET /types (Alert Manager v1)

        Args:
            os_type: Required list of OS filters (ios/linux/macos/windows).
            category: Filter by list of type categories.
            order: Order by column (id/severity/category), e.g. "desc(severity)".
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        params = {"os_type": os_type, "category": category, "order": order}
        try:
            result = await client.get(f"{_BASE}/types", params=params)
            return json.dumps(result, indent=2)
        except AcronisError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def acronis_get_resource_status(
        id: list[str] | None = None,
        embed_alert: bool | None = None,
    ) -> str:
        """Fetch the resources containing the highest-severity alerts found for them.

        API: GET /resource_status (Alert Manager v1)

        Args:
            id: Optional list of resource IDs to filter by; if omitted, returns
                statuses for all resources that have alerts.
            embed_alert: If true, include the full alert object in the response.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        params = {"id": id, "embed_alert": embed_alert}
        try:
            result = await client.get(f"{_BASE}/resource_status", params=params)
            return json.dumps(result, indent=2)
        except AcronisError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def acronis_get_alert_status(
        scope_key: str,
        scope_value: list[str] | None = None,
    ) -> str:
        """Fetch the last, most critical alerts grouped by the selected scope.

        API: GET /status (Alert Manager v1)

        Args:
            scope_key: Required context key or searchable detail to group by
                (see registered alert types for available keys).
            scope_value: Optional list of scope values to filter by; if omitted,
                returns the last most-critical status among available alerts.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        params = {"scope_key": scope_key, "scope_value": scope_value}
        try:
            result = await client.get(f"{_BASE}/status", params=params)
            return json.dumps(result, indent=2)
        except AcronisError as e:
            return f"Error: {e}"
