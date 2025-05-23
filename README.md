# Customers FastAPI

Este es un proyecto desarrollado con **FastAPI** para la gestión de clientes. Incluye funcionalidades para crear, leer, actualizar y eliminar información de clientes.

## Requisitos

- Python 3.9 o superior
- pip 
- Virtualenv

## Instalación

1. Clona este repositorio:
   ```bash
   git clone https://github.com/WENDY132310/Customers_FastAPI.git
   cd Customers_FastAPI
   ```

2. Crea y activa un entorno virtual (opcional, pero recomendado):
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Linux/Mac
   venv\Scripts\activate     # En Windows
   ```

3. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

## Uso

1. Ejecuta el servidor FastAPI:
   ```bash
   uvicorn app.main:app --reload
   ```

2. Abre tu navegador y ve a la documentación interactiva de la API:
   - [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) (Swagger UI)
   - [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc) (ReDoc)

## Estructura del Proyecto

```
curso-fastap-proyecto/
├── app/
│   ├── main.py          # Punto de entrada de la aplicación
│   ├── models/          # Modelos de datos
│   ├── routes/          # Rutas de la API
│   ├── schemas/         # Esquemas de validación
│   └── database.py      # Configuración de la base de datos
├── requirements.txt     # Dependencias del proyecto
└── README.md            # Documentación del proyecto
```

## Características

- CRUD de clientes
- Documentación automática con Swagger y ReDoc
- Configuración de base de datos
- autenticacion de credenciales con HTTPBasic

