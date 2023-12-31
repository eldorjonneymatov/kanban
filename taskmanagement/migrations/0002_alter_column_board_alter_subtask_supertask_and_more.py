# Generated by Django 4.2.3 on 2023-08-01 07:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('taskmanagement', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='column',
            name='board',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='columns', to='taskmanagement.board'),
        ),
        migrations.AlterField(
            model_name='subtask',
            name='supertask',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subtasks', to='taskmanagement.task'),
        ),
        migrations.AlterField(
            model_name='task',
            name='status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to='taskmanagement.column', verbose_name='Status'),
        ),
    ]
