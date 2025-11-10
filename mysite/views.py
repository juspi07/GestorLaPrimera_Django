from django.shortcuts import render
from .models import *
from datetime import datetime
from django.http import JsonResponse, HttpResponseForbidden, HttpResponse
from django.template.loader import render_to_string
from .Afip.wsaa import WSAA
from .Afip.wsfev1 import WSFEv1
import os
from asgiref.sync import sync_to_async
from django.views.decorators.cache import never_cache

import json
from base64 import b64encode
import qrcode
from io import BytesIO
import base64



def home(request):
    return render(request, 'home.html')

@never_cache
def facturador(request):
    fecha = datetime.today().strftime('%d/%m/%Y')
    clientes = Clientes.objects.all()

    contexto = {'fecha':fecha,
        'clientes':clientes}
    return render(request, 'facturador.html', contexto)


def buscar_clientes(request):
    query = request.GET.get('q', '')  # Obtener el parámetro de búsqueda
    if query:
        clientes = Clientes.objects.filter(razons__icontains=query)[:10]  # Filtrar resultados
    else:
        clientes = Clientes.objects.all()
    resultados = list(clientes.values('cuit', 'razons'))  # Convertir a JSON
    return JsonResponse({'clientes': resultados})  # Retornar los datos en JSON

def select_cliente(request):
    query = request.GET.get('q', '')  # Obtener el parámetro de búsqueda
    if query:
        clientes = Clientes.objects.filter(cuit__exact=query)
    resultados = list(clientes.values('razons', 'cuit', 'direccion', 'responsabilidad__descripcion', 'lista__nombre'))
    return JsonResponse({'dato_cli': resultados})

def buscar_productos(request):
    query = request.GET.get('q', '')
    query2 = request.GET.get('w', '')
    if query and query2:
        productos = Productos.objects.filter(lista__nombre=query2).filter(nombre__icontains=query)
    else:
        productos = Productos.objects.filter(lista=query2)
    resultados = list(productos.values())  # Convertir a JSON
    return JsonResponse({'productos': resultados})  # Retornar los datos en JSON

@sync_to_async
def obtener_Config():
    return Configuracion.objects.first()


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
        Wsfe.Cuit = 20218452788
        await obtener_Config()
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
    global Wsfe, letra
    query = request.GET.get('q', '')
    letra = int(query)
    config = await obtener_Config() 
    comprobante = Wsfe.CompUltimoAutorizado(int(query), int(config.punto_venta))
    return JsonResponse(
        {'Nrofact': config.punto_venta.zfill(5) + '-' + str(int(comprobante) + 1).zfill(8)})


#@csrf_exempt
def generarFactura(request):
    if request.method != 'POST': #or request.headers.get('X-Internal-Request') != 'true':
        return HttpResponseForbidden("Acceso no permitido por GET")
    
    

    global letra
    if letra == 1:
        Comp = 'A'
        comp = 'FACTURA A'
        Cod='001'
    else:
        Comp = 'B'
        comp = 'FACTURA B'
        Cod='006'
    Fecha=request.POST.get('date')
    N_fact=request.POST.get('Nrofact')
    Razons=request.POST.get('razons')
    Dir=request.POST.get('dir')
    Cuit=request.POST.get('cuit')
    Resp=request.POST.get('resp')
    Pan105=request.POST.get('neto105')
    Pan21=request.POST.get('neto21')
    Iva105=request.POST.get('iva105')
    Iva21=request.POST.get('iva21')
    Total=request.POST.get('total')
    Prod = json.loads(request.POST.get('inputJson'));
   
    Ventas.objects.create(
        fecha= datetime.strptime(Fecha, "%d/%m/%Y").strftime("%Y-%m-%d"),
        comprobante= Comprobantes.objects.get(descripcion=comp),
        n_fact=N_fact,
        cliente= Clientes.objects.get(cuit=Cuit),
        pan105=Pan105.split(' ')[1],
        pan21=Pan21.split(' ')[1],
        exento= '0.00',
        iva105=Iva105.split(' ')[1],
        iva21=Iva21.split(' ')[1],
        otros= '0.00',
        total=Total.split(' ')[1]
    )

    global Wsfe

    punto_vta = int(N_fact.split('-')[0])
    cbte_nro = int(N_fact.split('-')[1])
    nro_doc = Cuit.replace('-','')
    imp_total = Total.split(' ')[1]
    imp_neto = str(round((float(Pan105.split(' ')[1]) + float(Pan21.split(' ')[1])),2))
    imp_iva = str(round((float(Iva105.split(' ')[1]) + float(Iva21.split(' ')[1])),2))
    fecha_cbte = datetime.now().strftime("%Y%m%d")
    
    Wsfe.CrearFactura(
        concepto=1, nro_doc=nro_doc, tipo_cbte=1,
        cbt_desde=cbte_nro , cbt_hasta=cbte_nro, fecha_cbte=fecha_cbte,
        punto_vta=punto_vta, imp_total=imp_total,
        imp_neto=imp_neto, imp_iva=imp_iva,
        condicion_iva_receptor_id=1
    )

    if Pan21.split(' ')[1] != '0.00':
        Wsfe.AgregarIva(5, round(float(Pan21.split(' ')[1]),2), round(float(Iva21.split(' ')[1]),2))

    if Pan105.split(' ')[1] != '0.00':
        Wsfe.AgregarIva(4, round(float(Pan105.split(' ')[1]),2), round(float(Iva105.split(' ')[1]),2))
    
    Wsfe.CAESolicitar()

    #print(Wsfe.ErrMsg)
    #print(Wsfe.Obs)

    vto = Wsfe.Vencimiento[-2:] + '/' \
        + Wsfe.Vencimiento[-4:-2] + '/' \
        + Wsfe.Vencimiento[:4]

    afip = 'https://www.arca.gob.ar/fe/qr/?p='
    
    aux = { "ver":1,"fecha":datetime.now().strftime("%Y-%m-%d"),
    "cuit":30670206528,"ptoVta":punto_vta,"tipoCmp":letra,
    "nroCmp":cbte_nro,"importe":float(imp_total),"moneda":"PES",
    "ctz":"1.000","tipoDocRec":80,"nroDocRec":int(nro_doc),
    "tipoCodAut":"E","codAut":int(Wsfe.CAE) }
        
    code = b64encode(json.dumps(aux).encode('utf-8'))
    code = code.decode('utf-8')
    qr = afip + code
    
    datos_factura = {
        'Fecha': Fecha,
        'Comp': Comp,
        'Cod' : Cod,
        'N_fact': N_fact,
        'Razons': Razons,
        'Cuit': Cuit,
        'Dir': Dir,
        'Resp': Resp,
        'productos': Prod,
        'subtotal': imp_neto,
        'iva105': Iva105.split(' ')[1],
        'iva21': Iva21.split(' ')[1],
        'total': imp_total,
        'cae': Wsfe.CAE,
        'vto': vto,
        'qr': qr
    }

    print(datos_factura)
    
    
    html = render_to_string('factura.html', {'datos': datos_factura})
    return HttpResponse(html)


def imprimirFactura(request, datos):
    return render(request, 'factura.html', {'datos': datos})
