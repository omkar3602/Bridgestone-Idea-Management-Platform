# Generated by Django 3.2.17 on 2023-02-21 11:50

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0006_auto_20230221_1713'),
    ]

    operations = [
        migrations.AlterField(
            model_name='submission',
            name='key',
            field=models.CharField(max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='submission',
            name='modified_on',
            field=models.DateTimeField(default=datetime.datetime(2023, 2, 21, 11, 50, 36, 337582, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='submission',
            name='submitted_on',
            field=models.DateTimeField(default=datetime.datetime(2023, 2, 21, 11, 50, 36, 292062, tzinfo=utc)),
        ),
    ]
