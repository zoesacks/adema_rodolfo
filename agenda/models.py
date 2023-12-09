from collections.abc import Iterable
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models
from django.contrib.auth.models import User




CAJA = [
        ('caja_1', 'caja_1'),
        ('caja_2', 'caja_2'),
        ('caja_3', 'caja_3'),
        ('Administrador', 'Administrador'),
    ]

class Asignacion(models.Model):

    usuario = models.ForeignKey(User,on_delete=models.CASCADE)
    caja = models.CharField(max_length=15, choices=CAJA, default='caja_1')
    
    def __str__(self):
        return self.usuario.first_name


class Configuracion(models.Model):
    nombre = models.CharField(max_length=255,blank=True,null=True)
    direccion = models.CharField(max_length=255,blank=True,null=True)
    telefono = models.CharField(max_length=255,blank=True,null=True)
    contactos = models.CharField(max_length=255,blank=True,null=True)
    cuit = models.CharField(max_length=255,blank=True,null=True)
    tiket_comandera = models.BooleanField(default=False)
    vista_clasica = models.BooleanField(default=False)
    mostrar_foto = models.BooleanField(default=False)
    entrega = models.BooleanField(default=False)
    tipo_cambio = models.DecimalField(max_digits=20,decimal_places=2,default=1,blank=False,null=False)

    
@receiver(post_save, sender=Configuracion)
def calcular_precios_post_save(sender, instance, **kwargs):

    from producto.models import Producto  # Importa localmente dentro de la función

    productos = Producto.objects.all()
    configuracion = Configuracion.objects.all().first()

    if configuracion:
        tipo_cambio = configuracion.tipo_cambio
    else:
        tipo_cambio = 1

    for producto in productos:
        
        if producto.costo > 0 and producto.rentabilidad > 0 and producto.rentabilidad < 100:

            producto.precio = ((producto.costo * tipo_cambio) / (100 - producto.rentabilidad)) * 100
            producto.precio_usd =( (producto.costo) / (100 - producto.rentabilidad) )* 100
        
        producto.save()

# Definir un diccionario con el nombre de los meses en español
meses = {
    1: "ENERO",
    2: "FEBRERO",
    3: "MARZO",
    4: "ABRIL",
    5: "MAYO",
    6: "JUNIO",
    7: "JULIO",
    8: "AGOSTO",
    9: "SEPTIEMBRE",
    10: "OCTUBRE",
    11: "NOVIEMBRE",
    12: "DICIEMBRE",
}

def formatear_fecha(fecha):
    dia = fecha.day
    mes_numero = fecha.month
    mes_nombre = meses[mes_numero]
    return f"{dia} De {mes_nombre}"

# Create your models here.
class Cliente(models.Model):
    codigo = models.CharField(unique=True,max_length=200, null=True, blank=True)
    nombre = models.CharField(unique=True,verbose_name='Vendedor',max_length=200, null=True, blank=True)
    telefono = models.CharField(max_length=20,default=1,blank=True,null=True)
    direccion = models.CharField(max_length=200,blank=True,null=True)

    
    def __str__(self):
        return self.nombre

class TipoGasto(models.Model):
    descripcion = models.CharField(max_length=255,unique=True,blank=False,null=False)

    def __str__(self):
        return self.descripcion
    
class Gasto(models.Model):
    fecha = models.DateField(blank=False,null=True)
    categoria = models.ForeignKey(TipoGasto,on_delete=models.SET_NULL,blank=False,null=True)
    descripcion = models.CharField(max_length=255, null=False, blank=False)
    total = models.DecimalField(max_digits=20,decimal_places=2,blank=False,null=False)

    def __str__(self):
        msg = f'{self.categoria} | {self.descripcion} | ${self.total}'
        return msg
    
class Retiro(models.Model):
    fecha = models.DateField(blank=False,null=True)
    descripcion = models.CharField(max_length=255, null=False, blank=False)
    total = models.DecimalField(max_digits=20,decimal_places=2,blank=False,null=False)

    def __str__(self):
        msg = f'{self.fecha} | {self.descripcion} | ${self.total}'
        return msg
    
class Viaje(models.Model):
    estado = models.BooleanField(default=False)
    chofer = models.CharField(max_length=120, null=False, blank=False)
    patente_camion = models.CharField(max_length=120, null=False, blank=False)
    patente_semi = models.CharField(max_length=120, null=True, blank=True)
    fecha_salida = models.DateField(auto_now=True, null=False, blank=False)
    fecha_llegada = models.DateField(null=False, blank=False)
    costo_total_trasnlado = models.DecimalField(verbose_name="Costo de Translado",max_digits=15, decimal_places=2, null=False, blank=False)

    def __str__(self):
        
        if self.estado == True:
            return f'{self.chofer} | llega: 📆 {formatear_fecha(self.fecha_llegada)}'
        else:
            return f'{self.chofer} | llegó: 📆 {formatear_fecha(self.fecha_llegada)}'
        