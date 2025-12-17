#!/usr/bin/env python3
"""
Swiss21 - Rechnung in ABA Ninja erstellen
Basierend auf Abisco-Testdaten
"""

import requests
import json
from datetime import datetime, timedelta

# Konfiguration
API_BASE = "https://api.abaninja.ch"
API_TOKEN = "eyJhbGciOiJFZERTQSIsImtpZCI6IjFhZThhZDQ1LTIwYjItNGFiMC1iMjBjLWZkNDllNjI5MTg3OCJ9.eyJzdWIiOiIzODIyNGRkNy05ZTRiLTRlNzItYTg2MS0xYzQ0YzA0ZGY4MjAiLCJhdWQiOiIyMWVmYTM4OS1kMDExLTQ1ZjAtYjAxNS1lMGQ5MDE0ODZmYTYiLCJqdGkiOiIxNzc2NzAxMy03ZWUzLTQwNmMtODUzOC03NDMwMGQ1NmRlZjUiLCJpYXQiOjE3NjU5NjQxNzMsIm5iZiI6MTc2NTk2NDE3MywiaXNzIjoiaHR0cHM6XC9cL2FwaS5hYmFuaW5qYS5jaCIsImF6cCI6IkFQSSBUb2tlbiAxNzc2NzAxMy03ZWUzLTQwNmMtODUzOC03NDMwMGQ1NmRlZjUiLCJleHAiOjM0MDgyMjA3OTl9.SUN63U_CrmtJi3up2ihMOa528yXYeQZz73cg_BHWF1mwRLJExZRk_OCkuNld4PDu-nkdQDrx7rlECHEsqDrrAg"
ACCOUNT_UUID = "21efa389-d011-45f0-b015-e0d901486fa6"
CUSTOMER_UUID = "e6592469-5215-481d-b354-2227b75a6ad5"  # MT Transport GmbH

headers = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json"
}

# Abisco-Daten (aus Testrechnung RE1)
# Konvertiert von EUR zu CHF (Kurs 1:1 für Test)
abisco_data = {
    "rechnungsnummer": "RE1",
    "auftragsnummer": "A1",
    "datum": "2025-12-17",
    "faelligkeitsdatum": "2025-12-17",
    "kunde": {
        "name": "MT Transport GmbH",
        "strasse": "Lorenweg 22",
        "plz": "8610",
        "ort": "Uster",
        "land": "CH",
        "email": "info@mt-transport.ch"
    },
    "positionen": [
        {
            "beschreibung": "Ölfilter",
            "artikelnummer": "HU7020Z",
            "menge": 1,
            "einzelpreis": 14.12,  # EUR -> CHF
            "mwst": 8.1
        },
        {
            "beschreibung": "Zustellpauschale",
            "menge": 1,
            "einzelpreis": 10.00,  # EUR -> CHF
            "mwst": 0.0
        }
    ],
    "gesamtbetrag": 25.26  # EUR -> CHF
}

# Rechnung erstellen
today = datetime.now().strftime("%Y-%m-%d")
payment_date = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")

invoice_data = {
    "documents": [
        {
            "isTemplate": False,
            "receiver": {
                "address_uuid": CUSTOMER_UUID
            },
            "positions": [],
            "currencyCode": "CHF",
            "pricesIncludeVat": False,
            "title": f"Rechnung {abisco_data['rechnungsnummer']} (Auftrag {abisco_data['auftragsnummer']})",
            "invoiceDate": abisco_data['datum'],
            "deliveryDate": abisco_data['datum'],
            "paymentDate": payment_date,
            "paymentInstructions": {
                "type": "qrBill",
                "iban": "CH2200273273313689010",
                "text": f"Rechnung {abisco_data['rechnungsnummer']} - Auftrag {abisco_data['auftragsnummer']}"
            },
            "documentTotal": 0
        }
    ]
}

# Positionen hinzufügen
position_number = 1
for pos in abisco_data['positionen']:
        {
            "kind": "product",
            "type": "product",
            "positionNumber": pos_num,number,
        "productDescription": pos['beschreibung'],
        "quantity": pos['menge'],
        "unitPrice": pos['einzelpreis'],
        "unit": "pcs",
        "vat": {
            "type": "vat111" if pos['mwst'] > 0 else "vat0",
            "percentage": pos['mwst']
        }
    }
    
    # Artikelnummer falls vorhanden
    if 'artikelnummer' in pos:
        position["productNumber"] = pos['artikelnummer']
    
    invoice_data['documents'][0]['positions'].append(position)
    position_number += 1

print("=" * 80)
print("SWISS21 - Rechnung in ABA Ninja erstellen")
print("=" * 80)
print(f"\nAbisco-Rechnung: {abisco_data['rechnungsnummer']}")
print(f"Abisco-Auftrag: {abisco_data['auftragsnummer']}")
print(f"Kunde: {abisco_data['kunde']['name']}")
print(f"Gesamtbetrag: CHF {abisco_data['gesamtbetrag']:.2f}")
print(f"\nPositionen: {len(abisco_data['positionen'])}")
for i, pos in enumerate(abisco_data['positionen'], 1):
    print(f"  {i}. {pos['beschreibung']} - CHF {pos['einzelpreis']:.2f} ({pos['mwst']}% MwSt)")

print("\n" + "=" * 80)
print("Sende Rechnung an ABA Ninja API...")
print("=" * 80)

# Request senden
url = f"{API_BASE}/accounts/{ACCOUNT_UUID}/documents/v2/invoices"
print(f"\nURL: {url}")
print(f"\nRequest Body:")
print(json.dumps(invoice_data, indent=2))

try:
    response = requests.post(url, headers=headers, json=invoice_data, timeout=60)
    
    print(f"\n" + "=" * 80)
    print(f"Response Status: {response.status_code}")
    print("=" * 80)
    
    if response.status_code in [201, 202]:
        result = response.json()
        print("\n✅ ERFOLG! Rechnung erstellt!")
        print(f"\nResponse:")
        print(json.dumps(result, indent=2))
        
        if 'data' in result and 'uuid' in result['data']:
            invoice_uuid = result['data']['uuid']
            print(f"\n🎉 Rechnung UUID: {invoice_uuid}")
            print(f"📄 Rechnung in ABA Ninja: https://app.abaninja.ch/invoices/{invoice_uuid}")
    else:
        print(f"\n❌ FEHLER!")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        
except requests.exceptions.Timeout:
    print("\n⏱️ Request Timeout - Die API braucht länger als erwartet.")
    print("Die Rechnung könnte trotzdem erstellt worden sein.")
    print("Bitte prüfe das ABA Ninja Dashboard.")
except Exception as e:
    print(f"\n❌ Fehler: {e}")

print("\n" + "=" * 80)
