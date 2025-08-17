#!/bin/bash
set -e

# Procesar el archivo de configuración reemplazando variables de entorno
sed -e "s/\${ODOO_ADMIN_PASS}/${ODOO_ADMIN_PASS}/g" \
    -e "s/\${POSTGRES_USER}/${POSTGRES_USER}/g" \
    -e "s/\${POSTGRES_PASSWORD}/${POSTGRES_PASSWORD}/g" \
    /etc/odoo/odoo.conf.template > /etc/odoo/odoo.conf

# Ejecutar el comando original de Odoo
exec "$@"
