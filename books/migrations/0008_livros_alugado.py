# Generated by Django 3.2.7 on 2021-11-17 21:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0007_alter_livros_foto'),
    ]

    operations = [
        migrations.AddField(
            model_name='livros',
            name='alugado',
            field=models.BooleanField(default=False),
        ),
    ]
