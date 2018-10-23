# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
class sensorMuestreo(models.Model):
    fechaMuestreo = models.DateField()
    origenMuestreo = models.TextField(max_length=10)

    def __str__(self):
        return self.origenMuestreo


class sensorMovimiento(models.Model):
    movimiento = models.BooleanField(default=True)
    idMuestreo = models.ForeignKey(sensorMuestreo, on_delete=models.CASCADE)


class sensorDistancia(models.Model):
    distancia = models.FloatField()
    idMuestreo = models.ForeignKey(sensorMuestreo, on_delete=models.CASCADE)


class sensorAcelerometro(models.Model):
    ejeX = models.FloatField()
    ejeY = models.FloatField()
    ejeZ = models.FloatField()
    idMuestreo = models.ForeignKey(sensorMuestreo, on_delete=models.CASCADE)


class sensorTemperatura(models.Model):
    temperatura = models.FloatField()
    idMuestreo = models.ForeignKey(sensorMuestreo, on_delete=models.CASCADE)

class sensorHumedad(models.Model):
    humedad = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(100.0)])
    idMuestreo = models.ForeignKey(sensorMuestreo, on_delete=models.CASCADE)

class sensorActuador(models.Model):
    actuadorUno = models.BooleanField(default=False)
    actuadorDos = models.BooleanField(default=False)
    actuadorTres = models.BooleanField(default=False)
    actuadorCuatro = models.BooleanField(default=False)
    idMuestreo = models.ForeignKey(sensorMuestreo, on_delete=models.CASCADE)

