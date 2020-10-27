# Generated by Django 2.1.5 on 2020-10-18 18:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0012_auto_20201018_2054'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='prioritycount',
            name='priority_high',
        ),
        migrations.RemoveField(
            model_name='prioritycount',
            name='priority_id',
        ),
        migrations.RemoveField(
            model_name='prioritycount',
            name='priority_low',
        ),
        migrations.RemoveField(
            model_name='prioritycount',
            name='priority_medium',
        ),
        migrations.AddField(
            model_name='prioritycount',
            name='priority',
            field=models.IntegerField(choices=[(1, 'Высокий приоритет'), (2, 'Средний приоритет'), (3, 'Низкий приоритет')], default=2, verbose_name='Приоритет'),
        ),
    ]