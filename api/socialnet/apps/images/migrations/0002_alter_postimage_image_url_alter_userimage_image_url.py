# Generated by Django 5.2.4 on 2025-07-15 18:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postimage',
            name='image_url',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='userimage',
            name='image_url',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
