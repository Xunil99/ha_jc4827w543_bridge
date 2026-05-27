"""Constants for the JC4827W543 eBike Cockpit integration."""

DOMAIN = "jc4827w543_bridge"

CONF_DEVICE_NAME = "device_name"

# Setup-Hinweis im Config-Flow. Wird via {hint}-Platzhalter in der
# Translation-Datei angezeigt.
SETUP_HINT = (
    "Trage den ESPHome-Device-Namen Deines JC4827W543 ein "
    "(z.B. 'ebike-cockpit'). Dieser muss mit dem 'name:'-Eintrag "
    "in der ESPHome-YAML uebereinstimmen."
)
