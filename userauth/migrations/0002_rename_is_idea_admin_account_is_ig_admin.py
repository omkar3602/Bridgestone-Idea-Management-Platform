# Generated by Django 3.2.7 on 2023-02-15 08:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userauth', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='account',
            old_name='is_idea_admin',
            new_name='is_IG_admin',
        ),
    ]