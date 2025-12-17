# Swiss21 - Vollständige Projektstruktur

## Übersicht

Dieses Dokument beschreibt die vollständige Projektstruktur für die **Swiss21**-Integration zwischen **Abisco**, **ABA Ninja** und **E-Mail-Versand** mit QR-Code und Direktzahlung.

## Verzeichnisstruktur

```
Swiss21/
├── config/                          # Konfigurationsdateien
│   ├── config.json                  # Hauptkonfiguration (wird erstellt)
│   ├── config.example.json          # Beispiel-Konfiguration
│   └── logging.conf                 # Logging-Konfiguration
│
├── docs/                            # Dokumentation
│   ├── API_REFERENCE.md             # API-Referenz
│   ├── ABANINJA_INVOICE_API.md      # ABA Ninja Invoice API Analyse
│   ├── INTEGRATION_GUIDE.md         # Integrationsleitfaden
│   ├── INTEGRATION_STRATEGY.md      # Integrationsstrategie
│   ├── PROJECT_STRUCTURE.md         # Diese Datei
│   └── WEBISCO_ANALYSIS.md          # Webisco-Schnittstellenanalyse
│
├── examples/                        # Beispiele und Tests
│   ├── basic_usage.py               # Grundlegende Verwendung
│   ├── create_invoice_example.py    # Rechnungserstellung (neu)
│   ├── webisco_test.py              # Webisco-Test (neu)
│   └── email_test.py                # E-Mail-Test (neu)
│
├── src/                             # Quellcode
│   ├── __init__.py
│   │
│   ├── client.py                    # Haupt-API-Client (ABA Ninja)
│   ├── config.py                    # Konfigurationsverwaltung
│   ├── exceptions.py                # Exception-Definitionen
│   │
│   ├── connectors/                  # Externe System-Connectoren
│   │   ├── __init__.py
│   │   ├── webisco.py               # Webisco HTTP-Server (NEU)
│   │   └── webisco_parser.py        # XML-Parser für Webisco (NEU)
│   │
│   ├── endpoints/                   # ABA Ninja API-Endpoints
│   │   ├── __init__.py
│   │   ├── addresses.py             # Adressverwaltung (existiert)
│   │   └── invoices.py              # Rechnungsverwaltung (NEU)
│   │
│   ├── models/                      # Datenmodelle
│   │   ├── __init__.py
│   │   ├── invoice.py               # Invoice-Modell (NEU)
│   │   ├── customer.py              # Customer-Modell (NEU)
│   │   └── position.py              # Position-Modell (NEU)
│   │
│   ├── transformers/                # Datentransformation
│   │   ├── __init__.py
│   │   └── abisco_to_abaninja.py    # Abisco → ABA Ninja (NEU)
│   │
│   ├── utils/                       # Hilfsfunktionen
│   │   ├── __init__.py
│   │   ├── qr_code.py               # QR-Code-Generierung (NEU)
│   │   ├── payment_links.py         # Zahlungslink-Generierung (NEU)
│   │   ├── pdf_generator.py         # PDF-Generierung (NEU)
│   │   ├── email_sender.py          # E-Mail-Versand (NEU)
│   │   └── validators.py            # Validierungsfunktionen (NEU)
│   │
│   └── workflows/                   # Workflow-Orchestrierung
│       ├── __init__.py
│       └── invoice_workflow.py      # Haupt-Workflow (NEU)
│
├── templates/                       # Templates
│   ├── email/                       # E-Mail-Templates
│   │   ├── invoice_email.html       # HTML-E-Mail-Template (NEU)
│   │   └── invoice_email.txt        # Text-E-Mail-Template (NEU)
│   │
│   └── pdf/                         # PDF-Templates
│       └── invoice_template.html    # PDF-Template (NEU)
│
├── tests/                           # Unit-Tests
│   ├── __init__.py
│   ├── test_webisco.py              # Webisco-Tests (NEU)
│   ├── test_invoices.py             # Invoice-Tests (NEU)
│   ├── test_transformers.py         # Transformer-Tests (NEU)
│   └── test_utils.py                # Utils-Tests (NEU)
│
├── logs/                            # Log-Dateien (wird erstellt)
│   └── .gitkeep
│
├── data/                            # Daten-Verzeichnis
│   ├── qr_codes/                    # Generierte QR-Codes (NEU)
│   ├── pdfs/                        # Generierte PDFs (NEU)
│   └── .gitkeep
│
├── .env.example                     # Beispiel-Umgebungsvariablen (NEU)
├── .gitignore                       # Git-Ignore
├── README.md                        # Hauptdokumentation
├── requirements.txt                 # Python-Abhängigkeiten
├── PROJEKT_BERICHT.md               # Projektbericht
└── setup.py                         # Setup-Skript (NEU)
```

