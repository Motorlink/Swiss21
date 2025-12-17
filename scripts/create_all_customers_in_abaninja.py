#!/usr/bin/env python3
"""
Erstellt alle Kunden aus der CSV-Datei systematisch in ABA Ninja.
Speichert UUID-Mapping für spätere Verwendung.
"""

import requests
import json
import csv
import time
from pathlib import Path

# API Konfiguration
API_TOKEN = "eyJhbGciOiJFZERTQSIsImtpZCI6IjFhZThhZDQ1LTIwYjItNGFiMC1iMjBjLWZkNDllNjI5MTg3OCJ9.eyJzdWIiOiIzODIyNGRkNy05ZTRiLTRlNzItYTg2MS0xYzQ0YzA0ZGY4MjAiLCJhdWQiOiIyMWVmYTM4OS1kMDExLTQ1ZjAtYjAxNS1lMGQ5MDE0ODZmYTYiLCJqdGkiOiIxNzc2NzAxMy03ZWUzLTQwNmMtODUzOC03NDMwMGQ1NmRlZjUiLCJpYXQiOjE3NjU5NjQxNzMsIm5iZiI6MTc2NTk2NDE3MywiaXNzIjoiaHR0cHM6XC9cL2FwaS5hYmFuaW5qYS5jaCIsImF6cCI6IkFQSSBUb2tlbiAxNzc2NzAxMy03ZWUzLTQwNmMtODUzOC03NDMwMGQ1NmRlZjUiLCJleHAiOjM0MDgyMjA3OTl9.SUN63U_CrmtJi3up2ihMOa528yXYeQZz73cg_BHWF1mwRLJExZRk_OCkuNld4PDu-nkdQDrx7rlECHEsqDrrAg"
ACCOUNT_UUID = "21efa389-d011-45f0-b015-e0d901486fa6"
API_URL = f"https://api.abaninja.ch/accounts/{ACCOUNT_UUID}/addresses/v2/addresses"

# Pfade
CSV_PATH = "/home/ubuntu/upload/kundenliste.csv"
MAPPING_PATH = "/home/ubuntu/Swiss21/data/customer_uuid_mapping.json"
LOG_PATH = "/home/ubuntu/Swiss21/logs/customer_creation.log"

# Erstelle Verzeichnisse
Path(MAPPING_PATH).parent.mkdir(parents=True, exist_ok=True)
Path(LOG_PATH).parent.mkdir(parents=True, exist_ok=True)

# Kanton-Mapping (PLZ -> Kanton)
PLZ_KANTON_MAP = {
    "8000": "ZH", "8001": "ZH", "8002": "ZH", "8003": "ZH", "8004": "ZH",
    "8005": "ZH", "8006": "ZH", "8008": "ZH", "8032": "ZH", "8050": "ZH",
    "8102": "ZH", "8153": "ZH", "8600": "ZH", "8610": "ZH", "8700": "ZH",
    "8422": "ZH", "8302": "ZH",
    "6052": "NW",  # Hergiswil
    "8152": "ZH",  # Opfikon/Glattbrugg
}

def get_kanton_from_plz(plz):
    """Ermittelt Kanton aus PLZ."""
    if not plz:
        return "ZH"  # Default
    
    # Direkte Zuordnung
    if plz in PLZ_KANTON_MAP:
        return PLZ_KANTON_MAP[plz]
    
    # Fallback: Erste 2 Ziffern
    plz_prefix = plz[:2] if len(plz) >= 2 else plz
    
    if plz_prefix in ["80", "81", "82", "83", "84", "85", "86", "87", "88", "89"]:
        return "ZH"
    elif plz_prefix in ["60", "61"]:
        return "NW"
    elif plz_prefix in ["30", "31", "32"]:
        return "BE"
    elif plz_prefix in ["40", "41", "42"]:
        return "BL"
    elif plz_prefix in ["10", "11", "12"]:
        return "GE"
    
    return "ZH"  # Default Zürich

