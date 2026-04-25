"""Config flow for Entur Skyss integration."""
from __future__ import annotations

import logging
from typing import Any

import aiohttp
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.data_entry_flow import FlowResult

from .const import (
    API_URL,
    CLIENT_NAME,
    CONF_MAX_DEPARTURES,
    CONF_STOP_ID,
    CONF_STOP_NAME,
    DEFAULT_MAX_DEPARTURES,
    DOMAIN,
)

_LOGGER = logging.getLogger(__name__)

VALIDATE_QUERY = '{ stopPlace(id: "%s") { name } }'


async def validate_stop_id(stop_id: str) -> str | None:
    """Validate stop ID via Journey Planner API and return stop name, or None if not found."""
    headers = {
        "Content-Type": "application/json",
        "ET-Client-Name": CLIENT_NAME,
    }
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                API_URL,
                json={"query": VALIDATE_QUERY % stop_id},
                headers=headers,
            ) as resp:
                if resp.status != 200:
                    return None
                data = await resp.json()
                stop = data.get("data", {}).get("stopPlace")
                if stop:
                    return stop.get("name")
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

            if not stop_id.startswith("NSR:StopPlace:"):
                errors[CONF_STOP_ID] = "invalid_stop_id"
            else:
                try:
                    api_name = await validate_stop_id(stop_id)
                except Exception:  # noqa: BLE001
                    errors["base"] = "cannot_connect"
                else:
                    if api_name is None:
                        errors[CONF_STOP_ID] = "stop_not_found"
                    else:
                        stop_name = user_input.get(CONF_STOP_NAME, "").strip() or api_name

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
