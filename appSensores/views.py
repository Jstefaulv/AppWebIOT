# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.
from django.http import HttpResponse
from django.http import Http404
from django.template import loader
import datetime
from .models import *
from jchart import Chart #Para graficos
from jchart.config import Axes, DataSet, rgba

def index(request):
    #ultimosMuestreos = sensorMuestreo.objects.all()[:5]
    ultimosMuestreos = sensorMuestreo.objects.all().order_by('-id')[:10]
    template = loader.get_template('appSensores/index.html')
    context = {
        'ultimosMuestreos': ultimosMuestreos,
    }
    return HttpResponse(template.render(context, request))
    # return HttpResponse(ultimosMuestreos)


def detalleMuestreo(request, muestreo_id):
    try:
        detalle = sensorMuestreo.objects.get(pk=muestreo_id)
        detalleAcelerometro = sensorAcelerometro.objects.get(idMuestreo_id=muestreo_id)
        try:
            detalleActuador = sensorActuador.objects.get(idMuestreo_id=muestreo_id)
        except ObjectDoesNotExist:
            detalleActuador = None
        detalleDistancia = sensorDistancia.objects.get(idMuestreo_id=muestreo_id)
        detalleHumedad = sensorHumedad.objects.get(idMuestreo_id=muestreo_id)
        detalleMovimiento = sensorMovimiento.objects.get(idMuestreo_id=muestreo_id)
        detalleTemperatura = sensorTemperatura.objects.get(idMuestreo_id=muestreo_id)

    except sensorMuestreo.DoesNotExist:
        raise Http404("ID de muestreo no existe.")
    return render(request, 'appSensores/detalleMuestreo.html', {'detalle': detalle,
                                                                'detalleAcelerometro': detalleAcelerometro,
                                                                'detalleActuador': detalleActuador,
                                                                'detalleDistancia': detalleDistancia,
                                                                'detalleHumedad': detalleHumedad,
                                                                'detalleMovimiento': detalleMovimiento,
                                                                'detalleTemperatura': detalleTemperatura})

def manejoActuadores(request):
    detalleActuador = sensorActuador.objects.filter().order_by('-id')[0]
    return render(request, 'appSensores/manejoActuadores.html', {'detalleActuador': detalleActuador})

def manejoGraficos(request):
    detalle = sensorMuestreo.objects.filter().order_by('-id')[0]
    return render(request, 'appSensores/graficos.html', {'ultimoMuestreo': detalle})

#Para incluir graficos
class graficaTemperatura(Chart):
    chart_type = 'line'
    responsive = True
    scales = {
        'xAxes': [Axes(type='time', position='bottom')],
    }



    def get_datasets(self, **kwargs):
        #Se leen todas las temperaturas desde BD
        temperaturas = sensorTemperatura.objects.all()
        #Para cada registro de temperatura, se obtiene el ID del muestreo y valor. Se presenta como lista
        #data = [{'x': temp.idMuestreo_id, 'y': temp.temperatura} for temp in temperaturas]
        data = [{'x':temp.id, 'y': temp.temperatura} for temp in temperaturas]
        data_scatter = data
        data_line = data
        return [{
            'type':'line',
            'label': "Temperatura Registrada",
            'data': data,
            'borderColor':'brown'
        }
        ]

class graficaHumedad(Chart):
    chart_type = 'line'
    responsive = True
    scales = {
        'xAxes': [Axes(type='time', position='bottom')],
    }

    def get_datasets(self, **kwargs):
        #Se leen todas los registros de Humedad desde BD
        humedades = sensorHumedad.objects.all()
        #Para cada registro de humedad, se obtiene el ID del muestreo y valor. Se presenta como lista
        data = [{'y': hum.humedad, 'x': hum.id} for hum in humedades]
        return [{
            'label': "Humedad Registrada",
            'data': data,
            'borderColor': 'orange'
        }]
