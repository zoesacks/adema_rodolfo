# Generated by Django 4.1.7 on 2023-12-09 16:56

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import producto.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('descripcion', models.CharField(max_length=200)),
                ('imagen', models.ImageField(blank=True, null=True, upload_to='img/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'gif']), producto.models.validate_image_size])),
                ('precio', models.DecimalField(decimal_places=2, default=0, max_digits=25, verbose_name='Pesos')),
                ('precio_usd', models.DecimalField(decimal_places=2, default=0, max_digits=25, verbose_name='Dolares')),
                ('precio_bs', models.DecimalField(decimal_places=2, default=0, max_digits=25, verbose_name='Bolivianos')),
                ('en_stock', models.DecimalField(decimal_places=2, max_digits=25)),
                ('costo', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=25, null=True)),
                ('categoria', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='producto.categoria')),
            ],
        ),
    ]
