from typing import Any

import httpx


class AcronisError(Exception):
    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        super().__init__(f"Acronis API error {status_code}: {message}")


class AcronisClient:
    """Async httpx client wrapping the Acronis Cyber Platform REST APIs.

    Every Acronis Cyber Protect Cloud tenant is hosted on one of several
    regional data centers, so the base URL is per-request rather than fixed.
    """

    def __init__(self, access_token: str, datacenter_url: str):
        self._token = access_token
        self._base_url = datacenter_url.rstrip("/")

    def _headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {self._token}",
            "Accept": "application/json",
        }

    def _clean_params(self, params: dict | None) -> dict:
        if not params:
            return {}
        return {k: v for k, v in params.items() if v is not None}

    async def get(self, path: str, params: dict | None = None) -> Any:
        async with httpx.AsyncClient(timeout=30.0) as client:
            try:
                resp = await client.get(
                    f"{self._base_url}{path}",
                    headers=self._headers(),
                    params=self._clean_params(params),
                )
            except httpx.RequestError as e:
                raise AcronisError(0, f"{e or type(e).__name__} (url={self._base_url}{path})") from e
            self._raise_for_status(resp)
            return self._parse_body(resp)

    def _parse_body(self, resp: httpx.Response) -> Any:
        if not resp.content:
            return None
        try:
            return resp.json()
        except ValueError:
            return {"raw_response": resp.text}

    def _raise_for_status(self, resp: httpx.Response) -> None:
        if resp.status_code >= 400:
            try:
                detail = resp.json()
                if isinstance(detail, dict):
                    msg = detail.get("reason") or detail.get("code") or detail.get("message") or str(detail)
                else:
                    msg = str(detail)
            except ValueError:
                msg = resp.text
            raise AcronisError(resp.status_code, msg)
