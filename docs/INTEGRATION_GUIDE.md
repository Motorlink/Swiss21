"""
# Swiss21 - ABA Ninja API Integrationsleitfaden

Dieser Leitfaden beschreibt, wie die **Swiss21**-Integration in einem Python-Projekt eingerichtet und verwendet wird.

## 1. Installation

Stellen Sie sicher, dass Python 3.8+ installiert ist. Klonen Sie das Repository und installieren Sie die Abhängigkeiten.

```bash
# 1. Repository klonen
git clone https://github.com/Motorlink/Swiss21.git
cd Swiss21

# 2. Virtuelle Umgebung erstellen (empfohlen)
python3 -m venv venv
source venv/bin/activate  # Für Linux/macOS
# venv\Scripts\activate    # Für Windows

# 3. Abhängigkeiten installieren
pip install -r requirements.txt
```

## 2. Konfiguration

Die Konfiguration kann auf drei Arten erfolgen: über eine Konfigurationsdatei, Umgebungsvariablen oder direkt im Code.

### Methode A: Konfigurationsdatei (empfohlen)

Dies ist die sicherste Methode für die Verwaltung von Anmeldeinformationen.

1.  Erstellen Sie eine Kopie der Beispiel-Konfigurationsdatei:

    ```bash
    cp config/config.example.json config/config.json
    ```

2.  Öffnen Sie `config/config.json` und fügen Sie Ihre ABA Ninja-Anmeldeinformationen ein:

    ```json
    {
      "api_base_url": "https://api.abaninja.ch",
      "api_token": "DEIN_JWT_TOKEN_HIER",
      "account_uuid": "DEINE_ACCOUNT_UUID_HIER",
      "timeout": 30,
      "max_retries": 3
    }
    ```

3.  Laden Sie die Konfiguration in Ihrem Code:

    ```python
    from src.config import Config
    from src.client import AbaNinjaClient

    config = Config.from_file('config/config.json')
    client = AbaNinjaClient(config=config)
    ```

### Methode B: Umgebungsvariablen

Setzen Sie die folgenden Umgebungsvariablen:

```bash
export ABANINJA_API_TOKEN="DEIN_JWT_TOKEN"
export ABANINJA_ACCOUNT_UUID="DEINE_ACCOUNT_UUID"
```

Laden Sie die Konfiguration aus der Umgebung:

```python
from src.config import Config
from src.client import AbaNinjaClient

config = Config.from_env()
client = AbaNinjaClient(config=config)
```

### Methode C: Direkte Initialisierung

Für schnelle Tests können Sie den Client direkt mit Ihren Anmeldeinformationen initialisieren. **Vermeiden Sie dies in der Produktion.**

```python
from src.client import AbaNinjaClient

client = AbaNinjaClient(
    api_token="DEIN_JWT_TOKEN",
    account_uuid="DEINE_ACCOUNT_UUID"
)
```

## 3. Verwendung des Clients

Nach der Initialisierung des Clients können Sie auf die verschiedenen API-Endpunkte zugreifen.

### Adressen verwalten (`client.addresses`)

Der `AddressesEndpoint` bietet Funktionen zur Verwaltung von Unternehmens- und Personenadressen.

#### Unternehmensadressen abrufen

```python
# Alle Unternehmen mit automatischer Paginierung abrufen
all_companies = client.addresses.get_companies(auto_paginate=True)
print(f"Insgesamt {all_companies['meta']['total']} Unternehmen gefunden.")

# Eine einzelne Seite mit Unternehmen abrufen
companies_page = client.addresses.get_companies(page=1, limit=20)
for company in companies_page['data']:
    print(company['name'])
```

#### Ein einzelnes Unternehmen aktualisieren

```python
company_uuid = "..."
update_data = {
    "name": "Neuer Firmenname",
    "private_notes": "Wichtiger Kunde."
}

updated_company = client.addresses.update_company(company_uuid, update_data)
print(f"Unternehmen aktualisiert: {updated_company['data']['name']}")
```

### Fehlerbehandlung

Die Bibliothek löst spezifische Ausnahmen für verschiedene API-Fehler aus. Fangen Sie diese immer in Ihrem Code ab.

```python
from src.exceptions import AbaNinjaException, NotFoundError

try:
    # Versuchen, ein nicht existierendes Unternehmen abzurufen
    client.addresses.get_company("invalid-uuid")
except NotFoundError as e:
    print(f"Fehler: {e.message}")
    # >> Fehler: Resource not found.
except AbaNinjaException as e:
    print(f"Ein API-Fehler ist aufgetreten: {e.message}")
```

## 4. Ausführen der Beispiele

Das `examples`-Verzeichnis enthält Skripte, die die Verwendung der Bibliothek demonstrieren.

1.  Stellen Sie sicher, dass Sie Ihre Anmeldeinformationen in `examples/basic_usage.py` (oder über eine Konfigurationsdatei) eingefügt haben.

2.  Führen Sie das Beispielskript aus:

    ```bash
    python examples/basic_usage.py
    ```

Dieser Leitfaden bietet einen grundlegenden Überblick. Für eine vollständige Liste aller verfügbaren Methoden und Parameter lesen Sie bitte die [API-Referenz](API_REFERENCE.md).
"""
