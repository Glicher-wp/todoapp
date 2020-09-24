# Generated by Django 2.1.5 on 2020-09-15 17:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_remove_profile_avatar'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='key',
            field=models.CharField(blank=True, max_length=32, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='token',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
    ]
