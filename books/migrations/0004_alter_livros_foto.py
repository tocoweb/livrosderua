# Generated by Django 3.2.7 on 2021-09-30 18:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0003_alter_livros_foto'),
    ]

    operations = [
        migrations.AlterField(
            model_name='livros',
            name='foto',
            field=models.ImageField(blank=True, null=True, upload_to='static/img/fotos', verbose_name='Foto capa'),
        ),
    ]
