# Generated by Django 4.1.7 on 2023-12-09 17:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('producto', '0004_merma_fecha'),
    ]

    operations = [
        migrations.AddField(
            model_name='producto',
            name='rentabilidad',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5),
        ),
    ]