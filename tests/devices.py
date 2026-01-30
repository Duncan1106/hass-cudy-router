from __future__ import annotations

import asyncio
import json
from typing import Dict, List
from urllib.parse import unquote, urljoin

import requests
import urllib3
from bs4 import BeautifulSoup
from pathlib import Path
from urllib.parse import urlparse, urlunparse

from custom_components.hass_cudy_router.const import *



URLS = {
    MODULE_SYSTEM: [
        "/admin/system/status/detail/1",
    ],
    MODULE_LAN: [
        "/admin/network/lan/status/detail/1",
        "/admin/network/lan"
    ],
    MODULE_DHCP: [
        "/admin/services/dhcp/status/detail/1",
    ],
    MODULE_DEVICES: [
        "/admin/network/devices/status/detail/1",
    ],
    MODULE_WAN: [
        "/admin/network/wan/iface/wan/status/detail/1",
        "/admin/network/wan/status/detail/1",
    ],
    MODULE_WAN_SECONDARY: [
        "/admin/network/wan/iface/wand/status/detail/1",
    ],
    MODULE_MULTI_WAN: [
        "/admin/network/mwan3/status/detail/1",
    ],
    MODULE_MESH: [
        "/admin/network/mesh/status/detail/1",
    ],
    MODULE_VPN: [
        "/admin/network/vpn/status/detail/1",
    ],
    MODULE_WIRELESS_5G: [
        "/admin/network/wireless/status/detail/1/iface/wlan10",
        "/admin/network/wireless/iface/wlan10",
        "/admin/network/wireless/config/multi_ssid_config/embedded/iface/wlan10"
    ],
    MODULE_WIRELESS_24G: [
        "/admin/network/wireless/status/detail/1/iface/wlan00",
        "/admin/network/wireless/iface/wlan10",
        "/admin/network/wireless/config/multi_ssid_config/embedded/iface/wlan00"
    ],
    MODULE_WIRELESS_6G: [
        "/admin/network/wireless/status/detail/1/iface/wlan20",
        "/admin/network/wireless/iface/wlan20"
    ],
    MODULE_GSM: [
        "/admin/network/gcom/iface/4g/status/detail/1"
    ],
    MODULE_SMS: [
        "/admin/network/gcom/sms/iface/4g/status/detail/1",
    ],
    MODULE_USB: [
        "/admin/services/usb/status/detail/1",
    ],
    MODULE_DEVICE_LIST: [
        "/admin/network/devices/devlist/detail/1",
    ],
}

urllib3.disable_warnings()


def get_cudy_device_codes() -> List[str]:
    url = "https://support.cudy.com/emulator/"
    resp = requests.get(url, timeout=20)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")

    models: set[str] = set()

    for a in soup.select('a[href^="/emulator/"]'):
        href = a.get("href", "")
        code = href.replace("/emulator/", "").strip("/")
        code = unquote(code).strip()

        if not code:
            continue
        # ignore assets or anchors
        if code.lower().endswith((".css", ".js")) or code.startswith("#"):
            continue

        models.add(code)

    return sorted(models)


def _extract_more_detail_from_dom(html: str, base_url: str) -> Dict[str, str]:
    """Extract mapping of {panel_title: absolute_more_detail_url} from HTML DOM.

    Looks for div.panel > div.panel-heading > h3 as title and a link inside the
    panel whose text contains "more detail" (English) or typical translations.
    """
    soup = BeautifulSoup(html, "html.parser")
    sections: Dict[str, str] = {}

    # candidate link texts to match (lowercase)
    candidates = {"more detail", "more details", "more", "więcej", "więcej szczegółów", "más detalles"}

    for panel in soup.select("div.panel"):
        title_el = panel.select_one("div.panel-heading h3")
        if not title_el:
            continue
        title = title_el.get_text(strip=True)
        if not title:
            continue

        link_el = None
        for a in panel.select("a[href]"):
            label = a.get_text(" ", strip=True).lower()
            # allow partial match: e.g. 'More Detail' or 'More Details' or localised forms
            if any(c in label for c in candidates):
                link_el = a
                break

        if not link_el:
            continue

        href = link_el.get("href", "").strip()
        if not href:
            continue

        sections[title] = urljoin(base_url, href)

    return sections


