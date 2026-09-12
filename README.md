# ha-entur-skyss

> **🇳🇴 Norsk oppsummering:** Denne Home Assistant-integrasjonen viser sanntids avgangstider fra [Entur](https://entur.no) sitt API. Utviklet og testet med [Skyss](https://www.skyss.no) i Bergen, men fungerer med alle norske holdeplasser i Entur-nettverket. Installeres enkelt via HACS med et moderne UI-oppsett (ingen YAML nødvendig for selve integrasjonen), og viser linjenummer, destinasjon og minutter til avgang — oppdatert hvert 45. sekund. Se seksjonen [Template sensors](#template-sensors) lenger ned for hvordan du kan lage kombinerte sensorer for dashboard eller talemeldinger.

Home Assistant integration for real-time departures via the [Entur](https://entur.no) API. Developed and tested with [Skyss](https://www.skyss.no) in Bergen, but works with any Norwegian stop in the Entur network.

### Features

- Real-time departures from any Entur stop (NSR stop ID)
- Supports both full stops (`NSR:StopPlace:`) and individual platforms (`NSR:Quay:`, `SKY:Quay:`)
- Shows line number, destination and minutes until departure
- Configurable number of departures (1–20)
- Automatically fetches stop name from the Entur API
- Updates every 45 seconds (as recommended by Entur)
- Supports multiple stops — add as many as you need
- Display name and number of departures can be changed later without deleting the integration

### Related integrations

#### Official HA Entur integration
HA has a [built-in Entur integration](https://www.home-assistant.io/integrations/entur_public_transport), but it is **Legacy** and requires `configuration.yaml`. This one uses a modern UI and is installable via HACS.

#### ha-entur_sx by DTekNO
This integration is **not** the same as [ha-entur_sx by DTekNO](https://github.com/DTekNO/ha-entur_sx). They serve different purposes:

| | ha-entur_sx (DTekNO) | ha-entur-skyss (this) |
|---|---|---|
| **What** | Alerts about cancellations and delays | Next departures from a stop |
| **API** | SIRI-SX (Situation Exchange) | Journey Planner GraphQL |
| **Use case** | "Is my bus cancelled?" | "When does the next bus leave?" |

All three work great together!

### Installation

#### HACS (recommended)
1. Open HACS in Home Assistant
2. Search for **Entur Skyss** under Integrations
3. Install and restart Home Assistant

#### Manual
1. Download this repository as a ZIP
2. Extract and copy the `custom_components/ha_entur_skyss/` folder to your HA `config/custom_components/` directory
3. Restart Home Assistant

### Configuration

1. Go to **Settings → Devices & Services → Add Integration**
2. Search for **Entur Skyss**
3. Enter the stop ID for your stop or platform

Valid ID formats:

| Format | Example | Description |
|--------|---------|-------------|
| `NSR:StopPlace:XXXXX` | `NSR:StopPlace:62356` | Full stop — all departures from all platforms |
| `NSR:Quay:XXXXX` | `NSR:Quay:53118` | One specific platform (national ID) |
| `SKY:Quay:XXXXXXXX` | `SKY:Quay:12010204` | One specific platform (Skyss ID) |

> **Tip:** Stops with platforms in multiple directions will return departures from all directions when using `NSR:StopPlace:`. Use a quay ID to filter for a single direction.

#### Finding your stop ID

**Full stops** can be found at [entur.no](https://entur.no) or [stoppested.entur.org](https://stoppested.entur.org). The NSR ID always starts with `NSR:StopPlace:`.

**Platform IDs (quay)** can be found by looking up the stop at [stoppested.entur.org](https://stoppested.entur.org), selecting the correct platform, and copying the quay ID (starts with `NSR:Quay:` or `SKY:Quay:`).

#### Changing settings

Display name and number of departures can be changed at any time without deleting the integration: go to **Settings → Devices & Services → Entur Skyss**, click the stop you want to change, and select **Configure**. The stop/quay ID itself cannot be changed here — to monitor a different stop, add a new integration instance.

### Dashboard cards

Replace the entity ID with your own (find it under **Developer Tools → States**).

#### Markdown table card

![Markdown card](custom_components/ha_entur_skyss/docs/dashboard_markdown_card.png)

```yaml
type: markdown
title: 🚌 Departures
content: |
  {% set d = state_attr('sensor.entur_bergen_busstasjon', 'departures') %}
  | Line | Destination | Departure |
  |------|-------------|-----------|
  {% for a in d -%}
  | **{{ a.line }}** | {{ a.destination }} | {{ a.minutes }} min |
  {% endfor %}
```

#### Mushroom badge

Compact badge showing the next departure. Color changes automatically: teal (> 5 min), orange (2–5 min), red (< 2 min).

![Mushroom badge](custom_components/ha_entur_skyss/docs/dashboard_badge.png)

Requires [Mushroom Cards](https://github.com/piitaya/lovelace-mushroom) (available in HACS).

```yaml
type: custom:mushroom-template-badge
icon: mdi:bus
color: >
  {% set d = state_attr('sensor.entur_bergen_busstasjon', 'departures') %}
  {% if d %}
    {% set m = d[0].minutes %}
    {% if m <= 2 %}red{% elif m <= 5 %}orange{% else %}teal{% endif %}
  {% endif %}
label: >
  {% set d = state_attr('sensor.entur_bergen_busstasjon', 'departures') %}
  {% if d %}Linje {{ d[0].line }}{% endif %}
content: >
  {% set d = state_attr('sensor.entur_bergen_busstasjon', 'departures') %}
  {% if d %}{{ d[0].minutes }} min{% endif %}
```

#### Mushroom template card

Shows the next two departures with color indicator.

![Mushroom card](custom_components/ha_entur_skyss/docs/dashboard_card.png)

Requires [Mushroom Cards](https://github.com/piitaya/lovelace-mushroom) (available in HACS).

```yaml
type: custom:mushroom-template-card
entity: sensor.entur_bergen_busstasjon
primary: >
  {% set d = state_attr('sensor.entur_bergen_busstasjon', 'departures') %}
  {% if d %}Linje {{ d[0].line }} → {{ d[0].destination }}{% endif %}
secondary: >
  {% set d = state_attr('sensor.entur_bergen_busstasjon', 'departures') %}
  {% if d and d|length > 1 %}
    {{ d[0].minutes }} min · Neste: linje {{ d[1].line }} om {{ d[1].minutes }} min
  {% endif %}
icon: mdi:bus-clock
icon_color: >
  {% set d = state_attr('sensor.entur_bergen_busstasjon', 'departures') %}
  {% if d %}
    {% set m = d[0].minutes %}
    {% if m <= 2 %}red{% elif m <= 5 %}orange{% else %}teal{% endif %}
  {% endif %}
```

#### Mushroom picture card (with template sensors)

Compact card with a custom picture, pairs well with the [template sensors](#template-sensors) below — combines the next two departures into one readable line.

![Mushroom picture card](custom_components/ha_entur_skyss/docs/entur_skyss.png)

Requires [Mushroom Cards](https://github.com/piitaya/lovelace-mushroom) (available in HACS). Replace `entity` with your own template sensor, and `picture` with a path to your own image under `config/www/` (e.g. a stop or bus company logo — the Skyss icon above is available at [`docs/entur_skyss.png`](custom_components/ha_entur_skyss/docs/entur_skyss.png), copy it to `config/www/pictures/skyss.png` in your HA install).

```yaml
type: custom:mushroom-template-card
entity: sensor.neste_buss_mot_byen
primary: Neste buss mot byen
secondary: '{{ states(''sensor.neste_buss_mot_byen'') }}'
picture: /local/pictures/skyss.png
multiline_secondary: true
vertical: true
grid_options:
  columns: 6
  rows: auto
```

### Template sensors

You can combine multiple stop sensors into a single, human-readable template sensor — useful for a compact dashboard line or a voice announcement. Add this to your `templates.yaml` (or under `template:` in `configuration.yaml`), replacing the entity IDs and `unique_id` values with your own:

```yaml
- sensor:
    # ENTUR SKYSS INTEGRASJON
    - name: "Neste buss fra Holdeplass 1"
      unique_id: "REPLACE-WITH-YOUR-OWN-UUID"
      state: >
        {% set d = state_attr('sensor.entur_holdeplass_1', 'departures') %}
        {% if d %}
        Linje {{ d[0].line }} mot {{ d[0].destination }} om {{ d[0].minutes }} min (kl. {{ d[0].departure_time[11:16] }}).
        Neste: linje {{ d[1].line }} mot {{ d[1].destination }} om {{ d[1].minutes }} min.
        {% endif %}

    - name: "Neste buss fra Holdeplass 2"
      unique_id: "REPLACE-WITH-YOUR-OWN-UUID"
      state: >
        {% set d = state_attr('sensor.entur_holdeplass_2', 'departures') %}
        {% if d %}
        Linje {{ d[0].line }} mot {{ d[0].destination }} om {{ d[0].minutes }} min (kl. {{ d[0].departure_time[11:16] }}).
        Neste: linje {{ d[1].line }} mot {{ d[1].destination }} om {{ d[1].minutes }} min.
        {% endif %}
```

> **Tip:** Generate a fresh UUID for each `unique_id` (e.g. `uuidgen` on Linux/macOS, or any online UUID generator) — it must be unique across your whole Home Assistant instance. Replace `sensor.entur_holdeplass_1` / `sensor.entur_holdeplass_2` with the actual entity IDs of your Entur Skyss sensors (find them under **Developer Tools → States**).

### Troubleshooting

**"Invalid ID" error when adding the integration**
The stop/quay ID must start with `NSR:StopPlace:`, `NSR:Quay:` or `SKY:Quay:`. Check for typos or extra spaces.

**"Stop not found"**
The ID is correctly formatted but doesn't exist in Entur's database. Look it up again at [stoppested.entur.org](https://stoppested.entur.org) to confirm it's correct.

**"Cannot connect to Entur API"**
Home Assistant couldn't reach `api.entur.io` while validating the ID. Check your internet connection and DNS, then try again — this is usually transient.

**Sensor shows "unknown" or no departures**
1. Check **Settings → System → Logs** for messages from `custom_components.ha_entur_skyss`.
2. `No stop data for <id>` — the stop/quay ID may no longer be valid, or the API returned nothing for it.
3. `Entur API error: <status>` or `Connection error to Entur API` — a temporary API/network issue; the sensor will retry on the next update (every 45 seconds).
4. If departures are empty outside of these errors, the stop may simply have no scheduled departures at the moment (e.g. late night).

**Enable debug logging**

Add this to `configuration.yaml` and restart Home Assistant:

```yaml
logger:
  default: warning
  logs:
    custom_components.ha_entur_skyss: debug
```

---

## License

MIT License — see [LICENSE](LICENSE)
