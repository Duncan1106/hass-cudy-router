import pytest
from custom_components.hass_cudy_router.parser import *
from tests.cudy_router.fixtures import read_html
from tests.cudy_router.model_data import *


@pytest.mark.parametrize("model,parser,expected,html", [
    ("wr6500", parse_basic_info, WR6500_INFO, "info.html"),
    ("p5", parse_basic_info, P5_INFO, "info.html"),
    ("wr6500", parse_system_info, WR6500_SYSTEM, "system.html"),
    ("r700", parse_system_info, R700_SYSTEM, "system.html"),
    ("p5", parse_system_info, P5_SYSTEM, "system.html"),
    ("wr6500", parse_mesh_info, WR6500_MESH, "mesh.html"),
    ("p5", parse_mesh_info, P5_MESH, "mesh.html"),
    ("wr6500", parse_lan_info, WR6500_LAN, "lan.html"),
    ("r700", parse_lan_info, R700_LAN, "lan.html"),
    ("p5", parse_lan_info, P5_LAN, "lan.html"),
    ("wr6500", parse_wan_info, WR6500_WAN, "wan.html"),
    ("r700", parse_wan_info, R700_WAN, "wan.html"),
    ("p5", parse_wireless_24g_info, P5_WIRELESS_24G, "wifi_24g.html"),
    ("p5", parse_wireless_5g_info, P5_WIRELESS_5G, "wifi_5g.html"),
    ("wr6500", parse_dhcp_info, WR6500_DHCP, "dhcp.html"),
    ("r700", parse_dhcp_info, R700_DHCP, "dhcp.html"),
    ("p5", parse_dhcp_info, P5_DHCP, "dhcp.html"),
    ("p5", parse_gsm_info, P5_GSM, "gsm.html"),
    ("p5", parse_sms_info, P5_SMS, "sms.html"),
    ("wr6500", parse_devices, WR6500_DEVICES, "devices.html"),
    ("r700", parse_simple_devices, R700_DEVICES, "devices.html"),
    ("p5", parse_devices, P5_DEVICES, "devices.html"),
])
def test_parse_info(model, parser, expected, html):
    text = read_html(model, html)
    data = parser(text)

    for key, value in expected.items():
        assert key in data
        assert data[key] == value