# Generated by Django 5.0.6 on 2024-06-01 13:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0009_dailycounter'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShowResult',
            fields=[
                ('show_id', models.IntegerField(primary_key=True, serialize=False)),
                ('data', models.CharField(max_length=1000)),
            ],
            options={
                'db_table': 'show_result',
                'managed': False,
            },
        ),
    ]
