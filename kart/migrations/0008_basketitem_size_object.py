# Generated by Django 5.0.4 on 2024-05-24 12:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kart', '0007_remove_basketitem_size_object'),
    ]

    operations = [
        migrations.AddField(
            model_name='basketitem',
            name='size_object',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='kart.size'),
        ),
    ]
