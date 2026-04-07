from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("formulaciones", "0008_alter_formulaciondetalle_unidad_medida_varias_unidades"),
    ]

    operations = [
        migrations.AlterField(
            model_name="formulaciondetalle",
            name="unidad_medida",
            field=models.CharField(
                choices=[("%", "%"), ("g", "g"), ("ml", "ml"), ("oz", "oz")],
                default="%",
                max_length=10,
            ),
        ),
    ]