## Modulbeschreibungen

### 1. Connectors (`src/connectors/`)

#### `webisco.py`
**Zweck**: HTTP-Server für Webisco-Anfragen von Abisco

**Funktionen**:
- Flask/FastAPI HTTP-Server auf Port 8228
- Empfang von XML-Anfragen
- Routing zu entsprechenden Handlern
- Antwort-Generierung im Webisco-Format

**Klassen**:
- `WebiscoServer`: Haupt-Server-Klasse
- `WebiscoHandler`: Request-Handler

#### `webisco_parser.py`
**Zweck**: XML-Parsing für Webisco-Nachrichten

**Funktionen**:
- XML-Parsing mit lxml oder ElementTree
- Validierung der Envelope-Struktur
- Extraktion von Auftragsdaten
- Fehlerbehandlung bei ungültigem XML

**Klassen**:
- `WebiscoParser`: XML-Parser
- `WebiscoEnvelope`: Envelope-Datenklasse

### 2. Endpoints (`src/endpoints/`)

#### `invoices.py` (NEU)
**Zweck**: ABA Ninja Invoice API-Integration

**Funktionen**:
- `create_invoice()`: Rechnung erstellen
- `get_invoice()`: Rechnung abrufen
- `update_invoice()`: Rechnung aktualisieren
- `list_invoices()`: Rechnungen auflisten
- `execute_action()`: Aktion ausführen (z.B. send, mark_as_paid)

**Klassen**:
- `InvoicesEndpoint`: Invoice-Endpoint-Klasse

### 3. Models (`src/models/`)

#### `invoice.py` (NEU)
**Zweck**: Datenmodell für Rechnungen

**Klassen**:
```python
@dataclass
class Invoice:
    uuid: Optional[str]
    invoice_number: Optional[str]
    invoice_date: date
    due_date: Optional[date]
    customer: Customer
    positions: List[Position]
    subtotal: Decimal
    tax: Decimal
    total: Decimal
    currency: str = "CHF"
    language: str = "de"
    payment_terms: int = 30
    notes: Optional[str] = None
    private_notes: Optional[str] = None
```

#### `customer.py` (NEU)
**Zweck**: Datenmodell für Kunden

**Klassen**:
```python
@dataclass
class Customer:
    uuid: Optional[str]
    type: str  # "company" oder "person"
    name: str
    email: str
    address: Address
    customer_number: Optional[str] = None
    vat_number: Optional[str] = None
    currency_code: str = "CHF"
    language: str = "de"
    payment_terms: int = 30
```

#### `position.py` (NEU)
**Zweck**: Datenmodell für Rechnungspositionen

**Klassen**:
```python
@dataclass
class Position:
    description: str
    quantity: Decimal
    unit_price: Decimal
    tax_rate: Decimal
    total: Decimal
    article_uuid: Optional[str] = None
    discount: Decimal = Decimal("0")
```

### 4. Transformers (`src/transformers/`)

#### `abisco_to_abaninja.py` (NEU)
**Zweck**: Transformation von Abisco-Daten zu ABA Ninja-Format

**Funktionen**:
- `transform_order_to_invoice()`: Auftrag → Rechnung
- `transform_customer()`: Kunde-Transformation
- `transform_position()`: Position-Transformation
- `map_article_id()`: Artikel-ID-Mapping

**Klassen**:
- `AbiscoToAbaNinjaTransformer`: Haupt-Transformer

### 5. Utils (`src/utils/`)

#### `qr_code.py` (NEU)
**Zweck**: QR-Code-Generierung (Swiss QR-Bill)

**Funktionen**:
- `generate_swiss_qr_bill()`: Swiss QR-Bill generieren
- `generate_qr_code_image()`: QR-Code als PNG/SVG

**Bibliotheken**: `qrcode`, `segno`, `pillow`

#### `payment_links.py` (NEU)
**Zweck**: Zahlungslink-Generierung

**Funktionen**:
- `generate_twint_link()`: Twint-Zahlungslink
- `generate_ebanking_link()`: E-Banking-Link
- `generate_stripe_link()`: Stripe-Zahlungslink (optional)

#### `pdf_generator.py` (NEU)
**Zweck**: PDF-Rechnungsgenerierung

**Funktionen**:
- `generate_invoice_pdf()`: Rechnung als PDF
- `embed_qr_code()`: QR-Code in PDF einbetten

**Bibliotheken**: `weasyprint` oder `reportlab`

#### `email_sender.py` (NEU)
**Zweck**: E-Mail-Versand

