from typing import Final

from homeassistant.components.sensor import SensorEntityDescription, SensorStateClass
from homeassistant.const import EntityCategory

from . import ModelSpec, build_module_map, register_spec
from ..parser import *

SENSOR_DESCRIPTIONS_P5: Final = (
    # ----- INFO -----
    SensorEntityDescription(
        key=SENSOR_INFO_WORK_MODE,
        translation_key=SENSOR_INFO_WORK_MODE,
        icon=ICON_INFO_WORK_MODE,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    SensorEntityDescription(
        key=SENSOR_INFO_INTERFACE,
        translation_key=SENSOR_INFO_INTERFACE,
        icon=ICON_INFO_INTERFACE,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
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
    # ----- MESH -----
    SensorEntityDescription(
        key=SENSOR_MESH_NETWORK,
        translation_key=SENSOR_MESH_NETWORK,
        icon=ICON_MESH_NETWORK,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    SensorEntityDescription(
        key=SENSOR_MESH_UNITS,
        translation_key=SENSOR_MESH_UNITS,
        icon=ICON_MESH_UNITS,
        state_class=SensorStateClass.MEASUREMENT,
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
    # ----- WIFI 2.4G -----
    SensorEntityDescription(
        key=SENSOR_24G_WIFI_SSID,
        translation_key=SENSOR_24G_WIFI_SSID,
        icon=ICON_24G_WIFI_SSID,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    SensorEntityDescription(
        key=SENSOR_24G_WIFI_BSSID,
        translation_key=SENSOR_24G_WIFI_BSSID,
        icon=ICON_24G_WIFI_BSSID,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    SensorEntityDescription(
        key=SENSOR_24G_WIFI_ENCRYPTION,
        translation_key=SENSOR_24G_WIFI_ENCRYPTION,
        icon=ICON_24G_WIFI_ENCRYPTION,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    SensorEntityDescription(
        key=SENSOR_24G_WIFI_CHANNEL,
        translation_key=SENSOR_24G_WIFI_CHANNEL,
        icon=ICON_24G_WIFI_CHANNEL,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    # ----- WIFI 5G -----
    SensorEntityDescription(
        key=SENSOR_5G_WIFI_SSID,
        translation_key=SENSOR_5G_WIFI_SSID,
        icon=ICON_5G_WIFI_SSID,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    SensorEntityDescription(
        key=SENSOR_5G_WIFI_BSSID,
        translation_key=SENSOR_5G_WIFI_BSSID,
        icon=ICON_5G_WIFI_BSSID,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    SensorEntityDescription(
        key=SENSOR_5G_WIFI_ENCRYPTION,
        translation_key=SENSOR_5G_WIFI_ENCRYPTION,
        icon=ICON_5G_WIFI_ENCRYPTION,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    SensorEntityDescription(
        key=SENSOR_5G_WIFI_CHANNEL,
        translation_key=SENSOR_5G_WIFI_CHANNEL,
        icon=ICON_5G_WIFI_CHANNEL,
        state_class=SensorStateClass.MEASUREMENT,
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
    # ----- GSM -----
    SensorEntityDescription(
        key=SENSOR_GSM_NETWORK_TYPE,
        translation_key=SENSOR_GSM_NETWORK_TYPE,
        icon=ICON_GSM_NETWORK_TYPE,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    SensorEntityDescription(
        key=SENSOR_GSM_DOWNLOAD,
        translation_key=SENSOR_GSM_DOWNLOAD,
        icon=ICON_GSM_DOWNLOAD,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    SensorEntityDescription(
        key=SENSOR_GSM_UPLOAD,
        translation_key=SENSOR_GSM_UPLOAD,
        icon=ICON_GSM_UPLOAD,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    SensorEntityDescription(
        key=SENSOR_GSM_PUBLIC_IP,
        translation_key=SENSOR_GSM_PUBLIC_IP,
        icon=ICON_GSM_PUBLIC_IP,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    SensorEntityDescription(
        key=SENSOR_GSM_IP_ADDRESS,
        translation_key=SENSOR_GSM_IP_ADDRESS,
        icon=ICON_GSM_IP_ADDRESS,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    SensorEntityDescription(
        key=SENSOR_GSM_CONNECTED_TIME,
        translation_key=SENSOR_GSM_CONNECTED_TIME,
        icon=ICON_GSM_CONNECTED_TIME,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    # ----- SMS -----
    SensorEntityDescription(
        key=SENSOR_SMS_INBOX,
        translation_key=SENSOR_SMS_INBOX,
        icon=ICON_SMS_INBOX,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key=SENSOR_SMS_OUTBOX,
        translation_key=SENSOR_SMS_OUTBOX,
        icon=ICON_SMS_OUTBOX,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    # ----- DEVICES COUNTS -----
    SensorEntityDescription(
        key=SENSOR_DEVICE_COUNT,
        translation_key=SENSOR_DEVICE_COUNT,
        icon=ICON_DEVICE_COUNT,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key=SENSOR_WIFI_24_DEVICE_COUNT,
        translation_key=SENSOR_WIFI_24_DEVICE_COUNT,
        icon=ICON_WIFI_24_DEVICE_COUNT,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key=SENSOR_WIFI_5_DEVICE_COUNT,
        translation_key=SENSOR_WIFI_5_DEVICE_COUNT,
        icon=ICON_WIFI_5_DEVICE_COUNT,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key=SENSOR_WIRED_DEVICE_COUNT,
        translation_key=SENSOR_WIRED_DEVICE_COUNT,
        icon=ICON_WIRED_DEVICE_COUNT,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key=SENSOR_MESH_DEVICE_COUNT,
        translation_key=SENSOR_MESH_DEVICE_COUNT,
        icon=ICON_MESH_DEVICE_COUNT,
        state_class=SensorStateClass.MEASUREMENT,
    ),
)

P5_SPEC = ModelSpec(
    model="P5",
    pages={
        MODULE_INFO: "/admin/system/wizard",
        MODULE_SYSTEM: "/admin/system/status?detail=1",
        MODULE_MESH: "/admin/network/mesh/status?detail=1",
        MODULE_LAN: "/admin/network/lan/status?detail=1",
        MODULE_WIRELESS_24G: "/admin/network/wireless/status?detail=1&iface=wlan00",
        MODULE_WIRELESS_5G: "/admin/network/wireless/status?detail=1&iface=wlan10",
        MODULE_DHCP: "/admin/services/dhcp/status?detail=1",
        MODULE_GSM: "/admin/network/gcom/status",
        MODULE_SMS: "/admin/network/gcom/sms/status",
        MODULE_DEVICES: "/admin/network/devices/status?detail=1",
    },
    parsers={
        MODULE_INFO: parse_basic_info,
        MODULE_SYSTEM: parse_system_info,
        MODULE_MESH: parse_mesh_info,
        MODULE_LAN: parse_lan_info,
        MODULE_WIRELESS_24G: parse_wireless_24g_info,
        MODULE_WIRELESS_5G: parse_wireless_5g_info,
        MODULE_DHCP: parse_dhcp_info,
        MODULE_GSM: parse_gsm_info,
        MODULE_SMS: parse_sms_info,
        MODULE_DEVICES: parse_devices,
    },
    device_list_page="/admin/network/devices/devlist?detail=1",
    device_list_parser=parse_device_list,
    platforms={"sensor", "button", "device_tracker"},
    supports_reboot=True,
    module_map=build_module_map(),
    sensor_descriptions=SENSOR_DESCRIPTIONS_P5,
)
register_spec(P5_SPEC)
