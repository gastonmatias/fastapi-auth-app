# app/repositories/user_repository.py
"""
Repositorio de usuarios.
Capa de acceso a datos - maneja la persistencia en users.json.
"""

import json
import os
from typing import List, Optional
from datetime import datetime
from app.config import settings
from app.models import User, UserInDB


class UserRepository:
    """Repositorio para operaciones CRUD de usuarios"""
    
    def __init__(self, file_path: str = None):
        """
        Inicializa el repositorio.
        
        Args:
            file_path: Ruta del archivo JSON (opcional)
        """
        self.file_path = file_path or settings.USERS_FILE
    
    def _load_users(self) -> List[dict]:
        """
        Carga todos los usuarios desde el archivo JSON.
        
        Returns:
            Lista de diccionarios con datos de usuarios
        """
        if not os.path.exists(self.file_path):
            return []
        
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []
    
    def _save_users(self, users: List[dict]) -> None:
        """
        Guarda la lista de usuarios en el archivo JSON.
        
        Args:
            users: Lista de diccionarios con datos de usuarios
        """
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(users, f, indent=2, ensure_ascii=False)
    
    def get_by_email(self, email: str) -> Optional[UserInDB]:
        """
        Busca un usuario por su email.
        
        Args:
            email: Email del usuario a buscar
            
        Returns:
            Usuario encontrado o None
        """
        users = self._load_users()
        for user_data in users:
            if user_data["email"] == email:
                return UserInDB(**user_data)
        return None
    
    def email_exists(self, email: str) -> bool:
        """
        Verifica si un email ya está registrado.
        
        Args:
            email: Email a verificar
            
        Returns:
            True si el email existe, False en caso contrario
        """
        return self.get_by_email(email) is not None
    
    def create(self, email: str, hashed_password: str, full_name: Optional[str] = None) -> UserInDB:
        """
        Crea un nuevo usuario.
        
        Args:
            email: Email del usuario
            hashed_password: Contraseña encriptada
            full_name: Nombre completo (opcional)
            
        Returns:
            Usuario creado
        """
        users = self._load_users()
        
        new_user = {
            "email": email,
            "password": hashed_password,
            "full_name": full_name,
            "created_at": datetime.utcnow().isoformat()
        }
        
        users.append(new_user)
        self._save_users(users)
        
        return UserInDB(**new_user)
    
    def get_all(self) -> List[UserInDB]:
        """
        Obtiene todos los usuarios.
        
        Returns:
            Lista de todos los usuarios
        """
        users = self._load_users()
        return [UserInDB(**user_data) for user_data in users]
    
    def delete_by_email(self, email: str) -> bool:
        """
        Elimina un usuario por su email.
        
        Args:
            email: Email del usuario a eliminar
            
        Returns:
            True si se eliminó, False si no se encontró
        """
        users = self._load_users()
        initial_count = len(users)
        users = [u for u in users if u["email"] != email]
        
        if len(users) < initial_count:
            self._save_users(users)
            return True
        return False
    
    def update(self, email: str, **kwargs) -> Optional[UserInDB]:
        """
        Actualiza un usuario.
        
        Args:
            email: Email del usuario a actualizar
            **kwargs: Campos a actualizar
            
        Returns:
            Usuario actualizado o None si no se encontró
        """
        users = self._load_users()
        
        for i, user in enumerate(users):
            if user["email"] == email:
                user.update(kwargs)
                users[i] = user
                self._save_users(users)
                return UserInDB(**user)
        
        return None


# Instancia global del repositorio
user_repository = UserRepository()
