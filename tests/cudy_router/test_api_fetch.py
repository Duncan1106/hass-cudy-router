import pytest

from custom_components.hass_cudy_router.api import CudyApi
from custom_components.hass_cudy_router.const import *
from tests.cudy_router.fixtures import read_html, html_exists, FakeClient


@pytest.mark.asyncio
@pytest.mark.parametrize("model", CUDY_DEVICES)
async def test_api_get_data(model: str) -> None:
    client = FakeClient(model)
    api = CudyApi(client)

    data = await api.get_data()

    assert MODULE_SYSTEM in data
    assert MODULE_DEVICES in data