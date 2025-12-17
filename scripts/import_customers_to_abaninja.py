#!/usr/bin/env python3
"""
Importiert alle Kunden aus der CSV systematisch in ABA Ninja
"""
import requests
import json
import csv
import time

# API-Konfiguration
API_TOKEN = "eyJhbGciOiJFZERTQSIsImtpZCI6IjFhZThhZDQ1LTIwYjItNGFiMC1iMjBjLWZkNDllNjI5MTg3OCJ9.eyJzdWIiOiIzODIyNGRkNy05ZTRiLTRlNzItYTg2MS0xYzQ0YzA0ZGY4MjAiLCJhdWQiOiIyMWVmYTM4OS1kMDExLTQ1ZjAtYjAxNS1lMGQ5MDE0ODZmYTYiLCJqdGkiOiIxNzc2NzAxMy03ZWUzLTQwNmMtODUzOC03NDMwMGQ1NmRlZjUiLCJpYXQiOjE3NjU5NjQxNzMsIm5iZiI6MTc2NTk2NDE3MywiaXNzIjoiaHR0cHM6XC9cL2FwaS5hYmFuaW5qYS5jaCIsImF6cCI6IkFQSSBUb2tlbiAxNzc2NzAxMy03ZWUzLTQwNmMtODUzOC03NDMwMGQ1NmRlZjUiLCJleHAiOjM0MDgyMjA3OTl9.SUN63U_CrmtJi3up2ihMOa528yXYeQZz73cg_BHWF1mwRLJExZRk_OCkuNld4PDu-nkdQDrx7rlECHEsqDrrAg"
ACCOUNT_UUID = "21efa389-d011-45f0-b015-e0d901486fa6"

headers = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json"
}

print("=" * 80)
print("SCHRITT 1: Kundendaten aus CSV laden")
print("=" * 80)

kunden = []
with open('/home/ubuntu/upload/kundenliste.csv', 'r', encoding='ISO-8859-1') as f:
    reader = csv.DictReader(f, delimiter=';')
    
    for row in reader:
        kunde_nr = row.get('Nummer', '').strip()
        
        if not kunde_nr:
            continue
            
        kunden.append({
            'kundennummer': kunde_nr,
            'name': row.get('Name', '').strip(),
            'ansprechpartner': row.get('Name des Ansprechpartner', '').strip(),
            'email': row.get('E-Mail', '').strip(),
            'telefon': row.get('Telefon (gesch.)', '').strip(),
            'mobil': row.get('Mobil', '').strip(),
            'strasse': row.get('Straße', '').strip(),
            'plz': row.get('PLZ', '').strip(),
            'ort': row.get('Ort', '').strip(),
            'land': row.get('Land', '').strip() or 'Schweiz',
            'uid': row.get('USt-IdNr.', '').strip(),
        })

print(f"✓ {len(kunden)} Kunden aus CSV geladen")

print("\n" + "=" * 80)
print("SCHRITT 2: Prüfe welche Kunden bereits in ABA Ninja existieren")
print("=" * 80)

# Hole alle existierenden Kunden
url = f"https://api.abaninja.ch/accounts/{ACCOUNT_UUID}/addresses/v2/companies"
response = requests.get(url, headers=headers)

existierende_kunden = {}
if response.status_code == 200:
    result = response.json()
    if 'data' in result and 'addresses' in result['data']:
        for addr in result['data']['addresses']:
            customer_number = addr.get('customer_number', '')
            if customer_number:
                existierende_kunden[customer_number] = {
                    'addressUuid': addr.get('uuid'),
                    'companyUuid': addr.get('company', {}).get('uuid'),
                    'name': addr.get('company', {}).get('name', '')
                }
    print(f"✓ {len(existierende_kunden)} Kunden bereits in ABA Ninja vorhanden")
else:
    print(f"⚠ Fehler beim Abrufen: {response.status_code}")
    print(response.text)

print("\n" + "=" * 80)
print("SCHRITT 3: Erstelle fehlende Kunden in ABA Ninja")
print("=" * 80)

uuid_mapping = {}
erfolge = 0
fehler = 0

for kunde in kunden:
    kunde_nr = kunde['kundennummer']
    
    # Prüfe ob Kunde bereits existiert
    if kunde_nr in existierende_kunden:
        print(f"\n✓ Kunde {kunde_nr} ({kunde['name']}) existiert bereits")
        uuid_mapping[kunde_nr] = existierende_kunden[kunde_nr]
        continue
    
    print(f"\n→ Erstelle Kunde {kunde_nr}: {kunde['name']}")
    
    # Erstelle Adresse/Firma in ABA Ninja
    payload = {
        "addresses": [
            {
                "customer_number": kunde_nr,
                "company": {
                    "name": kunde['name']
                },
                "street": kunde['strasse'],
                "zip": kunde['plz'],
                "city": kunde['ort'],
                "country_code": "CH",
                "email": kunde['email'],
                "phone": kunde['telefon'] or kunde['mobil'],
                "vat_identifier": kunde['uid']
            }
        ]
    }
    
    url = f"https://api.abaninja.ch/accounts/{ACCOUNT_UUID}/addresses/v2/companies"
    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code in [200, 201]:
        result = response.json()
        if 'data' in result and 'addresses' in result['data']:
            addr = result['data']['addresses'][0]
            uuid_mapping[kunde_nr] = {
                'addressUuid': addr.get('uuid'),
                'companyUuid': addr.get('company', {}).get('uuid'),
                'name': kunde['name']
            }
            print(f"  ✓ Erfolgreich erstellt!")
            print(f"    - addressUuid: {addr.get('uuid')}")
            print(f"    - companyUuid: {addr.get('company', {}).get('uuid')}")
            erfolge += 1
        else:
            print(f"  ⚠ Unerwartete Antwort-Struktur")
            fehler += 1
    else:
        print(f"  ❌ Fehler {response.status_code}")
        print(f"  {response.text}")
        fehler += 1
    
    # Kurze Pause zwischen Requests
    time.sleep(0.5)

print("\n" + "=" * 80)
print("SCHRITT 4: Speichere UUID-Mapping")
print("=" * 80)

# Speichere Mapping als JSON
with open('/home/ubuntu/Swiss21/data/customer_uuid_mapping.json', 'w') as f:
    json.dump(uuid_mapping, f, indent=2, ensure_ascii=False)

print(f"✓ UUID-Mapping gespeichert: data/customer_uuid_mapping.json")

print("\n" + "=" * 80)
print("ZUSAMMENFASSUNG")
print("=" * 80)
print(f"Kunden gesamt: {len(kunden)}")
print(f"Bereits vorhanden: {len(existierende_kunden)}")
print(f"Neu erstellt: {erfolge}")
print(f"Fehler: {fehler}")
print(f"UUID-Mapping gespeichert: {len(uuid_mapping)} Kunden")
print("=" * 80)
