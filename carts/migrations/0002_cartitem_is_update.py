# Generated by Django 4.0.6 on 2022-07-29 12:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitem',
            name='is_update',
            field=models.BooleanField(default=True),
        ),
    ]
