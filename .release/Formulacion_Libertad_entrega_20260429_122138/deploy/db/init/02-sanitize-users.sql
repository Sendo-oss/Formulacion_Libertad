BEGIN;

UPDATE inventario_materiaprima
SET registrado_por_id = 1
WHERE registrado_por_id IS NOT NULL;

UPDATE formulaciones_formulacion
SET creado_por_id = 1
WHERE creado_por_id IS NOT NULL;

UPDATE alertas_alerta
SET atendida_por_id = 1
WHERE atendida_por_id IS NOT NULL;

UPDATE documentacion_documentotecnico
SET subido_por_id = 1
WHERE subido_por_id IS NOT NULL;

UPDATE noticias_noticia
SET creada_por_id = 1
WHERE creada_por_id IS NOT NULL;

UPDATE usuarios_historialsistema
SET usuario_id = 1
WHERE usuario_id IS NOT NULL;

UPDATE usuarios_solicitudrecuperacioncontrasena
SET usuario_id = 1
WHERE usuario_id IS NOT NULL;

UPDATE usuarios_solicitudrecuperacioncontrasena
SET atendida_por_id = 1
WHERE atendida_por_id IS NOT NULL;

UPDATE django_admin_log
SET user_id = 1
WHERE user_id IS NOT NULL;

DELETE FROM django_session;
DELETE FROM usuarios_usuario_groups WHERE usuario_id <> 1;
DELETE FROM usuarios_usuario_user_permissions WHERE usuario_id <> 1;
DELETE FROM usuarios_usuario WHERE id <> 1;

UPDATE usuarios_usuario
SET
    password = 'pbkdf2_sha256$1000000$X1MoKj3xnFb2wHJSMSbQIi$I+b1DIk0SuVMvLX552r2hCUcPZHLni9HaRm3UusRL9A=',
    last_login = NULL,
    is_superuser = true,
    username = 'admin',
    first_name = 'Usuario',
    last_name = 'Prueba',
    email = 'admin@example.com',
    is_staff = true,
    is_active = true,
    rol = 'ADMINISTRADOR',
    debe_cambiar_contrasena = false
WHERE id = 1;

SELECT pg_catalog.setval(
    'public.usuarios_usuario_id_seq',
    COALESCE((SELECT MAX(id) FROM usuarios_usuario), 1),
    true
);

COMMIT;
