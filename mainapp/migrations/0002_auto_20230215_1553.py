# Generated by Django 3.2.17 on 2023-02-15 10:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='businessunit',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='business_units/'),
        ),
        migrations.AlterField(
            model_name='submission',
            name='attachment',
            field=models.FileField(blank=True, null=True, upload_to='submission_attachments/'),
        ),
        migrations.AlterField(
            model_name='submission',
            name='remark',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='submission',
            name='similar_solutions',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
    ]