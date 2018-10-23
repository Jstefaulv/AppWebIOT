from django.conf.urls import url

from . import views
from jchart.views import ChartView
from views import graficaTemperatura, graficaHumedad

grafica_temp = graficaTemperatura()
grafica_hum = graficaHumedad()

urlpatterns = [
    #ejemplo: /home/
    url(r'^$', views.index, name='index'),
    url(r'^(?P<muestreo_id>[0-9]+)/$', views.detalleMuestreo, name='detalle'),
    url(r'^actuadores/$', views.manejoActuadores, name='actuadores'),
    url(r'^graficos/$', views.manejoGraficos, name='graficos'),
    url(r'^charts/line_temperatura/$', ChartView.from_chart(grafica_temp), name='plot_temperaturas'),
    url(r'^charts/line_humedad/$', ChartView.from_chart(grafica_hum), name='plot_humedad'),
]