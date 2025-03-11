import asyncio
import os
import aiohttp

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

# Deine Zugangsdaten
USERNAME = "AMBIENTIKA_USERNAME_EMAIL_HIER_HIN"
PASSWORD = "DEINPASSWORT"

async def main():
    print("🔄 Starte Authentifizierung...")

    try:
        ambientika = await authenticate(USERNAME, PASSWORD)
    except Exception as e:
        print(f"❌ Fehler beim Aufruf von authenticate(): {e}")
        return

    print("🔍 Debug: Inhalt von 'ambientika':", ambientika)

    if not ambientika:
        print("❌ Fehler bei der Authentifizierung - API gibt None zurück.")
        return

    # Prüfe, ob ambientika ein Ambientika-Objekt ist
    if not isinstance(ambientika, Ambientika):
        print("❌ ERROR: 'ambientika' ist kein gültiges Ambientika-Objekt! Debug:", type(ambientika))
        return

    if not hasattr(ambientika, "api"):
        print("❌ ERROR: 'ambientika' enthält keine API-Instanz!")
        return

    print("✅ Authentifizierung erfolgreich!")

    # Debugging: API-Endpunkt testen
    print("📡 Abruf der Häuserdaten...")
    try:
        raw_response = await ambientika.api.get("house/houses-info")
        print("🔍 API-Rohantwort:", raw_response)
    except Exception as e:
        print(f"❌ Fehler beim Abruf der Häuser: {e}")

if __name__ == "__main__":
    asyncio.run(main())
    