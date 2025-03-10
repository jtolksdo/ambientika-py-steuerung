import asyncio
import aiohttp
from init import authenticate

# Deine Zugangsdaten
USERNAME = "AMBIENTIKA_USERNAME_EMAIL_HIER_HIN"
PASSWORD = "DEINPASSWORT"

async def main():
    print("🔄 Starte Authentifizierung...")
    
    # Authentifiziere dich bei der Ambientika-API
    ambientika = await authenticate(USERNAME, PASSWORD)
    
    if not ambientika:
        print("❌ Fehler bei der Authentifizierung - API gibt None zurück.")
        return

    print("✅ Authentifizierung erfolgreich!")

    # Versuche, die Häuser abzurufen
    try:
        print("📡 Abruf der Häuserdaten...")
        houses = await ambientika.houses()
        
        # Debugging: API-Antwort ausgeben
        if not houses:
            print("⚠️ WARNUNG: Keine Häuser gefunden oder API-Antwort ist leer.")
            return

        print(f"🏠 Anzahl der gefundenen Häuser: {len(houses)}")

        # Detaillierte Ausgabe der Häuser und Geräte
        for house in houses:
            print(f"🏡 Haus: {house.name}, Adresse: {house.address}")

            for room in house.rooms:
                print(f"  🏠 Raum: {room.name}")

                for device in room.devices:
                    print(f"    🔌 Gerät: {device.name}, Seriennummer: {device.serial_number}")

    except AttributeError as e:
        print("❌ Fehler beim Zugriff auf 'houses':", str(e))
        print("🔍 Debugging: Die API-Antwort könnte fehlerhaft sein!")
        
        # Direkt die API-Antwort ausgeben
        response_data = await ambientika.api.get("house/houses-info")
        print("🔍 API-Rohdaten:", response_data)

    except Exception as e:
        print("❌ Unerwarteter Fehler:", str(e))

# Hauptfunktion ausführen
if __name__ == "__main__":
    asyncio.run(main())