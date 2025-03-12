import asyncio
from init import authenticate, OperatingMode, FanSpeed, HumidityLevel

# Zugangsdaten aus `config.py` importieren
try:
    from config import USERNAME, PASSWORD
    print("✅ Zugangsdaten erfolgreich aus config.py geladen!")
except ImportError:
    print("❌ Fehler: config.py konnte nicht geladen werden! Stelle sicher, dass die Datei existiert.")
    exit(1)
device_serial_number = 'HIER-SERIENNUMMER' # Die Seriennummer bekommst Du mit dem Seriennummer python script heraus
# Neuer Modus für das Gerät - hier die Informationen entsprechend anpassen
NEW_MODE = {
    'operating_mode': OperatingMode.Off,  # Off-Modus
    'fan_speed': FanSpeed.Medium,  # Lüftergeschwindigkeit
    'humidity_level': HumidityLevel.Normal  # Feuchtigkeitsniveau
}

async def main():
    print("🔄 Starte Authentifizierung...")

    # Authentifiziere dich bei der Ambientika-API
    ambientika = await authenticate(USERNAME, PASSWORD)
    if not ambientika:
        print("❌ Fehler bei der Authentifizierung")
        return

    print("✅ Authentifizierung erfolgreich!")

    # Informationen über alle Häuser abrufen
    houses = await ambientika.houses()
    if not houses:
        print("❌ Keine Häuser gefunden")
        return

    print(f"🏠 Gefundene Häuser: {len(houses)}")

    # Suche nach dem Gerät mit der angegebenen Seriennummer
    device_found = False
    for house in houses:
        print(f"🏡 Haus: {house.name}")
        for room in house.rooms:
            print(f"  🏠 Raum: {room.name}")
            for device in room.devices:
                print(f"    🔍 Prüfe Gerät: {device.name} (Seriennummer: {device.serial_number})")

                if device.serial_number == DEVICE_SERIAL_NUMBER:
                    print(f"✅ Gerät '{device.name}' mit Seriennummer {DEVICE_SERIAL_NUMBER} gefunden!")

                    # Setze den neuen Modus
                    success = await device.change_mode(NEW_MODE)
                    if success:
                        print(f"✅ Modus für Gerät {device.name} erfolgreich geändert!")
                    else:
                        print(f"❌ Fehler beim Ändern des Modus für Gerät {device.name}")

                    device_found = True
                    break  # Gerät gefunden, daher Schleife beenden

    if not device_found:
        print(f"❌ Gerät mit Seriennummer {DEVICE_SERIAL_NUMBER} nicht gefunden!")

# Hauptfunktion ausführen
if __name__ == "__main__":
    asyncio.run(main())