# Generated by Django 3.2.12 on 2024-05-19 07:26

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0008_delete_employee'),
    ]

    operations = [
        migrations.CreateModel(
            name='DailyCounter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('counter', models.IntegerField(default=0)),
            ],
            options={
                'db_table': 'dailycounter',
            },
        ),
    ]
