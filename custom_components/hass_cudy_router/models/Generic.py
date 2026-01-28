from typing import Final

from homeassistant.components.sensor import SensorEntityDescription, SensorStateClass
from homeassistant.const import EntityCategory

from . import ModelSpec, build_module_map, register_spec
from ..parser import *

SENSOR_DESCRIPTIONS_GENERIC: Final = (
    # ----- SYSTEM -----
    SensorEntityDescription(
        key=SENSOR_SYSTEM_FIRMWARE_VERSION,
        translation_key=SENSOR_SYSTEM_FIRMWARE_VERSION,
        icon=ICON_SYSTEM_FIRMWARE_VERSION,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    SensorEntityDescription(
        key=SENSOR_SYSTEM_HARDWARE,
        translation_key=SENSOR_SYSTEM_HARDWARE,
        icon=ICON_SYSTEM_HARDWARE,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    SensorEntityDescription(
        key=SENSOR_SYSTEM_UPTIME,
        translation_key=SENSOR_SYSTEM_UPTIME,
        icon=ICON_SYSTEM_UPTIME,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    SensorEntityDescription(
        key=SENSOR_SYSTEM_LOCALTIME,
        translation_key=SENSOR_SYSTEM_LOCALTIME,
        icon=ICON_SYSTEM_LOCALTIME,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    # ----- LAN -----
    SensorEntityDescription(
        key=SENSOR_LAN_IP,
        translation_key=SENSOR_LAN_IP,
        icon=ICON_LAN_IP,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    SensorEntityDescription(
        key=SENSOR_LAN_SUBNET,
        translation_key=SENSOR_LAN_SUBNET,
        icon=ICON_LAN_SUBNET,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    SensorEntityDescription(
        key=SENSOR_LAN_MAC,
        translation_key=SENSOR_LAN_MAC,
        name="MAC-Address",
        icon=ICON_LAN_MAC,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    # ----- DHCP -----
    SensorEntityDescription(
        key=SENSOR_DHCP_IP_START,
        translation_key=SENSOR_DHCP_IP_START,
        icon=ICON_DHCP_IP_START,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    SensorEntityDescription(
        key=SENSOR_DHCP_IP_END,
        translation_key=SENSOR_DHCP_IP_END,
        icon=ICON_DHCP_IP_END,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    SensorEntityDescription(
        key=SENSOR_DHCP_DNS_PRIMARY,
        translation_key=SENSOR_DHCP_DNS_PRIMARY,
        icon=ICON_DHCP_DNS_PRIMARY,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    SensorEntityDescription(
        key=SENSOR_DHCP_DNS_SECONDARY,
        translation_key=SENSOR_DHCP_DNS_SECONDARY,
        icon=ICON_DHCP_DNS_SECONDARY,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    SensorEntityDescription(
        key=SENSOR_DHCP_GATEWAY,
        translation_key=SENSOR_DHCP_GATEWAY,
        icon=ICON_DHCP_GATEWAY,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    SensorEntityDescription(
        key=SENSOR_DHCP_LEASE_TIME,
        translation_key=SENSOR_DHCP_LEASE_TIME,
        icon=ICON_DHCP_LEASE_TIME,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    # ----- DEVICES COUNTS -----
    SensorEntityDescription(
        key=SENSOR_DEVICE_COUNT,
        translation_key=SENSOR_DEVICE_COUNT,
        icon=ICON_DEVICE_COUNT,
        state_class=SensorStateClass.MEASUREMENT,
    ),
)

GENERIC_SPEC = ModelSpec(
    model="Generic",
    pages={
        MODULE_SYSTEM: "/admin/system/status?detail=1",
        MODULE_LAN: "/admin/network/lan/status?detail=1",
        MODULE_DEVICES: "/admin/network/devices/status?detail=1",
    },
    parsers={
        MODULE_SYSTEM: parse_system_info,
        MODULE_LAN: parse_lan_info,
        MODULE_DEVICES: parse_simple_devices,
    },
    device_list_page="/admin/network/devices/devlist?detail=1",
    device_list_parser=parse_device_list,
    platforms={"sensor", "device_tracker"},
    supports_reboot=False,
    module_map=build_module_map(),
    sensor_descriptions=SENSOR_DESCRIPTIONS_GENERIC,
)
register_spec(GENERIC_SPEC)
