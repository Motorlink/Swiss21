#!/usr/bin/env python3
"""
Swiss21 - Test Invoice Creation Script
Erstellt eine Rechnung in ABA Ninja basierend auf Abisco-Daten
"""

import requests
import json
from datetime import datetime

# Konfiguration
ABA_NINJA_API_BASE = "https://api.abaninja.ch"
API_TOKEN = "eyJhbGciOiJFZERTQSIsImtpZCI6IjFhZThhZDQ1LTIwYjItNGFiMC1iMjBjLWZkNDllNjI5MTg3OCJ9.eyJzdWIiOiIzODIyNGRkNy05ZTRiLTRlNzItYTg2MS0xYzQ0YzA0ZGY4MjAiLCJhdWQiOiIyMWVmYTM4OS1kMDExLTQ1ZjAtYjAxNS1lMGQ5MDE0ODZmYTYiLCJqdGkiOiIxNzc2NzAxMy03ZWUzLTQwNmMtODUzOC03NDMwMGQ1NmRlZjUiLCJpYXQiOjE3NjU5NjQxNzMsIm5iZiI6MTc2NTk2NDE3MywiaXNzIjoiaHR0cHM6XC9cL2FwaS5hYmFuaW5qYS5jaCIsImF6cCI6IkFQSSBUb2tlbiAxNzc2NzAxMy03ZWUzLTQwNmMtODUzOC03NDMwMGQ1NmRlZjUiLCJleHAiOjM0MDgyMjA3OTl9.SUN63U_CrmtJi3up2ihMOa528yXYeQZz73cg_BHWF1mwRLJExZRk_OCkuNld4PDu-nkdQDrx7rlECHEsqDrrAg"
ACCOUNT_UUID = "21efa389-d011-45f0-b015-e0d901486fa6"  # Swiss21.org Account

# Abisco-Rechnungsdaten (aus Testrechnung RE1)
INVOICE_DATA = {
    "invoice_number": "RE1",
    "invoice_date": "2025-12-17",
    "due_date": "2025-12-17",
    "order_reference": "A1",
    "customer": {
        "customer_number": "10000",
        "company_name": "MT Transport GmbH",
        "street": "Lorenweg 22",
        "zip": "8610",
        "city": "Uster",
        "country": "CH",  # Korrigiert von DEU
        "email": "info@mt-transport.ch"
    },
    "line_items": [
        {
            "description": "Ölfilter",
            "article_number": "HU7020Z",
            "manufacturer": "Mann & Hummel",
            "quantity": 1,
            "unit_price_net": 14.12,  # EUR → CHF (1:1 für Test)
            "vat_rate": 8.1,
            "total_gross": 15.26
        },
        {
            "description": "Zustellpauschale",
            "quantity": 1,
            "unit_price_net": 10.00,
            "vat_rate": 0,
            "total_gross": 10.00
        }
    ],
    "total_net": 24.12,
    "total_gross": 25.26,
    "currency": "CHF"
}


