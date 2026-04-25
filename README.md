# ha-entur-skyss

> 🇳🇴 Norsk versjon nedenfor / English version below 🇬🇧

---

## 🇬🇧 English

A [Home Assistant](https://www.home-assistant.io/) custom integration that fetches **real-time bus departures** from [Entur](https://entur.no) for stops served by [Skyss](https://www.skyss.no) in the Bergen region — installable via [HACS](https://hacs.xyz).

### Screenshot

![Dashboard card](custom_components/ha_entur_skyss/docs/markdown_kort1.png)

### Features

- Real-time departures from any Entur stop (NSR stop ID)
- Shows line number, destination and minutes until departure
- Configurable number of departures (1–20)
- Automatically fetches stop name from the Entur API
- Updates every 45 seconds (as recommended by Entur)
- Supports multiple stops — add as many as you need

### Complementary integration

This integration is **not** the same as [ha-entur_sx by DTekNO](https://github.com/DTekNO/ha-entur_sx). They serve different purposes:

| | ha-entur_sx (DTekNO) | ha-entur-skyss (this) |
|---|---|---|
| **What** | Alerts about cancellations and delays | Next departures from a stop |
| **API** | SIRI-SX (Situation Exchange) | Journey Planner GraphQL |
| **Use case** | "Is my bus cancelled?" | "When does the next bus leave?" |

They work great together!

### Installation

#### HACS (recommended)
1. Open HACS in Home Assistant
2. Go to **Integrations → Custom repositories**
3. Add `https://github.com/Trodah/ha-entur-skyss` as an **Integration**
4. Search for **Entur Skyss** and install
5. Restart Home Assistant

#### Manual
1. Download this repository as a ZIP
2. Extract and copy the `custom_components/ha_entur_skyss/` folder to your HA `config/custom_components/` directory
3. Restart Home Assistant

### Configuration

1. Go to **Settings → Devices & Services → Add Integration**
2. Search for **Entur Skyss**
3. Enter the NSR stop ID for your stop (e.g. `NSR:StopPlace:62356`)

#### Finding your stop ID
Look up your stop at [entur.no](https://entur.no) or search at [stoppested.entur.org](https://stoppested.entur.org). The NSR ID always starts with `NSR:StopPlace:`.

### Dashboard card

Add a Markdown card with this YAML to display departures as a table:

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

Replace `sensor.entur_bergen_busstasjon` with your sensor entity ID (find it under **Developer Tools → States**).

---

## 🇳🇴 Norsk

En tilpasset [Home Assistant](https://www.home-assistant.io/)-integrasjon som henter **sanntidsavganger** fra [Entur](https://entur.no) for stoppesteder betjent av [Skyss](https://www.skyss.no) i Bergensregionen — installerbar via [HACS](https://hacs.xyz).

### Skjermbilde

![Dashboard-kort](custom_components/ha_entur_skyss/docs/markdown_kort1.png)

### Funksjoner

- Sanntidsavganger fra alle Entur-stoppesteder (NSR stopp-ID)
- Viser linjenummer, destinasjon og minutter til avgang
- Valgfritt antall avganger (1–20)
- Henter stoppestedsnavn automatisk fra Entur API
- Oppdateres hvert 45. sekund (anbefalt av Entur)
- Støtter flere stoppesteder — legg til så mange du vil

### Komplementær integrasjon

Denne integrasjonen er **ikke** det samme som [ha-entur_sx av DTekNO](https://github.com/DTekNO/ha-entur_sx). De dekker ulike behov:

| | ha-entur_sx (DTekNO) | ha-entur-skyss (denne) |
|---|---|---|
| **Hva** | Varsler om innstillinger og forsinkelser | Neste avganger fra stoppested |
| **API** | SIRI-SX (Situation Exchange) | Journey Planner GraphQL |
| **Bruksområde** | "Er bussen innstilt?" | "Når går neste buss?" |

De fungerer utmerket sammen!

### Installasjon

#### HACS (anbefalt)
1. Åpne HACS i Home Assistant
2. Gå til **Integrasjoner → Egendefinerte pakkelagre**
3. Legg til `https://github.com/Trodah/ha-entur-skyss` som en **Integrasjon**
4. Søk etter **Entur Skyss** og installer
5. Start Home Assistant på nytt

#### Manuell installasjon
1. Last ned dette repoet som ZIP
2. Pakk ut og kopier mappen `custom_components/ha_entur_skyss/` til `config/custom_components/` på din HA-instans
3. Start Home Assistant på nytt

### Konfigurasjon

1. Gå til **Innstillinger → Enheter og tjenester → Legg til integrasjon**
2. Søk etter **Entur Skyss**
3. Skriv inn NSR stopp-ID for ditt stoppested (f.eks. `NSR:StopPlace:62356`)

#### Finn din stopp-ID
Søk opp stoppestedet ditt på [entur.no](https://entur.no) eller på [stoppested.entur.org](https://stoppested.entur.org). NSR-ID-en starter alltid med `NSR:StopPlace:`.

### Dashboard-kort

Legg til et Markdown-kort med denne YAML-koden for å vise avganger som en tabell:

```yaml
type: markdown
title: 🚌 Avganger
content: |
  {% set d = state_attr('sensor.entur_bergen_busstasjon', 'departures') %}
  | Linje | Destinasjon | Avgang |
  |-------|-------------|--------|
  {% for a in d -%}
  | **{{ a.line }}** | {{ a.destination }} | {{ a.minutes }} min |
  {% endfor %}
```

Bytt ut `sensor.entur_bergen_busstasjon` med din sensors entitets-ID (finn den under **Utviklerverktøy → Tilstander**).

---

## License

MIT License — see [LICENSE](LICENSE)
