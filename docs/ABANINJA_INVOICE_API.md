# ABA Ninja Invoice API - Vollständige Analyse

## Übersicht

Die ABA Ninja API bietet umfassende Endpoints für die Verwaltung von Rechnungen (Invoices). Diese Dokumentation beschreibt die relevanten Endpoints für die Swiss21-Integration.

## Basis-URL

```
https://api.abaninja.ch
```

## Authentifizierung

**Typ**: Bearer Token (JWT)

**Header**:
```
Authorization: Bearer YOUR_JWT_TOKEN
```

## Invoice Endpoints

### 1. Liste aller Rechnungen abrufen

**Endpoint**: `GET /accounts/{accountUuid}/documents/v2/invoices`

**Beschreibung**: Liefert eine Liste aller Rechnungen für einen Account

**Parameter**:
- `accountUuid` (required): UUID des Accounts
- `page` (optional): Seitennummer für Pagination
- `limit` (optional): Anzahl der Ergebnisse pro Seite

**Response** (200):
```json
{
  "status": 0,
  "message": "string",
  "data": [
    {
      "uuid": "string",
      "invoice_number": "string",
      "invoice_date": "2024-01-01",
      "due_date": "2024-01-31",
      "customer": {},
      "positions": [],
      "total": 0,
      "currency": "CHF"
    }
  ]
}
```

### 2. Rechnung erstellen (CREATE INVOICE) ⭐

**Endpoint**: `POST /accounts/{accountUuid}/documents/v2/invoices`

**Beschreibung**: Erstellt eine neue Rechnung in ABA Ninja

**Parameter**:
- `accountUuid` (required): UUID des Accounts

**Request Body**:
```json
{
  "documents": [
    {
      "type": "invoice",
      "customer_uuid": "095be615-a8ad-4c33-8e9c-c7612fbf6c9f",
      "invoice_date": "2024-01-01",
      "due_date": "2024-01-31",
      "currency_code": "CHF",
      "language": "de",
      "positions": [
        {
          "article_uuid": "string",
          "description": "string",
          "quantity": 1.0,
          "unit_price": 100.00,
          "tax_rate": 7.7,
          "total": 100.00
        }
      ],
      "payment_terms": 30,
      "notes": "string",
      "private_notes": "string"
    }
  ]
}
```

**Response** (201 - Invoice created):
```json
{
  "status": 0,
  "message": "string",
  "data": {
    "uuid": "095be615-a8ad-4c33-8e9c-c7612fbf6c9f",
    "invoice_number": "RE-2024-0001",
    "invoice_date": "2024-01-01",
    "due_date": "2024-01-31",
    "total": 107.70,
    "currency_code": "CHF"
  }
}
```

**Response** (202 - Async Processing):
```json
{
  "status": 0,
  "message": "string",
  "data": {
    "processing": true
  }
}
```

**Response** (400 - Validation Error):
```json
{
  "error": "string",
  "error_description": "string"
}
```

### 3. Einzelne Rechnung abrufen

**Endpoint**: `GET /accounts/{accountUuid}/documents/v2/invoices/{invoiceUuid}`

**Beschreibung**: Liefert Details zu einer spezifischen Rechnung

**Parameter**:
- `accountUuid` (required): UUID des Accounts
- `invoiceUuid` (required): UUID der Rechnung

**Response** (200):
```json
{
  "status": 0,
  "message": "string",
  "data": {
    "uuid": "095be615-a8ad-4c33-8e9c-c7612fbf6c9f",
    "invoice_number": "RE-2024-0001",
    "invoice_date": "2024-01-01",
    "due_date": "2024-01-31",
    "customer": {
      "uuid": "string",
      "name": "string",
      "email": "string"
    },
    "positions": [
      {
        "description": "string",
        "quantity": 1.0,
        "unit_price": 100.00,
        "tax_rate": 7.7,
        "total": 107.70
      }
    ],
    "subtotal": 100.00,
    "tax": 7.70,
    "total": 107.70,
    "currency_code": "CHF",
    "payment_terms": 30,
    "notes": "string"
  }
}
```

