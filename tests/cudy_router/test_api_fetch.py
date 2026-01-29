import pytest

from custom_components.hass_cudy_router.api import CudyApi
from custom_components.hass_cudy_router.const import *
from custom_components.hass_cudy_router.models import get_spec
from tests.cudy_router.fixtures import read_html


class FakeClient:
    def __init__(self, mapping: dict[str, str]) -> None:
        self.mapping = mapping
        self.requested: list[str] = []

    async def get(self, path: str) -> str:
        self.requested.append(path)
        return self.mapping[path]


@pytest.mark.asyncio
async def test_api_get_data_p5_fetches_all_pages():
    spec = get_spec("P5")

    mapping = {
        CudyApi.luci(spec.pages[MODULE_INFO]): read_html("p5", "info.html"),
        CudyApi.luci(spec.pages[MODULE_SYSTEM]): read_html("p5", "system.html"),
        CudyApi.luci(spec.pages[MODULE_MESH]): read_html("p5", "mesh.html"),
        CudyApi.luci(spec.pages[MODULE_LAN]): read_html("p5", "lan.html"),
        CudyApi.luci(spec.pages[MODULE_WIRELESS_24G]): read_html("p5", "wifi_24g.html"),
        CudyApi.luci(spec.pages[MODULE_WIRELESS_5G]): read_html("p5", "wifi_5g.html"),
        CudyApi.luci(spec.pages[MODULE_DHCP]): read_html("p5", "dhcp.html"),
        CudyApi.luci(spec.pages[MODULE_GSM]): read_html("p5", "gsm.html"),
        CudyApi.luci(spec.pages[MODULE_SMS]): read_html("p5", "sms.html"),
        CudyApi.luci(spec.pages[MODULE_DEVICES]): read_html("p5", "devices.html"),
    }

    if spec.device_list_page:
        mapping[CudyApi.luci(spec.device_list_page)] = read_html("p5", "device_list.html")

    client = FakeClient(mapping)
    api = CudyApi(client, spec)

    data = await api.get_data()

    assert MODULE_SYSTEM in data
    assert MODULE_LAN in data
    assert MODULE_GSM in data
    assert MODULE_DEVICES in data

    if spec.device_list_page:
        assert OPTIONS_DEVICE_LIST in data[MODULE_DEVICES]
        assert isinstance(data[MODULE_DEVICES][OPTIONS_DEVICE_LIST], list)

    assert len(client.requested) == len(mapping)