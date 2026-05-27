# ESPHome-Firmware fuer das eBike-Cockpit

Zwei Varianten in diesem Ordner:

| Datei | Zweck |
|-------|-------|
| `ebike-cockpit-base.yaml` | Standalone. Daten via HA-API. Kein LDI. |
| `ebike-cockpit-with-ldi.yaml` | Wie Base, plus direkte BLE-Anbindung an Bosch LDI. |

## Erwartete HA-Entitaeten

Die Firmware spricht eine Handvoll Sensoren ueber konfigurierbare Namen
an (Substitution `bike`, Default `performance_cx`):

| Funktion | Entitaet | Typ |
|----------|----------|------|
| Akku-SoC | `sensor.${bike}_battery_soc` | numeric (0..100) |
| Ladestatus | `binary_sensor.${bike}_charger_connected` | on/off |
| Reichweite | `sensor.${bike}_range_remaining` | numeric (km) |
| Kilometerstand | `sensor.${bike}_odometer` | numeric (km, total) |
| Tage seit letzter Fahrt | `sensor.${bike}_days_since_last_tour` | numeric (int) |
| Wartungs-Anzahl | `sensor.${bike}_due_maintenance_count` | numeric (int) |
| Wartungs-Label | `sensor.${bike}_next_maintenance_label` | text |

Die ersten vier liefert die `ha-bosch-ebike`-Integration ab Werk.
Die letzten drei muessen ggf. als Template-Sensor angelegt werden.

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
| LCD Reset | 4 |
| Backlight (LEDC PWM) | 1 |
| Touch I2C SDA | 8 |
| Touch I2C SCL | 4 |
| Touch INT | 3 |
| Touch Reset | 38 |

Der Touch-Controller ist ein CST816. Aktuell nicht fuer Interaktion
genutzt, aber vorbereitet.
