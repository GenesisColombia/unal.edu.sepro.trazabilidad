#!/bin/sh

echo "...Copiando script de inicio en /etc/init.d"
cp Script/init.d_SEPRO /etc/init.d/SEPRO
[ $? -ne 0 ] && echo "Falló copia del script de inicio" && exit 0

mkdir -p /opt/SEPRO/scripts
mkdir -p /opt/SEPRO/logs

echo "...Copiando script de auto-configuración en /opt/SEPRO/scripts/"
cp -a Script/. /opt/SEPRO/scripts
chmod +x /opt/SEPRO/scripts/bootstrap.sh
[ $? -ne 0 ] && echo "Falló copia del script de auto-configuración" && exit 0

echo "Inicio del servicio SEPRO"
chmod +x /etc/init.d/SEPRO
update-rc.d SEPRO defaults
[ $? -ne 0 ] && echo "Falló levantando el servicio" && exit 0


echo "Instalación exitosa."
