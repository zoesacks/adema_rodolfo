# Generated by Django 4.1.7 on 2023-12-09 17:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('producto', '0003_alter_merma_producto'),
    ]

    operations = [
        migrations.AddField(
            model_name='merma',
            name='fecha',
            field=models.DateField(auto_now=True),
        ),
    ]
