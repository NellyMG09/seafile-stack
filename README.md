# Stack de Seafile — Servidor de Archivos con OnlyOffice

Stack de servidor de archivos colaborativo desplegado con Docker Compose
y gestionado desde Portainer. Incluye Seafile, base de datos MariaDB,
caché con Memcached, edición en línea con OnlyOffice y Nginx como
reverse proxy con SSL.

## Servicios

| Servicio | Puerto externo | Descripción |
|---|---|---|
| Seafile | — | Servidor de archivos (acceso vía Nginx) |
| MariaDB | — | Base de datos (acceso solo interno) |
| Memcached | — | Caché de sesiones |
| OnlyOffice | — | Edición de documentos en línea |
| Nginx | 9455 (HTTPS), 9458 | Reverse proxy con SSL |

## Arquitectura

```
Internet
└── Nginx (9455 HTTPS / 9458)
    ├── Seafile (archivos, usuarios, API)
    │   ├── MariaDB (almacenamiento de datos)
    │   └── Memcached (caché de sesiones)
    └── OnlyOffice (edición de documentos)

Red externa: grafana-stack_monitoring
└── MariaDB expuesta como seafile-db (para mysqld_exporter)
```

## Requisitos previos

- Docker y Docker Compose instalados
- Portainer para gestión del stack
- Certificados SSL en `/etc/letsencrypt` (generados con Certbot)
- Red externa `grafana-stack_monitoring` creada previamente
- Imagen Nginx personalizada disponible en `ghcr.io/nellymg09/seafile-nginx:latest`

### Imagen Nginx personalizada

Esta imagen extiende Nginx oficial con la configuración específica
para Seafile y OnlyOffice (virtual hosts, proxy_pass, headers).
Repositorio: `github.com/nellymg09/seafile-nginx` *(actualizar con el repo real)*

Para regenerar la imagen manualmente:
```bash
docker build -t ghcr.io/nellymg09/seafile-nginx:latest .
docker push ghcr.io/nellymg09/seafile-nginx:latest
```

## Variables de entorno

Crear un archivo `.env` en la raíz del stack con los siguientes valores:

```env
# Base de datos
DB_ROOT_PASSWD=password_seguro_aqui
SEAFILE_DB_USER=seafile
SEAFILE_DB_PASS=password_seafile_aqui

# Aplicación
DOMAIN=tu-dominio.ejemplo.com
TIMEZONE=America/Mexico_City

# OnlyOffice
ONLYOFFICE_JWT_SECRET=secret_largo_y_seguro_aqui

# Solo necesario en el primer despliegue (comentar después)
# SEAFILE_ADMIN_EMAIL=admin@tudominio.com
# SEAFILE_ADMIN_PASSWORD=password_admin_inicial
```

> **Nota:** `SEAFILE_ADMIN_EMAIL` y `SEAFILE_ADMIN_PASSWORD` solo son
> necesarias en el **primer despliegue** para crear el usuario administrador.
> Una vez creado, comentar o eliminar esas variables y redesplegar.

## Despliegue

### Desde Portainer

1. Ir a **Stacks → Add Stack**
2. Pegar el contenido de `docker-compose.yml`
3. Agregar las variables de entorno en la sección **Environment variables**
4. Verificar que la red `grafana-stack_monitoring` existe:
```bash
   docker network ls | grep monitoring
```
5. Click en **Deploy the stack**

### Desde terminal

```bash
cp .env.example .env
# Editar .env con valores reales
docker compose up -d
```

### Primer despliegue

En el primer despliegue, descomentar en el `.env`:
```env
SEAFILE_ADMIN_EMAIL=admin@tudominio.com
SEAFILE_ADMIN_PASSWORD=password_inicial
```
Una vez que el stack esté corriendo y el admin creado, volver a comentar
esas líneas y hacer **Update the stack** en Portainer.

## Healthchecks

El stack incluye healthchecks en todos los servicios críticos:

| Servicio | Verificación | Intervalo |
|---|---|---|
| MariaDB | `mysqladmin ping` | 5s |
| Seafile | `curl http://localhost/` | 30s |
| OnlyOffice | `curl /healthcheck` | 30s |
| Nginx | `curl -fk https://127.0.0.1:9455/` | 30s |

Seafile espera a que MariaDB esté healthy antes de iniciar (`condition: service_healthy`).

## Volúmenes

| Volumen | Contenido |
|---|---|
| `seafile_db_prod` | Datos de MariaDB |
| `seafile_data_prod` | Archivos de Seafile (`/shared`) |

> Los volúmenes son persistentes. Para migrar el servidor, respaldar
> ambos volúmenes y el directorio de certificados SSL.

## Respaldos

El stack se respalda mediante scripts Bash programados con cron en el host:

```bash
# Backup de base de datos
mysqldump -h 127.0.0.1 -P 3306 -uroot -p seafile_server > backup_seafile.sql

# Backup de archivos
rsync -av /var/lib/docker/volumes/seafile_data_prod/ /ruta/destino/backup/
```

*Ver repositorio de scripts de respaldo para el procedimiento completo.*

## Integración con Monitoreo

MariaDB está conectada a la red `grafana-stack_monitoring` con el alias
`seafile-db`, lo que permite que `mysqld_exporter` (del stack de Prometheus)
acceda a sus métricas sin exponer puertos al host.

Ver stack de observabilidad: `github.com/nellymendez/monitoring-stack`

## Acceso

- Seafile: `https://tu-dominio.ejemplo.com:9455`
- OnlyOffice: interno, accedido desde Seafile

## Seguridad

- SSL gestionado con Let's Encrypt vía Certbot en el host
- Certificados montados como solo lectura en Nginx
- MariaDB sin puertos expuestos al exterior
- OnlyOffice protegido con JWT secret
- Credenciales gestionadas por variables de entorno
