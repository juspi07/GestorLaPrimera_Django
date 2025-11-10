from django.db.models.signals import post_migrate
from django.dispatch import receiver
from mysite.models import *
from django.utils import timezone
from django.contrib.auth import get_user_model



@receiver(post_migrate)
def crear_registros_iniciales(sender, **kwargs):
    if sender.name == 'mysite':
        if not RespIva.objects.exists():
            respiva_obj = RespIva.objects.create(descripcion='RESPONSABLE INSCRIPTO')
        if not Zonas.objects.exists():
            zonas_obj = Zonas.objects.create(nombre='BUENOS AIRES', dgr=27)
        if not Listas.objects.exists():
            lista_obj = Listas.objects.create(nombre='SUPERMERCADOS')
        if not Productos.objects.exists():
            ahora = timezone.now()
            Productos.objects.create(nombre='PAN DE PANCHO X6', lista=lista_obj, precio=1200.00, fecha=ahora, iva='21.0')
        if not Clientes.objects.exists():
            Clientes.objects.create(cuit='30716920093', razons= 'ASD SISTEMAS MEDICOS',
                direccion='UGARTE MANUEL 3867 Piso:3 Dpto:H', provincia=zonas_obj,
                lista=lista_obj, responsabilidad=respiva_obj, descuento=0, recargo=0)
        if not Comprobantes.objects.exists():
            Comprobantes.objects.create(descripcion='FACTURA A', codigo='001')
        if not Configuracion.objects.exists():
            Configuracion.objects.create(punto_venta='00040')


    User = get_user_model()
    username = 'admin'
    email = 'admin@example.com'
    password = '1234'

    if not User.objects.filter(username=username).exists():
        User.objects.create_superuser(username=username, email=email, password=password)
