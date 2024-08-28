import asyncio
from init import authenticate, OperatingMode, FanSpeed, HumidityLevel

# Deine Zugangsdaten
username = 'deinUserNameVonAmientika'
password = 'PASSWORT'

# Geräteinformationen und gewünschter Modus
device_serial_number = 'HIER-SERIENNUMMER' # Die Seriennummer bekommst Du mit dem Seriennummer python script heraus
new_mode = {
    'operating_mode': OperatingMode.Off,  # Off-Modus
    'fan_speed': FanSpeed.Medium,  # Lüftergeschwindigkeit
    'humidity_level': HumidityLevel.Normal  # Feuchtigkeitsniveau
}

async def main():
    # Authentifiziere dich bei der Ambientika-API
    ambientika = await authenticate(username, password)
    if not ambientika:
        print("Fehler bei der Authentifizierung")
        return

    # Informationen über alle Häuser abrufen
    houses = await ambientika.houses()
    if not houses:
        print("Keine Häuser gefunden")
        return

    # Suche nach dem Gerät in allen Häusern und Räumen
    for house in houses:
        for room in house.rooms:
            for device in room.devices:
                if device.serial_number == device_serial_number:
                    success = await device.change_mode(new_mode)
                    if success:
                        print(f"Modus für Gerät {device.name} erfolgreich geändert")
                    else:
                        print(f"Fehler beim Ändern des Modus für Gerät {device.name}")
                    return

    print(f"Gerät mit Seriennummer {device_serial_number} nicht gefunden")

# Hauptfunktion ausführen
if __name__ == "__main__":
    asyncio.run(main())
