# Generated by Django 3.2.23 on 2024-09-17 15:16

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='StockData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('symbol', models.TextField(null=True)),
                ('data', models.TextField(null=True)),
            ],
        ),
    ]
