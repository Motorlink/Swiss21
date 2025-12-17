# Zahlungsabgleich und Rückmeldung an Abisco

## Übersicht

Dieses Dokument beschreibt den **bidirektionalen Datenfluss** für die vollständige Integration zwischen Abisco, Swiss21 und ABA Ninja, inklusive automatischem Zahlungsabgleich und Rückmeldung an Abisco.

## Bidirektionaler Datenfluss

### Vorwärts-Flow (Rechnungserstellung)

```
Abisco (Rechnung erstellen)
  ↓ Webisco XML (createauftrag)
Swiss21 (Middleware)
  ↓ REST API
ABA Ninja (Rechnung speichern)
  ↓ Rechnungsdaten
Swiss21 (QR-Code + PDF + E-Mail)
  ↓ SMTP
Kunde (Rechnung erhalten)
```

### Rückwärts-Flow (Zahlungsabgleich) ⭐ NEU

```
Kunde (Zahlung ausführen)
  ↓ Banküberweisung/Twint/Kreditkarte
Bankkonto
  ↓ Kontoauszug/API
ABA Ninja (Zahlung erfassen)
  ↓ Webhook/Polling
Swiss21 (Zahlungserkennung)
  ↓ Webisco XML (zahlung)
Abisco (Zahlung als erledigt markieren)
```

## Webisco: Zahlung-Ressource

### Endpoint: `zahlung`

**Beschreibung**: Fügt eine Anzahlung oder vollständige Zahlung zu einem Auftrag in Abisco hinzu.

**HTTP-Header**: Ressource `zahlung`

### XML-Struktur

```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<webisco version="55" username="testuser" password="geheim" type="request">
  <content>
    <zahlung>
      <belegnummer>RE-2024-0001</belegnummer>
      <betrag>1234.56</betrag>
      <datum>2024-12-17</datum>
      <zahlungsart>3</zahlungsart>
      <bemerkung>Zahlung via Twint erhalten</bemerkung>
    </zahlung>
  </content>
</webisco>
```

### Zahlung-Attribute

| Attribut | Typ | Pflicht | Beschreibung |
|----------|-----|---------|--------------|
| `belegnummer` | #TEXT | ✓ | Die Belegnummer des Auftrags (Rechnungsnummer) |
| `betrag` | #PREIS | ✓ | Der gezahlte Betrag in Euro (Komma als Dezimaltrennzeichen) |
| `datum` | #DATUM | ✓ | Das Datum der Zahlung (YYYY-MM-DD) |
| `zahlungsart` | #ZAHL | ✓ | ID der Zahlungsart (siehe unten) |
| `bemerkung` | #TEXT | | Optional: Bemerkung zur Zahlung |

### Zahlungsart-IDs

| ID | Zahlungsart |
|----|-------------|
| 0 | Rechnung (auf Rechnung) |
| 1 | Vorauskasse |
| 2 | Nachnahme |
| 3 | **Bankeinzug** |
| 6 | PayPal |
| 8 | Sofortüberweisung |
| 9 | VorOrtZahlung |
| 10 | PayDirekt |

**Hinweis**: Für Twint-Zahlungen kann ID **3 (Bankeinzug)** oder **6 (PayPal)** verwendet werden, da Twint nicht explizit aufgeführt ist. Alternativ kann in der `bemerkung` "Twint" vermerkt werden.

### Beispiel: Vollständige Zahlung

```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<webisco version="55" adminid="your_admin_id" type="request">
  <content>
    <zahlung>
      <belegnummer>RE-2024-0001</belegnummer>
      <betrag>1234.56</betrag>
      <datum>2024-12-17</datum>
      <zahlungsart>3</zahlungsart>
      <bemerkung>Vollständige Zahlung via Twint erhalten - QR-Code</bemerkung>
    </zahlung>
  </content>
</webisco>
```

### Beispiel: Teilzahlung

```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<webisco version="55" adminid="your_admin_id" type="request">
  <content>
    <zahlung>
      <belegnummer>RE-2024-0001</belegnummer>
      <betrag>500.00</betrag>
      <datum>2024-12-17</datum>
      <zahlungsart>3</zahlungsart>
      <bemerkung>Teilzahlung 1 von 2 - Banküberweisung</bemerkung>
    </zahlung>
  </content>
</webisco>
```

