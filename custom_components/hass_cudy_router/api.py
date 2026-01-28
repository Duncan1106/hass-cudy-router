from __future__ import annotations

from typing import Any

from .client import CudyClient
from .const import *
from .models import ModelSpec


class CudyApi:
    def __init__(self, client: CudyClient, spec: ModelSpec) -> None:
        self._client = client
        self._spec = spec

    @staticmethod
    def luci(path: str) -> str:
        if not path.startswith("/"):
            path = "/" + path
        return "/cgi-bin/luci" + path

    async def get_data(self) -> dict[str, Any]:
        out: dict[str, Any] = {}

        for module, path in self._spec.pages.items():
            html = await self._client.get(self.luci(path))
            parser = self._spec.parsers.get(module)
            out[module] = parser(html) if parser else {}

        if self._spec.device_list_page and self._spec.device_list_parser:
            html = await self._client.get(self.luci(self._spec.device_list_page))
            devs = out.setdefault(MODULE_DEVICES, {})
            devs[OPTIONS_DEVICE_LIST] = self._spec.device_list_parser(html)

        return out

    async def reboot(self) -> None:
        if not self._spec.supports_reboot:
            return
        await self._client.post(self.luci("/admin/system/reboot"), data={"reboot": "1"})