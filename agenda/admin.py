from django.contrib import admin
from .models import Cliente,Gasto,TipoGasto,Retiro,Asignacion,Viaje,Configuracion



@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nombre','telefono','direccion',)

@admin.register(Configuracion)
class ConfiguracionAdmin(admin.ModelAdmin):
    list_display = ('nombre','vista_clasica','mostrar_foto','entrega',)

@admin.register(Asignacion)
class AsignacionAdmin(admin.ModelAdmin):
    list_display = ('usuario','caja',)
        
@admin.register(Retiro)
class RetiroAdmin(admin.ModelAdmin):
    list_display = ('fecha','descripcion','total')

@admin.register(Gasto)
class GastoAdmin(admin.ModelAdmin):
    list_display = ('categoria','descripcion','total')

@admin.register(TipoGasto)
class TipoGastoAdmin(admin.ModelAdmin):
    list_display = ('descripcion',)

@admin.register(Viaje)
class ViajeAdmin(admin.ModelAdmin):
    list_display = ('status','chofer','fecha_llegada','costo_viaje')
    exclude = ('estado','fecha_salida')

    def costo_viaje(self, obj):
        return "💲{:,.2f}".format(obj.costo_total_trasnlado)
    
    def status(self, obj):
        if obj.estado == False:
            return "🛻 En viaje"
        else:
            return "🟢 Controlado"