# Generated by Django 4.1.4 on 2023-01-05 05:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0004_task_historicaltask_alter_historicaltaskcomment_task_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='historicaltaskcomment',
            name='history_user',
        ),
        migrations.RemoveField(
            model_name='historicaltaskcomment',
            name='task',
        ),
        migrations.RemoveField(
            model_name='historicaltaskcomment',
            name='user',
        ),
        migrations.DeleteModel(
            name='HistoricalTask',
        ),
        migrations.DeleteModel(
            name='HistoricalTaskComment',
        ),
    ]
