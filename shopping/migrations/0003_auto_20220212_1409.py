# Generated by Django 3.0 on 2022-02-12 08:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopping', '0002_remove_addtocart_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='addtocart',
            name='quantity',
            field=models.IntegerField(default=1),
        ),
    ]
