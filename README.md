# API Auth con FastApi

API de autenticación con FastAPI

## 🏗️ Arquitectura

Este proyecto sigue una arquitectura con separación de responsabilidades:

```
app/
├── config/              # Configuraciones
│   └── settings.py      # Configuración centralizada
├── models/              # Modelos de dominio
│   └── user.py         # Entidades de usuario
├── schemas/             # DTOs (Data Transfer Objects)
│   └── auth.py         # Schemas de request/response
├── repositories/        # Capa de acceso a datos
│   └── user_repository.py
├── services/           # Lógica de negocio
│   ├── auth_service.py
│   └── user_service.py
├── routes/             # Endpoints/Controllers
│   └── auth_routes.py
├── dependencies/       # Inyección de dependencias
│   └── auth.py
├── middleware/         # Middlewares personalizados
│   └── auth_middleware.py
├── utils/             # Utilidades
│   └── security.py    # Hash y JWT
└── main.py           # Punto de entrada
```

## 🎯 Principios Aplicados

### 1. **Separación de Responsabilidades**
- **Routes**: Solo manejan HTTP (request/response)
- **Services**: Contienen la lógica de negocio
- **Repositories**: Manejan el acceso a datos
- **Models**: Definen las entidades del dominio
- **Schemas**: Validan entrada/salida de datos

### 2. **Inyección de Dependencias**
```python
# Las dependencias se inyectan automáticamente
@router.get("/me")
def get_me(current_user: UserInDB = Depends(get_current_user)):
    return current_user
```

### 3. **Single Responsibility**
Cada clase/módulo tiene una única responsabilidad:
- `UserRepository`: Solo acceso a datos de usuarios
- `AuthService`: Solo lógica de autenticación
- `SecurityUtils`: Solo operaciones de seguridad

### 4. **Configuración Centralizada**
Todas las configuraciones en `config/settings.py`:
```python
from app.config import settings

settings.SECRET_KEY
settings.ACCESS_TOKEN_EXPIRE_MINUTES
```

## 🚀 Instalación

```bash
# Crear entorno virtual (RECOMENDADISIMO! no saltar!)
python3.12 -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Instalar dependencias
pip install -r requirements.txt
```

## ▶️ Ejecución

```bash
# Desarrollo (con auto-reload)
uvicorn app.main:app --reload

# Producción
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

La API estará disponible en:
- **API**: http://localhost:8000
- **Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 📚 Estructura Detallada

### Config (`app/config/`)
**Responsabilidad**: Configuración centralizada de la aplicación.

```python
# settings.py
class Settings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    # ...
```

### Models (`app/models/`)
**Responsabilidad**: Entidades del dominio (objetos de negocio).

```python
# user.py
class User(BaseModel):
    email: EmailStr
    password: str
    full_name: Optional[str]
    created_at: str
```

### Schemas (`app/schemas/`)
**Responsabilidad**: DTOs para validación de entrada/salida.

```python
# auth.py
class UserRegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=72)
    full_name: Optional[str] = None
```

### Repositories (`app/repositories/`)
**Responsabilidad**: Acceso y persistencia de datos.

```python
# user_repository.py
class UserRepository:
    def get_by_email(self, email: str) -> Optional[UserInDB]:
        # Lógica de acceso a datos
        
    def create(self, email: str, hashed_password: str) -> UserInDB:
        # Lógica de creación
```

### Services (`app/services/`)
**Responsabilidad**: Lógica de negocio.

```python
# auth_service.py
class AuthService:
    def register_user(self, user_data: UserRegisterRequest) -> UserPublic:
        # Validaciones de negocio
        # Llamadas a repository
        
    def authenticate_user(self, credentials: UserLoginRequest) -> TokenResponse:
        # Lógica de autenticación
```

### Routes (`app/routes/`)
**Responsabilidad**: Definir endpoints HTTP.

```python
# auth_routes.py
@router.post("/register")
def register(user_data: UserRegisterRequest):
    return auth_service.register_user(user_data)
```

### Dependencies (`app/dependencies/`)
**Responsabilidad**: Inyección de dependencias de FastAPI.

```python
# auth.py
def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> UserInDB:
    # Validar token y retornar usuario
```

### Utils (`app/utils/`)
**Responsabilidad**: Funciones auxiliares reutilizables.

```python
# security.py
def get_password_hash(password: str) -> str:
    # Hash de contraseña
    
def create_access_token(data: dict) -> str:
    # Crear JWT
```

### Middleware (`app/middleware/`)
**Responsabilidad**: Procesamiento de requests/responses.

```python
# auth_middleware.py
class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        # Logging, validaciones, etc.
```

## 🔄 Flujo de una Request

```
1. Request HTTP
   ↓
2. Middleware (logging, CORS)
   ↓
3. Route/Controller (auth_routes.py)
   ↓
4. Dependency Injection (si es necesario)
   ↓
5. Service (lógica de negocio)
   ↓
6. Repository (acceso a datos)
   ↓
7. Response
```

**Ejemplo concreto: POST /register**

```
1. POST /register
   ↓
2. CORSMiddleware valida origen
   ↓
3. auth_routes.register() recibe request
   ↓
4. Valida UserRegisterRequest (Pydantic)
   ↓
5. auth_service.register_user()
   │  - Verifica email duplicado
   │  - Hash de contraseña
   ↓
6. user_repository.create()
   │  - Guarda en users.json
   ↓
7. Response 201 Created
```

## 🔐 Seguridad

- ✅ Contraseñas hasheadas con bcrypt
- ✅ JWT con expiración
- ✅ Validación en múltiples capas
- ✅ Inyección de dependencias para autenticación
- ✅ CORS configurado
- ✅ Separation of concerns


## 📖 Recursos

- [FastAPI Best Practices](https://fastapi.tiangolo.com/tutorial/)
- [Clean Architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
- [SOLID Principles](https://en.wikipedia.org/wiki/SOLID)

---