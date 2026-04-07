# Archivos de despliegue

Esta carpeta contiene ejemplos para desplegar el proyecto en Ubuntu Server con:

- Gunicorn
- systemd
- Nginx
- PostgreSQL

## Archivos

- `production.env.example`
  Plantilla del archivo `.env` para el servidor.

- `formulacion.service.example`
  Servicio `systemd` para dejar Gunicorn corriendo.

- `nginx-formulacion.example`
  Configuración base de `nginx` para servir Django.

## Uso recomendado

1. Copia `production.env.example` a `.env` en la raíz del proyecto del servidor.
2. Edita `formulacion.service.example` y reemplaza `TU_USUARIO`.
3. Copia ese archivo a:

```bash
/etc/systemd/system/formulacion.service
```

4. Edita `nginx-formulacion.example` y reemplaza:
   - `TU_USUARIO`
   - `TU_DOMINIO_O_IP`

5. Copia ese archivo a:

```bash
/etc/nginx/sites-available/formulacion
```

6. Activa el sitio y reinicia servicios.

## Comandos típicos

```bash
sudo systemctl daemon-reload
sudo systemctl enable formulacion
sudo systemctl restart formulacion
sudo ln -s /etc/nginx/sites-available/formulacion /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```
