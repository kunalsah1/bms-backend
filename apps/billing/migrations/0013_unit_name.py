# Generated by Django 5.1.5 on 2025-02-01 11:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0012_unit_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='unit',
            name='name',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
