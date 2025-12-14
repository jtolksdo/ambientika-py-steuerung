import asyncio
import os

# Zugangsdaten aus `config.py` importieren
try:
    from config import USERNAME, PASSWORD
    print("✅ Zugangsdaten erfolgreich aus config.py geladen!")
except ImportError as e:
    print(f"❌ Fehler: config.py konnte nicht geladen werden! {e}")
    raise SystemExit(1)

# Prüfen, ob `init.py` existiert
init_path = "init.py"
if not os.path.exists(init_path):
    print(f"❌ Fehler: Die Datei {init_path} wurde nicht gefunden!")
    raise SystemExit(1)

print(f"✅ Die Datei {init_path} wurde gefunden. Versuche, sie zu importieren...")

try:
    from init import authenticate
    print("✅ Erfolgreich: init.py wurde importiert!")
except ImportError as e:
    print(f"❌ Fehler beim Import von init.py: {e}")
    raise SystemExit(1)


def unwrap_if_needed(obj):
    """
    Unterstützt beide Varianten:
    - obj ist bereits Ambientika
    - obj ist returns.result.Success(Ambientika)
    """
    # returns.result.Success hat i.d.R. .unwrap()
    if hasattr(obj, "unwrap") and callable(getattr(obj, "unwrap")):
        try:
            return obj.unwrap()
        except Exception:
            # Manche returns-Versionen nutzen .value_or / .value_or_none
            pass

    # Alternative: value_or / value_or_none
    if hasattr(obj, "value_or") and callable(getattr(obj, "value_or")):
        try:
            return obj.value_or(None)
        except Exception:
            pass

    if hasattr(obj, "value_or_none") and callable(getattr(obj, "value_or_none")):
        try:
            return obj.value_or_none()
        except Exception:
            pass

    return obj


async def main():
    print("🔄 Starte Authentifizierung...")

    try:
        result = await authenticate(USERNAME, PASSWORD)
    except Exception as e:
        print(f"❌ Fehler beim Aufruf von authenticate(): {e}")
        return

    print("🔍 Debug: Inhalt von `authenticate()`:", repr(result))
    ambientika = unwrap_if_needed(result)

    print("🔍 Debug: nach unwrap_if_needed():", repr(ambientika))
    print("🔍 Typ:", type(ambientika))

    # Plausibilitätscheck: hat es die erwarteten Attribute?
    if not hasattr(ambientika, "api") or not hasattr(ambientika, "houses"):
        print("❌ Sieht nicht nach einem Ambientika-Objekt aus (api/houses fehlt).")
        print("➡️ Tipp: Du nutzt sehr wahrscheinlich eine init.py-Variante, die returns.Success/Failure nutzt.")
        return

    print("✅ Ambientika-Objekt sieht gültig aus (api & houses vorhanden).")

    # Häuser abrufen (API-Wrapper)
    try:
        houses = await ambientika.houses()
    except Exception as e:
        print(f"❌ Fehler beim Abruf der Häuser über ambientika.houses(): {e}")
        return

    if not houses:
        print("⚠️ Keine Häuser gefunden.")
        return

    print(f"🏠 Gefundene Häuser: {len(houses)}")

    # Für jedes Haus: komplette Infos ziehen und Geräte ausgeben
    for house in houses:
        # house kann je nach init.py bereits ein House-Objekt sein
        house_id = getattr(house, "id", None)
        house_name = getattr(house, "name", None)

        # Falls houses() nur houseId/houseName liefert, versuche Fallback
        if house_id is None and isinstance(house, dict):
            house_id = house.get("houseId")
            house_name = house.get("houseName")

        print(f"\n🏡 Haus: {house_name} (ID: {house_id})")

        if not hasattr(ambientika, "house_complete_info") or house_id is None:
            print("⚠️ house_complete_info nicht verfügbar oder house_id fehlt – überspringe Detailabruf.")
            continue

        try:
            house_info = await ambientika.house_complete_info(house_id)
        except Exception as e:
            print(f"❌ Fehler bei house_complete_info({house_id}): {e}")
            continue

        if not house_info:
            print("⚠️ house_complete_info lieferte None/leer.")
            continue

        # Räume / Geräte ausgeben
        rooms = getattr(house_info, "rooms", []) or []
        for room in rooms:
            print(f"  🏠 Raum: {room.name}")
            for device in room.devices:
                print(f"    🔌 Gerät: {device.name}")
                print(f"       📌 Seriennummer: {device.serial_number}")


if __name__ == "__main__":
    asyncio.run(main())