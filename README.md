# Swiss21 - ABA Ninja API Integration

**Swiss21** ist eine professionelle Python-Integration für die ABA Ninja API, entwickelt für die nahtlose Anbindung von Geschäftsanwendungen an das ABA Ninja ERP-System.

## Projektübersicht

Dieses Projekt bietet eine vollständige, modulare und wartbare Integration mit der ABA Ninja API (Version 2.0.4). Die Implementierung folgt professionellen IT-Standards und der **Konus-Regel** für saubere, updatefähige Module.

## Hauptfunktionen

- **Authentifizierung**: Sichere JWT-basierte Authentifizierung mit Bearer Token
- **Adressverwaltung**: Verwaltung von Unternehmens- und Personenadressen
- **Dokumentenverwaltung**: Zugriff auf Angebote, Rechnungen, Lieferscheine, Gutschriften
- **Produktverwaltung**: Verwaltung von Produkten, Produktgruppen und Einheiten
- **Mitarbeiterverwaltung**: Zugriff auf Mitarbeiterdaten, Aktivitäten und Statistiken
- **Finanzverwaltung**: Bankkonten und Finanzdaten
- **Fehlerbehandlung**: Robuste Fehlerbehandlung mit detaillierten Fehlermeldungen
- **Pagination**: Automatische Behandlung von paginierten Responses

## Technologie-Stack

- **Sprache**: Python 3.11+
- **HTTP-Client**: requests
- **Authentifizierung**: JWT Bearer Token
- **API-Version**: ABA Ninja API 2.0.4
- **Lizenz**: MIT

## Projektstruktur

```
Swiss21/
├── README.md                 # Projektdokumentation
├── requirements.txt          # Python-Abhängigkeiten
├── .gitignore               # Git-Ignore-Datei
├── config/                  # Konfigurationsdateien
│   └── config.example.json  # Beispiel-Konfiguration
├── src/                     # Quellcode
│   ├── __init__.py
│   ├── client.py           # Haupt-API-Client
│   ├── auth.py             # Authentifizierung
│   ├── models/             # Datenmodelle
│   │   ├── __init__.py
│   │   ├── address.py      # Adressmodelle
│   │   ├── document.py     # Dokumentmodelle
│   │   └── product.py      # Produktmodelle
│   └── endpoints/          # API-Endpoints
│       ├── __init__.py
│       ├── addresses.py    # Adressen-Endpoints
│       ├── documents.py    # Dokument-Endpoints
│       └── products.py     # Produkt-Endpoints
├── examples/               # Beispiele
│   ├── basic_usage.py
│   ├── address_management.py
│   └── document_handling.py
├── tests/                  # Unit-Tests
│   ├── __init__.py
│   └── test_client.py
└── docs/                   # Dokumentation
    ├── API_REFERENCE.md    # API-Referenz
    └── INTEGRATION_GUIDE.md # Integrationsanleitung
```

## Installation

```bash
# Repository klonen
git clone https://github.com/Motorlink/Swiss21.git
cd Swiss21

# Virtuelle Umgebung erstellen
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# oder
venv\Scripts\activate  # Windows

# Abhängigkeiten installieren
pip install -r requirements.txt
```

## Konfiguration

1. Kopiere die Beispiel-Konfiguration:
```bash
cp config/config.example.json config/config.json
```

2. Füge deinen API-Token in `config/config.json` ein:
```json
{
  "api_base_url": "https://api.abaninja.ch",
  "api_token": "DEIN_JWT_TOKEN_HIER",
  "account_uuid": "DEINE_ACCOUNT_UUID"
}
```

## Schnellstart

```python
from src.client import AbaNinjaClient

# Client initialisieren
client = AbaNinjaClient(
    api_token="DEIN_JWT_TOKEN",
    account_uuid="DEINE_ACCOUNT_UUID"
)

# Alle Unternehmensadressen abrufen
companies = client.addresses.get_companies()
for company in companies:
    print(f"{company['name']} - {company['customer_number']}")

# Einzelnes Unternehmen abrufen
company = client.addresses.get_company(company_uuid="...")
print(company)
```

## Entwicklungsprinzipien

Dieses Projekt folgt der **Konus-Regel** und professionellen IT-Standards:

- **Modularität**: Jedes Modul ist unabhängig und updatefähig
- **Sauberer Code**: Keine unnötigen Abhängigkeiten
- **Fehlerbehandlung**: Robuste Fehlerbehandlung auf allen Ebenen
- **Dokumentation**: Vollständige Dokumentation aller Funktionen
- **Tests**: Umfassende Unit-Tests für alle Module

## API-Dokumentation

Die vollständige API-Dokumentation von ABA Ninja findest du unter:
https://www.abaninja.ch/apidocs/

## Lizenz

MIT License - siehe LICENSE Datei für Details

## Kontakt

**ABACUS Research AG**
- Email: info@abacus.ch
- Website: https://www.abacus.ch

## Version

**Version**: 1.0.0  
**API-Version**: ABA Ninja API 2.0.4  
**Letztes Update**: 2024
