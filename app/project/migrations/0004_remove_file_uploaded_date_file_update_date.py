# Generated by Django 4.1.4 on 2022-12-14 03:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0003_alter_project_description'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='file',
            name='uploaded_date',
        ),
        migrations.AddField(
            model_name='file',
            name='update_date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]