## ABA Ninja: Bank Accounts und Zahlungsabgleich

### Bank Accounts Endpoints

#### 1. Liste aller Bankkonten

**Endpoint**: `GET /accounts/{accountUuid}/finances/v2/bank-accounts`

**Response**:
```json
{
  "status": 0,
  "message": "string",
  "data": [
    {
      "uuid": "095be615-a8ad-4c33-8e9c-c7612fbf6c9f",
      "name": "My Bank",
      "bankName": "Test Bank",
      "iban": "CH9300762011623852957",
      "bic": "POFICHBEXXX",
      "currency": "CHF",
      "balance": 10000.00
    }
  ]
}
```

#### 2. Einzelnes Bankkonto

**Endpoint**: `GET /accounts/{accountUuid}/finances/v2/bank-accounts/{bankAccountUuid}`

### Zahlungsabgleich-Strategien

Es gibt mehrere Möglichkeiten, Zahlungen zu erkennen und abzugleichen:

#### Option 1: Manuelle Erfassung in ABA Ninja + Webhook

1. Zahlung wird manuell in ABA Ninja erfasst
2. ABA Ninja sendet Webhook an Swiss21
3. Swiss21 verarbeitet Webhook und sendet Zahlung an Abisco

**Vorteil**: Einfach, keine zusätzliche Integration  
**Nachteil**: Manuelle Erfassung erforderlich

#### Option 2: QR-Code-Referenz-Matching (Empfohlen) ⭐

1. Swiss21 generiert eindeutige Zahlungsreferenz im QR-Code
2. Kunde zahlt mit QR-Code (Referenz wird übermittelt)
3. Bank-API oder Kontoauszug-Import liefert Zahlungen mit Referenz
4. Swiss21 matched Referenz mit Rechnung
5. Swiss21 sendet Zahlung an Abisco

**Vorteil**: Vollautomatisch, zuverlässig  
**Nachteil**: Bank-API oder Kontoauszug-Import erforderlich

#### Option 3: Polling von ABA Ninja Invoices

1. Swiss21 pollt regelmäßig ABA Ninja Invoice-Status
2. Wenn Status = "paid", sende Zahlung an Abisco

**Vorteil**: Einfach zu implementieren  
**Nachteil**: Verzögerung durch Polling-Intervall

#### Option 4: Bank-API-Integration (z.B. PostFinance, UBS)

1. Swiss21 verbindet sich direkt mit Bank-API
2. Abruf von Transaktionen in Echtzeit
3. Matching via QR-Referenz oder IBAN
4. Automatische Zahlung an Abisco

**Vorteil**: Echtzeit, vollautomatisch  
**Nachteil**: Bank-API-Zugang erforderlich

## Implementierung in Swiss21

### Modul-Struktur

```
src/
├── connectors/
│   ├── webisco.py              # Webisco HTTP-Server (existiert)
│   └── webisco_payment.py      # Zahlungsmeldung an Abisco (NEU)
│
├── endpoints/
│   ├── invoices.py             # Invoice-Endpoint (existiert)
│   └── bank_accounts.py        # Bank-Account-Endpoint (NEU)
│
├── services/
│   ├── payment_reconciliation.py   # Zahlungsabgleich-Service (NEU)
│   └── bank_api_connector.py       # Bank-API-Connector (NEU, optional)
│
└── workflows/
    ├── invoice_workflow.py         # Rechnungs-Workflow (existiert)
    └── payment_workflow.py         # Zahlungs-Workflow (NEU)
```

### 1. Webisco Payment Sender (`src/connectors/webisco_payment.py`)

