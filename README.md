Requisitos: certificados válidos ya presentes en el host en /etc/letsencrypt (los montamos read-only al contenedor nginx).

Puertos abiertos: (Seafile) y (OnlyOffice).

Pasos en Portainer:

Stacks → Add stack → Git repository

Repository URL: <tu repo>
Compose path: seafile-stack/docker-compose.yml

Environment variables: pega el contenido de .env.example con los valores reales (o sube un .env en la UI si tu Portainer lo permite).

Deploy the stack. Pruebas de deploy

Verificación:

curl -I https://TU-DOMINIO:PUERTO/seafhttp/ping → 204

curl -I https://TU-DOMINIO:PUERTO/onlyoffice/web-apps/apps/api/documents/api.js → 200
