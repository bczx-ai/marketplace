---
name: weather-pollen
displayName: "Weather Pollen"
description: "利用免费API提供任意地点的天气和花粉报告。获取当前天气状况、预报及花粉数据。"
version: "1.0.3"
tags:
  - office_productivity
license: "Unknown"
---

# Weather and Pollen Skill

Get weather and pollen reports for any location using free APIs.

## Usage

When asked about weather or pollen in Anna, TX (or configured location), use the `weather_report` tool from this skill.

## Tools

### weather_report
Get weather and pollen data for a specified location.

**Args:**
- `includePollen` (boolean, default: true) - Include pollen data
- `location` (string, optional) - Location name to display (coordinates configured via env)

**Example:**
```json
{"includePollen": true, "location": "Anna, TX"}
```

## Configuration

Set location via environment variables (defaults for Anna, TX):
- `WEATHER_LAT` - Latitude (default: 33.3506)
- `WEATHER_LON` - Longitude (default: -96.3175)
- `WEATHER_LOCATION` - Location display name (default: "Anna, TX")

## APIs Used
- **Weather:** Open-Meteo (free, no API key)
- **Pollen:** Pollen.com (free, no API key)