```python
import requests
from xml.etree.ElementTree import Element, SubElement, tostring
from datetime import date
from decimal import Decimal

class WebiscoPaymentSender:
    """Sendet Zahlungsmeldungen an Abisco via Webisco."""
    
    def __init__(self, host: str, port: int, admin_id: str):
        self.base_url = f"http://{host}:{port}"
        self.admin_id = admin_id
        self.version = "55"
    
    def send_payment(
        self,
        invoice_number: str,
        amount: Decimal,
        payment_date: date,
        payment_method: int = 3,  # 3 = Bankeinzug
        note: str = ""
    ) -> dict:
        """
        Sendet eine Zahlungsmeldung an Abisco.
        
        Args:
            invoice_number: Rechnungsnummer (Belegnummer)
            amount: Gezahlter Betrag
            payment_date: Zahlungsdatum
            payment_method: Zahlungsart-ID (0-10)
            note: Optional: Bemerkung
            
        Returns:
            Response-Dictionary von Abisco
        """
        # XML erstellen
        root = Element("webisco")
        root.set("version", self.version)
        root.set("adminid", self.admin_id)
        root.set("type", "request")
        
        content = SubElement(root, "content")
        zahlung = SubElement(content, "zahlung")
        
        SubElement(zahlung, "belegnummer").text = invoice_number
        SubElement(zahlung, "betrag").text = str(amount).replace(".", ",")
        SubElement(zahlung, "datum").text = payment_date.strftime("%Y-%m-%d")
        SubElement(zahlung, "zahlungsart").text = str(payment_method)
        
        if note:
            SubElement(zahlung, "bemerkung").text = note
        
        # XML zu String
        xml_str = tostring(root, encoding="utf-8", xml_declaration=True)
        
        # HTTP-POST an Webisco
        response = requests.post(
            f"{self.base_url}/zahlung",
            data=xml_str,
            headers={"Content-Type": "text/html; charset=utf-8"}
        )
        
        # Response parsen
        # TODO: XML-Response parsen und zurückgeben
        
        return {"status": "success", "response": response.text}
```

### 2. Payment Reconciliation Service (`src/services/payment_reconciliation.py`)

```python
from typing import List, Optional
from decimal import Decimal
from datetime import date
from dataclasses import dataclass

@dataclass
class Payment:
    """Repräsentiert eine Zahlung."""
    amount: Decimal
    payment_date: date
    reference: str  # QR-Referenz oder Verwendungszweck
    payer_name: Optional[str] = None
    payer_iban: Optional[str] = None
    payment_method: str = "bank_transfer"

class PaymentReconciliationService:
    """Service für automatischen Zahlungsabgleich."""
    
    def __init__(self, abaninja_client, webisco_sender):
        self.abaninja = abaninja_client
        self.webisco = webisco_sender
    
    def match_payment_to_invoice(self, payment: Payment) -> Optional[str]:
        """
        Matched eine Zahlung zu einer Rechnung anhand der QR-Referenz.
        
        Args:
            payment: Payment-Objekt mit Zahlungsdaten
            
        Returns:
            Invoice UUID wenn Match gefunden, sonst None
        """
        # Suche Rechnung anhand der Referenz
        # TODO: Implementierung
        pass
    
    def process_payment(self, payment: Payment) -> bool:
        """
        Verarbeitet eine Zahlung:
        1. Matched zu Rechnung
        2. Markiert Rechnung in ABA Ninja als bezahlt
        3. Sendet Zahlung an Abisco
        
        Args:
            payment: Payment-Objekt
            
        Returns:
            True wenn erfolgreich, False sonst
        """
        # 1. Match zu Rechnung
        invoice_uuid = self.match_payment_to_invoice(payment)
        if not invoice_uuid:
            return False
        
        # 2. Hole Rechnungsdetails von ABA Ninja
        invoice = self.abaninja.invoices.get_invoice(invoice_uuid)
        
        # 3. Markiere als bezahlt in ABA Ninja
        self.abaninja.invoices.execute_action(
            invoice_uuid,
            action="mark_as_paid",
            payment_date=payment.payment_date,
            amount=payment.amount
        )
        
        # 4. Sende Zahlung an Abisco
        payment_method_id = self._map_payment_method(payment.payment_method)
        note = f"Zahlung via {payment.payment_method} - Ref: {payment.reference}"
        
        self.webisco.send_payment(
            invoice_number=invoice["invoice_number"],
            amount=payment.amount,
            payment_date=payment.payment_date,
            payment_method=payment_method_id,
            note=note
        )
        
        return True
    
    def _map_payment_method(self, method: str) -> int:
        """Mapped Zahlungsmethode zu Webisco-ID."""
        mapping = {
            "bank_transfer": 3,  # Bankeinzug
            "twint": 3,          # Twint → Bankeinzug
            "paypal": 6,
            "credit_card": 3,
            "cash": 9,           # VorOrtZahlung
        }
        return mapping.get(method, 3)
```

