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

    # Debug: Prüfe, ob das `ambientika`-Objekt eine API-Verbindung enthält
    if not hasattr(ambientika, "api"):
        print("❌ ERROR: 'ambientika' enthält keine API-Instanz! Debug:", ambientika)
        return

    # Versuche, die Häuser abzurufen
    try:
        print("📡 Abruf der Häuserdaten...")

        # **WICHTIG:** Debugging - API-Rohantwort vor der Verarbeitung ausgeben
        raw_response = await ambientika.api.get("house/houses-info")
        print("🔍 API-Rohantwort:", raw_response)  # Hier siehst du, was die API zurückgibt

        if not raw_response:
            print("⚠️ WARNUNG: API gibt keine Daten zurück.")
            return

        # Überprüfe, ob die Antwort die erwarteten Daten enthält
        if isinstance(raw_response, dict) and "houses" not in raw_response:
            print("❌ Fehler: 'houses' fehlt in der API-Antwort!")
            return

        # Häuser-Array auslesen
        houses = raw_response.get("houses", [])

        print(f"🏠 Anzahl der gefundenen Häuser: {len(houses)}")

        # Detaillierte Ausgabe der Häuser und Geräte
        for house in houses:
            print(f"🏡 Haus: {house.get('name', 'Unbekannt')}, Adresse: {house.get('address', 'Keine Adresse')}")

            for room in house.get("rooms", []):
                print(f"  🏠 Raum: {room.get('name', 'Unbekannter Raum')}")

                for device in room.get("devices", []):
                    print(f"    🔌 Gerät: {device.get('name', 'Unbekannt')}, Seriennummer: {device.get('serialNumber', 'Keine SN')}")

    except AttributeError as e:
        print("❌ Fehler beim Zugriff auf 'houses':", str(e))
        print("🔍 Debugging: Die API-Antwort könnte fehlerhaft sein!")

    except Exception as e:
        print("❌ Unerwarteter Fehler:", str(e))

# Hauptfunktion ausführen
if __name__ == "__main__":
    asyncio.run(main())