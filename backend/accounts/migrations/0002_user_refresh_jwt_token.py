# Generated by Django 3.2 on 2022-01-23 04:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='refresh_jwt_token',
            field=models.CharField(blank=True, max_length=500, verbose_name='JWT 갱신 토큰'),
        ),
    ]