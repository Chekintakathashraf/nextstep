# Generated by Django 4.0.6 on 2022-07-29 12:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0002_cartitem_is_update'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartitem',
            name='is_update',
        ),
        migrations.RemoveField(
            model_name='cartitem',
            name='variations',
        ),
    ]
