from django.contrib import admin
from django.core.exceptions import ValidationError
from .models import *


# Register your models here.

#@admin.register(Configuracion)
#class ConfiguracionAdmin(admin.ModelAdmin):
#    def has_add_permission(self, request):
#        # Solo permitir agregar si no existe ninguna instancia
#        return not Configuracion.objects.exists()

#    def has_delete_permission(self, request, obj=None):
        # Nunca permitir eliminar
#            return False