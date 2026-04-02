from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("inventario", "0003_materiaprima_requiere_control_caducidad_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="materiaprima",
            name="dias_alerta_vencimiento",
            field=models.PositiveIntegerField(default=30),
        ),
    ]