### 4. Rechnung aktualisieren

**Endpoint**: `PATCH /accounts/{accountUuid}/documents/v2/invoices/{invoiceUuid}`

**Beschreibung**: Aktualisiert eine bestehende Rechnung

**Parameter**:
- `accountUuid` (required): UUID des Accounts
- `invoiceUuid` (required): UUID der Rechnung

**Request Body**: Ähnlich wie bei CREATE, nur die zu ändernden Felder

### 5. Aktionen für eine Rechnung abrufen

**Endpoint**: `GET /accounts/{accountUuid}/documents/v2/invoices/{invoiceUuid}/actions`

**Beschreibung**: Liefert verfügbare Aktionen für eine Rechnung (z.B. "send", "mark_as_paid")

### 6. Aktion auf Rechnung ausführen

**Endpoint**: `PATCH /accounts/{accountUuid}/documents/v2/invoices/{invoiceUuid}/actions`

**Beschreibung**: Führt eine Aktion auf einer Rechnung aus (z.B. Rechnung versenden, als bezahlt markieren)

**Mögliche Aktionen**:
- `send` - Rechnung per E-Mail versenden
- `mark_as_paid` - Rechnung als bezahlt markieren
- `download_pdf` - PDF herunterladen

## Datenmodell: Invoice

### Hauptfelder

| Feld | Typ | Pflicht | Beschreibung |
|------|-----|---------|--------------|
| `type` | string | ✓ | Dokumenttyp: "invoice" |
| `customer_uuid` | string (uuid) | ✓ | UUID des Kunden (aus Addresses) |
| `invoice_date` | string (date) | ✓ | Rechnungsdatum (YYYY-MM-DD) |
| `due_date` | string (date) | | Fälligkeitsdatum (YYYY-MM-DD) |
| `currency_code` | string | | Währungscode (CHF, EUR, USD) |
| `language` | string | | Sprache (de, fr, it, en) |
| `payment_terms` | integer | | Zahlungsziel in Tagen (-1, 7, 10, 14, 15, 20, 30, 60, 90) |
| `notes` | string | | Öffentliche Notizen (sichtbar für Kunden) |
| `private_notes` | string | | Private Notizen (nur intern) |
| `positions` | array | ✓ | Array von Rechnungspositionen |

### Position-Felder

| Feld | Typ | Pflicht | Beschreibung |
|------|-----|---------|--------------|
| `article_uuid` | string (uuid) | | UUID des Artikels (aus Products) |
| `description` | string | ✓ | Beschreibung der Position |
| `quantity` | number | ✓ | Menge |
| `unit_price` | number | ✓ | Einzelpreis (netto) |
| `tax_rate` | number | | Steuersatz in Prozent (z.B. 7.7 für 7.7%) |
| `total` | number | | Gesamtbetrag der Position |
| `discount` | number | | Rabatt in Prozent |

## Wichtige Hinweise für die Integration

### 1. Kunden-UUID erforderlich

Bevor eine Rechnung erstellt werden kann, muss der Kunde in ABA Ninja existieren. Die `customer_uuid` muss aus dem Addresses-Endpoint abgerufen oder der Kunde muss zuerst erstellt werden.

**Workflow**:
1. Prüfe ob Kunde existiert (via E-Mail oder Kundennummer)
2. Falls nicht: Erstelle Kunde via `POST /accounts/{accountUuid}/addresses/v2/companies` oder `persons`
3. Verwende die zurückgegebene UUID für die Rechnung

### 2. Artikel-UUID optional

Positionen können entweder mit `article_uuid` (Verweis auf Produkt) oder nur mit `description` und `unit_price` erstellt werden.

### 3. Währung und Sprache

- **Währung**: Standard ist CHF, kann aber auf EUR, USD etc. gesetzt werden
- **Sprache**: Standard ist "de", verfügbar sind: de, fr, it, en

### 4. Zahlungsbedingungen

