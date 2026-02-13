# app/main.py
"""
Punto de entrada de la aplicación FastAPI.
Configura la aplicación, middlewares y rutas.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.routes import auth_router
from app.middleware import AuthMiddleware


# Crear la aplicación FastAPI
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="API de autenticación con JWT",
    docs_url="/docs",
    redoc_url="/redoc"
)


# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=settings.CORS_CREDENTIALS,
    allow_methods=settings.CORS_METHODS,
    allow_headers=settings.CORS_HEADERS,
)


# Agregar middleware personalizado (opcional)
# app.add_middleware(AuthMiddleware)


# Incluir routers
app.include_router(auth_router)


# Endpoint raíz
@app.get("/", tags=["General"])
def root():
    """
    Endpoint raíz de la API.
    Retorna información básica de la API.
    """
    return {
        "message": "API de Autenticación activa",
        "version": settings.APP_VERSION,
        "docs": "/docs"
    }


# Health check
@app.get("/health", tags=["General"])
def health_check():
    """
    Endpoint de health check.
    Útil para verificar que la API está funcionando.
    """
    return {
        "status": "healthy",
        "version": settings.APP_VERSION
    }


# Para ejecutar con uvicorn:
# uvicorn app.main:app --reload
