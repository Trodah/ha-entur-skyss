"""Sensor platform for ha-entur-skyss."""
from __future__ import annotations

import logging
from datetime import datetime, timedelta

import aiohttp

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.util import dt as dt_util

from .const import (
    API_URL,
    CLIENT_NAME,
    CONF_MAX_DEPARTURES,
    CONF_STOP_ID,
    CONF_STOP_NAME,
    DEFAULT_MAX_DEPARTURES,
    DOMAIN,
    SCAN_INTERVAL_SECONDS,
)

_LOGGER = logging.getLogger(__name__)

SCAN_INTERVAL = timedelta(seconds=SCAN_INTERVAL_SECONDS)

GRAPHQL_QUERY = """
{
  stopPlace(id: "%s") {
    id
    name
    estimatedCalls(numberOfDepartures: %d) {
      expectedDepartureTime
      destinationDisplay { frontText }
      serviceJourney {
        line {
          publicCode
          transportMode
        }
      }
    }
  }
}
"""


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Entur Skyss sensor from config entry."""
    stop_id = entry.data[CONF_STOP_ID]
    stop_name = entry.data.get(CONF_STOP_NAME, stop_id)
    max_departures = entry.data.get(CONF_MAX_DEPARTURES, DEFAULT_MAX_DEPARTURES)

    async_add_entities(
        [EnturSkysSensor(stop_id, stop_name, max_departures)],
        update_before_add=True,
    )


class EnturSkysSensor(SensorEntity):
    """Sensor that shows next departures from a stop."""

    def __init__(self, stop_id: str, stop_name: str, max_departures: int) -> None:
        """Initialize the sensor."""
        self._stop_id = stop_id
        self._stop_name = stop_name
        self._max_departures = max_departures
        self._state = None
        self._departures = []
        self._attr_unique_id = f"{DOMAIN}_{stop_id}"
        self._attr_name = f"Entur {stop_name}"
        self._attr_icon = "mdi:bus-clock"

    @property
    def native_value(self):
        """Return minutes until next departure."""
        return self._state

    @property
    def native_unit_of_measurement(self):
        return "min"

    @property
    def extra_state_attributes(self):
        """Return departure list as attributes."""
        return {"departures": self._departures}

    async def async_update(self) -> None:
        """Fetch new data from Entur API."""
        query = GRAPHQL_QUERY % (self._stop_id, self._max_departures)
        headers = {
            "Content-Type": "application/json",
            "ET-Client-Name": CLIENT_NAME,
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    API_URL, json={"query": query}, headers=headers
                ) as resp:
                    if resp.status != 200:
                        _LOGGER.error("Entur API error: %s", resp.status)
                        return

                    data = await resp.json()

            stop = data.get("data", {}).get("stopPlace")
            if not stop:
                _LOGGER.warning("No stop data for %s", self._stop_id)
                return

            calls = stop.get("estimatedCalls", [])
            self._departures = []

            now = dt_util.now()

            for call in calls:
                departure_time = datetime.fromisoformat(
                    call["expectedDepartureTime"]
                )
                minutes = int((departure_time - now).total_seconds() / 60)
                self._departures.append({
                    "line": call["serviceJourney"]["line"]["publicCode"],
                    "mode": call["serviceJourney"]["line"]["transportMode"],
                    "destination": call["destinationDisplay"]["frontText"],
                    "departure_time": call["expectedDepartureTime"],
                    "minutes": minutes,
                })

            if self._departures:
                self._state = self._departures[0]["minutes"]
            else:
                self._state = None

        except aiohttp.ClientError as err:
            _LOGGER.error("Connection error to Entur API: %s", err)
