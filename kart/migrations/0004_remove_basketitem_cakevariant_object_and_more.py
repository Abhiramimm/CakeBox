# Generated by Django 5.0.4 on 2024-05-19 14:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kart', '0003_remove_basketitem_cakevariant_object_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='basketitem',
            name='cakevariant_object',
        ),
        migrations.AddField(
            model_name='basketitem',
            name='cakevariant_object',
            field=models.ManyToManyField(null=True, to='kart.cakevariant'),
        ),
    ]