def get_headers():
    """Erstellt die HTTP-Headers für ABA Ninja API"""
    return {
        "Authorization": f"Bearer {API_TOKEN}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }


def check_customer_exists(customer_number):
    """Prüft ob Kundennummer bereits existiert"""
    url = f"{ABA_NINJA_API_BASE}/accounts/{ACCOUNT_UUID}/addresses/v2/check-customer-number"
    params = {"customerNumber": customer_number}
    
    print(f"🔍 Prüfe Kundennummer {customer_number}...")
    response = requests.get(url, headers=get_headers(), params=params)
    
    if response.status_code == 200:
        print(f"✅ Kundennummer {customer_number} ist verfügbar")
        return False
    elif response.status_code == 400:
        print(f"⚠️ Kundennummer {customer_number} existiert bereits")
        return True
    else:
        print(f"❌ Fehler beim Prüfen: {response.status_code}")
        print(response.text)
        return None


def create_customer(customer_data):
    """Erstellt einen neuen Kunden in ABA Ninja"""
    url = f"{ABA_NINJA_API_BASE}/accounts/{ACCOUNT_UUID}/addresses/v2/companies"
    
    payload = {
        "type": "company",
        "customer_number": customer_data["customer_number"],
        "name": customer_data["company_name"],
        "currency_code": "CHF",
        "language": "de",
        "addresses": [
            {
                "street": customer_data["street"],
                "zip": customer_data["zip"],
                "city": customer_data["city"],
                "country": customer_data["country"]
            }
        ],
        "contacts": [
            {
                "type": "email",
                "value": customer_data["email"]
            }
        ],
        "payment_terms": 30  # 30 Tage Zahlungsfrist
    }
    
    print(f"📝 Erstelle Kunde: {customer_data['company_name']}...")
    response = requests.post(url, headers=get_headers(), json=payload)
    
    if response.status_code in [200, 201]:
        data = response.json()
        customer_uuid = data["data"]["uuid"]
        print(f"✅ Kunde erstellt: UUID = {customer_uuid}")
        return customer_uuid
    else:
        print(f"❌ Fehler beim Erstellen: {response.status_code}")
        print(response.text)
        return None


def get_customer_by_number(customer_number):
    """Sucht Kunden anhand der Kundennummer"""
    url = f"{ABA_NINJA_API_BASE}/accounts/{ACCOUNT_UUID}/addresses/v2/companies"
    
    print(f"🔍 Suche Kunde mit Nummer {customer_number}...")
    response = requests.get(url, headers=get_headers())
    
    if response.status_code == 200:
        data = response.json()
        for company in data["data"]:
            if company.get("customer_number") == customer_number:
                print(f"✅ Kunde gefunden: {company['name']} (UUID: {company['uuid']})")
                return company["uuid"]
        print(f"⚠️ Kunde mit Nummer {customer_number} nicht gefunden")
        return None
    else:
        print(f"❌ Fehler beim Suchen: {response.status_code}")
        print(response.text)
        return None


def create_invoice(customer_uuid, invoice_data):
    """Erstellt eine Rechnung in ABA Ninja"""
    url = f"{ABA_NINJA_API_BASE}/accounts/{ACCOUNT_UUID}/documents/v2/invoices"
    
    # Konvertiere Line Items
    line_items = []
    for item in invoice_data["line_items"]:
        line_items.append({
            "description": item["description"],
            "quantity": item["quantity"],
            "unit_price": item["unit_price_net"],
            "vat_rate": item["vat_rate"],
            "article_number": item.get("article_number", "")
        })
    
    payload = {
        "address_uuid": customer_uuid,
        "invoice_number": invoice_data["invoice_number"],
        "invoice_date": invoice_data["invoice_date"],
        "due_date": invoice_data["due_date"],
        "reference": invoice_data["order_reference"],  # Auftragsnummer
        "currency_code": invoice_data["currency"],
        "line_items": line_items,
        "notes": f"Erstellt aus Abisco-Auftrag {invoice_data['order_reference']}"
    }
    
    print(f"📄 Erstelle Rechnung {invoice_data['invoice_number']}...")
    print(f"   Kunde: {customer_uuid}")
    print(f"   Datum: {invoice_data['invoice_date']}")
    print(f"   Fällig: {invoice_data['due_date']}")
    print(f"   Betrag: {invoice_data['total_gross']} {invoice_data['currency']}")
    
    response = requests.post(url, headers=get_headers(), json=payload)
    
    if response.status_code in [200, 201]:
        data = response.json()
        invoice_uuid = data["data"]["uuid"]
        print(f"✅ Rechnung erstellt: UUID = {invoice_uuid}")
        print(f"   Rechnungsnummer: {data['data'].get('invoice_number', 'N/A')}")
        return invoice_uuid
    else:
        print(f"❌ Fehler beim Erstellen: {response.status_code}")
        print(response.text)
        print(f"Request Payload: {json.dumps(payload, indent=2)}")
        return None


def main():
    """Hauptfunktion"""
    print("=" * 60)
    print("Swiss21 - Test Invoice Creation")
    print("=" * 60)
    print()
    
    # 1. Prüfe ob Kunde existiert
    customer_exists = check_customer_exists(INVOICE_DATA["customer"]["customer_number"])
    
    # 2. Hole oder erstelle Kunde
    if customer_exists:
        customer_uuid = get_customer_by_number(INVOICE_DATA["customer"]["customer_number"])
    else:
        customer_uuid = create_customer(INVOICE_DATA["customer"])
    
    if not customer_uuid:
        print("❌ Kunde konnte nicht erstellt/gefunden werden. Abbruch.")
        return
    
    print()
    
    # 3. Erstelle Rechnung
    invoice_uuid = create_invoice(customer_uuid, INVOICE_DATA)
    
    if invoice_uuid:
        print()
        print("=" * 60)
        print("✅ ERFOLG! Rechnung wurde in ABA Ninja erstellt")
        print("=" * 60)
        print(f"Kunde UUID: {customer_uuid}")
        print(f"Rechnung UUID: {invoice_uuid}")
        print(f"Rechnungsnummer: {INVOICE_DATA['invoice_number']}")
        print(f"Auftragsnummer: {INVOICE_DATA['order_reference']}")
        print(f"Betrag: {INVOICE_DATA['total_gross']} {INVOICE_DATA['currency']}")
    else:
        print()
        print("=" * 60)
        print("❌ FEHLER! Rechnung konnte nicht erstellt werden")
        print("=" * 60)


if __name__ == "__main__":
    main()
