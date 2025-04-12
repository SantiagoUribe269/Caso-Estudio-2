# Caso-Estudio-2
## Descripción del POC
Reserva de autos en el distrito de Pueblo Libre
## Descripción del Sistema
Sistema para gestionar reservas de cocheras con integración de pagos. Permite:
- Registrar cocheras, usuarios y dueños
- Gestionar reservas de cocheras
- Procesar pagos asociados a las reservas
- Actualizar estados de reservas y pagos

## Configuración del entorno

### 1. Crear y activar entorno virtual
```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
```

### 2. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 3. Configurar base de datos PostgreSQL
1. Crear una base de datos llamada `kuadra_db`
2. Configurar las credenciales en `.env`:
```env
DATABASE_URL=postgresql://postgres:tu_contraseña@localhost:5432/kuadra_db
```

## Inicialización del sistema
Al iniciar la aplicación:
1. Se crean automáticamente todas las tablas necesarias
2. Se insertan datos iniciales:
   - Distrito "Pueblo Libre"
   - Dueño de cochera
   - Cochera disponible
   - Usuario de prueba

## Endpoints disponibles

### Distritos
- `POST /distrito/` - Crear nuevo distrito
- `GET /distrito/` - Listar distritos

### Dueños
- `POST /dueno/` - Registrar nuevo dueño
- `GET /dueno/{dueno_id}` - Obtener dueño específico

### Cocheras
- `POST /cochera/` - Registrar nueva cochera
- `GET /cochera/` - Listar cocheras
- `GET /cochera/disponibles` - Listar cocheras disponibles

### Usuarios
- `POST /user/` - Registrar nuevo usuario
- `GET /user/` - Listar usuarios
- `GET /user/{user_id}` - Obtener usuario específico

### Reservas
- `POST /reserva/` - Crear nueva reserva
- `GET /reserva/` - Listar reservas
- `GET /reserva/{reserva_id}` - Obtener reserva específica

### Pagos
- `GET /pago/` - Listar pagos
- `GET /pago/{pago_id}` - Obtener pago específico
- `POST /pago/{pago_id}/completar` - Completar pago

## Flujo para realizar una reserva

### 1. Obtener IDs necesarios
```bash
GET /cochera/  # Anotar ID de cochera disponible
GET /user/     # Anotar ID de usuario
```

### 2. Crear reserva (estado: pendiente)
```bash
POST /reserva/
{
  "fecha_inicio": "2025-04-15T10:00:00",
  "fecha_fin": "2025-04-15T14:00:00",
  "cochera_id": "<cochera_id>",
  "usuario_id": "<usuario_id>"
}
```

Respuesta incluirá ID del pago generado.

### 3. Obtener ID pago
```bash
GET /pago/  # Anotar ID de pago disponible
```
### 4. Completar pago (actualiza estados)
```bash
POST /pago/<id_pago/completar
```

Esto actualizará:
- Estado de pago a "completado"
- Estado de reserva a "confirmada"

### 4. Verificar reserva
```bash
GET /reserva/<id_reserva>
```

## Estructura del proyecto
```
caso-estudio-2/
├── main.py            # Aplicación FastAPI principal
├── models.py          # Modelos SQLModel
├── database.py        # Configuración de base de datos
├── distrito.py        # Rutas de distritos
├── dueno.py          # Rutas de dueños
├── cochera.py        # Rutas de cocheras
├── user.py           # Rutas de usuarios
├── reserva.py        # Rutas de reservas
├── pago.py           # Rutas de pagos
├── enums.py          # Enumeraciones
├── requirements.txt  # Dependencias
└── .env              # Configuración de entorno
```

## Ejecutar la aplicación
```bash
uvicorn main:app --reload
```

La API estará disponible en `http://localhost:8000`

