"""JC4827W543 eBike Cockpit Bridge integration.

Diese Integration ist bewusst schlank gehalten. Die eigentliche
Datenanzeige laeuft direkt auf dem ESPHome-Geraet, das sich seine
HA-Sensoren via `homeassistant:`-Plattform abholt. Hier registrieren
wir lediglich den Config-Entry, damit das Geraet als verwaltete
Integration in HA auftaucht und der User einen sauberen Konfigurations-
einstieg hat.
"""

from __future__ import annotations

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Setze den ConfigEntry auf. Aktuell kein Background-Setup noetig."""
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = {
        "device_name": entry.data["device_name"],
    }
    _LOGGER.debug(
        "JC4827W543 cockpit bridge entry geladen: device_name=%s",
        entry.data["device_name"],
    )
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Entry-Aufraeumen."""
    hass.data.get(DOMAIN, {}).pop(entry.entry_id, None)
    return True
