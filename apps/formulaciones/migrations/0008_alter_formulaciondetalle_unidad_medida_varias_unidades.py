from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("formulaciones", "0007_alter_formulaciondetalle_unidad_medida_base_100"),
    ]

    operations = [
        migrations.AlterField(
            model_name="formulaciondetalle",
            name="unidad_medida",
            field=models.CharField(
                choices=[("%", "%"), ("g", "g"), ("ml", "ml"), ("u", "u"), ("oz", "oz")],
                default="%",
                max_length=10,
            ),
        ),
    ]
