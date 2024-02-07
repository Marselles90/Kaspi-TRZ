# Generated by Django 5.0.1 on 2024-01-18 05:40

import accounts.utils
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True, validators=[accounts.utils.validate_email]),
        ),
    ]
