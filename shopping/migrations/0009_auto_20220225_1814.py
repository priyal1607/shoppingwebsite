# Generated by Django 3.0 on 2022-02-25 12:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopping', '0008_deresses'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='date',
            field=models.DateField(blank=True),
        ),
    ]
