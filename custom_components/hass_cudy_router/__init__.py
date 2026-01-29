from __future__ import annotations

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from . import registry
from .client import CudyClient
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    protocol = entry.data.get("protocol", "http")
    use_https = protocol.lower() in ("https", "ssl", "tls")

    client = CudyClient(
        host=entry.data.get("host"),
        username=entry.data.get("username"),
        password=entry.data.get("password"),
        use_https=use_https,
    )

    try:
        from .model_detect import detect_model
        model = await detect_model(client)
    except Exception:
        _LOGGER.debug("Model detection failed, falling back to Generic", exc_info=True)
        model = "Generic"

    integration = await registry.create_model_integration(
        model, hass, entry, client
    )

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = {
        "client": client,
        "integration": integration,
        "coordinator": integration.coordinator,
        "spec": integration.spec,
    }

    await hass.config_entries.async_forward_entry_setups(
        entry,
        list(integration.spec.platforms),
    )

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    data = hass.data.get(DOMAIN, {}).pop(entry.entry_id, None)
    if not data:
        return True

    spec = data.get("spec")

    if spec is not None:
        await hass.config_entries.async_unload_platforms(
            entry,
            list(spec.platforms),
        )

    client = data.get("client")
    if client:
        close_fn = getattr(client, "async_close", None) or getattr(client, "close", None)
        if close_fn:
            try:
                await close_fn()
            except Exception:
                _LOGGER.debug("Error closing client", exc_info=True)

    return True