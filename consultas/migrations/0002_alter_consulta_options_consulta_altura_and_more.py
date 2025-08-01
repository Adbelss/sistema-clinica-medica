# Generated by Django 5.2.4 on 2025-07-26 18:27

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('consultas', '0001_initial'),
        ('pacientes', '0004_alter_paciente_options_paciente_contacto_emergencia_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='consulta',
            options={'ordering': ['-fecha'], 'verbose_name': 'Consulta', 'verbose_name_plural': 'Consultas'},
        ),
        migrations.AddField(
            model_name='consulta',
            name='altura',
            field=models.DecimalField(blank=True, decimal_places=2, help_text='Altura en metros', max_digits=3, null=True),
        ),
        migrations.AddField(
            model_name='consulta',
            name='costo_consulta',
            field=models.DecimalField(blank=True, decimal_places=2, help_text='Costo de la consulta', max_digits=8, null=True),
        ),
        migrations.AddField(
            model_name='consulta',
            name='dosis_medicamentos',
            field=models.TextField(blank=True, help_text='Dosis y frecuencia de medicamentos', null=True),
        ),
        migrations.AddField(
            model_name='consulta',
            name='duracion_consulta',
            field=models.IntegerField(blank=True, help_text='Duración en minutos', null=True),
        ),
        migrations.AddField(
            model_name='consulta',
            name='estado',
            field=models.CharField(choices=[('Programada', 'Programada'), ('En Progreso', 'En Progreso'), ('Completada', 'Completada'), ('Cancelada', 'Cancelada'), ('Reagendada', 'Reagendada')], default='Completada', max_length=20),
        ),
        migrations.AddField(
            model_name='consulta',
            name='fecha_actualizacion',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='consulta',
            name='frecuencia_cardiaca',
            field=models.IntegerField(blank=True, help_text='Latidos por minuto', null=True),
        ),
        migrations.AddField(
            model_name='consulta',
            name='medicamentos_recetados',
            field=models.TextField(blank=True, help_text='Medicamentos prescritos', null=True),
        ),
        migrations.AddField(
            model_name='consulta',
            name='notas_adicionales',
            field=models.TextField(blank=True, help_text='Notas adicionales del doctor', null=True),
        ),
        migrations.AddField(
            model_name='consulta',
            name='observaciones_cita',
            field=models.TextField(blank=True, help_text='Observaciones para la próxima cita', null=True),
        ),
        migrations.AddField(
            model_name='consulta',
            name='paciente',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='consultas', to='pacientes.paciente'),
        ),
        migrations.AddField(
            model_name='consulta',
            name='peso',
            field=models.DecimalField(blank=True, decimal_places=2, help_text='Peso en kg', max_digits=5, null=True),
        ),
        migrations.AddField(
            model_name='consulta',
            name='presion_arterial',
            field=models.CharField(blank=True, help_text='Ej: 120/80', max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='consulta',
            name='proxima_cita',
            field=models.DateTimeField(blank=True, help_text='Fecha de la próxima cita', null=True),
        ),
        migrations.AddField(
            model_name='consulta',
            name='sintomas',
            field=models.TextField(blank=True, help_text='Síntomas presentados por el paciente', null=True),
        ),
        migrations.AddField(
            model_name='consulta',
            name='temperatura',
            field=models.DecimalField(blank=True, decimal_places=1, help_text='Temperatura en °C', max_digits=4, null=True),
        ),
        migrations.AddField(
            model_name='consulta',
            name='tipo_consulta',
            field=models.CharField(choices=[('Primera Vez', 'Primera Vez'), ('Control', 'Control'), ('Emergencia', 'Emergencia'), ('Seguimiento', 'Seguimiento'), ('Especialista', 'Especialista')], default='Control', max_length=20),
        ),
        migrations.AlterField(
            model_name='consulta',
            name='diagnostico',
            field=models.TextField(help_text='Diagnóstico médico'),
        ),
        migrations.AlterField(
            model_name='consulta',
            name='motivo',
            field=models.TextField(help_text='Motivo principal de la consulta'),
        ),
        migrations.AlterField(
            model_name='consulta',
            name='paciente_nombre',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='consulta',
            name='tratamiento',
            field=models.TextField(help_text='Tratamiento prescrito'),
        ),
        migrations.AddIndex(
            model_name='consulta',
            index=models.Index(fields=['paciente', 'fecha'], name='consultas_c_pacient_af1e14_idx'),
        ),
        migrations.AddIndex(
            model_name='consulta',
            index=models.Index(fields=['doctor', 'fecha'], name='consultas_c_doctor__6256d0_idx'),
        ),
        migrations.AddIndex(
            model_name='consulta',
            index=models.Index(fields=['estado', 'fecha'], name='consultas_c_estado_b50e4e_idx'),
        ),
        migrations.AddIndex(
            model_name='consulta',
            index=models.Index(fields=['tipo_consulta', 'fecha'], name='consultas_c_tipo_co_3b462f_idx'),
        ),
    ]
