import asyncio
from init import authenticate

# Deine Zugangsdaten
username = 'AMBIENTIKA_USERNAME_EMAIL_HIER_HIN'
password = 'PASSWORT'

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

    # Das erste Haus auswählen
    house = houses[0]
    print(f"Haus: {house.name}, Adresse: {house.address}")

    # Informationen über die Geräte im Haus abrufen
    for room in house.rooms:
        print(f"Raum: {room.name}")
        for device in room.devices:
            status = await device.status()
            if status:
                print(f"Gerät: {device.name}, Temperatur: {status['temperature']}, Luftfeuchtigkeit: {status['humidity']}")
            else:
                print(f"Status für Gerät {device.name} konnte nicht abgerufen werden")

# Hauptfunktion ausführen
if __name__ == "__main__":
    asyncio.run(main())
    print("Script abgeschlossen")  # Füge dies hinzu, um sicherzustellen, dass das Skript abgeschlossen ist