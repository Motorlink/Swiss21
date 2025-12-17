#!/usr/bin/env python3
"""
Webisco Test: Erstelle Auftrag 2 über Webisco-Schnittstelle
"""

import requests
import xml.etree.ElementTree as ET

# Webisco-Konfiguration
WEBISCO_HOST = "www.webisco.de"
WEBISCO_PORT = 8228
WEBISCO_URL = f"http://{WEBISCO_HOST}:{WEBISCO_PORT}/createauftrag"

# Lade XML
with open('/home/ubuntu/Swiss21/test/webisco_auftrag_2_test.xml', 'r') as f:
    xml_content = f.read()

print("=" * 80)
print("WEBISCO TEST: Auftrag 2 erstellen")
print("=" * 80)
print(f"URL: {WEBISCO_URL}")
print(f"Kunde: 10000 (MT Transport GmbH)")
print(f"Username: 10000")
print(f"Password: aachen5446")
print("=" * 80)
print("\nXML-Request:")
print(xml_content)
print("=" * 80)

# Sende Request
try:
    response = requests.post(
        WEBISCO_URL,
        data=xml_content.encode('utf-8'),
        headers={
            'Content-Type': 'text/xml; charset=UTF-8',
            'Connection': 'Keep-Alive',
            'Host': f'{WEBISCO_HOST}:{WEBISCO_PORT}'
        },
        timeout=30
    )
    
    print(f"\n✓ Response Status: {response.status_code}")
    print(f"✓ Response Headers:")
    for key, value in response.headers.items():
        print(f"  {key}: {value}")
    
    print(f"\n✓ Response Body:")
    print(response.text)
    
    # Parse Response XML
    try:
        root = ET.fromstring(response.text)
        error_msg = root.get('errormessage', '')
        response_type = root.get('type', '')
        
        print("\n" + "=" * 80)
        if response_type == 'response' and not error_msg:
            print("✅ ERFOLG! Auftrag wurde erstellt!")
        else:
            print(f"❌ FEHLER: {error_msg}")
        print("=" * 80)
        
    except ET.ParseError as e:
        print(f"\n⚠️ Konnte Response XML nicht parsen: {e}")

except requests.exceptions.RequestException as e:
    print(f"\n❌ Request fehlgeschlagen: {e}")
    print("=" * 80)

print("\n✓ Test abgeschlossen")
