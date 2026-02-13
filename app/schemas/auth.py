# app/schemas/auth.py
"""
Schemas de autenticación (DTOs - Data Transfer Objects).
Definen la estructura de datos para requests y responses.
"""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from app.config import settings


class UserRegisterRequest(BaseModel):
    """Schema para registro de usuario"""
    email: EmailStr
    password: str = Field(
        ..., 
        min_length=settings.PASSWORD_MIN_LENGTH,
        max_length=settings.PASSWORD_MAX_LENGTH,
        description="Contraseña del usuario"
    )
    full_name: Optional[str] = Field(None, description="Nombre completo del usuario")
    
    class Config:
        json_schema_extra = {
            "example": {
                "email": "usuario@example.com",
                "password": "contraseña123",
                "full_name": "Nombre Completo"
            }
        }


class UserLoginRequest(BaseModel):
    """Schema para login de usuario"""
    email: EmailStr
    password: str = Field(..., description="Contraseña del usuario")
    
    class Config:
        json_schema_extra = {
            "example": {
                "email": "usuario@example.com",
                "password": "contraseña123"
            }
        }


class TokenResponse(BaseModel):
    """Schema para respuesta de token"""
    access_token: str
    token_type: str = "bearer"
    
    class Config:
        json_schema_extra = {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer"
            }
        }


class UserResponse(BaseModel):
    """Schema para respuesta de usuario"""
    email: EmailStr
    full_name: Optional[str] = None
    created_at: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "email": "usuario@example.com",
                "full_name": "Nombre Completo",
                "created_at": "2025-02-13T10:30:00"
            }
        }
