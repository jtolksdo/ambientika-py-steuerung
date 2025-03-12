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

    # ✅ `ambientika` ist bereits ein `Ambientika`-Objekt, keine `unwrap()` nötig!
    if isinstance(ambientika, Ambientika):
        print("✅ `ambientika` ist ein gültiges `Ambientika`-Objekt!")

        # Zeige ALLE Attribute des `Ambientika`-Objekts
        print("🔍 Attribute von `ambientika`: ", dir(ambientika))

        if hasattr(ambientika, "api"):
            print("✅ `ambientika` enthält eine API-Instanz!")

            # Teste eine API-Anfrage
            print("📡 Abruf der Häuserdaten...")
            try:
                raw_response = await ambientika.api.get("house/houses-info")
                print("🔍 API-Rohantwort:", raw_response)
            except Exception as e:
                print(f"❌ Fehler beim Abruf der Häuser: {e}")

        else:
            print("❌ `ambientika` hat keine `api`-Instanz!")

    else:
        print("❌ `ambientika` ist kein `Ambientika`-Objekt! Tatsächlicher Typ:", type(ambientika))

if __name__ == "__main__":
    asyncio.run(main())