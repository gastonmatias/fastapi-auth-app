# app/services/user_service.py
"""
Servicio de usuarios.
Contiene la lógica de negocio relacionada con usuarios.
"""

from typing import Optional
from app.models import UserInDB, UserPublic
from app.repositories import user_repository


class UserService:
    """Servicio para operaciones de usuarios"""
    
    def __init__(self):
        self.repository = user_repository
    
    def get_user_by_email(self, email: str) -> Optional[UserInDB]:
        """
        Obtiene un usuario por su email.
        
        Args:
            email: Email del usuario
            
        Returns:
            Usuario encontrado o None
        """
        return self.repository.get_by_email(email)
    
    def user_to_public(self, user: UserInDB) -> UserPublic:
        """
        Convierte un usuario de BD a formato público (sin contraseña).
        
        Args:
            user: Usuario de la base de datos
            
        Returns:
            Usuario en formato público
        """
        return UserPublic(
            email=user.email,
            full_name=user.full_name,
            created_at=user.created_at
        )


# Instancia global del servicio
user_service = UserService()
