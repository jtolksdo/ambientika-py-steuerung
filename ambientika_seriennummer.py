import asyncio
from init import authenticate

# Zugangsdaten aus `config.py` importieren
try:
    from config import USERNAME, PASSWORD
except ImportError:
    print("❌ Fehler: config.py konnte nicht geladen werden!")
    exit(1)

async def main():
    print("🔄 Starte Authentifizierung...")

    # Authentifizierung
    ambientika = await authenticate(USERNAME, PASSWORD)
    if not ambientika:
        print("❌ Fehler bei der Authentifizierung")
        return

    print("✅ Authentifizierung erfolgreich!")

    # Abruf der Häuser
    houses = await ambientika.houses()
    if not houses:
        print("❌ Keine Häuser gefunden")
        return

    print(f"🏠 Gefundene Häuser: {len(houses)}")

    # Hole vollständige Hausinformationen
    for house in houses:
        print(f"📡 Abruf der vollständigen Infos für Haus '{house.name}'...")
        house_info = await ambientika.house_complete_info(house.id)

        if not house_info:
            print(f"⚠️ Keine Daten für Haus '{house.name}' erhalten!")
            continue

        # Durchsuche Räume und Geräte
        print(f"🏡 Haus: {house_info.name} (Adresse: {house_info.address})")

        for room in house_info.rooms:
            print(f"  🏠 Raum: {room.name}")

            for device in room.devices:
                print(f"    🔌 Gerät: {device.name}, Seriennummer: {device.serial_number}")

if __name__ == "__main__":
    asyncio.run(main())