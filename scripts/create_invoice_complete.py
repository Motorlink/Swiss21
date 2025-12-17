#!/usr/bin/env python3
"""
Swiss21 - Rechnung aus Abisco-Daten in ABA Ninja erstellen
"""
import requests
import json
from datetime import datetime, timedelta

# API-Konfiguration
API_TOKEN = "eyJhbGciOiJFZERTQSIsImtpZCI6IjFhZThhZDQ1LTIwYjItNGFiMC1iMjBjLWZkNDllNjI5MTg3OCJ9.eyJzdWIiOiIzODIyNGRkNy05ZTRiLTRlNzItYTg2MS0xYzQ0YzA0ZGY4MjAiLCJhdWQiOiIyMWVmYTM4OS1kMDExLTQ1ZjAtYjAxNS1lMGQ5MDE0ODZmYTYiLCJqdGkiOiIxNzc2NzAxMy03ZWUzLTQwNmMtODUzOC03NDMwMGQ1NmRlZjUiLCJpYXQiOjE3NjU5NjQxNzMsIm5iZiI6MTc2NTk2NDE3MywiaXNzIjoiaHR0cHM6XC9cL2FwaS5hYmFuaW5qYS5jaCIsImF6cCI6IkFQSSBUb2tlbiAxNzc2NzAxMy03ZWUzLTQwNmMtODUzOC03NDMwMGQ1NmRlZjUiLCJleHAiOjM0MDgyMjA3OTl9.SUN63U_CrmtJi3up2ihMOa528yXYeQZz73cg_BHWF1mwRLJExZRk_OCkuNld4PDu-nkdQDrx7rlECHEsqDrrAg"
ACCOUNT_UUID = "21efa389-d011-45f0-b015-e0d901486fa6"
CUSTOMER_UUID = "e6592469-5215-481d-b354-2227b75a6ad5"  # MT Transport GmbH
UBS_IBAN = "CH2200273273313689010"

# Abisco-Testdaten (aus RE1)
abisco_data = {
    "rechnungsnummer": "RE1",
    "auftragsnummer": "A1",
    "datum": "2025-12-17",
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
            "einzelpreis": 14.12,
            "mwst": 8.1
        },
        {
            "beschreibung": "Zustellpauschale",
            "menge": 1,
            "einzelpreis": 10.00,
            "mwst": 0.0
        }
    ],
    "gesamtbetrag": 25.26
}

# Zahlungsbedingungen
today = datetime.now().strftime("%Y-%m-%d")
payment_date = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")

# Positionen erstellen
positions = []
for idx, pos in enumerate(abisco_data['positionen'], start=1):
    # MwSt-Typ bestimmen
    vat_type = "vat0"
    if pos['mwst'] == 8.1:
        vat_type = "vat111"  # 8.1% MwSt
    elif pos['mwst'] == 7.7:
        vat_type = "vat11"   # 7.7% MwSt
    elif pos['mwst'] == 2.5:
        vat_type = "vat1"    # 2.5% MwSt
    
    position = {
        "kind": "product",
        "positionNumber": idx,
        "productDescription": pos['beschreibung'],
        "quantity": pos['menge'],
        "singlePrice": pos['einzelpreis'],
        "unit": "pcs",
        "vat": {
            "type": vat_type,
            "percentage": pos['mwst']
        }
    }
    
    # Artikelnummer hinzufügen, falls vorhanden
    if 'artikelnummer' in pos:
        position["productNumber"] = pos['artikelnummer']
    
    positions.append(position)

# Rechnung erstellen
invoice_data = {
    "documents": [
        {
            "isTemplate": False,
            "receiver": {
                "companyUuid": CUSTOMER_UUID
            },
            "positions": positions,
            "currencyCode": "CHF",
            "pricesIncludeVat": False,
            "title": f"Rechnung {abisco_data['rechnungsnummer']} (Auftrag {abisco_data['auftragsnummer']})",
            "invoiceDate": abisco_data['datum'],
            "deliveryDate": abisco_data['datum'],
            "paymentDate": payment_date,
            "paymentInstructions": {
                "type": "qrBill",
                "iban": UBS_IBAN,
                "text": f"Rechnung {abisco_data['rechnungsnummer']} - Auftrag {abisco_data['auftragsnummer']}"
            },
            "documentTotal": 0
        }
    ]
}

# API-Request
url = f"https://api.abaninja.ch/accounts/{ACCOUNT_UUID}/documents/v2/invoices"
headers = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json"
}

print("=" * 80)
print("RECHNUNG ERSTELLEN IN ABA NINJA")
print("=" * 80)
print(f"Kunde: {abisco_data['kunde']['name']}")
print(f"Rechnung: {abisco_data['rechnungsnummer']}")
print(f"Auftrag: {abisco_data['auftragsnummer']}")
print(f"Betrag: CHF {abisco_data['gesamtbetrag']}")
print(f"IBAN: {UBS_IBAN}")
print("=" * 80)
print("\nRequest Payload:")
print(json.dumps(invoice_data, indent=2, ensure_ascii=False))
print("=" * 80)

response = requests.post(url, headers=headers, json=invoice_data)

print(f"\nResponse Status: {response.status_code}")
print("=" * 80)

if response.status_code == 200 or response.status_code == 201:
    print("✅ ERFOLG!")
    print("\nRechnung erfolgreich erstellt!")
    result = response.json()
    print(json.dumps(result, indent=2, ensure_ascii=False))
else:
    print("❌ FEHLER!")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")
print("=" * 80)
