# app/dependencies/auth.py
"""
Dependencias de autenticación para FastAPI.
Se usan para inyectar el usuario actual en los endpoints protegidos.
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.models import UserInDB
from app.services import auth_service


# Esquema de seguridad Bearer
security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> UserInDB:
    """
    Dependencia para obtener el usuario actual desde el token JWT.
    
    Args:
        credentials: Credenciales Bearer del header Authorization
        
    Returns:
        Usuario autenticado
        
    Raises:
        HTTPException: Si el token es inválido o el usuario no existe
        
    Uso en endpoints:
        @app.get("/me")
        def get_me(current_user: UserInDB = Depends(get_current_user)):
            return current_user
    """
    token = credentials.credentials
    return auth_service.get_current_user_from_token(token)
