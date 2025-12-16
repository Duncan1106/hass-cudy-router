"""Helper methods to parse HTML returned by Cudy routers"""

import re
from typing import Any
from bs4 import BeautifulSoup
from dateutil.relativedelta import relativedelta
from datetime import datetime

from homeassistant.const import STATE_UNAVAILABLE

from .const import SECTION_DETAILED


def parse_speed(input_string: str) -> float:
    """Parses transfer speed string (e.g. '12.5 Kbps') to megabits per second"""
    if not input_string:
        return 0.0
    
    # Hledame cislo a jednotku pomoci Regexu (ignoruje ikony a mezery okolo)
    # Hleda: cislo (vcetne desetinne tecky) + volitelne mezery + jednotku (kbps, mbps...)
    match = re.search(r"(\d+(?:\.\d+)?)\s*([kKmMgG]?bps)", input_string, re.IGNORECASE)
    
    if match:
        try:
            value = float(match.group(1))
            unit = match.group(2).lower()
            
            if "mbps" in unit:
                return value
            if "gbps" in unit:
                return value * 1024
            if "kbps" in unit:
                 return round(value / 1024, 2)
            if "bps" in unit:
                 return round(value / 1024 / 1024, 2)
        except ValueError:
            pass
            
    return 0.0


def get_all_devices(input_html: str) -> list[dict[str, Any]]:
    """Parses an HTML table extracting key-value pairs."""
    devices = []
    soup = BeautifulSoup(input_html, "html.parser")
    
    # Nahradime <br> za novy radek
    for br in soup.find_all("br"):
        br.replace_with("\n")

    # Hledame radky tabulky
    rows = soup.find_all("tr", id=re.compile(r"^cbi-table-\d+"))

    for row in rows:
        try:
            ip = "Unknown"
            mac = "Unknown"
            up_speed_str = "0"
            down_speed_str = "0"
            hostname = "Unknown"
            signal = "---"
            online = "---"
            connection = "Unknown"

            # 1. IP a MAC
            ipmac_div = row.find("div", id=re.compile(r"-ipmac$"))
            if ipmac_div:
                text = ipmac_div.get_text(strip=True, separator="\n")
                parts = text.split("\n")
                if len(parts) >= 1:
                    ip = parts[0].strip()
                if len(parts) >= 2:
                    mac = parts[1].strip()

            # 2. Hostname
            host_div = row.find("div", id=re.compile(r"-hostnamexs$"))
            if host_div:
                text = host_div.get_text(strip=True, separator="\n")
                parts = text.split("\n")
                if len(parts) > 0:
                    hostname = parts[0].strip()

            # OPRAVA: Pokud je hostname "Unknown", pouzijeme IP adresu
            if hostname.lower() == "unknown" and ip != "Unknown":
                hostname = ip

            # 3. Rychlost (hledame div koncici na -speed)
            speed_div = row.find("div", id=re.compile(r"-speed$"))
            if speed_div:
                # Text vypada jako: "UP_ICON 10 Kbps \n DOWN_ICON 20 Kbps"
                # get_text s mezerou oddeli ikony od textu
                text = speed_div.get_text(strip=True, separator="\n")
                parts = text.split("\n")
                if len(parts) >= 2:
                    up_speed_str = parts[0].strip()
                    down_speed_str = parts[1].strip()

            # 4. Signal
            sig_div = row.find("div", id=re.compile(r"-signal$"))
            if sig_div:
                signal = sig_div.get_text(strip=True)

            # 5. Online cas
            online_div = row.find("div", id=re.compile(r"-online$"))
            if online_div:
                online = online_div.get_text(strip=True)

            # 6. Typ pripojeni
            iface_div = row.find("div", id=re.compile(r"-iface$"))
            if iface_div:
                connection = iface_div.get_text(strip=True)

            # Pridame zarizeni
            if mac != "Unknown" or ip != "Unknown":
                devices.append(
                    {
                        "hostname": hostname,
                        "ip": ip,
                        "mac": mac,
                        "up_speed": parse_speed(up_speed_str),
                        "down_speed": parse_speed(down_speed_str),
                        "signal": signal,
                        "online": online,
                        "connection": connection,
                    }
                )
        except Exception:
            continue

    return devices


