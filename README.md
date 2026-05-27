# JC4827W543 eBike Cockpit Bridge

Standalone Home-Assistant-Integration plus ESPHome-Firmware für das
**Guition JC4827W543** ESP32-S3 Display als Flur-/Garagen-Cockpit für ein
Bosch Smart System eBike.

Das Display zeigt im Hochformat (272 × 480) sieben Kerninformationen
zum Bike auf einen Blick:

1. Datum + Tagesname
2. Uhrzeit
3. Akkustand in Prozent (groß) mit Ladestatus-Icon
4. Geschätzte Restreichweite in km
5. Tage seit der letzten Fahrt
6. Fällige Wartungen (Anzahl + dringlichste)
7. Kilometerstand (Lifetime)

Zwei Firmware-Varianten:

- **`ebike-cockpit-base.yaml`**: Das Display lebt rein vom HA-API.
  HA bezieht die Daten aus der `ha-bosch-ebike`-Integration (oder einer
  beliebigen anderen Quelle) und schiebt sie an das ESP.
- **`ebike-cockpit-with-ldi.yaml`**: Zusätzlich integriert das ESP die
  Bosch-LDI-Bridge direkt per BLE, sodass es Live-Daten auch ohne
  laufenden HA-Server anzeigen kann.

## Status

Privates Projekt, aktuell nicht öffentlich verteilt. Wird lokal entwickelt
und getestet.

## Schnellstart

1. **HA-Integration installieren**: `custom_components/jc4827w543_bridge/`
   nach `<HA-Config>/custom_components/` kopieren, HA neu starten,
   Integration über `Einstellungen → Geräte & Dienste → Integration
   hinzufügen → JC4827W543` einrichten. Im Setup gibst Du den
   ESPHome-Device-Namen ein (z.B. `ebike-cockpit`).

2. **Display flashen**: Eine der beiden Varianten in `esphome/` öffnen,
   die Substitutions (WiFi, Bike-Entitäts-Präfixe, Bike-Name) anpassen,
   in ESPHome importieren und auf das JC4827W543 flashen.

3. **Eingangsdaten in HA bereitstellen**: Die Firmware erwartet eine
   Handvoll Sensoren mit konfigurierbaren Namen. Standardwerte:

   | Sensor | Default-Entität |
   |--------|-----------------|
   | Akkustand | `sensor.${bike}_battery_soc` |
   | Ladezustand | `binary_sensor.${bike}_charger_connected` |
   | Reichweite | `sensor.${bike}_range_remaining` |
   | Kilometerstand | `sensor.${bike}_odometer` |
   | Letztes Fahrt-Datum | `sensor.${bike}_last_tour_date` |
   | Wartungs-Anzahl | `sensor.${bike}_due_maintenance_count` |
   | Wartungs-Label | `sensor.${bike}_next_maintenance_label` |

   `${bike}` wird über eine Substitution in der YAML gesetzt
   (z.B. `performance_cx`).

## Beziehung zu `ha-bosch-ebike`

Diese Integration ist bewusst von `ha-bosch-ebike` entkoppelt: Du kannst
sie auch verwenden, wenn Dein Bosch-Setup nicht über `ha-bosch-ebike`
läuft (z.B. mit eigenen Template-Sensoren). Empfohlen ist trotzdem die
Kombination, weil dort `last_tour_date`, `due_maintenance_count` und
`next_maintenance_label` ohne Eigenbau bereitgestellt werden.

## Hardware

- Display: **Guition JC4827W543** mit ESP32-S3 (16 MB Flash, PSRAM)
  - 480 × 272 NV3041A QSPI (intern; LVGL rotiert auf 272 × 480 Hochformat)
- Stromversorgung: USB-C, 5 V / 1 A reicht
- Optional Gehäuse 3D-gedruckt

## Lizenz

MIT (siehe `LICENSE`).
