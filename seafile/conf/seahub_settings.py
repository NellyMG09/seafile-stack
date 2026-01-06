# -*- coding: utf-8 -*-
import os
# Genera un secreto largo y pegalo aquí (string plano, no bytes)
SECRET_KEY = "b'6eo@4i(pw*_cl##!6@)s8p#t3(h0le5oz22=z6@o(sll0x$8r0"

# URLs externas detrás de Nginx
SERVICE_URL = f"https://{os.environ.get('DOMAIN', 'localhost')}:9455"
FILE_SERVER_ROOT = f"{SERVICE_URL}/seafhttp/"

# DB desde entorno (igual que en compose)
DATABASES = {
  'default': {
    'ENGINE': 'django.db.backends.mysql',
    'NAME': 'seahub_db',
    'USER': os.environ.get('SEAFILE_DB_USER', 'seafile'),
    'PASSWORD': os.environ.get('SEAFILE_DB_PASS', ''),
    'HOST': 'db',
    'PORT': '3306',
    'OPTIONS': {'charset': 'utf8mb4'},
  }
}

# OnlyOffice – usa el puerto 9458 con prefijo /onlyoffice/
ENABLE_ONLYOFFICE = True
VERIFY_ONLYOFFICE_CERTIFICATE = True
onlyoffice_base = f"https://{os.environ.get('DOMAIN', 'localhost')}:9458/onlyoffice"
ONLYOFFICE_APIJS_URL = f"{onlyoffice_base}/web-apps/apps/api/documents/api.js"
ONLYOFFICE_JWT_SECRET = os.environ.get('ONLYOFFICE_JWT_SECRET', '')
ONLYOFFICE_EDITOR_BASE_URL = onlyoffice_base + "/"


