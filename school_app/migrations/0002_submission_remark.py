# Generated by Django 3.2.24 on 2024-06-07 12:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='submission',
            name='remark',
            field=models.TextField(blank=True, null=True),
        ),
    ]