**Funktionen**:
- `send_invoice_email()`: Rechnung per E-Mail versenden
- `attach_pdf()`: PDF anhängen
- `embed_qr_code()`: QR-Code einbetten

**Bibliotheken**: `smtplib`, `email`, `jinja2` (für Templates)

#### `validators.py` (NEU)
**Zweck**: Validierungsfunktionen

**Funktionen**:
- `validate_email()`: E-Mail-Validierung
- `validate_iban()`: IBAN-Validierung
- `validate_vat_number()`: UID/MwSt-Nummer-Validierung
- `validate_xml()`: XML-Schema-Validierung

### 6. Workflows (`src/workflows/`)

#### `invoice_workflow.py` (NEU)
**Zweck**: Haupt-Workflow-Orchestrierung

**Funktionen**:
- `process_invoice_from_abisco()`: Kompletter Workflow
  1. Webisco-Daten empfangen
  2. Daten transformieren
  3. Kunde in ABA Ninja suchen/erstellen
  4. Rechnung in ABA Ninja erstellen
  5. QR-Code generieren
  6. PDF erstellen
  7. E-Mail versenden

**Klassen**:
- `InvoiceWorkflow`: Workflow-Orchestrator

## Konfiguration

### `config/config.json`

```json
{
  "webisco": {
    "host": "0.0.0.0",
    "port": 8228,
    "admin_id": "your_admin_id"
  },
  "abaninja": {
    "api_token": "your_jwt_token",
    "account_uuid": "your_account_uuid",
    "api_base_url": "https://api.abaninja.ch"
  },
  "payment": {
    "iban": "CH9300762011623852957",
    "bic": "POFICHBEXXX",
    "account_holder": "Your Company GmbH",
    "twint_merchant_id": "your_twint_id"
  },
  "email": {
    "smtp_host": "smtp.gmail.com",
    "smtp_port": 587,
    "smtp_user": "your_email@gmail.com",
    "smtp_password": "your_password",
    "from_email": "rechnungen@yourcompany.ch",
    "from_name": "Your Company"
  },
  "pdf": {
    "company_name": "Your Company GmbH",
    "company_logo": "/path/to/logo.png",
    "company_address": {
      "street": "Musterstrasse 123",
      "zip": "8000",
      "city": "Zürich",
      "country": "Schweiz"
    }
  },
  "logging": {
    "level": "INFO",
    "file": "logs/swiss21.log"
  }
}
```

### `.env.example`

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
BIC=POFICHBEXXX
ACCOUNT_HOLDER=Your Company GmbH
TWINT_MERCHANT_ID=your_twint_id

# Email
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_email@gmail.com
SMTP_PASSWORD=your_password
EMAIL_FROM=rechnungen@yourcompany.ch
EMAIL_FROM_NAME=Your Company

# PDF
COMPANY_NAME=Your Company GmbH
COMPANY_LOGO=/path/to/logo.png

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/swiss21.log
```

## Abhängigkeiten (`requirements.txt`)

```txt
# Bestehende Abhängigkeiten
requests>=2.31.0
python-dotenv>=1.0.0

# Neue Abhängigkeiten
# Web-Framework
flask>=3.0.0
# oder
fastapi>=0.104.0
uvicorn>=0.24.0

# XML-Parsing
lxml>=4.9.3

# QR-Code
qrcode>=7.4.2
segno>=1.6.0
pillow>=10.1.0

# PDF-Generierung
weasyprint>=60.1
# oder
reportlab>=4.0.7

# E-Mail
jinja2>=3.1.2

# Validierung
email-validator>=2.1.0
schwifty>=2023.11.0  # IBAN-Validierung

# Datenmodelle
pydantic>=2.5.0

# Testing
pytest>=7.4.3
pytest-cov>=4.1.0
```

## Deployment

### Docker (optional)

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8228

CMD ["python", "-m", "src.connectors.webisco"]
```

### Systemd Service (Linux)

```ini
[Unit]
Description=Swiss21 Webisco Server
After=network.target

[Service]
Type=simple
User=swiss21
WorkingDirectory=/opt/swiss21
ExecStart=/usr/bin/python3 -m src.connectors.webisco
Restart=always

[Install]
WantedBy=multi-user.target
```

## Nächste Schritte

1. ✅ Projektstruktur definiert
2. ⏳ Abhängigkeiten in `requirements.txt` aktualisieren
3. ⏳ Datenmodelle implementieren
4. ⏳ Webisco-Connector implementieren
5. ⏳ Invoice-Endpoint implementieren
6. ⏳ Transformer implementieren
7. ⏳ Utils implementieren (QR, PDF, E-Mail)
8. ⏳ Workflow-Orchestrierung implementieren
9. ⏳ Tests schreiben
10. ⏳ Dokumentation vervollständigen
