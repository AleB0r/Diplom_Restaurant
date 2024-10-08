# Generated by Django 5.1 on 2024-08-17 18:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dishes', '0002_initial'),
        ('orders', '0004_alter_order_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='dishes',
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('completed', 'Completed'), ('canceled', 'Canceled')], default='pending', max_length=10),
        ),
        migrations.CreateModel(
            name='OrderDish',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField()),
                ('dish', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dishes.dish')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_dishes', to='orders.order')),
            ],
        ),
    ]
