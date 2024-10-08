# Generated by Django 5.1 on 2024-08-16 17:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0001_initial'),
        ('reservations', '0002_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reservation',
            name='user',
        ),
        migrations.AddField(
            model_name='reservation',
            name='client',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='reservations', to='client.client'),
            preserve_default=False,
        ),
    ]
