# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A Home Assistant custom component that fetches real-time departures from the Entur Journey Planner v3 GraphQL API and exposes them as sensor entities. Targeted at Norwegian public transport (Skyss/Entur), published on GitHub and submitted to HACS default.

## Validation

There are no local build or test commands. Correctness is validated via GitHub Actions on push/PR:

- **hassfest** — checks HA integration manifest and structure
- **HACS validate** — checks HACS compatibility

To test locally, copy `custom_components/ha_entur_skyss/` into the `custom_components/` folder of a running Home Assistant instance and restart.

## Architecture

The integration is a minimal single-platform (sensor) component with no coordinator:

- `__init__.py` — sets up and tears down config entries, forwards to the `sensor` platform
- `config_flow.py` — UI-driven setup; validates the stop/quay ID against the Entur API before creating the entry
- `sensor.py` — `EnturSkysSensor` fetches data directly in `async_update` (no DataUpdateCoordinator); runs every 45 seconds per Entur's recommendation
- `const.py` — all constants including API URL, client name, and config keys

## Stop ID types

The integration distinguishes between two query shapes based on the ID:

| Prefix | GraphQL query | Returns |
|--------|--------------|---------|
| `NSR:StopPlace:` | `stopPlace(id: ...)` | All departures across all quays at a stop |
| `NSR:Quay:` / `SKY:Quay:` | `quay(id: ...)` | Departures from one specific platform/direction |

Detection is via `":Quay:" in stop_id`. This logic exists in both `config_flow.py` and `sensor.py` — keep them in sync if changed.

## API details

- Endpoint: `https://api.entur.io/journey-planner/v3/graphql` (no auth required)
- Required header: `ET-Client-Name: privateperson-ha-entur-skyss`
- Queries use inline GraphQL strings (not a library); see `sensor.py` for the full query shapes

## Translations

UI strings are in `strings.json` (Norwegian, used by HA) and `translations/en.json` (English). Both must be updated when adding new config fields or error codes.
