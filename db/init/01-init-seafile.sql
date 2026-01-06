-- Crea bases
CREATE DATABASE IF NOT EXISTS ccnet_db   CHARACTER SET utf8;
CREATE DATABASE IF NOT EXISTS seafile_db CHARACTER SET utf8;
CREATE DATABASE IF NOT EXISTS seahub_db  CHARACTER SET utf8;

-- Crea usuario de app (sustituido en runtime por compose/env)
-n.
CREATE USER IF NOT EXISTS 'seafile'@'%' IDENTIFIED BY 'Bitala23';

GRANT ALL PRIVILEGES ON ccnet_db.*   TO 'seafile'@'%';
GRANT ALL PRIVILEGES ON seafile_db.* TO 'seafile'@'%';
GRANT ALL PRIVILEGES ON seahub_db.*  TO 'seafile'@'%';

FLUSH PRIVILEGES;
