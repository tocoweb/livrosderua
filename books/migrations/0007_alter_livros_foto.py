# Generated by Django 3.2.7 on 2021-09-30 19:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0006_alter_livros_foto'),
    ]

    operations = [
        migrations.AlterField(
            model_name='livros',
            name='foto',
            field=models.ImageField(blank=True, null=True, upload_to='fotos', verbose_name='Foto capa'),
        ),
    ]