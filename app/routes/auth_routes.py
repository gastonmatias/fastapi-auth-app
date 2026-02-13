# app/routes/auth_routes.py
"""
Rutas de autenticación (Controllers/Endpoints).
Define los endpoints de la API relacionados con autenticación.
"""

from fastapi import APIRouter, Depends, status
from app.schemas import (
    UserRegisterRequest,
    UserLoginRequest,
    TokenResponse,
    UserResponse
)
from app.models import UserInDB
from app.services import auth_service, user_service
from app.dependencies import get_current_user


# Crear el router
router = APIRouter(
    prefix="",
    tags=["Autenticación"]
)


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar nuevo usuario",
    description="Crea una nueva cuenta de usuario con email y contraseña"
)
def register(user_data: UserRegisterRequest) -> UserResponse:
    """
    Registra un nuevo usuario en el sistema.
    
    - **email**: Email único del usuario
    - **password**: Contraseña (6-72 caracteres)
    - **full_name**: Nombre completo (opcional)
    
    Retorna la información del usuario creado (sin la contraseña).
    """
    user = auth_service.register_user(user_data)
    return UserResponse(
        email=user.email,
        full_name=user.full_name,
        created_at=user.created_at
    )


@router.post(
    "/login",
    response_model=TokenResponse,
    summary="Iniciar sesión",
    description="Autentica un usuario y retorna un token JWT de acceso"
)
def login(credentials: UserLoginRequest) -> TokenResponse:
    """
    Autentica un usuario y genera un token JWT.
    
    - **email**: Email del usuario
    - **password**: Contraseña del usuario
    
    Retorna un token JWT válido por 30 minutos.
    """
    return auth_service.authenticate_user(credentials)


@router.get(
    "/me",
    response_model=UserResponse,
    summary="Obtener usuario actual",
    description="Retorna la información del usuario autenticado (endpoint protegido)"
)
def get_current_user_info(
    current_user: UserInDB = Depends(get_current_user)
) -> UserResponse:
    """
    Obtiene la información del usuario actual.
    
    **Requiere autenticación:** Header `Authorization: Bearer <token>`
    
    Retorna la información del usuario sin la contraseña.
    """
    user_public = user_service.user_to_public(current_user)
    return UserResponse(
        email=user_public.email,
        full_name=user_public.full_name,
        created_at=user_public.created_at
    )
