from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from agenda.models import Configuracion

# Create your models here.
class Categoria(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

# Validador personalizado para el tamaño de la imagen
def validate_image_size(value):
    width, height = value.width, value.height
    if width != 500 or height != 500:
        raise ValidationError('La imagen debe ser de 500x500 píxeles.')


class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=200)
    imagen = models.ImageField(
        upload_to='img/',
        blank=True,
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'gif']), validate_image_size]
    )
    costo = models.DecimalField(max_digits=25, decimal_places=2,default=0 ,blank=True,null=True)
    rentabilidad = models.DecimalField(max_digits=5, decimal_places=2,default=0 ,blank=False,null=False)
    precio = models.DecimalField(verbose_name="Bolivares",default=0,max_digits=25, decimal_places=2)
    precio_usd = models.DecimalField(verbose_name="Dolares",default=0,max_digits=25, decimal_places=2)
    en_stock = models.DecimalField(max_digits=25, decimal_places=2)

    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.nombre + " " + self.descripcion

    def save(self, *args, **kwargs):
        if self.en_stock:
            pass
        else:
            self.en_stock = 0

        configuracion = Configuracion.objects.all().first()

        if configuracion:
            tipo_cambio = configuracion.tipo_cambio
        else:
            tipo_cambio = 1
        
        self.precio = ((self.costo * tipo_cambio) / (100 - self.rentabilidad)) * 100
        self.precio_usd =( (self.costo) / (100 - self.rentabilidad) )* 100

        super(Producto, self).save(*args, **kwargs)

    def stock_actual(self):

        from compra.models import Compra  # Importa Compra aquí para evitar el ciclo de importación circular
        from venta.models import DetalleVenta  # Importa DetalleVenta aquí para evitar el ciclo de importación circular

        mermas = Merma.objects.filter(producto=self)
        compras = Compra.objects.filter(producto=self,estado=True)
        ventas = DetalleVenta.objects.filter(producto=self,venta__estado=3)

        compras_totales = compras.aggregate(total_compras=models.Sum('cantidad')).get('total_compras') or 0
        ventas_totales = ventas.aggregate(total_ventas=models.Sum('cantidad')).get('total_ventas') or 0
        mermas_totales = mermas.aggregate(total_mermas=models.Sum('cantidad')).get('total_mermas') or 0

        stock = compras_totales - ventas_totales - mermas_totales
   
        return stock
    

# Create your models here.
class Merma(models.Model):
    fecha = models.DateField(auto_now=True)
    producto = models.ForeignKey(Producto, on_delete=models.SET_NULL, null=True, blank=True)
    cantidad = models.IntegerField(default=1)
    motivo = models.CharField(max_length=255,blank=False,null=False)

    def __str__(self):
        return f'{self.producto}'