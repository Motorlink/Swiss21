"""
Swiss21 - ABA Ninja API Integration
Main API Client

Dieses Modul implementiert den Haupt-API-Client mit Authentifizierung,
Request-Handling und Fehlerbehandlung.
"""

import requests
import time
from typing import Optional, Dict, Any, List
from .config import Config
from .exceptions import (
    AbaNinjaException,
    AuthenticationError,
    AuthorizationError,
    NotFoundError,
    ConflictError,
    BadRequestError,
    RateLimitError,
    ServerError
)
from .endpoints.addresses import AddressesEndpoint


class AbaNinjaClient:
    """
    Haupt-Client für die ABA Ninja API.
    
    Dieser Client verwaltet die Authentifizierung, HTTP-Requests und
    Fehlerbehandlung für alle API-Endpoints.
    """
    
    def __init__(self, config: Optional[Config] = None, api_token: str = None, account_uuid: str = None):
        """
        Initialisiert den ABA Ninja API Client.
        
        Args:
            config: Config-Objekt (optional)
            api_token: JWT Bearer Token (wird verwendet wenn config nicht gesetzt ist)
            account_uuid: Account UUID (wird verwendet wenn config nicht gesetzt ist)
        """
        if config is None:
            if api_token and account_uuid:
                config = Config(api_token=api_token, account_uuid=account_uuid)
            else:
                raise ValueError("Either config or both api_token and account_uuid must be provided")
        
        self.config = config
        self.session = requests.Session()
        self.session.headers.update(self.config.get_headers())
        
        # Initialisiere Endpoints
        self.addresses = AddressesEndpoint(self)
    
    def _build_url(self, endpoint: str) -> str:
        """
        Erstellt die vollständige URL für einen Endpoint.
        
        Args:
            endpoint: API-Endpoint (z.B. "/addresses/v2/companies")
            
        Returns:
            Vollständige URL
        """
        endpoint = endpoint.lstrip('/')
        return f"{self.config.api_base_url}/{endpoint}"
    
    def _handle_response(self, response: requests.Response) -> Dict[str, Any]:
        """
        Verarbeitet die API-Response und behandelt Fehler.
        
        Args:
            response: HTTP-Response-Objekt
            
        Returns:
            Parsed JSON-Response
            
        Raises:
            AbaNinjaException: Bei API-Fehlern
        """
        try:
            response_data = response.json() if response.text else {}
        except ValueError:
            response_data = {}
        
        # Erfolgreiche Responses (2xx)
        if 200 <= response.status_code < 300:
            return response_data
        
        # Fehlerbehandlung basierend auf Status-Code
        error_message = response_data.get('error_description') or response_data.get('error') or response.text
        
        if response.status_code == 400:
            raise BadRequestError(error_message, response_data=response_data)
        elif response.status_code == 401:
            raise AuthenticationError(error_message, response_data=response_data)
        elif response.status_code == 403:
            raise AuthorizationError(error_message, response_data=response_data)
        elif response.status_code == 404:
            raise NotFoundError(error_message, response_data=response_data)
        elif response.status_code == 409:
            raise ConflictError(error_message, response_data=response_data)
        elif response.status_code == 429:
            raise RateLimitError(error_message, response_data=response_data)
        elif 500 <= response.status_code < 600:
            raise ServerError(error_message, status_code=response.status_code, response_data=response_data)
        else:
            raise AbaNinjaException(
                f"Unexpected error: {error_message}",
                status_code=response.status_code,
                response_data=response_data
            )
    
    def _request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        retry_count: int = 0
    ) -> Dict[str, Any]:
        """
        Führt einen HTTP-Request aus mit automatischer Fehlerbehandlung und Retry-Logik.
        
        Args:
            method: HTTP-Methode (GET, POST, PATCH, DELETE)
            endpoint: API-Endpoint
            params: Query-Parameter
            data: Request-Body-Daten
            retry_count: Aktueller Retry-Versuch
            
        Returns:
            API-Response als Dictionary
            
        Raises:
            AbaNinjaException: Bei API-Fehlern
        """
        url = self._build_url(endpoint)
        
        try:
            response = self.session.request(
                method=method,
                url=url,
                params=params,
                json=data,
                timeout=self.config.timeout
            )
            
            return self._handle_response(response)
            
        except (requests.ConnectionError, requests.Timeout) as e:
            # Retry bei Verbindungsfehlern
            if retry_count < self.config.max_retries:
                time.sleep(2 ** retry_count)  # Exponential backoff
                return self._request(method, endpoint, params, data, retry_count + 1)
            else:
                raise AbaNinjaException(f"Connection error after {self.config.max_retries} retries: {str(e)}")
        
        except RateLimitError as e:
            # Retry bei Rate-Limiting
            if retry_count < self.config.max_retries:
                time.sleep(5 * (retry_count + 1))  # Längere Wartezeit bei Rate-Limiting
                return self._request(method, endpoint, params, data, retry_count + 1)
            else:
                raise e
    
    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Führt einen GET-Request aus.
        
        Args:
            endpoint: API-Endpoint
            params: Query-Parameter
            
        Returns:
            API-Response
        """
        return self._request('GET', endpoint, params=params)
    
    def post(self, endpoint: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Führt einen POST-Request aus.
        
        Args:
            endpoint: API-Endpoint
            data: Request-Body-Daten
            
        Returns:
            API-Response
        """
        return self._request('POST', endpoint, data=data)
    
    def patch(self, endpoint: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Führt einen PATCH-Request aus.
        
        Args:
            endpoint: API-Endpoint
            data: Request-Body-Daten
            
        Returns:
            API-Response
        """
        return self._request('PATCH', endpoint, data=data)
    
    def delete(self, endpoint: str) -> Dict[str, Any]:
        """
        Führt einen DELETE-Request aus.
        
        Args:
            endpoint: API-Endpoint
            
        Returns:
            API-Response
        """
        return self._request('DELETE', endpoint)
    
    def get_paginated(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        limit: Optional[int] = None,
        auto_paginate: bool = False
    ) -> Dict[str, Any]:
        """
        Führt einen GET-Request mit Pagination aus.
        
        Args:
            endpoint: API-Endpoint
            params: Query-Parameter
            limit: Anzahl Einträge pro Seite (verwendet default_limit wenn nicht gesetzt)
            auto_paginate: Wenn True, werden automatisch alle Seiten abgerufen
            
        Returns:
            API-Response mit Pagination-Metadaten
        """
        if params is None:
            params = {}
        
        if limit is None:
            limit = self.config.default_limit
        
        params['limit'] = min(limit, self.config.max_limit)
        
        if not auto_paginate:
            return self.get(endpoint, params=params)
        
        # Auto-Pagination: Alle Seiten abrufen
        all_data = []
        page = 1
        
        while True:
            params['page'] = page
            response = self.get(endpoint, params=params)
            
            data = response.get('data', [])
            all_data.extend(data)
            
            meta = response.get('meta', {})
            current_page = meta.get('current_page', 1)
            last_page = meta.get('last_page', 1)
            
            if current_page >= last_page:
                break
            
            page += 1
        
        return {
            'data': all_data,
            'meta': {
                'total': len(all_data)
            }
        }
