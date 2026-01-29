import pytest

from custom_components.hass_cudy_router.model_detect import detect_model
from tests.cudy_router.fixtures import read_html

class FakeClient:
    def __init__(self, html: str) -> None:
        self._html = html
    async def get(self, path: str) -> str:
        return self._html

@pytest.mark.asyncio
async def test_detect_model_wr6500():
    html = read_html("wr6500", "system.html")
    client = FakeClient(html)
    model = await detect_model(client)
    assert model  == "WR6500"

@pytest.mark.asyncio
async def test_detect_model_p5():
    html = read_html("p5", "system.html")
    client = FakeClient(html)
    model = await detect_model(client)
    assert model == "P5"


@pytest.mark.asyncio
async def test_detect_model_r700():
    html = read_html("r700", "system.html")
    client = FakeClient(html)
    model = await detect_model(client)
    assert model == "R700"