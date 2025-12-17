"""
# Swiss21 - ABA Ninja API Referenz

Diese Dokumentation bietet eine detaillierte Referenz für den `AbaNinjaClient` und seine Module.

## `AbaNinjaClient`

Der Haupt-Client für die Interaktion mit der ABA Ninja API.

### Initialisierung

```python
from src.client import AbaNinjaClient

# Mit direkten Parametern
client = AbaNinjaClient(
    api_token="YOUR_JWT_TOKEN",
    account_uuid="YOUR_ACCOUNT_UUID"
)

# Mit einem Config-Objekt
from src.config import Config

config = Config(
    api_token="YOUR_JWT_TOKEN",
    account_uuid="YOUR_ACCOUNT_UUID"
)
client = AbaNinjaClient(config=config)
```

### Attribute

- `config`: Das `Config`-Objekt.
- `session`: Die `requests.Session`-Instanz.
- `addresses`: Der `AddressesEndpoint`-Handler.

### Methoden

- `get(endpoint, params)`: Führt einen GET-Request aus.
- `post(endpoint, data)`: Führt einen POST-Request aus.
- `patch(endpoint, data)`: Führt einen PATCH-Request aus.
- `delete(endpoint)`: Führt einen DELETE-Request aus.
- `get_paginated(endpoint, params, limit, auto_paginate)`: Führt einen GET-Request mit Pagination aus.

## `AddressesEndpoint`

Zugänglich über `client.addresses`.

### Methoden

#### `check_customer_number(customer_number, address_uuid)`
Prüft, ob eine Kundennummer verfügbar ist.

- **Args**:
  - `customer_number` (str): Die zu prüfende Kundennummer.
  - `address_uuid` (str, optional): Eine Adress-UUID, die bei der Prüfung ignoriert werden soll.
- **Returns**: `bool` - `True`, wenn verfügbar, sonst `False`.

#### `get_companies(page, limit, tags, auto_paginate)`
Ruft eine Liste von Unternehmensadressen ab.

- **Args**:
  - `page` (int, optional): Seitenzahl.
  - `limit` (int, optional): Anzahl der Ergebnisse pro Seite.
  - `tags` (list, optional): Liste von Tags zum Filtern.
  - `auto_paginate` (bool): Wenn `True`, werden alle Seiten abgerufen.
- **Returns**: `dict` - Die API-Antwort.

#### `get_company(company_uuid)`
Ruft ein einzelnes Unternehmen ab.

- **Args**: `company_uuid` (str): Die UUID des Unternehmens.
- **Returns**: `dict` - Die Unternehmensdaten.

#### `update_company(company_uuid, company_data)`
Aktualisiert ein Unternehmen.

- **Args**:
  - `company_uuid` (str): Die UUID des Unternehmens.
  - `company_data` (dict): Die zu aktualisierenden Daten.
- **Returns**: `dict` - Die aktualisierten Unternehmensdaten.

#### `delete_company(company_uuid)`
Löscht ein Unternehmen.

- **Args**: `company_uuid` (str): Die UUID des Unternehmens.
- **Returns**: `dict` - Die Bestätigung der Löschung.

#### `get_persons(...)` / `get_person(...)` / `update_person(...)` / `delete_person(...)`
Funktionen für Personenadressen, analog zu den Unternehmensfunktionen.

## Exceptions

Alle Exceptions erben von `AbaNinjaException`.

- `AuthenticationError`: 401 - Token abgelaufen oder ungültig.
- `AuthorizationError`: 403 - Keine Berechtigung.
- `NotFoundError`: 404 - Ressource nicht gefunden.
- `ConflictError`: 409 - Ressourcenkonflikt.
- `BadRequestError`: 400 - Ungültige Anfrage.
- `RateLimitError`: 429 - Rate-Limit überschritten.
- `ServerError`: 5xx - Serverfehler.
- `ValidationError`: Validierungsfehler auf Client-Seite.
- `ConfigurationError`: Konfigurationsfehler.
"""
