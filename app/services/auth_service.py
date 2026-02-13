# app/services/auth_service.py
"""
Servicio de autenticación.
Contiene la lógica de negocio para registro, login y validación de tokens.
"""

from datetime import timedelta
from typing import Optional
from fastapi import HTTPException, status
from app.models import UserInDB, UserPublic
from app.schemas import UserRegisterRequest, UserLoginRequest, TokenResponse
from app.repositories import user_repository
from app.utils import (
    verify_password, 
    get_password_hash, 
    create_access_token,
    decode_access_token
)
from app.config import settings


class AuthService:
    """Servicio de autenticación"""
    
    def __init__(self):
        self.repository = user_repository
    
    def register_user(self, user_data: UserRegisterRequest) -> UserPublic:
        """
        Registra un nuevo usuario.
        
        Args:
            user_data: Datos del usuario a registrar
            
        Returns:
            Usuario creado (sin contraseña)
            
        Raises:
            HTTPException: Si el email ya está registrado
        """

        if self.repository.email_exists(user_data.email):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="El email ya está registrado"
            )            
        
        # Encriptar la contraseña
        hashed_password = get_password_hash(user_data.password)
        
        # Crear el usuario
        user = self.repository.create(
            email=user_data.email,
            hashed_password=hashed_password,
            full_name=user_data.full_name
        )
        
        # Retornar sin la contraseña
        return UserPublic(
            email=user.email,
            full_name=user.full_name,
            created_at=user.created_at
        )
    
    def authenticate_user(self, credentials: UserLoginRequest) -> TokenResponse:
        """
        Autentica un usuario y genera un token JWT.
        
        Args:
            credentials: Credenciales de login
            
        Returns:
            Token de acceso JWT
            
        Raises:
            HTTPException: Si las credenciales son inválidas
        """
        # Buscar el usuario
        user = self.repository.get_by_email(credentials.email)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Email o contraseña incorrectos"
            )
        
        # Verificar la contraseña
        if not verify_password(credentials.password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Email o contraseña incorrectos"
            )
        
        # Crear el token
        access_token_expires = timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
        access_token = create_access_token(
            data={"sub": user.email},
            expires_delta=access_token_expires
        )
        
        return TokenResponse(
            access_token=access_token,
            token_type="bearer"
        )
    
    def get_current_user_from_token(self, token: str) -> UserInDB:
        """
        Obtiene el usuario actual desde un token JWT.
        
        Args:
            token: Token JWT
            
        Returns:
            Usuario autenticado
            
        Raises:
            HTTPException: Si el token es inválido o el usuario no existe
        """
        # Decodificar el token
        payload = decode_access_token(token)
        
        if payload is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido o expirado",
                headers={"WWW-Authenticate": "Bearer"}
            )
        
        # Obtener el email del payload
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido",
                headers={"WWW-Authenticate": "Bearer"}
            )
        
        # Buscar el usuario
        user = self.repository.get_by_email(email)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado"
            )
        
        return user


# Instancia global del servicio
auth_service = AuthService()
