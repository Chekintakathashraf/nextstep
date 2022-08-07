# Generated by Django 4.0.6 on 2022-08-06 15:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('coupon_code', models.CharField(max_length=200, unique=True)),
                ('is_available', models.BooleanField(default=True)),
                ('quantity', models.IntegerField()),
                ('amount', models.IntegerField(default=50)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='CouponUsers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_used', models.BooleanField(default=False)),
                ('date_used', models.DateTimeField(auto_now_add=True)),
                ('amount', models.IntegerField(null=True)),
                ('coupon', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coupon.coupon')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]