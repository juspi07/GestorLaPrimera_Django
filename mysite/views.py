from django.shortcuts import render
from .models import *
from datetime import datetime
from django.http import JsonResponse
from PyAfipWS.wsaa import WSAA
from PyAfipWS.wsfev1 import WSFEv1
import os
import asyncio

#Productos.objects.using('mysql').all()

def home(request):
    return render(request, 'home.html')

def facturador(request):
    fecha = datetime.today().strftime('%d/%m/%Y')
    clientes = Clientes.objects.using('mysql').all()
    
    contexto = {'fecha':fecha,
        'clientes':clientes}
    return render(request, 'facturador.html', contexto)
    #if conectar_Afip():
    #    return render(request, 'facturador.html', contexto)
    #else:
    #    pass

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

def conectar_Afip():
    try:
        ruta_base = os.path.dirname(__file__)  # Carpeta donde está views.py
        Crt = os.path.join(ruta_base, 'static\cert\\testingCRT.crt')
        Key = os.path.join(ruta_base, 'static\cert\\testingKey.key')
    
        Wsfe = WSFEv1()
        Wsfe.SetTicketAcceso(
            WSAA().Autenticar("wsfe", Crt, Key))
        Wsfe.Cuit = 20218452788

        
        Wsfe.Conectar()
        
        #Wsfe.Cuit = 30670206528
        return True
    except:
        return False

async def conectar_wsaa(request):
    ruta_base = os.path.dirname(__file__)  # Carpeta donde está views.py
    Crt = os.path.join(ruta_base, 'static\cert\\testingCRT.crt')
    Key = os.path.join(ruta_base, 'static\cert\\testingKey.key')
    msg = ''
    err = 0
    try:
        Wsfe = WSFEv1()
        Wsfe.SetTicketAcceso(
            WSAA().Autenticar("wsfe", Crt, Key))
        Wsfe.Cuit = 20218452789

        await Wsfe.Conectar()
    except Exception as e:
        print(str(e))
        if str(e) == 'key values mismatch':
            err = 1
            msg = 'Error: La clave privada no coincide con el certificado'
        elif str(e).startswith('Unable to find the server'):
            err = 2
            msg = 'El servidor de AFIP no está disponible, revise que tenga internet tambien.'
    return JsonResponse({'mensaje': msg, 'err': err})
    