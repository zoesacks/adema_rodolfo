from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from agenda.models import Configuracion
# Register your models here.
from producto.models import Producto, Categoria,Merma

def calcular_precios(self, request, queryset):

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

    self.message_user(request, f'Se calcularon los precios en dólares para todos los productos.')


@admin.register(Categoria)
class CategoriaAdmin(ImportExportModelAdmin):
    list_display = ('nombre',)

@admin.register(Merma)
class MermaAdmin(ImportExportModelAdmin):
    list_display = ('fecha','producto','cantidad','motivo',)

@admin.register(Producto)
class ProductoAdmin(ImportExportModelAdmin):
    list_display = ('categoria','nombre','descripcion','Costo','rentabilidad','Bolivares','dolar','stock')
    list_filter = ('categoria','nombre','descripcion')
    search_fields = ('nombre',)
    exclude = ('precio','precio_usd','en_stock')
    list_display_links = ('categoria','nombre',)
    actions = [calcular_precios,]

    def Costo(self, obj):
        return "💲{:,.2f}".format(obj.costo) 
    
    def Bolivares(self, obj):
        return "💲{:,.2f}".format(obj.precio)    

    def dolar(self, obj):
        return "💲{:,.2f}".format(obj.precio_usd)
        
    def stock(self, obj):

        return "{:,.0f}".format(obj.stock_actual())    


