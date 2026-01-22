from __future__ import annotations
import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.insert(0, ROOT)

from custom_components.hass_cudy_router.parser import *


from pathlib import Path

from custom_components.hass_cudy_router.parser import parse_system_info


def _read_fixture(rel_path: str) -> str:
    """Read an HTML fixture as UTF-8 text."""
    root = Path(__file__).resolve().parent.parent  # project root (…/hass-cudy-router)
    return (root / rel_path).read_text(encoding="utf-8")


def test_parse_system_info_from_fixture_system_html():
    html = _read_fixture("cudy_router/html/system.html")

    data = parse_system_info(html)

    assert isinstance(data, dict), "parse_system_info() should return a dict"
    assert data, "parse_system_info() returned an empty dict"
    possible_keys = {
        SENSOR_FIRMWARE_VERSION,
        SENSOR_HARDWARE,
        SENSOR_SYSTEM_UPTIME
    }
    assert (
        possible_keys.intersection(data.keys())
    ), f"Expected at least one of these keys to be parsed: {sorted(possible_keys)}"

    assert data[SENSOR_FIRMWARE_VERSION] == "2.3.15-20250805-113843"
    assert data[SENSOR_HARDWARE] == "WR6500 V1.0"
    assert data[SENSOR_SYSTEM_UPTIME] == "08:09:48"


def test_parse_mesh_info_from_fixture_system_html():
    html = _read_fixture("cudy_router/html/mesh.html")

    data = parse_mesh_info(html)

    assert isinstance(data, dict), "parse_mesh_info() should return a dict"
    assert data, "parse_mesh_info() returned an empty dict"
    possible_keys = {
        SENSOR_MESH_NETWORK,
        SENSOR_MESH_UNITS
    }
    assert (
        possible_keys.intersection(data.keys())
    ), f"Expected at least one of these keys to be parsed: {sorted(possible_keys)}"

    assert data[SENSOR_MESH_NETWORK] == "Mesh_5456"
    assert data[SENSOR_MESH_UNITS] == "2"


def test_parse_lan_info_from_fixture_system_html():
    html = _read_fixture("cudy_router/html/lan.html")

    data = parse_lan_info(html)

    assert isinstance(data, dict), "parse_lan_info() should return a dict"
    assert data, "parse_lan_info() returned an empty dict"
    possible_keys = {
        SENSOR_LAN_IP
    }
    assert (
        possible_keys.intersection(data.keys())
    ), f"Expected at least one of these keys to be parsed: {sorted(possible_keys)}"

    assert data[SENSOR_LAN_IP] == "192.168.178.1"


def test_parse_wan_info_from_fixture_system_html():
    html = _read_fixture("cudy_router/html/wan.html")

    data = parse_wan_info(html)

    assert isinstance(data, dict), "parse_wan_info() should return a dict"
    assert data, "parse_wan_info() returned an empty dict"
    possible_keys = {
        SENSOR_WAN_TYPE,
        SENSOR_WAN_IP,
        SENSOR_WAN_UPTIME,
        SENSOR_WAN_PUBLIC_IP,
        SENSOR_WAN_DNS,
    }
    assert (
        possible_keys.intersection(data.keys())
    ), f"Expected at least one of these keys to be parsed: {sorted(possible_keys)}"

    assert data[SENSOR_WAN_TYPE] == "DHCP client"
    assert data[SENSOR_WAN_IP] == "192.168.10.150"
    assert data[SENSOR_WAN_UPTIME] == "08:26:31"
    assert data[SENSOR_WAN_PUBLIC_IP] == "83.238.165.41 *"
    assert data[SENSOR_WAN_DNS] == "8.8.8.8/62.233.233.233"


def test_parse_devices_info_from_fixture_system_html():
    html = _read_fixture("cudy_router/html/devices.html")

    data = parse_devices(html)

    assert isinstance(data, dict), "parse_devices() should return a dict"
    assert data, "parse_devices() returned an empty dict"
    possible_keys = {
        SENSOR_DEVICE_COUNT,
        SENSOR_WIFI_24_DEVICE_COUNT,
        SENSOR_WIFI_5_DEVICE_COUNT,
        SENSOR_WIRED_DEVICE_COUNT,
        SENSOR_MESH_DEVICE_COUNT,
    }
    assert (
        possible_keys.intersection(data.keys())
    ), f"Expected at least one of these keys to be parsed: {sorted(possible_keys)}"

    assert data[SENSOR_DEVICE_COUNT] == "30"
    assert data[SENSOR_WIFI_24_DEVICE_COUNT] == "4"
    assert data[SENSOR_WIFI_5_DEVICE_COUNT] == "2"
    assert data[SENSOR_WIRED_DEVICE_COUNT] == "5"
    assert data[SENSOR_MESH_DEVICE_COUNT] == "19"


def test_parse_device_list_from_fixture_system_html():
    html = _read_fixture("cudy_router/html/device_list.html")

    data = parse_device_list(html)

    assert isinstance(data, list), "parse_device_list() should return a list"
    assert data, "parse_device_list() returned an empty list"
    possible_keys = {
        DEVICE_HOSTNAME,
        DEVICE_IP,
        DEVICE_MAC,
        DEVICE_UPLOAD_SPEED,
        DEVICE_DOWNLOAD_SPEED,
        DEVICE_SIGNAL,
        DEVICE_ONLINE_TIME,
        DEVICE_CONNECTION,
        DEVICE_CONNECTION_TYPE,
    }

    assert len(data) == 31
    for device in data:
        assert (
            possible_keys.intersection(device.keys())
        ), f"Expected at least one of these keys to be parsed: {sorted(possible_keys)}"
