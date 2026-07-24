import json
from collections.abc import Callable

from mcp.server.fastmcp import FastMCP

from ..api_client import AcronisClient, AcronisError
from ._common import NO_TOKEN

_BASE = "/api/task_manager/v2"


def register(mcp: FastMCP, client_factory: Callable[[], AcronisClient | None]) -> None:

    @mcp.tool()
    async def acronis_get_tasks(
        state: str | None = None,
        type: str | None = None,
        priority: str | None = None,
        resourceId: str | None = None,
        policyId: str | None = None,
        updatedAt: str | None = None,
        limit: int | None = None,
        after: str | None = None,
        order: str | None = None,
        lod: str | None = None,
        extra_params: dict[str, object] | None = None,
    ) -> str:
        """Fetch a list of tasks.

        API: GET /tasks (Task Manager v2)

        Args:
            state: Filter by state (enqueued/assigned/started/paused/completed).
            type: Filter by task type.
            priority: Filter by priority (low/belowNormal/normal/aboveNormal/high).
            resourceId: Filter by resource ID.
            policyId: Filter by policy ID.
            updatedAt: Filter by update time (single entry, e.g. "ge(2024-11-01T08:20:36Z)").
            limit: Number of tasks per page (use with `after`).
            after: Pagination token for the next page (requires `limit`).
            order: e.g. "asc(updatedAt)" or "desc(startedAt)".
            lod: Level of detail — tiny/short/long/full/debug/count.
            extra_params: Additional raw query params (executorId, id, uuid,
                queue, startedBy, policyName, policyType, resourceName,
                resourceType, workflowId, resultCode, enqueuedAt, assignedAt,
                startedAt, completedAt, tag, affinityAgentId, affinityClusterId,
                allow_deleted).
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        params = {
            "state": state,
            "type": type,
            "priority": priority,
            "resourceId": resourceId,
            "policyId": policyId,
            "updatedAt": updatedAt,
            "limit": limit,
            "after": after,
            "order": order,
            "lod": lod,
            **(extra_params or {}),
        }
        try:
            result = await client.get(f"{_BASE}/tasks", params=params)
            return json.dumps(result, indent=2)
        except AcronisError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def acronis_get_task_activities(
        state: str | None = None,
        type: str | None = None,
        taskId: int | None = None,
        resourceId: str | None = None,
        policyId: str | None = None,
        updatedAt: str | None = None,
        limit: int | None = None,
        after: str | None = None,
        order: str | None = None,
        lod: str | None = None,
        extra_params: dict[str, object] | None = None,
    ) -> str:
        """Fetch a list of task activities.

        API: GET /activities (Task Manager v2)

        Args:
            state: Filter by state (enqueued/assigned/started/paused/completed).
            type: Filter by activity type.
            taskId: Filter by parent task ID.
            resourceId: Filter by resource ID.
            policyId: Filter by policy ID.
            updatedAt: Filter by update time (single entry).
            limit: Number of activities per page (use with `after`).
            after: Pagination token for the next page (requires `limit`).
            order: e.g. "asc(createdAt)" or "desc(completedAt)".
            lod: Level of detail — tiny/short/long/full/debug/count.
            extra_params: Additional raw query params (id, uuid, startedBy,
                policyName, policyType, resourceName, resourceType, workflowId,
                parentActivityId, resultCode, createdAt, startedAt, completedAt,
                tag, sustainable, allow_deleted).
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        params = {
            "state": state,
            "type": type,
            "taskId": taskId,
            "resourceId": resourceId,
            "policyId": policyId,
            "updatedAt": updatedAt,
            "limit": limit,
            "after": after,
            "order": order,
            "lod": lod,
            **(extra_params or {}),
        }
        try:
            result = await client.get(f"{_BASE}/activities", params=params)
            return json.dumps(result, indent=2)
        except AcronisError as e:
            return f"Error: {e}"
