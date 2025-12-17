"""
Swiss21 - ABA Ninja API Integration
Exceptions Module

Dieses Modul definiert alle benutzerdefinierten Exceptions für die API-Integration.
"""


class AbaNinjaException(Exception):
    """Basis-Exception für alle ABA Ninja API Fehler"""
    
    def __init__(self, message: str, status_code: int = None, response_data: dict = None):
        self.message = message
        self.status_code = status_code
        self.response_data = response_data
        super().__init__(self.message)


class AuthenticationError(AbaNinjaException):
    """Exception für Authentifizierungsfehler (401)"""
    
    def __init__(self, message: str = "Authentication failed. Token expired or invalid.", response_data: dict = None):
        super().__init__(message, status_code=401, response_data=response_data)


class AuthorizationError(AbaNinjaException):
    """Exception für Autorisierungsfehler (403)"""
    
    def __init__(self, message: str = "Client/Token is not allowed to access this resource.", response_data: dict = None):
        super().__init__(message, status_code=403, response_data=response_data)


class NotFoundError(AbaNinjaException):
    """Exception für nicht gefundene Ressourcen (404)"""
    
    def __init__(self, message: str = "Resource not found.", response_data: dict = None):
        super().__init__(message, status_code=404, response_data=response_data)


class ConflictError(AbaNinjaException):
    """Exception für Konflikte (409)"""
    
    def __init__(self, message: str = "Resource conflict. Resource may be in use.", response_data: dict = None):
        super().__init__(message, status_code=409, response_data=response_data)


class BadRequestError(AbaNinjaException):
    """Exception für fehlerhafte Anfragen (400)"""
    
    def __init__(self, message: str = "Bad request. Invalid parameters or data.", response_data: dict = None):
        super().__init__(message, status_code=400, response_data=response_data)


class RateLimitError(AbaNinjaException):
    """Exception für Rate-Limiting (429)"""
    
    def __init__(self, message: str = "Rate limit exceeded. Please try again later.", response_data: dict = None):
        super().__init__(message, status_code=429, response_data=response_data)


class ServerError(AbaNinjaException):
    """Exception für Server-Fehler (5xx)"""
    
    def __init__(self, message: str = "Server error occurred.", status_code: int = 500, response_data: dict = None):
        super().__init__(message, status_code=status_code, response_data=response_data)


class ValidationError(AbaNinjaException):
    """Exception für Validierungsfehler"""
    
    def __init__(self, message: str, response_data: dict = None):
        super().__init__(message, response_data=response_data)


class ConfigurationError(AbaNinjaException):
    """Exception für Konfigurationsfehler"""
    
    def __init__(self, message: str):
        super().__init__(message)
