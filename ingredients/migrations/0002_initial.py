# Generated by Django 5.1 on 2024-08-15 18:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('ingredients', '0001_initial'),
        ('suppliers', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ingredient',
            name='supplier',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ingredients', to='suppliers.supplier'),
        ),
    ]
