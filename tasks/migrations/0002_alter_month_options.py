# Generated by Django 4.2.3 on 2023-08-09 07:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='month',
            options={'ordering': ['month_id']},
        ),
    ]
