from django.contrib import admin
from .models import *


# Register your models here.
admin.site.register(Comprobantes)
#admin.site.register(Ventas)
admin.site.register(VentaProductos)
#admin.site.register(Clientes)
admin.site.register(RespIva)
admin.site.register(Zonas)
admin.site.register(Listas)
#admin.site.register(Productos)
#admin.site.register(Configuracion)



@admin.register(Clientes)
class ClientesAdmin(admin.ModelAdmin):
    list_display = ["razons", "cuit", 'responsabilidad', 'lista', 'alias']
    search_fields = ('razons', 'cuit')
    
@admin.register(Ventas)
class VentasAdmin(admin.ModelAdmin):
    def cliente_name(self, obj):
        return obj.cliente.nombre    
    
    list_display = ["fecha", "comprobante", 'n_fact', 'cliente', 'total']
    search_fields = ('fecha', 'comprobante', 'cliente')

@admin.register(Configuracion)
class ConfiguracionAdmin(admin.ModelAdmin):
    list_display = ['punto_venta']

@admin.register(Productos)
class ProductosAdmin(admin.ModelAdmin):
    list_display = ["nombre", "lista", 'precio', 'fecha']
    search_fields = ('nombre', "lista")