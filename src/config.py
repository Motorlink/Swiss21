"""
Swiss21 - ABA Ninja API Integration
Configuration Module

Dieses Modul verwaltet die Konfiguration für die API-Integration.
"""

import json
import os
from typing import Optional
from .exceptions import ConfigurationError


class Config:
    """Konfigurationsklasse für ABA Ninja API Client"""
    
    def __init__(
        self,
        api_token: Optional[str] = None,
        account_uuid: Optional[str] = None,
        api_base_url: str = "https://api.abaninja.ch",
        timeout: int = 30,
        max_retries: int = 3,
        default_limit: int = 50,
        max_limit: int = 100
    ):
        """
        Initialisiert die Konfiguration.
        
        Args:
            api_token: JWT Bearer Token für die Authentifizierung
            account_uuid: UUID des ABA Ninja Accounts
            api_base_url: Basis-URL der API
            timeout: Timeout für API-Requests in Sekunden
            max_retries: Maximale Anzahl von Wiederholungsversuchen
            default_limit: Standard-Limit für Pagination
            max_limit: Maximales Limit für Pagination
        """
        self.api_token = api_token
        self.account_uuid = account_uuid
        self.api_base_url = api_base_url.rstrip('/')
        self.timeout = timeout
        self.max_retries = max_retries
        self.default_limit = default_limit
        self.max_limit = max_limit
        
        self._validate()
    
    def _validate(self):
        """Validiert die Konfiguration"""
        if not self.api_token:
            raise ConfigurationError("API Token is required. Please provide api_token.")
        
        if not self.account_uuid:
            raise ConfigurationError("Account UUID is required. Please provide account_uuid.")
        
        if not self.api_base_url:
            raise ConfigurationError("API Base URL is required.")
        
        if self.timeout <= 0:
            raise ConfigurationError("Timeout must be greater than 0.")
        
        if self.max_retries < 0:
            raise ConfigurationError("Max retries must be 0 or greater.")
    
    @classmethod
    def from_file(cls, config_path: str) -> 'Config':
        """
        Lädt die Konfiguration aus einer JSON-Datei.
        
        Args:
            config_path: Pfad zur Konfigurationsdatei
            
        Returns:
            Config-Instanz
            
        Raises:
            ConfigurationError: Wenn die Datei nicht gelesen werden kann
        """
        if not os.path.exists(config_path):
            raise ConfigurationError(f"Configuration file not found: {config_path}")
        
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            return cls(
                api_token=data.get('api_token'),
                account_uuid=data.get('account_uuid'),
                api_base_url=data.get('api_base_url', 'https://api.abaninja.ch'),
                timeout=data.get('timeout', 30),
                max_retries=data.get('max_retries', 3),
                default_limit=data.get('pagination', {}).get('default_limit', 50),
                max_limit=data.get('pagination', {}).get('max_limit', 100)
            )
        except json.JSONDecodeError as e:
            raise ConfigurationError(f"Invalid JSON in configuration file: {e}")
        except Exception as e:
            raise ConfigurationError(f"Error reading configuration file: {e}")
    
    @classmethod
    def from_env(cls) -> 'Config':
        """
        Lädt die Konfiguration aus Umgebungsvariablen.
        
        Returns:
            Config-Instanz
        """
        return cls(
            api_token=os.getenv('ABANINJA_API_TOKEN'),
            account_uuid=os.getenv('ABANINJA_ACCOUNT_UUID'),
            api_base_url=os.getenv('ABANINJA_API_BASE_URL', 'https://api.abaninja.ch'),
            timeout=int(os.getenv('ABANINJA_TIMEOUT', '30')),
            max_retries=int(os.getenv('ABANINJA_MAX_RETRIES', '3')),
            default_limit=int(os.getenv('ABANINJA_DEFAULT_LIMIT', '50')),
            max_limit=int(os.getenv('ABANINJA_MAX_LIMIT', '100'))
        )
    
    def get_headers(self) -> dict:
        """
        Gibt die HTTP-Header für API-Requests zurück.
        
        Returns:
            Dictionary mit HTTP-Headern
        """
        return {
            'Authorization': f'Bearer {self.api_token}',
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
