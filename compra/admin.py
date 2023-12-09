from django.contrib import admin
from compra.models import Compra
from producto.models import Producto
from django.core.exceptions import ValidationError
from import_export.admin import ImportExportModelAdmin

@admin.register(Compra)
class CompraAdmin(ImportExportModelAdmin):
    list_display = ('status','producto', 'cantidad', 'costo', 'total_')
    exclude = ('total', 'estado')

    def costo_(self, obj):
        return "💲{:,.2f}".format(obj.costo)

    def total_(self, obj):
        return "💲{:,.2f}".format(obj.total)

    def status(self, obj):
        if obj.estado == False:
            return "🔴 Pendiente"
        else:
            return "🟢 Controlado"

    def clean(self):
        if self.estado == True:
            raise ValidationError("Este producto ya fue controlado. No se puede modificar.")
        super().clean()

    def save(self, *args, **kwargs):
        super(Compra, self).save(*args, **kwargs)

    def ingresar_compra(self, request, queryset):
        
        for compra in queryset:
            if  compra.estado == False:  # Verifica que el estado sea False antes de cambiarlo
                
                producto = Producto.objects.filter(id=compra.producto.id).first()
                producto.costo = compra.costo
                producto.save()

                compra.estado = True
                compra.save()   
            
    ingresar_compra.short_description = "Ingresar mercaderia"  # Descripción de la acción

    actions = [ingresar_compra]  # Asociar la acción personalizada a la clase CompraAdmin
