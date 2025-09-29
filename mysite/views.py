from django.shortcuts import render
from .models import *
from datetime import datetime
from django.http import JsonResponse
from .Afip.wsaa import WSAA
from .Afip.wsfev1 import WSFEv1
import os
from asgiref.sync import sync_to_async






def home(request):
    return render(request, 'home.html')

def facturador(request):
    fecha = datetime.today().strftime('%d/%m/%Y')
    clientes = Clientes.objects.using('mysql').all()

    contexto = {'fecha':fecha,
        'clientes':clientes}
    return render(request, 'facturador.html', contexto)


def buscar_clientes(request):
    query = request.GET.get('q', '')  # Obtener el parámetro de búsqueda
    if query:
        clientes = Clientes.objects.using('mysql').filter(razons__icontains=query)[:10]  # Filtrar resultados
    else:
        clientes = Clientes.objects.using('mysql').all()
    resultados = list(clientes.values('cuit', 'razons'))  # Convertir a JSON
    return JsonResponse({'clientes': resultados})  # Retornar los datos en JSON

def select_cliente(request):
    query = request.GET.get('q', '')  # Obtener el parámetro de búsqueda
    if query:
        clientes = Clientes.objects.using('mysql').filter(cuit__exact=query)
    resultados = list(clientes.values('razons', 'cuit', 'direccion', 'responsabilidad_id', 'lista'))
    return JsonResponse({'dato_cli': resultados})

def buscar_productos(request):
    query = request.GET.get('q', '')
    query2 = request.GET.get('w', '')
    if query and query2:
        productos = Productos.objects.using('mysql').filter(lista=query2).filter(nombre__icontains=query)
    else:
        productos = Productos.objects.using('mysql').filter(lista=query2)
    resultados = list(productos.values())  # Convertir a JSON
    return JsonResponse({'productos': resultados})  # Retornar los datos en JSON

@sync_to_async
def obtener_Config():
    return Configuracion.objects.using('mysql').first()


async def conectar_wsaa(request):
    ruta_base = os.path.dirname(__file__)  # Carpeta donde está views.py
    Crt = os.path.join(ruta_base, 'static\cert\\testingCRT.crt')
    Key = os.path.join(ruta_base, 'static\cert\\testingKey.key')
    msg = ''
    err = 0
    try:
        global Wsfe
        Wsfe = WSFEv1()
        Wsfe.SetTicketAcceso(
            WSAA().Autenticar("wsfe", Crt, Key))
        Wsfe.Cuit = 20218452789
        config = await obtener_Config()
        Wsfe.Conectar()

    except Exception as e:
        print(str(e))
        if str(e) == 'key values mismatch':
            err = 1
            msg = 'Error: La clave privada no coincide con el certificado'
        elif str(e).startswith('Unable to find the server'):
            err = 2
            msg = 'El servidor de ARCA no está disponible, revise que tenga internet tambien.'
        elif str(e).startswith('ns1:cms.cert.untrusted: Certificado'):
            err = 2
            msg = 'Certificado no emitido por AC de confianza.'
    return JsonResponse({'mensaje': msg, 'err': err})

async def obtener_nrofact(request):
    global Wsfe
    query = request.GET.get('q', '')  # Obtener el parámetro de búsqueda
    config = await obtener_Config() 
    comprobante = Wsfe.CompUltimoAutorizado(int(query), int(config.punto_venta))
    return JsonResponse(
        {'Nrofact': config.punto_venta.zfill(5) + '-' + str(int(comprobante) + 1).zfill(8)})