def create_customer(customer_data):
    """Erstellt einen Kunden in ABA Ninja."""
    
    headers = {
        "Authorization": f"Bearer {API_TOKEN}",
        "Content-Type": "application/json"
    }
    
    # Kontakte vorbereiten
    contacts = []
    if customer_data.get('email'):
        contacts.append({
            "type": "email",
            "value": customer_data['email'],
            "primary": True
        })
    
    if customer_data.get('telefon'):
        contacts.append({
            "type": "phone",
            "value": customer_data['telefon'],
            "primary": False
        })
    
    if customer_data.get('mobil'):
        contacts.append({
            "type": "mobile",
            "value": customer_data['mobil'],
            "primary": False
        })
    
    # Adresse vorbereiten
    addresses = []
    
    # Prüfe ob Adressdaten vorhanden sind
    if customer_data.get('ort') or customer_data.get('plz'):
        kanton = get_kanton_from_plz(customer_data.get('plz', ''))
        
        address = {
            "city": customer_data.get('ort') or 'Unbekannt',
            "zip_code": customer_data.get('plz') or '0000',
            "country_code": customer_data.get('land', 'CH'),
            "state": kanton
        }
        
        # Straße optional hinzufügen
        if customer_data.get('strasse'):
            address['street_number'] = customer_data['strasse']
        
        addresses.append(address)
    else:
        # Dummy-Adresse wenn keine Daten vorhanden
        addresses.append({
            "city": "Unbekannt",
            "zip_code": "0000",
            "country_code": "CH",
            "state": "ZH"
        })
    
    # Payload erstellen
    payload = {
        "type": "company",
        "customer_number": customer_data['kundennummer'],
        "name": customer_data['name'],
        "currency_code": "CHF",
        "language": "de",
        "payment_terms": 30
    }
    
    # Optionale Felder
    if customer_data.get('uid'):
        payload['id_number'] = customer_data['uid']
    
    if contacts:
        payload['contacts'] = contacts
    
    if addresses:
        payload['addresses'] = addresses
    
    # API-Request
    response = requests.post(API_URL, headers=headers, json=payload)
    
    return response

def load_customers_from_csv():
    """Lädt Kunden aus CSV-Datei."""
    customers = []
    
    with open(CSV_PATH, 'r', encoding='iso-8859-1') as f:
        reader = csv.DictReader(f, delimiter=';')
        
        for row in reader:
            kundennummer = row.get('Nummer', '').strip()
            name = row.get('Name', '').strip()
            
            # Überspringe Kunden ohne Nummer oder Name
            if not kundennummer or not name:
                continue
            
            # Überspringe Kunde 10000 (existiert bereits)
            if kundennummer == "10000":
                print(f"⊘ Überspringe {kundennummer} (existiert bereits)")
                continue
            
            # Land-Feld bereinigen
            land = row.get('Land', '').strip()
            if not land or land == '-' or land == 'Schweiz':
                land = 'CH'
            
            customers.append({
                'kundennummer': kundennummer,
                'name': name,
                'ansprechpartner': row.get('Name des Ansprechpartner', '').strip(),
                'email': row.get('E-Mail', '').strip(),
                'telefon': row.get('Telefon (gesch.)', '').strip(),
                'mobil': row.get('Mobil', '').strip(),
                'strasse': row.get('Straße', '').strip(),
                'plz': row.get('PLZ', '').strip(),
                'ort': row.get('Ort', '').strip(),
                'land': land,
                'uid': row.get('USt-IdNr.', '').strip()
            })
    
    return customers

