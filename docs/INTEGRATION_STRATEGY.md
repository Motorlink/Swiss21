# Integrationsstrategie: Abisco → Swiss21 → ABA Ninja → E-Mail mit QR-Code

## Projektziel

Entwicklung einer vollautomatischen Integration, die Rechnungen aus **Abisco** über **Swiss21** an **ABA Ninja** überträgt und anschließend per E-Mail mit **QR-Code** und **Direktzahlungslinks** (Twint, etc.) an Kunden versendet.

## Systemübersicht

### Beteiligte Systeme

1. **Abisco 8.8** (ByteRider)
   - Warenwirtschaftssystem für Kfz-Teile-Handel, technischen Großhandel
   - Webisco-Schnittstelle (Port 8228, XML über HTTP-POST)
   - Erstellt Rechnungen und Aufträge

2. **Swiss21** (Middleware/Integration Layer)
   - Python-basierte Integration
   - Empfängt Daten von Abisco via Webisco
   - Kommuniziert mit ABA Ninja API
   - Generiert QR-Codes
   - Versendet E-Mails

3. **ABA Ninja** (ABACUS Research AG)
   - Cloud-basiertes ERP-System
   - REST API für Rechnungsverwaltung
   - Dokumentenverwaltung

## Datenfluss

```
┌─────────────┐
│   Abisco    │
│  (Rechnung  │
│  erstellen) │
└──────┬──────┘
       │
       │ Webisco XML
       │ (HTTP-POST Port 8228)
       │
       ▼
┌──────────────────┐
│     Swiss21      │
│  (Middleware)    │
│                  │
│  1. Empfang      │
│  2. Validierung  │
│  3. Transformation│
└──────┬───────────┘
       │
       │ ABA Ninja API
       │ (REST/JSON)
       │
       ▼
┌──────────────────┐
│   ABA Ninja      │
│  (Rechnung       │
│   speichern)     │
└──────┬───────────┘
       │
       │ Rechnungsdaten
       │
       ▼
┌──────────────────┐
│     Swiss21      │
│                  │
│  1. QR-Code      │
│     generieren   │
│  2. PDF erstellen│
│  3. E-Mail       │
│     vorbereiten  │
└──────┬───────────┘
       │
       │ SMTP/E-Mail
       │
       ▼
┌──────────────────┐
│      Kunde       │
│                  │
│  - Rechnung PDF  │
│  - QR-Code       │
│  - Twint-Link    │
│  - Zahlungslink  │
└──────────────────┘
```

## Technische Architektur

### Modul 1: Webisco-Connector (`src/connectors/webisco.py`)

**Aufgabe**: Empfang von Auftragsdaten aus Abisco

**Funktionen**:
- HTTP-Server auf Port 8228 (oder konfigurierbar)
- XML-Parsing von Webisco-Requests
- Validierung der Envelope-Struktur
- Extraktion von Auftragsdaten
- Transformation in internes Datenformat

**Eingabeformat**: Webisco XML
```xml
<webisco version="21" username="..." password="..." type="request">
  <content>
    <auftrag>
      <typ>bestellung</typ>
      <position>...</position>
      <rechnungsadresse>
        <email>kunde@example.com</email>
        ...
      </rechnungsadresse>
      ...
    </auftrag>
  </content>
</webisco>
```

**Ausgabeformat**: Python Dictionary
```python
{
    'order_type': 'bestellung',
    'customer': {
        'email': 'kunde@example.com',
        'name': '...',
        'address': {...}
    },
    'positions': [...],
    'total': 1234.56,
    ...
}
```

### Modul 2: ABA Ninja Invoice Creator (`src/endpoints/invoices.py`)

**Aufgabe**: Erstellung von Rechnungen in ABA Ninja

**Funktionen**:
- Transformation von Abisco-Auftragsdaten zu ABA Ninja Invoice-Format
- API-Call zu ABA Ninja `/accounts/{accountUuid}/documents/invoices`
- Fehlerbehandlung und Retry-Logik
- Rückgabe der erstellten Rechnungs-UUID

**API-Endpoint**: `POST /accounts/{accountUuid}/documents/v2/invoices`

**Eingabeformat**: ABA Ninja Invoice JSON
```json
{
  "type": "invoice",
  "customer_uuid": "...",
  "positions": [
    {
      "article_id": "...",
      "quantity": 1,
      "price": 100.00
    }
  ],
  "payment_terms": 30,
  ...
}
```

**Ausgabeformat**: Invoice UUID + Rechnungsnummer

### Modul 3: QR-Code Generator (`src/utils/qr_code.py`)

**Aufgabe**: Generierung von Schweizer QR-Rechnungen (QR-Code nach Swiss QR-Bill Standard)

**Funktionen**:
- Generierung von Swiss QR-Bill kompatiblen QR-Codes
- Einbettung von:
  - IBAN
  - Betrag
  - Währung (CHF/EUR)
  - Rechnungsnummer
  - Kundeninformationen
  - Zahlungsreferenz
- Export als PNG/SVG

**Standard**: ISO 20022 (Swiss QR-Bill)

**Bibliothek**: `qrcode` + `segno` (für Swiss QR-Bill)

### Modul 4: Payment Link Generator (`src/utils/payment_links.py`)

**Aufgabe**: Generierung von Direktzahlungslinks

**Funktionen**:
- **Twint**: Generierung von Twint-Payment-Links
- **Kreditkarte**: Integration mit Payment-Gateway (Stripe, PayPal, etc.)
- **E-Banking**: Generierung von E-Banking-Links

