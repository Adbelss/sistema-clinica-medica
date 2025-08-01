# Generated by Django 5.2.4 on 2025-07-26 20:10

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('consultas', '0002_alter_consulta_options_consulta_altura_and_more'),
        ('pacientes', '0004_alter_paciente_options_paciente_contacto_emergencia_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ConfiguracionImpresion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_clinica', models.CharField(default='Clínica Médica', max_length=200)),
                ('direccion_clinica', models.TextField(default='Dirección de la clínica')),
                ('telefono_clinica', models.CharField(default='', max_length=20)),
                ('email_clinica', models.EmailField(default='', max_length=254)),
                ('sitio_web_clinica', models.URLField(blank=True)),
                ('logo_clinica', models.ImageField(blank=True, null=True, upload_to='logos/')),
                ('sello_clinica', models.ImageField(blank=True, null=True, upload_to='sellos/')),
                ('pie_pagina_default', models.TextField(default='Documento generado automáticamente por el sistema')),
                ('incluir_codigo_qr', models.BooleanField(default=True)),
                ('incluir_fecha_generacion', models.BooleanField(default=True)),
                ('incluir_numero_pagina', models.BooleanField(default=True)),
                ('tamano_papel_default', models.CharField(choices=[('A4', 'A4'), ('letter', 'Carta'), ('legal', 'Legal')], default='A4', max_length=20)),
                ('orientacion_default', models.CharField(choices=[('portrait', 'Vertical'), ('landscape', 'Horizontal')], default='portrait', max_length=10)),
                ('margenes_default', models.CharField(choices=[('normal', 'Normal'), ('estrecho', 'Estrecho'), ('ancho', 'Ancho'), ('personalizado', 'Personalizado')], default='normal', max_length=20)),
                ('incluir_watermark', models.BooleanField(default=False)),
                ('texto_watermark', models.CharField(blank=True, default='DOCUMENTO OFICIAL', max_length=100)),
            ],
            options={
                'verbose_name': 'Configuración de Impresión',
                'verbose_name_plural': 'Configuración de Impresión',
            },
        ),
        migrations.CreateModel(
            name='PlantillaDocumento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('tipo', models.CharField(choices=[('consulta', 'Consulta Médica'), ('receta', 'Receta Médica'), ('gestion', 'Gestión de Paciente'), ('certificado', 'Certificado Médico'), ('orden_laboratorio', 'Orden de Laboratorio'), ('orden_imagen', 'Orden de Imagenología')], max_length=20)),
                ('descripcion', models.TextField(blank=True)),
                ('html_template', models.TextField(help_text='Plantilla HTML')),
                ('css_template', models.TextField(help_text='Estilos CSS')),
                ('es_activa', models.BooleanField(default=True)),
                ('es_predeterminada', models.BooleanField(default=False)),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('fecha_modificacion', models.DateTimeField(auto_now=True)),
                ('creado_por', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Plantilla de Documento',
                'verbose_name_plural': 'Plantillas de Documentos',
                'ordering': ['tipo', 'nombre'],
            },
        ),
        migrations.CreateModel(
            name='DocumentoImpresion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo_documento', models.CharField(choices=[('consulta', 'Consulta Médica'), ('receta', 'Receta Médica'), ('gestion', 'Gestión de Paciente'), ('certificado', 'Certificado Médico'), ('orden_laboratorio', 'Orden de Laboratorio'), ('orden_imagen', 'Orden de Imagenología')], max_length=20)),
                ('titulo', models.CharField(max_length=200)),
                ('numero_documento', models.CharField(blank=True, max_length=50, unique=True)),
                ('estado', models.CharField(choices=[('borrador', 'Borrador'), ('finalizado', 'Finalizado'), ('impreso', 'Impreso'), ('archivado', 'Archivado')], default='borrador', max_length=20)),
                ('contenido_html', models.TextField(help_text='Contenido HTML del documento')),
                ('contenido_texto', models.TextField(blank=True, help_text='Contenido en texto plano')),
                ('incluir_logo', models.BooleanField(default=True)),
                ('incluir_pie_pagina', models.BooleanField(default=True)),
                ('incluir_firma', models.BooleanField(default=True)),
                ('incluir_sello', models.BooleanField(default=True)),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('fecha_modificacion', models.DateTimeField(auto_now=True)),
                ('fecha_impresion', models.DateTimeField(blank=True, null=True)),
                ('orientacion', models.CharField(choices=[('portrait', 'Vertical'), ('landscape', 'Horizontal')], default='portrait', max_length=10)),
                ('tamano_papel', models.CharField(choices=[('A4', 'A4'), ('letter', 'Carta'), ('legal', 'Legal')], default='A4', max_length=20)),
                ('margenes', models.CharField(choices=[('normal', 'Normal'), ('estrecho', 'Estrecho'), ('ancho', 'Ancho'), ('personalizado', 'Personalizado')], default='normal', max_length=20)),
                ('consulta', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='consultas.consulta')),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('paciente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pacientes.paciente')),
            ],
            options={
                'verbose_name': 'Documento de Impresión',
                'verbose_name_plural': 'Documentos de Impresión',
                'ordering': ['-fecha_creacion'],
                'indexes': [models.Index(fields=['tipo_documento', 'estado'], name='impresion_d_tipo_do_88f267_idx'), models.Index(fields=['paciente', 'fecha_creacion'], name='impresion_d_pacient_a7d8d3_idx'), models.Index(fields=['doctor', 'fecha_creacion'], name='impresion_d_doctor__2c76f6_idx')],
            },
        ),
    ]
