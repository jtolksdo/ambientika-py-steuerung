import asyncio
import os
import aiohttp

# Zugangsdaten aus `config.py` importieren
try:
    from config import USERNAME, PASSWORD
    print("✅ Zugangsdaten erfolgreich aus config.py geladen!")
except ImportError as e:
    print(f"❌ Fehler: config.py konnte nicht geladen werden! {e}")
    exit(1)

# Prüfen, ob `init.py` existiert
init_path = "init.py"
if not os.path.exists(init_path):
    print(f"❌ Fehler: Die Datei {init_path} wurde nicht gefunden!")
    exit(1)

print(f"✅ Die Datei {init_path} wurde gefunden. Versuche, sie zu importieren...")

try:
    from init import authenticate, Ambientika
    print("✅ Erfolgreich: init.py wurde importiert!")
except ImportError as e:
    print(f"❌ Fehler beim Import von init.py: {e}")
    exit(1)

async def main():
    print("🔄 Starte Authentifizierung...")

    try:
        ambientika = await authenticate(USERNAME, PASSWORD)
    except Exception as e:
        print(f"❌ Fehler beim Aufruf von authenticate(): {e}")
        return

    print("🔍 Debug: Inhalt von `ambientika`:", repr(ambientika))

    if not isinstance(ambientika, Ambientika):
        print("❌ `ambientika` ist kein `Ambientika`-Objekt! Tatsächlicher Typ:", type(ambientika))
        return

    print("✅ `ambientika` ist ein gültiges `Ambientika`-Objekt!")
    
    if not hasattr(ambientika, "api"):
        print("❌ `ambientika` hat keine `api`-Instanz!")
        return

    print("✅ `ambientika` enthält eine API-Instanz!")

    # Abruf der Hausübersicht
    print("📡 Abruf der Häuserdaten...")
    try:
        houses = await ambientika.houses()
        if not houses:
            print("❌ Keine Häuser gefunden.")
            return
        print(f"🏠 Gefundene Häuser: {len(houses)}")
    except Exception as e:
        print(f"❌ Fehler beim Abruf der Häuser: {e}")
        return

    # Durchlaufe ALLE gefundenen Häuser
    for house in houses:
        print(f"\n🏡 **Haus:** {house.name} (ID: {house.id})")

        try:
            house_info = await ambientika.house_complete_info(house.id)
            if not house_info:
                print(f"❌ Keine vollständigen Informationen für Haus '{house.name}' erhalten!")
                continue
        except Exception as e:
            print(f"❌ Fehler beim Abruf der vollständigen Hausinformationen für {house.name}: {e}")
            continue

        # Durchsuche Räume und Geräte
        for room in house_info.rooms:
            print(f"  🏠 **Raum:** {room.name}")

            for device in room.devices:
                print(f"    🔌 **Gerät:** {device.name}")
                print(f"       📌 **Seriennummer:** {device.serial_number}")

if __name__ == "__main__":
    asyncio.run(main())