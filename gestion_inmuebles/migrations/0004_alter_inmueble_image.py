# Generated by Django 5.1.2 on 2024-11-24 00:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_inmuebles', '0003_alter_inmueble_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inmueble',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='inmuebles/'),
        ),
    ]