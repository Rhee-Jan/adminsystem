# Generated by Django 3.2.7 on 2021-09-25 07:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiling', '0004_auto_20210925_1527'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stock_in',
            name='date_added',
        ),
    ]
