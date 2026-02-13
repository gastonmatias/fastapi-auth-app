# app/models/user.py
"""
Modelos de dominio para usuarios.
Representan la estructura de datos interna de la aplicación.
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr


class User(BaseModel):
    """Modelo de usuario en la base de datos"""
    email: EmailStr
    password: str  # Hash de la contraseña
    full_name: Optional[str] = None
    created_at: str
    
    class Config:
        from_attributes = True


class UserInDB(User):
    """Modelo de usuario con información adicional de BD"""
    pass


class UserPublic(BaseModel):
    """Modelo de usuario para respuestas públicas (sin contraseña)"""
    email: EmailStr
    full_name: Optional[str] = None
    created_at: str
    
    class Config:
        from_attributes = True
