"""Config flow for Entur Skyss integration."""
from __future__ import annotations

import logging
from typing import Any

import aiohttp
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.data_entry_flow import FlowResult

from .const import (
    CONF_MAX_DEPARTURES,
    CONF_STOP_ID,
    CONF_STOP_NAME,
    DEFAULT_MAX_DEPARTURES,
    DOMAIN,
    GEOCODER_URL,
)

_LOGGER = logging.getLogger(__name__)


async def lookup_stop(stop_id: str) -> str | None:
    """Look up stop name from Entur geocoder."""
    headers = {"ET-Client-Name": "privatperson-ha-entur-skyss"}
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                GEOCODER_URL,
                params={"text": stop_id, "lang": "no", "size": 1, "layers": "venue"},
                headers=headers,
            ) as resp:
                if resp.status != 200:
                    return None
                data = await resp.json()
                features = data.get("features", [])
                if features:
                    return features[0]["properties"].get("label")
    except aiohttp.ClientError:
        return None
    return None


class EnturSkyssConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Entur Skyss."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}

        if user_input is not None:
            stop_id = user_input[CONF_STOP_ID].strip()

            # Look up stop name if not provided
            stop_name = user_input.get(CONF_STOP_NAME, "").strip()
            if not stop_name:
                stop_name = await lookup_stop(stop_id) or stop_id

            await self.async_set_unique_id(stop_id)
            self._abort_if_unique_id_configured()

            return self.async_create_entry(
                title=stop_name,
                data={
                    CONF_STOP_ID: stop_id,
                    CONF_STOP_NAME: stop_name,
                    CONF_MAX_DEPARTURES: user_input.get(
                        CONF_MAX_DEPARTURES, DEFAULT_MAX_DEPARTURES
                    ),
                },
            )

        schema = vol.Schema(
            {
                vol.Required(CONF_STOP_ID): str,
                vol.Optional(CONF_STOP_NAME): str,
                vol.Optional(
                    CONF_MAX_DEPARTURES, default=DEFAULT_MAX_DEPARTURES
                ): vol.All(int, vol.Range(min=1, max=20)),
            }
        )

        return self.async_show_form(
            step_id="user",
            data_schema=schema,
            errors=errors,
        )