### 3. Payment Workflow (`src/workflows/payment_workflow.py`)

```python
from typing import List
from .payment_reconciliation import PaymentReconciliationService, Payment

class PaymentWorkflow:
    """Orchestriert den Zahlungsabgleich-Workflow."""
    
    def __init__(self, reconciliation_service: PaymentReconciliationService):
        self.reconciliation = reconciliation_service
    
    def process_bank_transactions(self, transactions: List[dict]) -> dict:
        """
        Verarbeitet eine Liste von Banktransaktionen.
        
        Args:
            transactions: Liste von Transaktions-Dicts
            
        Returns:
            Statistik-Dictionary
        """
        stats = {
            "total": len(transactions),
            "matched": 0,
            "unmatched": 0,
            "errors": 0
        }
        
        for tx in transactions:
            try:
                payment = Payment(
                    amount=tx["amount"],
                    payment_date=tx["date"],
                    reference=tx.get("reference", ""),
                    payer_name=tx.get("payer_name"),
                    payer_iban=tx.get("payer_iban"),
                    payment_method=tx.get("method", "bank_transfer")
                )
                
                if self.reconciliation.process_payment(payment):
                    stats["matched"] += 1
                else:
                    stats["unmatched"] += 1
                    
            except Exception as e:
                stats["errors"] += 1
                # TODO: Logging
        
        return stats
```

## QR-Code-Referenz-Generierung

### Swiss QR-Bill Referenz

Die QR-Referenz muss nach ISO 11649 (Creditor Reference) oder ESR-Referenz formatiert sein.

```python
def generate_qr_reference(invoice_number: str, customer_id: str) -> str:
    """
    Generiert eine eindeutige QR-Referenz.
    
    Format: RF + Prüfziffer + Rechnungsnummer + Kundennummer
    """
    # Beispiel: RF18RE20240001K12345
    base = f"RE{invoice_number}K{customer_id}"
    checksum = calculate_rf_checksum(base)
    return f"RF{checksum:02d}{base}"

def calculate_rf_checksum(reference: str) -> int:
    """Berechnet ISO 11649 Prüfziffer."""
    # TODO: Implementierung nach ISO 11649
    pass
```

## Deployment-Szenarien

### Szenario 1: Polling-basiert (Einfach)

1. Cronjob alle 15 Minuten
2. Ruft ABA Ninja Invoices ab
3. Prüft auf Status-Änderungen
4. Sendet Zahlungen an Abisco

**Cron**: `*/15 * * * * python -m src.workflows.payment_workflow`

### Szenario 2: Webhook-basiert (Mittel)

1. ABA Ninja Webhook konfigurieren (falls verfügbar)
2. Swiss21 empfängt Webhook bei Zahlungseingang
3. Verarbeitet Zahlung sofort
4. Sendet an Abisco

### Szenario 3: Bank-API-basiert (Fortgeschritten)

1. Integration mit PostFinance/UBS/etc. API
2. Echtzeit-Benachrichtigung bei Zahlungseingang
3. Automatisches Matching via QR-Referenz
4. Sofortige Meldung an Abisco

## Konfiguration

### `config/config.json`

```json
{
  "payment_reconciliation": {
    "enabled": true,
    "mode": "polling",
    "polling_interval_minutes": 15,
    "auto_match_threshold": 0.99,
    "require_qr_reference": true
  },
  "bank_api": {
    "enabled": false,
    "provider": "postfinance",
    "api_key": "your_api_key",
    "account_number": "CH9300762011623852957"
  }
}
```

## Nächste Schritte

1. ✅ Zahlungsabgleich-Konzept definiert
2. ⏳ Webisco Payment Sender implementieren
3. ⏳ Payment Reconciliation Service implementieren
4. ⏳ QR-Referenz-Generierung implementieren
5. ⏳ Bank-API-Connector implementieren (optional)
6. ⏳ Payment Workflow implementieren
7. ⏳ Tests schreiben
8. ⏳ Dokumentation vervollständigen