Zahlungsziel in Tagen:
- `-1`: Sofort fällig
- `7`, `10`, `14`, `15`, `20`, `30`, `60`, `90`: Tage bis Fälligkeit

### 5. Steuersätze (Schweiz)

- **7.7%**: Normalsatz (Standard)
- **2.5%**: Reduzierter Satz
- **0%**: Steuerfrei

### 6. Async Processing

Bei großen Rechnungen oder vielen Positionen kann die API mit Status 202 antworten, was bedeutet, dass die Verarbeitung asynchron erfolgt.

## Integration mit Abisco

### Mapping: Abisco → ABA Ninja

| Abisco (Webisco XML) | ABA Ninja API |
|----------------------|---------------|
| `<auftrag><typ>bestellung</typ>` | `type: "invoice"` |
| `<rechnungsadresse><email>` | Kunde-Lookup via E-Mail |
| `<position><artikelid>` | `article_uuid` (nach Mapping) |
| `<position><beschreibung>` | `description` |
| `<position><menge>` | `quantity` |
| `<position><einzelpreis_netto>` | `unit_price` |
| `<position><mwst>` | `tax_rate` |
| `<wunschlieferdatum>` | `due_date` |
| `<bemerkung>` | `notes` |

### Beispiel-Transformation

**Abisco XML**:
```xml
<auftrag>
  <typ>bestellung</typ>
  <position>
    <artikelid>12345</artikelid>
    <beschreibung>Bremsbeläge vorne</beschreibung>
    <menge>2</menge>
    <einzelpreis_netto>45.50</einzelpreis_netto>
    <mwst>7.7</mwst>
  </position>
  <rechnungsadresse>
    <name>Müller AG</name>
    <email>info@mueller-ag.ch</email>
  </rechnungsadresse>
</auftrag>
```

**ABA Ninja JSON**:
```json
{
  "documents": [
    {
      "type": "invoice",
      "customer_uuid": "...",
      "invoice_date": "2024-12-17",
      "currency_code": "CHF",
      "language": "de",
      "positions": [
        {
          "description": "Bremsbeläge vorne",
          "quantity": 2.0,
          "unit_price": 45.50,
          "tax_rate": 7.7,
          "total": 91.00
        }
      ],
      "payment_terms": 30
    }
  ]
}
```

## CSV-Import Alternative

Falls die direkte API-Integration nicht möglich ist, bietet ABA Ninja auch einen CSV-Import über die Weboberfläche. Die Struktur wäre:

```csv
customer_number,invoice_date,due_date,description,quantity,unit_price,tax_rate
"K-12345","2024-01-01","2024-01-31","Bremsbeläge vorne",2,45.50,7.7
```

**Hinweis**: Der CSV-Import ist weniger flexibel und erfordert manuelle Schritte. Die direkte API-Integration ist zu bevorzugen.

## Fehlerbehandlung

### Häufige Fehler

| Status | Fehler | Lösung |
|--------|--------|--------|
| 400 | Invalid customer_uuid | Kunde existiert nicht → Kunde zuerst erstellen |
| 400 | Invalid date format | Datum muss im Format YYYY-MM-DD sein |
| 400 | Missing required field | Pflichtfeld fehlt (customer_uuid, positions, etc.) |
| 401 | Access Token expired | Token erneuern |
| 403 | Client not allowed | API-Token hat keine Berechtigung |
| 500 | Unexpected error | Server-Fehler → Retry mit exponential backoff |

## Nächste Schritte für Swiss21

1. ✅ API-Endpoints identifiziert
2. ⏳ Invoice-Endpoint-Modul implementieren (`src/endpoints/invoices.py`)
3. ⏳ Kunden-Lookup und -Erstellung implementieren
4. ⏳ Abisco → ABA Ninja Datentransformation
5. ⏳ PDF-Download nach Rechnungserstellung
6. ⏳ QR-Code-Generierung
7. ⏳ E-Mail-Versand mit Rechnung + QR-Code
