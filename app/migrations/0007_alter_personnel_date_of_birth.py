# Generated by Django 5.0.4 on 2025-03-30 00:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_country_names'),
    ]

    operations = [
        migrations.AlterField(
            model_name='personnel',
            name='date_of_birth',
            field=models.DateField(blank=True, null=True),
        ),
    ]
