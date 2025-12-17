#!/usr/bin/env python3
"""
Swiss21 - Rechnung aus Abisco-Daten in ABA Ninja erstellen
Basierend auf der Struktur der existierenden Rechnung
"""
import requests
import json
from datetime import datetime, timedelta

# API-Konfiguration
API_TOKEN = "eyJhbGciOiJFZERTQSIsImtpZCI6IjFhZThhZDQ1LTIwYjItNGFiMC1iMjBjLWZkNDllNjI5MTg3OCJ9.eyJzdWIiOiIzODIyNGRkNy05ZTRiLTRlNzItYTg2MS0xYzQ0YzA0ZGY4MjAiLCJhdWQiOiIyMWVmYTM4OS1kMDExLTQ1ZjAtYjAxNS1lMGQ5MDE0ODZmYTYiLCJqdGkiOiIxNzc2NzAxMy03ZWUzLTQwNmMtODUzOC03NDMwMGQ1NmRlZjUiLCJpYXQiOjE3NjU5NjQxNzMsIm5iZiI6MTc2NTk2NDE3MywiaXNzIjoiaHR0cHM6XC9cL2FwaS5hYmFuaW5qYS5jaCIsImF6cCI6IkFQSSBUb2tlbiAxNzc2NzAxMy03ZWUzLTQwNmMtODUzOC03NDMwMGQ1NmRlZjUiLCJleHAiOjM0MDgyMjA3OTl9.SUN63U_CrmtJi3up2ihMOa528yXYeQZz73cg_BHWF1mwRLJExZRk_OCkuNld4PDu-nkdQDrx7rlECHEsqDrrAg"
ACCOUNT_UUID = "21efa389-d011-45f0-b015-e0d901486fa6"

# UUIDs aus existierender Rechnung
ADDRESS_UUID = "ad08bb56-373d-48df-b906-e994cb27eaf9"
COMPANY_UUID = "e6592469-5215-481d-b354-2227b75a6ad5"
BANK_ACCOUNT_UUID = "3e2f38d3-c957-4ecc-b1d0-ae563b3fab7b"
UNIT_UUID_PIECE = "fb9abcdc-534c-434f-9ac3-6d51182febc1"  # Stück
VAT_UUID_81 = "1c414ea5-f38e-4d73-ad7b-2a3072c2a4b6"  # 8.1%

# Abisco-Testdaten (aus RE1)
abisco_data = {
    "rechnungsnummer": "RE1",
    "auftragsnummer": "A1",
    "datum": "2025-12-17",
    "faelligkeitsdatum": "2026-01-16",
    "kunde": {
        "kundennummer": "10000",
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
            "mwst_prozent": 8.1,
            "mwst_betrag": 1.14,
            "gesamtpreis": 15.26
        },
        {
            "beschreibung": "Zustellpauschale",
            "menge": 1,
            "einzelpreis": 10.00,
            "mwst_prozent": 0.0,
            "mwst_betrag": 0.00,
            "gesamtpreis": 10.00
        }
    ],
    "gesamtbetrag_netto": 24.12,
    "gesamtbetrag_brutto": 25.26,
    "skonto_prozent": 2,
    "skonto_tage": 10
}

# Positionen erstellen (exakt wie in existierender Rechnung)
positions = []
for idx, pos in enumerate(abisco_data['positionen'], start=1):
    # VAT UUID bestimmen
    vat_uuid = None
    if pos['mwst_prozent'] == 8.1:
        vat_uuid = VAT_UUID_81
    # Für andere MwSt-Sätze müssten wir die UUIDs noch ermitteln
    
    position = {
        "positionNumber": idx,
        "kind": "product",
        "productNumber": pos.get('artikelnummer', str(idx)),
        "productDescription": pos['beschreibung'],
        "quantity": pos['menge'],
        "unitCode": "C62",  # UN/CEFACT Code für "Stück"
        "unitUuid": UNIT_UUID_PIECE,
        "singlePrice": pos['einzelpreis'],
        "positionTotal": pos['gesamtpreis'],
        "discount": {
            "percentage": 0
        }
    }
    
    # VAT nur hinzufügen, wenn vorhanden
    if vat_uuid:
        position["vatUuid"] = vat_uuid
        position["vat"] = {
            "percentage": pos['mwst_prozent'],
            "amount": pos['mwst_betrag']
        }
    
    positions.append(position)

# Rechnung erstellen (exakt wie existierende Struktur)
invoice_data = {
    "documents": [
        {
            "isTemplate": False,
            "currencyCode": "CHF",
            "title": f"Rechnung {abisco_data['rechnungsnummer']}",
            "reference": f"Auftrag {abisco_data['auftragsnummer']}",
            "terms": "",
            "publicNotes": "",
            "footerText": "",
            "receiver": {
                "addressUuid": ADDRESS_UUID,
                "companyUuid": COMPANY_UUID
            },
            "invoiceDate": abisco_data['datum'],
            "dueDate": abisco_data['faelligkeitsdatum'],
            "deliverDate": abisco_data['datum'],
            "deliveryDate": abisco_data['datum'],
            "paymentInstructions": {
                "bankAccountUuid": BANK_ACCOUNT_UUID
            },
            "pricesIncludeVat": False,
            "documentTotal": 0,  # Skonto in Prozent
            "documentDiscount": {
                "percentage": 0
            },
            "positions": positions,
            "cashDiscounts": [
                {
                    "days": abisco_data['skonto_tage'],
                    "percentage": abisco_data['skonto_prozent']
                }
            ]
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
print("RECHNUNG ERSTELLEN IN ABA NINJA (aus Abisco-Daten)")
print("=" * 80)
print(f"Kunde: {abisco_data['kunde']['name']} ({abisco_data['kunde']['kundennummer']})")
print(f"Rechnung: {abisco_data['rechnungsnummer']}")
print(f"Auftrag: {abisco_data['auftragsnummer']}")
print(f"Datum: {abisco_data['datum']}")
print(f"Fällig: {abisco_data['faelligkeitsdatum']}")
print(f"Betrag: CHF {abisco_data['gesamtbetrag_brutto']:.2f}")
print(f"Skonto: {abisco_data['skonto_prozent']}% bei Zahlung innerhalb {abisco_data['skonto_tage']} Tage")
print("=" * 80)
print("\nPositionen:")
for pos in abisco_data['positionen']:
    print(f"  - {pos['beschreibung']}: {pos['menge']} x CHF {pos['einzelpreis']:.2f} = CHF {pos['gesamtpreis']:.2f}")
print("=" * 80)
print("\nRequest Payload:")
print(json.dumps(invoice_data, indent=2, ensure_ascii=False))
print("=" * 80)

response = requests.post(url, headers=headers, json=invoice_data)

print(f"\nResponse Status: {response.status_code}")
print("=" * 80)

if response.status_code == 200 or response.status_code == 201:
    print("✅ ERFOLG!")
    print("\nRechnung erfolgreich in ABA Ninja erstellt!")
    result = response.json()
    print(json.dumps(result, indent=2, ensure_ascii=False))
    
    if 'data' in result and 'documents' in result['data']:
        invoice_uuid = result['data']['documents'][0]['uuid']
        invoice_number = result['data']['documents'][0].get('invoiceNumber', 'N/A')
        print("\n" + "=" * 80)
        print(f"Rechnung UUID: {invoice_uuid}")
        print(f"Rechnungsnummer: {invoice_number}")
        print("=" * 80)
else:
    print("❌ FEHLER!")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")
print("=" * 80)