**Twint-Link-Format**:
```
twint://pay?iban=CH...&amount=123.45&currency=CHF&reference=...
```

### Modul 5: Email Sender (`src/utils/email_sender.py`)

**Aufgabe**: Versand von Rechnungen per E-Mail

**Funktionen**:
- SMTP-Konfiguration
- HTML-E-Mail-Templates
- Anhänge (PDF-Rechnung)
- Eingebettete QR-Codes
- Zahlungslinks im E-Mail-Body
- Fehlerbehandlung und Logging

**E-Mail-Struktur**:
- **Betreff**: "Ihre Rechnung Nr. {invoice_number}"
- **Body**: HTML mit Zahlungsinformationen, QR-Code, Links
- **Anhang**: PDF-Rechnung

### Modul 6: PDF Generator (`src/utils/pdf_generator.py`)

**Aufgabe**: Generierung von PDF-Rechnungen

**Funktionen**:
- Erstellung von professionellen Rechnungs-PDFs
- Einbettung von QR-Codes
- Firmenlogo
- Rechnungspositionen
- Zahlungsinformationen

**Bibliothek**: `reportlab` oder `weasyprint`

## Datenmodelle

### Invoice Model (`src/models/invoice.py`)

```python
class Invoice:
    invoice_number: str
    invoice_date: date
    due_date: date
    customer: Customer
    positions: List[InvoicePosition]
    subtotal: Decimal
    tax: Decimal
    total: Decimal
    currency: str = "CHF"
    payment_reference: str
    iban: str
    
class Customer:
    name: str
    email: str
    address: Address
    
class InvoicePosition:
    article_id: str
    description: str
    quantity: Decimal
    unit_price: Decimal
    tax_rate: Decimal
    total: Decimal
```

## Konfiguration

### Umgebungsvariablen

```bash
# Webisco
WEBISCO_HOST=0.0.0.0
WEBISCO_PORT=8228
WEBISCO_ADMIN_ID=your_admin_id

# ABA Ninja
ABANINJA_API_TOKEN=your_jwt_token
ABANINJA_ACCOUNT_UUID=your_account_uuid
ABANINJA_API_BASE_URL=https://api.abaninja.ch

# Payment
IBAN=CH9300762011623852957
PAYMENT_GATEWAY_API_KEY=...
TWINT_MERCHANT_ID=...

# Email
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_email@gmail.com
SMTP_PASSWORD=your_password
EMAIL_FROM=rechnungen@yourcompany.ch

# PDF
COMPANY_NAME=Your Company GmbH
COMPANY_LOGO=/path/to/logo.png
```

## Implementierungsschritte

### Phase 1: Webisco-Connector
1. HTTP-Server für Webisco-Anfragen
2. XML-Parser für Webisco-Envelope
3. Datenextraktion und Validierung
4. Unit-Tests

### Phase 2: ABA Ninja Invoice Integration
1. Invoice-Endpoint in `src/endpoints/invoices.py`
2. Datentransformation Abisco → ABA Ninja
3. API-Integration mit Fehlerbehandlung
4. Unit-Tests

### Phase 3: QR-Code und Payment Links
1. Swiss QR-Bill Generator
2. Twint-Link-Generator
3. Payment-Gateway-Integration
4. Unit-Tests

### Phase 4: PDF und E-Mail
1. PDF-Generator mit Template
2. E-Mail-Sender mit SMTP
3. HTML-E-Mail-Template
4. Unit-Tests

### Phase 5: End-to-End Integration
1. Workflow-Orchestrierung
2. Logging und Monitoring
3. Fehlerbehandlung
4. Integration-Tests

### Phase 6: Deployment und Dokumentation
1. Docker-Container
2. Deployment-Anleitung
3. API-Dokumentation
4. Benutzerhandbuch

## Sicherheitsüberlegungen

1. **Authentifizierung**:
   - Webisco: Admin-ID oder Username/Password
   - ABA Ninja: JWT Bearer Token
   - SMTP: TLS/SSL

2. **Datenvalidierung**:
   - XML-Schema-Validierung
   - E-Mail-Adress-Validierung
   - IBAN-Validierung

3. **Fehlerbehandlung**:
   - Retry-Logik bei API-Fehlern
   - Logging aller Transaktionen
   - Fehler-Benachrichtigungen

4. **Datenschutz**:
   - Keine Speicherung von Passwörtern
   - Verschlüsselte Übertragung (HTTPS/TLS)
   - DSGVO-konforme Datenverarbeitung

## Technologie-Stack

- **Python**: 3.11+
- **Web-Framework**: Flask oder FastAPI (für Webisco HTTP-Server)
- **HTTP-Client**: requests
- **XML-Parsing**: xml.etree.ElementTree oder lxml
- **QR-Code**: qrcode, segno (Swiss QR-Bill)
- **PDF**: reportlab oder weasyprint
- **E-Mail**: smtplib, email
- **Testing**: pytest
- **Logging**: logging, structlog

## Nächste Schritte

1. ✅ Analyse der Schnittstellenbeschreibungen (abgeschlossen)
2. ⏳ Implementierung des Webisco-Connectors
3. ⏳ Implementierung des Invoice-Endpoints
4. ⏳ Implementierung der QR-Code-Generierung
5. ⏳ Implementierung des E-Mail-Versands
6. ⏳ End-to-End-Tests
7. ⏳ Dokumentation und Deployment
