import asyncio
import os
import aiohttp

# Zugangsdaten aus externer Datei `config.py` importieren
try:
    from config import USERNAME, PASSWORD
    print("✅ Zugangsdaten erfolgreich aus config.py geladen!")
except ImportError as e:
    print(f"❌ Fehler: config.py konnte nicht geladen werden! {e}")
    exit(1)

# Prüfen, ob init.py existiert
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

    if hasattr(ambientika, "unwrap"):  # Falls `Success`-Wrapper genutzt wird
        print("✅ `ambientika` ist ein `Success`-Objekt!")

        try:
            actual_ambientika = ambientika.unwrap()  # Extrahiere echtes `Ambientika`-Objekt
            print("🔍 Extracted `ambientika.unwrap()`: ", repr(actual_ambientika))

            # Zeige ALLE Attribute des `Ambientika`-Objekts
            print("🔍 Attribute von `ambientika.unwrap()`: ", dir(actual_ambientika))

            if hasattr(actual_ambientika, "api"):
                print("✅ `ambientika.unwrap()` enthält eine API-Instanz!")

                # Teste eine API-Anfrage
                print("📡 Abruf der Häuserdaten...")
                raw_response = await actual_ambientika.api.get("house/houses-info")
                print("🔍 API-Rohantwort:", raw_response)

            else:
                print("❌ `ambientika.unwrap()` hat keine `api`-Instanz!")

        except Exception as e:
            print(f"❌ Fehler beim Extrahieren von `ambientika.unwrap()`: {e}")

    else:
        print("❌ `ambientika` ist kein `Success`-Objekt! Tatsächlicher Typ:", type(ambientika))
        print("🔍 Rohdaten von `ambientika`:", repr(ambientika))

if __name__ == "__main__":
    asyncio.run(main())