def main():
    """Hauptfunktion."""
    print("=" * 80)
    print("SYSTEMATISCHES ERSTELLEN ALLER KUNDEN IN ABA NINJA")
    print("=" * 80)
    print()
    
    # Lade Kunden aus CSV
    print("📋 Lade Kunden aus CSV...")
    customers = load_customers_from_csv()
    print(f"✓ {len(customers)} Kunden geladen\n")
    
    # UUID-Mapping
    uuid_mapping = {}
    
    # Lade existierendes Mapping (falls vorhanden)
    if Path(MAPPING_PATH).exists():
        with open(MAPPING_PATH, 'r') as f:
            uuid_mapping = json.load(f)
        print(f"✓ {len(uuid_mapping)} existierende UUIDs geladen\n")
    
    # Log-Datei
    log_entries = []
    
    # Erstelle Kunden systematisch
    success_count = 0
    error_count = 0
    skipped_count = 0
    
    for i, customer in enumerate(customers, 1):
        kundennummer = customer['kundennummer']
        name = customer['name']
        
        print(f"[{i}/{len(customers)}] Kunde {kundennummer}: {name}")
        
        # Überspringe wenn bereits vorhanden
        if kundennummer in uuid_mapping:
            print(f"  ⊘ Bereits vorhanden (UUID: {uuid_mapping[kundennummer]['uuid'][:8]}...)")
            skipped_count += 1
            log_entries.append({
                "kundennummer": kundennummer,
                "name": name,
                "status": "skipped",
                "reason": "already_exists"
            })
            print()
            continue
        
        # Erstelle Kunde
        try:
            response = create_customer(customer)
            
            if response.status_code == 201:
                data = response.json()['data']
                uuid = data['uuid']
                
                # Speichere UUID
                uuid_mapping[kundennummer] = {
                    "uuid": uuid,
                    "name": name,
                    "company_name": data.get('company_name', name)
                }
                
                print(f"  ✓ Erstellt! UUID: {uuid}")
                success_count += 1
                
                log_entries.append({
                    "kundennummer": kundennummer,
                    "name": name,
                    "status": "success",
                    "uuid": uuid
                })
                
                # Speichere Mapping nach jedem Erfolg
                with open(MAPPING_PATH, 'w') as f:
                    json.dump(uuid_mapping, f, indent=2, ensure_ascii=False)
                
            elif response.status_code == 409:
                print(f"  ⚠ Konflikt: Kundennummer bereits vergeben")
                error_count += 1
                log_entries.append({
                    "kundennummer": kundennummer,
                    "name": name,
                    "status": "error",
                    "error": "duplicate_customer_number"
                })
            else:
                error_msg = response.json().get('message', response.text)
                print(f"  ✗ Fehler {response.status_code}: {error_msg}")
                error_count += 1
                log_entries.append({
                    "kundennummer": kundennummer,
                    "name": name,
                    "status": "error",
                    "error": error_msg
                })
        
        except Exception as e:
            print(f"  ✗ Exception: {str(e)}")
            error_count += 1
            log_entries.append({
                "kundennummer": kundennummer,
                "name": name,
                "status": "error",
                "error": str(e)
            })
        
        print()
        
        # Kurze Pause zwischen Requests
        time.sleep(0.5)
    
    # Zusammenfassung
    print("=" * 80)
    print("ZUSAMMENFASSUNG")
    print("=" * 80)
    print(f"✓ Erfolgreich erstellt: {success_count}")
    print(f"⊘ Übersprungen:        {skipped_count}")
    print(f"✗ Fehler:              {error_count}")
    print(f"━ Gesamt:              {len(customers)}")
    print()
    
    # Speichere Log
    with open(LOG_PATH, 'w') as f:
        json.dump({
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "summary": {
                "total": len(customers),
                "success": success_count,
                "skipped": skipped_count,
                "error": error_count
            },
            "entries": log_entries
        }, f, indent=2, ensure_ascii=False)
    
    print(f"✓ UUID-Mapping gespeichert: {MAPPING_PATH}")
    print(f"✓ Log gespeichert: {LOG_PATH}")
    print()

if __name__ == "__main__":
    main()
