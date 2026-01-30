#!/usr/bin/env python3
import os
import sys
import asyncio
from datetime import datetime

from custom_components.hass_cudy_router.api import CudyApi
from custom_components.hass_cudy_router.const import *
from custom_components.hass_cudy_router.model_detect import detect_model

# ------------------------------------------------------------------
# Allow running directly via `python -m tests.cudy_router.smoke_test_wr6500`
# ------------------------------------------------------------------
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
sys.path.insert(0, ROOT)

from custom_components.hass_cudy_router.client import CudyClient

# ------------------------------------------------------------------
# CONFIG (via env vars)
# ------------------------------------------------------------------
MODEL = os.getenv("CUDY_MODEL", "Generic")
PROTOCOL = os.getenv("CUDY_PROTOCOL", "http")
HOST = os.getenv("CUDY_HOST", "192.168.1.1")
USERNAME = os.getenv("CUDY_USER", "admin")
PASSWORD = os.getenv("CUDY_PASS")

if not PASSWORD:
    print("❌ Set CUDY_PASS env variable")
    sys.exit(1)

USE_HTTPS = PROTOCOL == "https"


def print_module(name: str, values: dict) -> None:
    print(f"Values for {name}: \n")
    for key, value in values.items():
        print(f"{key}: {value} \n")
    print("_______________________________________ \n")


async def main() -> None:
    print("=== Cudy Router Smoke Test ===")
    print(f"Host: {PROTOCOL}://{HOST}")
    print(f"User: {USERNAME}")
    print(f"Pass: {PASSWORD}")
    print("-----------------------------")

    client = CudyClient(
        host=HOST,
        username=USERNAME,
        password=PASSWORD,
        use_https=USE_HTTPS,
    )

    try:
        print("🔐 Authenticating...")
        ok = await client.authenticate()
        print(f"Auth result: {ok}")
        print(f"sysauth set: {client.sysauth}")
        print(f"Auth cookie: {'SET' if ok else 'NOT SET'}")

        if not ok:
            print("❌ Authentication failed, aborting")
            return

        found_model = await detect_model(client)
        print(f"\n🛜 Looking for {MODEL} device - found: {found_model}")

        print("\n📦 Running CudyApi.get_data()")
        api = CudyApi(client)
        data = await api.get_data()

        print("\n=== Parsed modules ===")
        for key in data:
            value = data.get(key)
            if isinstance(value, dict):
                print_module(key, value)
            else:
                print(f"Value for {key}: {value}")

        print("\n🕒 Finished at", datetime.now().isoformat())

    finally:
        await client.close()


if __name__ == "__main__":
    asyncio.run(main())