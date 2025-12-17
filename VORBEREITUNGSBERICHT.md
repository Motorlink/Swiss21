# Swiss21 - Vorbereitungsbericht

**Datum**: 17. Dezember 2024  
**Projekt**: Swiss21 - Abisco ↔ ABA Ninja Integration  
**Status**: Vorbereitung abgeschlossen ✅

---

## Zusammenfassung

Die vollständige Vorbereitung für die **Swiss21-Integration** zwischen **Abisco** (Warenwirtschaft), **ABA Ninja** (Cloud-ERP) und **E-Mail-Versand** mit QR-Code und Direktzahlung ist abgeschlossen. Das Projekt ist nun bereit für die schrittweise Implementierung.

## Projektziel

Entwicklung einer vollautomatischen, **bidirektionalen** Integration:

### Vorwärts-Flow (Rechnungserstellung)
1. **Abisco** erstellt Rechnung
2. **Webisco-Schnittstelle** sendet Daten an Swiss21 (XML über HTTP-POST)
3. **Swiss21** transformiert Daten und erstellt Rechnung in **ABA Ninja**
4. **Swiss21** generiert **Swiss QR-Bill** (QR-Code nach ISO 20022)
5. **Swiss21** erstellt **PDF-Rechnung**
6. **Swiss21** versendet E-Mail mit:
   - PDF-Rechnung als Anhang
   - Eingebetteter QR-Code
   - **Twint-Zahlungslink**
   - Weitere Direktzahlungslinks

### Rückwärts-Flow (Zahlungsabgleich) ⭐
1. Kunde zahlt via QR-Code/Twint/Banküberweisung
2. **ABA Ninja** oder **Bank-API** erfasst Zahlung
3. **Swiss21** erkennt Zahlung (via QR-Referenz-Matching)
4. **Swiss21** sendet Zahlungsmeldung an **Abisco** (Webisco `zahlung`-Ressource)
5. **Abisco** markiert Rechnung als bezahlt

## Durchgeführte Analysen

### 1. Webisco-Schnittstellenanalyse ✅

**Dokument**: `docs/WEBISCO_ANALYSIS.md`

**Erkenntnisse**:
- **Protokoll**: XML über HTTP-POST auf Port 8228
- **Authentifizierung**: Admin-ID oder Username/Password
- **Wichtige Ressourcen**:
  - `createauftrag`: Auftrag/Rechnung erstellen
  - `zahlung`: Zahlung zu Auftrag hinzufügen ⭐
  - `kundensuche`: Kunde suchen
  - `createkunde`: Kunde erstellen
