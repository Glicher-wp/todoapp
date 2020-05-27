# Generated by Django 2.1.5 on 2020-05-15 12:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tasks', '0002_auto_20200430_1050'),
    ]

    operations = [
        migrations.AddField(
            model_name='todoitem',
            name='owner',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
