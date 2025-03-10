import asyncio
import aiohttp
from init import authenticate
# Deine Zugangsdaten (niemals in Klartext posten!)
username = "dein user hier"
password = "dein passwort hier"

async def authenticate(username: str, password: str, host: str = "https://app.ambientika.eu:4521"):
    login_data = {
        'username': username,
        'password': password
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url=f"{host}/users/authenticate", json=login_data) as response:
            print("Login Response Code:", response.status)

            try:
                response_data = await response.json()
                print("Login Response Data:", response_data)
            except Exception as e:
                print("Fehler beim Parsen der Antwort:", e)
                return None

            if response.status == 200 and "jwtToken" in response_data:
                return response_data  # Gibt das Token zurück
            else:
                print("Fehler bei der Authentifizierung")
                return None

# Testen des Skripts
async def main():
    token = await authenticate(username, password)
    if token:
        print("Erfolgreich eingeloggt:", token["jwtToken"])
    else:
        print("Login fehlgeschlagen.")

# Ausführen des Skripts
asyncio.run(main())