import asyncio
from init import authenticate

# Deine Zugangsdaten
username = 'AMBIENTIKA_USERNAME_EMAIL_HIER_HIN'
password = 'DEINPASSWORT'

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

    # Informationen über die Geräte in allen Häusern abrufen
    for house in houses:
        print(f"Haus: {house.name}, Adresse: {house.address}")
        for room in house.rooms:
            print(f"  Raum: {room.name}")
            for device in room.devices:
                print(f"    Gerät: {device.name}, Seriennummer: {device.serial_number}")

# Hauptfunktion ausführen
if __name__ == "__main__":
    asyncio.run(main())
