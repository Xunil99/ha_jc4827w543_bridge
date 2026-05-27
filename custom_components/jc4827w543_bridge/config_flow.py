"""Config-Flow fuer JC4827W543 Cockpit Bridge."""

from __future__ import annotations

from typing import Any

import voluptuous as vol

from homeassistant.config_entries import ConfigFlow, ConfigFlowResult
from homeassistant.helpers import selector

from .const import CONF_DEVICE_NAME, DOMAIN, SETUP_HINT


class JC4827W543BridgeConfigFlow(ConfigFlow, domain=DOMAIN):
    """User-initiated Config-Flow."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Erster und einziger Schritt: ESPHome-Device-Name abfragen."""
        errors: dict[str, str] = {}

        if user_input is not None:
            device_name = str(user_input[CONF_DEVICE_NAME]).strip().lower()
            await self.async_set_unique_id(device_name)
            self._abort_if_unique_id_configured()
            return self.async_create_entry(
                title=f"JC4827W543 ({device_name})",
                data={CONF_DEVICE_NAME: device_name},
            )

        schema = vol.Schema(
            {
                vol.Required(CONF_DEVICE_NAME): selector.TextSelector(),
            }
        )
        return self.async_show_form(
            step_id="user",
            data_schema=schema,
            description_placeholders={"hint": SETUP_HINT},
            errors=errors,
        )
