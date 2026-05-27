# JC4827W543 eBike Cockpit Bridge

Ein Touch-Display im Hochformat (272 × 480) für den Flur oder die
Garage, das auf vier Seiten Bosch-eBike-Status, lokales Wetter,
Hausenergie (PV, Hausakku, E-Auto, Mülltermin) und einen MG4-Detail-
Bildschirm zusammenführt. Läuft auf dem **Guition JC4827W543**
(ESP32-S3, NV3041A QSPI 480 × 272, GT911 Touch) mit ESPHome 2026.5+
und LVGL.

Die Anzeige bezieht ihre Daten aus Home Assistant per ESPHome-Native-
API, ergänzt durch zwei Setup-freie Quellen direkt am ESP:

- **Open-Meteo** für aktuelle Wetterlage und 5-Tage-Forecast (kein
  API-Key, keine HA-Wetter-Entity nötig)
- **ESPHome `sun:`-Component** für Sonnenauf-/-untergang und
  automatisches Tag/Nacht-Backlight-Dimming aus den
  Heimatkoordinaten

## Seitenübersicht

| Seite | Inhalt | Aufruf |
|-------|--------|--------|
| 1 | eBike-Cockpit: Datum, Uhrzeit, Wetter, Sonnenauf-/-untergang, Bike-Name, Akku %, Akku-Bar, Letzte Tour, Wochen-km, Tage seit letzter Fahrt, Wartungs-Stand, Kilometerstand | Standard |
| 2 | 5-Tage-Wetter-Forecast (Tagesname, Icon, Max-/Min-Temperatur in farbcodiert nach Schwellen) | Wischen nach links |
| 3 | Hausenergie: PV-Leistung, Verbrauch, Hausakku (SoC + Bar + Lade-/Entlade-Leistung), MG4 (SoC + Bar + Lade-/Fahrtstatus + Steckdosen-Temperatur), nächster Müllabfuhrtermin | Zweimal nach links wischen |
| 4 | MG4-Detail: SoC groß, Kilometerstand, Restreichweite, Ladezeitende | Tap auf MG4-Sektion in Page 3 |

Swipe-Navigation zwischen Seite 1 / 2 / 3. Seite 4 ist nicht in der
Swipe-Sequenz, sondern nur per Tap aus Seite 3 zu erreichen und kehrt
auf jeden weiteren Tap zurück zu Seite 3.

## Hardware

- Display: **Guition JC4827W543** (ESP32-S3-WROOM-1, 8 MB Octal-PSRAM,
  16 MB Flash, 4,3 Zoll IPS QSPI mit NV3041A-Treiber, GT911-Touch)
- Stromversorgung: USB-C, 5 V / 1 A reicht
- Optional: 3D-gedrucktes Gehäuse

## Aufbau

```
ha_jc4827w543_bridge/
├── custom_components/jc4827w543_bridge/   # Home-Assistant-Integration
│   ├── __init__.py
│   ├── config_flow.py                     # Setup-Dialog (Device-Name)
│   ├── manifest.json
│   ├── const.py
│   └── translations/                      # en, de, nl, fr, it, es
└── esphome/
    ├── ebike-cockpit-base.yaml            # Hauptfirmware
    ├── ebike-cockpit-with-ldi.yaml        # Variante mit Bosch-LDI-Bridge
    └── README.md                          # Pinout + Template-Sensoren
```

## Schnellstart

1. **HA-Integration installieren**: `custom_components/jc4827w543_bridge/`
   nach `<HA-Config>/custom_components/` kopieren, HA neu starten,
   Integration über *Einstellungen → Geräte & Dienste → Integration
   hinzufügen → JC4827W543* einrichten. ESPHome-Device-Name eintragen.

2. **ESPHome-Firmware anpassen**: In `esphome/ebike-cockpit-base.yaml`
   die `substitutions:` am Anfang auf das eigene Setup anpassen:
   - `home_latitude` / `home_longitude` (Heimatkoordinaten)
   - `bike_name` (Anzeigename)
   - Alle `entity_*`-Substitutionen auf die eigenen HA-Entitäten
     umstellen. Sensoren, die nicht existieren, auf
     `sensor.dummy` zeigen — die betroffenen Felder bleiben dann leer.

3. **secrets.yaml** im `esphome/`-Ordner mit `wifi_ssid` und
   `wifi_password`.

4. **Flashen**: YAML in die ESPHome-Dashboard-Konfiguration ziehen oder
   via `esphome run` aufs Display schieben.

## Datenquellen

Pflicht (Bosch eBike):
- Akku-SoC, Ladestatus, Kilometerstand, Wartungsinfo

Empfehlung (für die Hausenergie-Seite):
- PV-Leistung (z. B. Shelly 1PM)
- Hausverbrauch (Gesamtstrom-Sensor)
- Hausakku (z. B. Marstek Venus per LiLyGO-RS485)
- E-Auto-Telemetrie (z. B. MG4 über die `mg-saic`-Integration)
- Müllabfuhr-Kalender (z. B. Awido)

Setup-frei (direkt am ESP):
- Wetter + 5-Tage-Forecast: Open-Meteo
- Sonnenauf-/-untergang: ESPHome sun:-Component aus Koordinaten

Welche HA-Template-Sensoren ggf. anzulegen sind (Tage seit letzter
Fahrt, Wochenkilometer), siehe `esphome/README.md`.

## Bezug zu `ha-bosch-ebike`

Die HA-Integration in diesem Repo ist eigenständig und nicht von
`ha-bosch-ebike` abhängig. Empfohlen ist die Kombination, weil
`ha-bosch-ebike` viele der erwarteten Sensoren bereits liefert.

Die ESPHome-Variante `ebike-cockpit-with-ldi.yaml` integriert das
External-Component `bosch_ebike_ldi` aus dem Schwester-Repo, womit
das Display Live-Akkudaten direkt per BLE vom Bosch Smart System
beziehen kann (auch ohne laufenden HA-Server).

## Lizenz

[MIT](LICENSE).

## Mitwirken

Dies ist primär ein persönliches Setup, das offen geteilt wird —
Pull Requests und Issues sind willkommen, insbesondere für Bug-Reports,
zusätzliche Übersetzungen oder Hardware-Varianten.
