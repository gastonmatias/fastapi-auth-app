# app/middleware/auth_middleware.py
"""
Middleware de autenticación.
Puede usarse para logging, validación adicional, etc.
"""

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from typing import Callable
import logging

logger = logging.getLogger(__name__)


class AuthMiddleware(BaseHTTPMiddleware):
    """
    Middleware para logging y manejo de autenticación.
    Registra todas las peticiones autenticadas.
    """
    
    async def dispatch(self, request: Request, call_next: Callable):
        """
        Procesa cada request antes y después de llegar al endpoint.
        
        Args:
            request: Request de FastAPI
            call_next: Siguiente middleware o endpoint
            
        Returns:
            Response del endpoint
        """
        # Log de la petición
        logger.info(f"{request.method} {request.url.path}")
        
        # Verificar si tiene header de autorización
        auth_header = request.headers.get("authorization")
        if auth_header:
            logger.info(f"Request autenticado desde {request.client.host}")
        
        # Procesar la petición
        response = await call_next(request)
        
        # Log de la respuesta
        logger.info(f"Response status: {response.status_code}")
        
        return response
