# Generated by Django 3.2.7 on 2023-02-14 07:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userauth', '0002_alter_account_fullname'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='is_idea_admin',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='account',
            name='is_ideator',
            field=models.BooleanField(default=False),
        ),
    ]
