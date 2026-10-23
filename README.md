# Sistema de Votaciones

API REST sencilla para registrar votantes, candidatos y votos, construida con Django REST Framework y PostgreSQL.

## Tecnologías

Python 3.12, Django, Django REST Framework, PostgreSQL, Docker Compose y drf-spectacular (Swagger).

## Estructura

- `config/`: configuración, rutas y arranque WSGI de Django.
- `voting/`: modelos, serializers, vistas, rutas, migraciones y pruebas de la API.
- `Dockerfile`, `docker-compose.yml`: construcción y ejecución de los servicios web y db.

## Configuración y ejecución

Copie `.env.example` como `.env` y configure, como mínimo, `POSTGRES_PASSWORD` y `SECRET_KEY` con valores propios. En PowerShell:

```powershell
Copy-Item .env.example .env
docker compose up --build -d
```

Compose inicia PostgreSQL y espera a que esté disponible. El contenedor web aplica las migraciones al iniciar y publica la API en <http://localhost:8000>. Para detenerla: `docker compose down` (los datos persisten en el volumen `postgres_data`).

Swagger interactivo: <http://localhost:8000/api/docs/>. La especificación OpenAPI está en `/api/schema/`.

## Endpoints

| Método | Ruta | Acción |
|---|---|---|
| POST, GET | `/voters` | Crear y listar votantes |
| GET, DELETE | `/voters/{id}` | Consultar o eliminar votante |
| POST, GET | `/candidates` | Crear y listar candidatos |
| GET, DELETE | `/candidates/{id}` | Consultar o eliminar candidato |
| POST, GET | `/votes` | Registrar y listar votos |
| GET | `/votes/statistics` | Consultar estadísticas |

Ejemplo de registro:

```json
POST /voters
{"name":"Ana Pérez","email":"ana@example.com"}
```

Respuesta `201`:

```json
{"id":1,"name":"Ana Pérez","email":"ana@example.com","has_voted":false}
```

Registrar candidato: `POST /candidates` con `{"name":"Luis","email":"luis@example.com","party":"Partido A"}`.

Emitir un voto usando IDs existentes: `POST /votes` con `{"voter":1,"candidate":1}`. Se responde `201` con el voto creado. Un votante no puede votar dos veces; eliminar votantes/candidatos con votos responde `409 Conflict`. IDs inexistentes al emitir voto responden `400`.

Ejemplo de `GET /votes/statistics`:

```json
{"total_votes":1,"total_voters_voted":1,"candidates":[{"id":1,"name":"Luis","votes":1,"percentage":100.0}]}
```

## Pruebas

Con Docker en ejecución: `docker compose exec web python manage.py test`. Se cubren registros, correos, votación, actualizaciones, estadísticas y eliminaciones.

## Decisiones técnicas

Se usan vistas genéricas para operaciones CRUD y una vista APIView sencilla para el registro transaccional de votos. La restricción OneToOne en `Vote` impide votos duplicados también ante solicitudes simultáneas; `transaction.atomic()`, bloqueos de fila y `F()` mantienen consistentes el voto, el indicador del votante y el contador.

Se añadió `email` único a `Candidate` porque el enunciado no proporciona un identificador común entre votantes y candidatos. Los serializers comprueban que un correo no exista en el otro modelo. Los emails son obligatorios para candidatos para poder aplicar esta validación.

## Captura de estadísticas

Inicie los servicios, registre algunos votantes y candidatos desde Swagger, envíe votos y abra `GET /votes/statistics`. Para la entrega, tome una captura de la respuesta JSON (por ejemplo, con la herramienta de captura del sistema) mostrando tanto la solicitud como el resultado.
