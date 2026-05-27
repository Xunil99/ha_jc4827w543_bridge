# ESPHome-Firmware fuer das eBike-Cockpit

Zwei Varianten in diesem Ordner:

| Datei | Zweck |
|-------|-------|
| `ebike-cockpit-base.yaml` | Standalone. Daten via HA-API. Kein LDI. |
| `ebike-cockpit-with-ldi.yaml` | Wie Base, plus direkte BLE-Anbindung an Bosch LDI. |

## Erwartete HA-Entitaeten

Die Firmware spricht eine Handvoll Sensoren ueber konfigurierbare Namen
an. Defaults zeigen auf das `gartenhaus_ebike`-Setup, anpassen ueber
die `substitutions:` am Anfang der YAML.

| Funktion | Default-Entitaet | Typ |
|----------|-----------------|------|
| Akku-SoC | `sensor.gartenhaus_ebike_battery_soc_live` | numeric (0..100) |
| Ladestatus | `binary_sensor.gartenhaus_ebike_charger_connected` | on/off |
| Letzte-Tour-Distanz | `sensor.drive_unit_performance_line_cx_last_ride_distance` | numeric (km) |
| Kilometerstand | `sensor.gartenhaus_ebike_odometer_live` | numeric (km, total) |
| Tage seit letzter Fahrt | `sensor.gartenhaus_ebike_days_since_last_tour` | numeric (int) |
| Wartungs-Anzahl | `sensor.gartenhaus_ebike_due_maintenance_count` | numeric (int) |
| Wartungs-Label | `sensor.gartenhaus_ebike_next_maintenance_label` | text |
| Wochenkilometer | `sensor.gartenhaus_ebike_week_distance` | numeric (km) |

**Nicht** mehr als HA-Sensor noetig:
- Wetter (aktuell + 5 Tage): kommt von Open-Meteo direkt am ESP
- Sonnenauf-/untergang: ESPHome-`sun:`-Component aus Koordinaten

## Beispiel-Template-Sensor: `days_since_last_tour`

In `configuration.yaml` (oder einer Template-Sensor-Datei):

```yaml
template:
  - sensor:
      - name: "Performance CX Days Since Last Tour"
        unique_id: performance_cx_days_since_last_tour
        unit_of_measurement: "d"
        state_class: measurement
        state: >
          {% set last = states('sensor.performance_cx_last_tour_date') %}
          {% if last in ['unknown', 'unavailable', 'none', ''] %}
            -1
          {% else %}
            {{ ((now() - as_datetime(last)).days) | int(default=-1) }}
          {% endif %}
        availability: >
          {{ has_value('sensor.performance_cx_last_tour_date') }}
```

## Beispiel-Template-Sensoren: `due_maintenance_count` + `next_maintenance_label`

Setzt voraus, dass `ha-bosch-ebike` einen Wartungs-Status fuer das Bike
liefert. Wenn nicht, kannst Du eine eigene `input_number`-Eintraege
nutzen.

```yaml
template:
  - sensor:
      - name: "Performance CX Due Maintenance Count"
        unique_id: performance_cx_due_maintenance_count
        state_class: measurement
        state: >
          {{ state_attr('sensor.performance_cx_maintenance', 'due_count') | int(0) }}

      - name: "Performance CX Next Maintenance Label"
        unique_id: performance_cx_next_maintenance_label
        state: >
          {{ state_attr('sensor.performance_cx_maintenance', 'next_label') | default('', true) }}
```

## Sonnenauf- und Sonnenuntergang: Koordinaten setzen

**Kein HA-Template-Sensor mehr noetig.** ESPHome's eingebautes
`sun:`-Component berechnet Sonnenauf- und -untergang direkt aus
Laengen- und Breitengrad. Einmal die Heimat-Koordinaten in den
Substitutions setzen:

```yaml
substitutions:
  home_latitude: "52.520008"    # Default: Berlin-Mitte
  home_longitude: "13.404954"
```

Die Werte fuer das eigene Zuhause findest Du in den HA-Einstellungen
unter Einstellungen → System → Allgemein → Standort (oder einmal kurz
auf [openstreetmap.org](https://www.openstreetmap.org/) den Standort
suchen und Koordinaten ablesen).

Der NOAA-Algorithmus im sun:-Component ist auf rund eine Minute genau.

## Beispiel-Template-Sensor: `gartenhaus_ebike_week_distance`

Summe der Tour-Distanzen der laufenden Woche (Montag bis heute).
Setzt voraus, dass `ha-bosch-ebike` einen oder mehrere
`tour_distance`-Sensoren mit `state_class: total_increasing` liefert.

Variante A (einfach, falls die Integration einen `week_distance`-Wert
mitliefert):

```yaml
template:
  - sensor:
      - name: "Gartenhaus eBike Week Distance"
        unique_id: gartenhaus_ebike_week_distance
        unit_of_measurement: "km"
        state: "{{ state_attr('sensor.gartenhaus_ebike_stats', 'week_km') | float(0) }}"
```

Variante B (Utility-Meter ueber die HA-Statistics):

```yaml
utility_meter:
  ebike_week_distance:
    source: sensor.gartenhaus_ebike_odometer_live
    cycle: weekly
```

## Wetter (aktuelle Temperatur + 5-Tage-Forecast): kein HA-Setup noetig

Beides kommt direkt von **Open-Meteo** (open-meteo.com), einer freien
Wetter-API ohne Account, ohne API-Key, mit grosszuegigen Fair-Use-
Limits (10.000 Anfragen pro Tag pro IP).

Das ESP zieht alle 15 Minuten **einen** HTTPS-Call mit den weiter oben
gesetzten Koordinaten und befuellt damit:

- Wetter-Icon + aktuelle Temperatur auf Page 1
- 5-Tage-Forecast (Tagesname, Icon, Max/Min) auf Page 2

Beim Boot wird der erste Call kurz nach WLAN-Connect ausgeloest, danach
laeuft das 15-Min-Interval.

Falls Du Open-Meteo absichtlich nicht nutzen willst (z.B. weil keine
Internet-Verbindung erlaubt), kannst Du den `http_request:`, `script:`
und das 15-Min-Interval rauspatchen und stattdessen wieder eigene
HA-Template-Sensoren anbinden.

## Flashen

1. `secrets.yaml` im ESPHome-Ordner anlegen mit `wifi_ssid`, `wifi_password`,
   `api_encryption_key`, `ota_password`.
2. Substitutions in der gewuenschten YAML anpassen (Bike-Praefix, Bike-Name).
3. `esphome run ebike-cockpit-base.yaml` (oder die mit-LDI-Variante).
4. Erstes Flashen ueber USB-C. Folge-Updates per OTA.

## Hardware-Pinout (JC4827W543)

| Funktion | GPIO |
|----------|------|
| QSPI CLK | 47 |
| QSPI Data 0..3 | 21, 48, 40, 39 |
| LCD CS | 45 |
| LCD Reset | (kein HW-Reset, Software-Reset via init_sequence) |
| Backlight (LEDC PWM) | 1 |
| Touch I2C SDA | 8 |
| Touch I2C SCL | 4 |
| Touch INT | 3 |
| Touch Reset | 38 |

Der Touch-Controller ist beim JC4827W543C ein **GT911** (laut offizieller
ESPHome-Geraete-Referenz). Bei anderen Varianten (z.B. JC4827W543R mit
CST816) die `platform:`-Zeile im `touchscreen:`-Block entsprechend anpassen.
Aktuell ist Touch noch nicht fuer Interaktion genutzt, aber vorbereitet.