def parse_devices(input_html: str, device_list_str: str, previous_devices: dict[str, Any] = None) -> dict[str, Any]:
    """Parses devices page and tracks last_seen timestamps for each device."""
    
    devices = get_all_devices(input_html)
    data = {"device_count": {"value": len(devices)}}
    
    # Razeni podle casu online
    def time_to_minutes(time_str):
        if not time_str or time_str == "---":
            return 999999
        try:
            parts = time_str.split(":")
            if len(parts) == 3:
                return int(parts[0]) * 60 + int(parts[1])
            if len(parts) == 2:
                return int(parts[0])
        except (ValueError, IndexError):
            pass
        return 999999
    
    devices.sort(key=lambda d: time_to_minutes(d.get("online", "---")))
    
    # Formatovani seznamu pro atributy
    all_devices_formatted = []
    for device in devices:
        device_info = {
            "hostname": device.get("hostname", "Unknown"),
            "ip": device.get("ip", "Unknown"),
            "mac": device.get("mac", "Unknown"),
            "upload_speed": device.get("up_speed", 0),
            "download_speed": device.get("down_speed", 0),
            "signal": device.get("signal", "---"),
            "online_time": device.get("online", "---"),
            "connection": device.get("connection", "Unknown"),
        }
        all_devices_formatted.append(device_info)
    
    data["connected_devices"] = {
        "value": len(devices), 
        "attributes": {
            "devices": all_devices_formatted,
            "device_count": len(devices),
            "last_updated": datetime.now().isoformat(),
        }
    }
    
    if devices:
        # Top downloader
        top_download_device = max(devices, key=lambda item: item.get("down_speed", 0))
        data["top_downloader_speed"] = {"value": top_download_device.get("down_speed")}
        data["top_downloader_mac"] = {"value": top_download_device.get("mac")}
        data["top_downloader_hostname"] = {"value": top_download_device.get("hostname")}
        
        # Top uploader
        top_upload_device = max(devices, key=lambda item: item.get("up_speed", 0))
        data["top_uploader_speed"] = {"value": top_upload_device.get("up_speed")}
        data["top_uploader_mac"] = {"value": top_upload_device.get("mac")}
        data["top_uploader_hostname"] = {"value": top_upload_device.get("hostname")}

        data[SECTION_DETAILED] = {}
        device_list = [x.strip() for x in (device_list_str or "").split(",")]
        now_ts = datetime.now().timestamp()
        previous_detailed = (previous_devices or {}).get(SECTION_DETAILED, {}) if previous_devices else {}
        
        for device in devices:
            key = device.get("mac")
            # Fallback na hostname/IP pokud neni mac v listu
            if key not in device_list and device.get("hostname") in device_list:
                key = device.get("hostname")

            if key and key in device_list:
                prev = previous_detailed.get(key, {})
                device["last_seen"] = now_ts
                if prev.get("last_seen") and prev["last_seen"] > device["last_seen"]:
                     device["last_seen"] = prev["last_seen"]
                data[SECTION_DETAILED][key] = device
                
        # Zachovani historie pro offline zarizeni
        for key in device_list:
            if key not in data[SECTION_DETAILED] and key in previous_detailed:
                data[SECTION_DETAILED][key] = previous_detailed[key]
                
        data["total_down_speed"] = {
            "value": sum(device.get("down_speed", 0) for device in devices)
        }
        data["total_up_speed"] = {
            "value": sum(device.get("up_speed", 0) for device in devices)
        }
    return data


def parse_modem_info(input_html: str) -> dict[str, Any]:
    """Cudy AC1200 nema LTE modem, vracime prazdne nebo zakladni info."""
    return {
        "network": {"value": "N/A (WiFi Router)"},
        "signal": {"value": 0},
    }
