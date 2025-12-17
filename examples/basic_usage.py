"""
Swiss21 - ABA Ninja API Integration
Basic Usage Example
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.client import AbaNinjaClient
from src.config import Config
from src.exceptions import AbaNinjaException


def main():
    print("=== Swiss21 - ABA Ninja API Integration ===\n")
    
    try:
        client = AbaNinjaClient(
            api_token="YOUR_JWT_TOKEN_HERE",
            account_uuid="YOUR_ACCOUNT_UUID_HERE"
        )
        
        print("Client erfolgreich initialisiert\n")
        
        # Beispiel: Unternehmensadressen abrufen
        companies_response = client.addresses.get_companies(limit=10)
        companies = companies_response.get('data', [])
        
        print(f"Anzahl Unternehmen: {len(companies)}")
        
    except AbaNinjaException as e:
        print(f"API-Fehler: {e.message}")


if __name__ == "__main__":
    main()
