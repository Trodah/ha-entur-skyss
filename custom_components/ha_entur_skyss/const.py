"""Constants for ha-entur-skyss."""

DOMAIN = "ha_entur_skyss"
CONF_STOP_ID = "stop_id"
CONF_STOP_NAME = "stop_name"
CONF_MAX_DEPARTURES = "max_departures"

DEFAULT_MAX_DEPARTURES = 5
SCAN_INTERVAL_SECONDS = 45  # Entur anbefaler ikke hyppigere enn dette

API_URL = "https://api.entur.io/journey-planner/v3/graphql"
GEOCODER_URL = "https://api.entur.io/geocoder/v1/autocomplete"
CLIENT_NAME = "privatperson-ha-entur-skyss"
