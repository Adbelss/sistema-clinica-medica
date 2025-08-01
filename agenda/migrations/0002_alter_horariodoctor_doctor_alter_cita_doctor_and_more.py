# Generated by Django 5.2.4 on 2025-07-26 19:51

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agenda', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='horariodoctor',
            name='doctor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='horarios', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='cita',
            name='doctor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='citas', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='disponibilidad',
            name='doctor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='disponibilidades', to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='Doctor',
        ),
    ]
