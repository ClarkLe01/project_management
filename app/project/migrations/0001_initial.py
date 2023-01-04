# Generated by Django 4.1.4 on 2023-01-04 04:42

import app.storage
import ckeditor.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import project.files.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('utils', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', ckeditor.fields.RichTextField()),
                ('created_date', models.DateField(auto_now_add=True)),
                ('updated_date', models.DateField(auto_now=True)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('status', models.IntegerField(default=0)),
                ('cost', models.DecimalField(decimal_places=4, default=0, max_digits=19)),
                ('base', models.CharField(default='USD', max_length=10)),
                ('collaborators', models.ManyToManyField(related_name='project_collaborator', to=settings.AUTH_USER_MODEL)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('langcode_tags', models.ManyToManyField(blank=True, to='utils.programminglanguage')),
            ],
            options={
                'db_table': 'Project',
                'permissions': [('olp_view_project', 'OLP can view project'), ('olp_update_project', 'OLP can update project'), ('olp_delete_project', 'OLP can delete project'), ('olp_view_collaborator_project', 'OLP can view project'), ('olp_add_collaborator_project', 'OLP can add collaborator project'), ('olp_update_collaborator_project', 'OLP can update collaborator project'), ('olp_delete_collaborator_project', 'OLP can delete collaborator project')],
            },
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('status', models.CharField(choices=[('backlog', 'backlog'), ('todo', 'todo'), ('working', 'working'), ('done', 'done')], default='backlog', max_length=255)),
                ('due_date', models.DateField()),
                ('task_details', models.CharField(blank=True, max_length=255, null=True)),
                ('assignee', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project.project')),
            ],
        ),
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(max_length=500, storage=app.storage.OverwriteStorage(), upload_to=project.files.models.user_project_directory_path)),
                ('update_date', models.DateTimeField(auto_now=True)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='files', to='project.project')),
            ],
        ),
    ]
