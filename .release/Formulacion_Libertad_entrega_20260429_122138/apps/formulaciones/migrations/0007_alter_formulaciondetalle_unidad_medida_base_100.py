from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("formulaciones", "0006_alter_formulacion_fuente_referencia"),
    ]

    operations = [
        migrations.AlterField(
            model_name="formulaciondetalle",
            name="unidad_medida",
            field=models.CharField(
                choices=[("%", "%")],
                default="%",
                max_length=10,
            ),
        ),
    ]
