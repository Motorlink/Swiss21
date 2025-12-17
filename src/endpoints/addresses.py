"""
Swiss21 - ABA Ninja API Integration
Addresses Endpoint Module

Dieses Modul implementiert alle Endpoints für die Adressverwaltung
(Unternehmen und Personen).
"""

from typing import Optional, Dict, Any, List


class AddressesEndpoint:
    """
    Endpoint-Handler für Adressverwaltung.
    
    Verwaltet Unternehmens- und Personenadressen in ABA Ninja.
    """
    
    def __init__(self, client):
        """
        Initialisiert den Addresses-Endpoint.
        
        Args:
            client: AbaNinjaClient-Instanz
        """
        self.client = client
        self.account_uuid = client.config.account_uuid
    
    # ========== Customer Number Validation ==========
    
    def check_customer_number(
        self,
        customer_number: str,
        address_uuid: Optional[str] = None
    ) -> bool:
        """
        Prüft, ob eine Kundennummer bereits verwendet wird.
        
        Args:
            customer_number: Zu prüfende Kundennummer
            address_uuid: Adressen-UUID zum Ausschließen (optional)
            
        Returns:
            True wenn Nummer verfügbar, False wenn bereits verwendet
        """
        endpoint = f"accounts/{self.account_uuid}/addresses/v2/check-customer-number"
        params = {'customerNumber': customer_number}
        
        if address_uuid:
            params['addressUuid'] = address_uuid
        
        try:
            self.client.get(endpoint, params=params)
            return True  # 200 = Nummer verfügbar
        except Exception:
            return False  # 400 = Nummer bereits verwendet
    
    # ========== Companies (Unternehmen) ==========
    
    def get_companies(
        self,
        page: Optional[int] = None,
        limit: Optional[int] = None,
        tags: Optional[List[str]] = None,
        auto_paginate: bool = False
    ) -> Dict[str, Any]:
        """
        Ruft eine Liste aller Unternehmensadressen ab.
        
        Args:
            page: Seitennummer für Pagination
            limit: Anzahl Einträge pro Seite
            tags: Liste von Tags zum Filtern
            auto_paginate: Wenn True, werden alle Seiten automatisch abgerufen
            
        Returns:
            Dictionary mit Unternehmensdaten und Pagination-Metadaten
        """
        endpoint = f"accounts/{self.account_uuid}/addresses/v2/companies"
        params = {}
        
        if page:
            params['page'] = page
        if tags:
            params['tags[]'] = tags
        
        return self.client.get_paginated(endpoint, params=params, limit=limit, auto_paginate=auto_paginate)
    
    def get_company(self, company_uuid: str) -> Dict[str, Any]:
        """
        Ruft ein einzelnes Unternehmen ab.
        
        Args:
            company_uuid: UUID des Unternehmens
            
        Returns:
            Unternehmensdaten
        """
        endpoint = f"accounts/{self.account_uuid}/addresses/v2/companies/{company_uuid}"
        return self.client.get(endpoint)
    
    def update_company(self, company_uuid: str, company_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Aktualisiert ein Unternehmen.
        
        Args:
            company_uuid: UUID des Unternehmens
            company_data: Zu aktualisierende Daten
            
        Returns:
            Aktualisierte Unternehmensdaten
        """
        endpoint = f"accounts/{self.account_uuid}/addresses/v2/companies/{company_uuid}"
        
        # Stelle sicher, dass type und uuid gesetzt sind
        if 'type' not in company_data:
            company_data['type'] = 'company'
        if 'uuid' not in company_data:
            company_data['uuid'] = company_uuid
        
        return self.client.patch(endpoint, data=company_data)
    
    def delete_company(self, company_uuid: str) -> Dict[str, Any]:
        """
        Löscht ein Unternehmen.
        
        Args:
            company_uuid: UUID des Unternehmens
            
        Returns:
            Bestätigung der Löschung
        """
        endpoint = f"accounts/{self.account_uuid}/addresses/v2/companies/{company_uuid}"
        return self.client.delete(endpoint)
    
    # ========== Persons (Personen) ==========
    
    def get_persons(
        self,
        page: Optional[int] = None,
        limit: Optional[int] = None,
        tags: Optional[List[str]] = None,
        auto_paginate: bool = False
    ) -> Dict[str, Any]:
        """
        Ruft eine Liste aller Personenadressen ab.
        
        Args:
            page: Seitennummer für Pagination
            limit: Anzahl Einträge pro Seite
            tags: Liste von Tags zum Filtern
            auto_paginate: Wenn True, werden alle Seiten automatisch abgerufen
            
        Returns:
            Dictionary mit Personendaten und Pagination-Metadaten
        """
        endpoint = f"accounts/{self.account_uuid}/addresses/v2/persons"
        params = {}
        
        if page:
            params['page'] = page
        if tags:
            params['tags[]'] = tags
        
        return self.client.get_paginated(endpoint, params=params, limit=limit, auto_paginate=auto_paginate)
    
    def get_person(self, person_uuid: str) -> Dict[str, Any]:
        """
        Ruft eine einzelne Person ab.
        
        Args:
            person_uuid: UUID der Person
            
        Returns:
            Personendaten
        """
        endpoint = f"accounts/{self.account_uuid}/addresses/v2/persons/{person_uuid}"
        return self.client.get(endpoint)
    
    def update_person(self, person_uuid: str, person_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Aktualisiert eine Person.
        
        Args:
            person_uuid: UUID der Person
            person_data: Zu aktualisierende Daten
            
        Returns:
            Aktualisierte Personendaten
        """
        endpoint = f"accounts/{self.account_uuid}/addresses/v2/persons/{person_uuid}"
        
        # Stelle sicher, dass type und uuid gesetzt sind
        if 'type' not in person_data:
            person_data['type'] = 'person'
        if 'uuid' not in person_data:
            person_data['uuid'] = person_uuid
        
        return self.client.patch(endpoint, data=person_data)
    
    def delete_person(self, person_uuid: str) -> Dict[str, Any]:
        """
        Löscht eine Person.
        
        Args:
            person_uuid: UUID der Person
            
        Returns:
            Bestätigung der Löschung
        """
        endpoint = f"accounts/{self.account_uuid}/addresses/v2/persons/{person_uuid}"
        return self.client.delete(endpoint)
