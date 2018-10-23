# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from .models import sensorMuestreo,\
    sensorAcelerometro,sensorActuador,\
    sensorDistancia,\
    sensorHumedad,\
    sensorMovimiento,\
    sensorTemperatura
admin.site.register(sensorMuestreo)
admin.site.register(sensorAcelerometro)
admin.site.register(sensorActuador)
admin.site.register(sensorDistancia)
admin.site.register(sensorHumedad)
admin.site.register(sensorMovimiento)
admin.site.register(sensorTemperatura)