- **Datenformat**: UTF-8 XML mit spezifischen Datentypen (#TEXT, #PREIS, #DATUM, etc.)
- **Zahlungsarten**: 0-10 (Rechnung, Vorauskasse, Bankeinzug, PayPal, Twint, etc.)

### 2. ABA Ninja API-Analyse ✅

**Dokument**: `docs/ABANINJA_INVOICE_API.md`

**Erkenntnisse**:
- **Basis-URL**: `https://api.abaninja.ch`
- **Authentifizierung**: JWT Bearer Token
- **Invoice-Endpoints**:
  - `POST /accounts/{accountUuid}/documents/v2/invoices`: Rechnung erstellen ✅
  - `GET /accounts/{accountUuid}/documents/v2/invoices/{invoiceUuid}`: Rechnung abrufen
  - `PATCH /accounts/{accountUuid}/documents/v2/invoices/{invoiceUuid}/actions`: Aktionen ausführen (z.B. "mark_as_paid")
- **Bank-Endpoints**:
  - `GET /accounts/{accountUuid}/finances/v2/bank-accounts`: Bankkonten abrufen
- **Datenformat**: JSON mit UUID-basierten Referenzen
- **Währungen**: CHF, EUR, USD
- **Steuersätze**: 7.7% (Normal), 2.5% (Reduziert), 0% (Steuerfrei)

### 3. Integrationsstrategie ✅

**Dokument**: `docs/INTEGRATION_STRATEGY.md`

**Komponenten**:
1. **Webisco-Connector**: HTTP-Server für Abisco-Anfragen
2. **ABA Ninja Invoice Creator**: Rechnungserstellung via API
3. **QR-Code Generator**: Swiss QR-Bill nach ISO 20022
4. **Payment Link Generator**: Twint, E-Banking, Kreditkarte
5. **PDF Generator**: Professionelle Rechnungs-PDFs
6. **Email Sender**: SMTP mit HTML-Templates

**Technologie-Stack**:
- Python 3.11+
- Flask (Webisco HTTP-Server)
- requests (HTTP-Client)
- lxml (XML-Parsing)
- qrcode + segno (QR-Code)
- weasyprint (PDF)
- jinja2 (E-Mail-Templates)

### 4. Zahlungsabgleich-Konzept ✅

**Dokument**: `docs/PAYMENT_RECONCILIATION.md`

**Strategien**:
1. **QR-Code-Referenz-Matching** (Empfohlen): Automatisches Matching via eindeutige QR-Referenz
2. **Polling von ABA Ninja**: Regelmäßige Abfrage von Invoice-Status
3. **Webhook-basiert**: Echtzeit-Benachrichtigung von ABA Ninja (falls verfügbar)
4. **Bank-API-Integration**: Direkte Integration mit PostFinance/UBS/etc.

**Webisco Zahlung-Ressource**:
- Endpoint: `zahlung`
- Sendet Zahlungsmeldung an Abisco
- Parameter: Belegnummer, Betrag, Datum, Zahlungsart, Bemerkung

## Projektstruktur

**Dokument**: `docs/PROJECT_STRUCTURE.md`

```
Swiss21/
├── config/                      # Konfiguration
├── docs/                        # Dokumentation (5 Dokumente)
├── examples/                    # Beispiele
├── src/                         # Quellcode
│   ├── connectors/             # Webisco-Connector
│   ├── endpoints/              # ABA Ninja API (Addresses, Invoices)
│   ├── models/                 # Datenmodelle (Invoice, Customer, Position)
│   ├── transformers/           # Abisco → ABA Ninja Transformation
│   ├── utils/                  # QR-Code, PDF, E-Mail, Payment Links
│   ├── workflows/              # Workflow-Orchestrierung
│   └── services/               # Zahlungsabgleich-Service
├── templates/                   # E-Mail- und PDF-Templates
├── tests/                       # Unit-Tests
├── data/                        # Generierte Dateien (QR, PDF)
└── logs/                        # Log-Dateien
```

## Erstellte Dokumentation

| Dokument | Beschreibung | Seiten |
|----------|--------------|--------|
| `WEBISCO_ANALYSIS.md` | Vollständige Webisco-Schnittstellenanalyse | ~200 Zeilen |
| `ABANINJA_INVOICE_API.md` | ABA Ninja Invoice API-Referenz | ~400 Zeilen |
| `INTEGRATION_STRATEGY.md` | Detaillierte Integrationsstrategie | ~350 Zeilen |
| `PROJECT_STRUCTURE.md` | Vollständige Projektstruktur | ~450 Zeilen |
| `PAYMENT_RECONCILIATION.md` | Zahlungsabgleich und Rückmeldung | ~500 Zeilen |
| `API_REFERENCE.md` | API-Referenz (existiert) | ~150 Zeilen |
| `INTEGRATION_GUIDE.md` | Integrationsleitfaden (existiert) | ~200 Zeilen |

**Gesamt**: ~2.250 Zeilen Dokumentation

## Konfigurationsdateien

### `requirements.txt` ✅
Alle benötigten Python-Pakete:
- Flask (Webisco-Server)
- lxml (XML-Parsing)
- qrcode, segno, pillow (QR-Code)
- weasyprint (PDF)
- jinja2 (Templates)
- email-validator, schwifty (Validierung)
- pydantic (Datenmodelle)
- pytest (Testing)

### `.env.example` ✅
Vollständige Umgebungsvariablen-Vorlage:
- Webisco-Konfiguration
- ABA Ninja API-Token
- Zahlungsinformationen (IBAN, Twint)
- E-Mail-Konfiguration (SMTP)
- PDF-Konfiguration (Firmenlogo, etc.)

### `.gitignore` ✅
Aktualisiert für:
- Generierte Dateien (QR-Codes, PDFs)
- Konfigurationsdateien
- Logs

## Verzeichnisstruktur erstellt ✅

Alle erforderlichen Verzeichnisse wurden erstellt:
- `src/connectors/`
- `src/transformers/`
- `src/utils/`
- `src/workflows/`
- `src/services/`
- `templates/email/`
- `templates/pdf/`
- `data/qr_codes/`
- `data/pdfs/`
- `data/temp/`
- `logs/`

## Implementierungsplan

### Phase 1: Grundlagen (Priorität: Hoch)
- [ ] Datenmodelle (`src/models/invoice.py`, `customer.py`, `position.py`)
- [ ] Konfigurationsverwaltung erweitern
- [ ] Logging-Setup

### Phase 2: Webisco-Integration (Priorität: Hoch)
- [ ] Webisco HTTP-Server (`src/connectors/webisco.py`)
- [ ] XML-Parser (`src/connectors/webisco_parser.py`)
- [ ] Webisco Payment Sender (`src/connectors/webisco_payment.py`)

### Phase 3: ABA Ninja Integration (Priorität: Hoch)
- [ ] Invoice-Endpoint (`src/endpoints/invoices.py`)
- [ ] Datentransformation (`src/transformers/abisco_to_abaninja.py`)
- [ ] Kunden-Lookup und -Erstellung

### Phase 4: QR-Code und PDF (Priorität: Mittel)
- [ ] Swiss QR-Bill Generator (`src/utils/qr_code.py`)
- [ ] PDF-Generator (`src/utils/pdf_generator.py`)
- [ ] PDF-Template (`templates/pdf/invoice_template.html`)

### Phase 5: E-Mail-Versand (Priorität: Mittel)
- [ ] E-Mail-Sender (`src/utils/email_sender.py`)
- [ ] E-Mail-Templates (`templates/email/invoice_email.html`, `.txt`)
- [ ] Payment-Link-Generator (`src/utils/payment_links.py`)

### Phase 6: Zahlungsabgleich (Priorität: Mittel)
- [ ] Payment Reconciliation Service (`src/services/payment_reconciliation.py`)
- [ ] Payment Workflow (`src/workflows/payment_workflow.py`)
- [ ] Bank-API-Connector (optional)

### Phase 7: Workflow-Orchestrierung (Priorität: Hoch)
- [ ] Invoice Workflow (`src/workflows/invoice_workflow.py`)
- [ ] End-to-End-Integration
- [ ] Fehlerbehandlung und Logging

### Phase 8: Testing und Dokumentation (Priorität: Mittel)
- [ ] Unit-Tests für alle Module
- [ ] Integration-Tests
- [ ] Beispiel-Skripte (`examples/`)
- [ ] Deployment-Anleitung

## Offene Fragen (zu klären vor Implementierung)

### 1. Webisco-Server
- **Frage**: Soll Swiss21 als HTTP-Server auf Port 8228 lauschen, oder soll Swiss21 aktiv Daten von Abisco abholen?
- **Empfehlung**: HTTP-Server (Push von Abisco)

### 2. Zahlungsinformationen
- **IBAN**: Wird benötigt für QR-Rechnung
- **Twint-Merchant-ID**: Wird benötigt für Twint-Links
- **Weitere Zahlungsmethoden**: Kreditkarte, PayPal?

### 3. E-Mail-Konfiguration
- **SMTP-Server**: Gmail, SendGrid, eigener Server?
- **E-Mail-Templates**: Gibt es Corporate Design-Vorgaben?

### 4. Deployment
- **Server**: Wo soll Swiss21 laufen? (Docker, VPS, Cloud)
- **Betriebssystem**: Linux (empfohlen), Windows?
- **Monitoring**: Welche Monitoring-Tools sollen verwendet werden?

### 5. Bank-API
- **Bank**: PostFinance, UBS, Raiffeisen, andere?
- **API-Zugang**: Ist API-Zugang vorhanden oder geplant?

## Nächste Schritte

### Sofort (vor Implementierung)
1. **Offene Fragen klären** (siehe oben)
2. **Konfiguration vorbereiten**:
   - `.env` Datei erstellen (basierend auf `.env.example`)
   - ABA Ninja API-Token eintragen
   - IBAN und Zahlungsinformationen eintragen
   - SMTP-Zugangsdaten eintragen

### Implementierung (nach Freigabe)
1. **Phase 1-3 implementieren** (Grundlagen + Webisco + ABA Ninja)
2. **Ersten Test durchführen**: Abisco → Swiss21 → ABA Ninja
3. **Phase 4-5 implementieren** (QR-Code + PDF + E-Mail)
4. **Zweiten Test durchführen**: Kompletter Vorwärts-Flow
5. **Phase 6 implementieren** (Zahlungsabgleich)
6. **Dritten Test durchführen**: Bidirektionaler Flow
7. **Phase 7-8 implementieren** (Workflow + Tests + Doku)
8. **Produktiv-Deployment**

## Konus-Regel Compliance ✅

Das Projekt folgt der **Konus-Regel**:
- ✅ **Modulare Architektur**: Jedes Modul ist unabhängig
- ✅ **Keine unnötigen Abhängigkeiten**: Klare Trennung der Verantwortlichkeiten
- ✅ **Updatefähig**: Jedes Modul kann einzeln aktualisiert werden
- ✅ **Sauberer Code**: Professionelle IT-Standards
- ✅ **Dokumentiert**: Umfassende Dokumentation für jedes Modul

## Git-Repository Status

**Repository**: https://github.com/Motorlink/Swiss21

**Letzter Commit**: 
```
docs: Add comprehensive integration preparation
- 18 files changed, 2085 insertions(+)
```

**Branches**: `master` (main branch)

**Bereit für**: Implementierung nach Freigabe

---

## Fazit

Die **Swiss21-Integration** ist vollständig vorbereitet und dokumentiert. Alle Schnittstellen wurden analysiert, die Architektur ist definiert, und die Projektstruktur ist erstellt. 

Das Projekt ist **produktionsreif** in Bezug auf:
- ✅ Konzeption
- ✅ Dokumentation
- ✅ Architektur
- ✅ Projektstruktur

**Nächster Schritt**: Klärung der offenen Fragen und Start der Implementierung nach Freigabe.

---

**Erstellt von**: Manus AI  
**Datum**: 17. Dezember 2024  
**Version**: 1.0
