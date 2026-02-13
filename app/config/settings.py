# app/config/settings.py
"""
Configuración centralizada de la aplicación.
Todas las configuraciones en un solo lugar.
"""

from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Configuración de la aplicación"""
    
    # Información de la API
    APP_NAME: str = "Auth API"
    APP_VERSION: str = "1.0.0"
    
    # Seguridad
    SECRET_KEY: str = "tu_clave_secreta_super_segura_cambiala_en_produccion"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Base de datos (archivo JSON)
    USERS_FILE: str = "users.json"
    
    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:4200"]
    CORS_CREDENTIALS: bool = True
    CORS_METHODS: List[str] = ["*"]
    CORS_HEADERS: List[str] = ["*"]
    
    # Validación de contraseñas
    PASSWORD_MIN_LENGTH: int = 6
    PASSWORD_MAX_LENGTH: int = 72  # Límite de bcrypt
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Instancia global de configuración
settings = Settings()
