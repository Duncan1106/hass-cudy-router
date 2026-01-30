import re

import pytest

from custom_components.hass_cudy_router.const import CUDY_DEVICES
from custom_components.hass_cudy_router.model_detect import detect_model, normalize_model_name
from tests.cudy_router.fixtures import read_html

class FakeClient:
    def __init__(self, html: str) -> None:
        self._html = html
    async def get(self, path: str) -> str:
        return self._html

@pytest.mark.asyncio
@pytest.mark.parametrize("model", CUDY_DEVICES)
async def test_detect_model(model):
    html = read_html(model, "system.html")
    client = FakeClient(html)

    found_model = await detect_model(client)
    assert normalize_model_name(found_model) == model