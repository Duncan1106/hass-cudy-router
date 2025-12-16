# Cudy Router integration for Home Assistant

This is a custom integration for Cudy routers, specifically adapted for the **Cudy AC1200 (WR1200)** model.

It is based on the original integration for LT18/WR3600 but has been modified to parse the different HTML structure used by the AC1200 firmware.

## Features

This integration logs in to the router's web administration interface and scrapes status data.

- **Connected Devices:** Tracks the number of connected clients.
- **Device Tracker:** Creates `device_tracker` entities for connected devices (based on MAC address).
- **Bandwidth Monitoring:**
  - Real-time download/upload speed per device.
  - Total router download/upload speed.
  - Identifies top bandwidth users (Top Downloader/Uploader sensors).
- **Connection Details:** attributes showing connection type (Wired, 2.4G WiFi, 5G WiFi) and signal strength (for wireless clients).

*Note: As the AC1200 is a standard Wi-Fi router (not an LTE modem), cellular sensors (SIM, 4G Signal, Bands) are not available.*

## Installation

1. Go to your Home Assistant `config/custom_components` directory.
2. Create a folder named `cudy_router`.
3. Copy all the files from this repository into that folder.
   - The structure should look like:
     ```
     custom_components/
       cudy_router/
         __init__.py
         config_flow.py
         const.py
         coordinator.py
         device_tracker.py
         manifest.json
         parser.py
         router.py
         sensor.py
         strings.json
         translations/
           en.json
     ```
4. Restart Home Assistant.

## Configuration

1. Navigate to **Settings** -> **Devices & Services**.
2. Click **Add Integration**.
3. Search for **Cudy Router**.
4. Enter the router's IP address (e.g., `192.168.10.1`), username (usually `admin`), and password.
5. (Optional) In the configuration options, you can specify a list of MAC addresses to track specifically or adjust the update interval.

## Troubleshooting

- **"Unknown" Device Names:** If the router doesn't provide a hostname, the integration falls back to displaying the IP address.
- **Speed 0.00 Mbit/s:** This indicates the router is reporting zero traffic for that device at the moment of the scan. Try downloading a large file to test.

## Credits

Based on the work of [armendkadrija](https://github.com/armendkadrija/hass-cudy-router-wr3600) and other contributors.
Modified for Cudy AC1200 HTML parsing compatibility.