def get_emulator_sections_static(device_code: str) -> Dict[str, str]:
    """Try to extract panel titles and their "More Detail" links from the static HTML.

    Returns a dict mapping title -> absolute URL. May return empty dict if the
    page is JS-driven.
    """
    base_url = f"https://support.cudy.com/emulator/{device_code}/cgi-bin/luci/"
    resp = requests.get(base_url, timeout=20)
    resp.raise_for_status()

    return _extract_more_detail_from_dom(resp.text, base_url)


async def get_emulator_sections_playwright(device_code: str) -> Dict[str, str]:
    """Use Playwright (Chromium) to render the page and then extract links.

    This requires `playwright` to be installed and browsers to be installed
    (`python -m playwright install chromium`). The function is async and can be
    awaited or called via asyncio.run.
    """
    try:
        from playwright.async_api import async_playwright
    except Exception as exc:  # pragma: no cover - environment may not have playwright
        raise RuntimeError(
            "Playwright not installed. Install with: pip install playwright \n"
            "and then run: python -m playwright install chromium"
        ) from exc

    base_url = f"https://support.cudy.com/emulator/{device_code}/cgi-bin/luci/"

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(base_url, wait_until="networkidle", timeout=60_000)

        # wait for typical DOM element (but don't fail if it doesn't appear)
        try:
            await page.wait_for_selector("div.panel-heading h3", timeout=8_000)
        except Exception:
            pass

        html = await page.content()
        await browser.close()

    return _extract_more_detail_from_dom(html, base_url)


def get_emulator_sections(device_code: str, use_playwright_fallback: bool = True) -> Dict[str, str]:
    """Smart wrapper: try static parse first, fall back to Playwright when needed.

    Returns a mapping title -> url. If nothing found and playwright fallback is
    disabled, returns empty dict.
    """
    sections = get_emulator_sections_static(device_code)
    if sections:
        return sections

    if not use_playwright_fallback:
        return {}

    try:
        return asyncio.run(get_emulator_sections_playwright(device_code))
    except Exception:
        return {}


def _ensure_detail_1(url: str) -> str:
    parsed = urlparse(url)
    return urlunparse(parsed._replace(query="detail=1"))


def download_emulator_module_pages(
        out_root: str = "cudy_router/html",
        timeout: int = 20,
) -> dict[str, dict[str, str]]:
    base_out = Path(out_root)
    base_out.mkdir(parents=True, exist_ok=True)

    session = requests.Session()
    session.verify = False
    session.headers.update({"User-Agent": "cudy-emulator-downloader"})

    results: dict[str, dict[str, str]] = {}

    for model in CUDY_DEVICES:
        print(f"\n== {model} ==")
        model_dir = base_out / model
        model_dir.mkdir(parents=True, exist_ok=True)
        results[model] = {}

        for module, paths in URLS.items():
            for path in paths:
                base_url = f"https://support.cudy.com/emulator/{model}/cgi-bin/luci/"
                rel_path = path.lstrip("/")
                url = _ensure_detail_1(urljoin(base_url, rel_path))

                try:
                    r = session.get(url, timeout=timeout, allow_redirects=True)
                except Exception:
                    continue

                if r.status_code != 200 or not r.text or len(r.text) < 200:
                    continue

                out_file = model_dir / f"{module}.html"
                out_file.write_text(r.text, encoding="utf-8")
                results[model][module] = str(out_file)
                print(f"  {module}: saved {out_file}")
                break

    try:
        session.close()
    except Exception:
        pass

    return results


if __name__ == "__main__":
    saved = download_emulator_module_pages(out_root="cudy_router/html")
    print(json.dumps(saved, indent=2))
