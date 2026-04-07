# Puesta en marcha y solución de errores comunes en Django

## Error: `/accounts/login/` devuelve 404

Si al abrir la aplicación aparece un error como este:

- `Page not found (404)`
- `Request URL: http://127.0.0.1:8000/accounts/login/?next=/`

entonces Django está intentando redirigir al usuario a la ruta de login por defecto: `/accounts/login/`.

Eso ocurre normalmente cuando:

1. una vista usa `@login_required`,
2. se utilizan mixins como `LoginRequiredMixin`, o
3. el panel principal exige autenticación.

En el proyecto, sin embargo, la ruta configurada para autenticación es `login/` y no `accounts/login/`. Por eso Django muestra 404 si no se define explícitamente la URL de login en `settings.py`.

## Causa técnica

Django usa por defecto esta configuración interna:

- `LOGIN_URL = '/accounts/login/'`

Si tu archivo `config/urls.py` tiene una ruta como esta:

```python
path('login/', auth_views.LoginView.as_view(), name='login')
```

pero **no** defines `LOGIN_URL`, cualquier redirección automática seguirá apuntando a `/accounts/login/`.

## Solución recomendada

En `settings.py`, agrega estas variables:

```python
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'inicio'
LOGOUT_REDIRECT_URL = 'login'
```

Con eso, Django dejará de redirigir a `/accounts/login/` y usará la ruta nombrada `login`.

## Alternativa válida

Si prefieres conservar el comportamiento por defecto de Django, puedes agregar estas rutas en `config/urls.py`:

```python
from django.urls import include, path

urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
]
```

Eso crea rutas como:

- `/accounts/login/`
- `/accounts/logout/`
- `/accounts/password_change/`

## Recomendación para este proyecto

Como ya existe un patrón `login/` según el error reportado, la opción más consistente es:

1. mantener `login/` y `logout/`,
2. configurar `LOGIN_URL = 'login'`,
3. configurar `LOGIN_REDIRECT_URL = 'inicio'`, y
4. verificar que el nombre de la vista principal realmente sea `inicio`.

## Checklist para otra máquina

Cuando el proyecto se mueve a otro equipo, verifica:

1. que exista el archivo `.env` o la configuración local equivalente,
2. que la base de datos y migraciones estén aplicadas,
3. que `ALLOWED_HOSTS` incluya el host que se usa,
4. que `LOGIN_URL` coincida con la URL real declarada en `urls.py`,
5. que las plantillas de autenticación existan si se usa `LoginView`, y
6. que el usuario administrador haya sido creado con `createsuperuser` si hace falta entrar al panel.

## Comandos útiles de verificación

```bash
python manage.py show_urls
python manage.py check
python manage.py migrate
python manage.py createsuperuser
```

> `show_urls` requiere paquetes adicionales como `django-extensions`. Si no lo tienes instalado, puedes revisar `config/urls.py` manualmente.
