# Generated by Django 3.0 on 2022-02-09 16:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='register',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=254)),
                ('phoneno', models.IntegerField()),
                ('password', models.CharField(max_length=10)),
                ('cpassword', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('img', models.ImageField(upload_to='photo')),
                ('description', models.CharField(max_length=400)),
                ('availableproduct', models.IntegerField()),
                ('price', models.IntegerField()),
                ('cat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shopping.category')),
            ],
        ),
        migrations.CreateModel(
            name='addtocart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.IntegerField()),
                ('updated', models.DateTimeField(null=True)),
                ('status', models.IntegerField()),
                ('quantity', models.IntegerField()),
                ('personname', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shopping.register')),
                ('productname', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shopping.product')),
            ],
        ),
    ]