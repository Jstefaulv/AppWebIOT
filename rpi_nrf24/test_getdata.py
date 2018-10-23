import RPi.GPIO as GPIO
from lib_nrf24 import NRF24
import spidev
import time
import ctypes
from struct import *
import sqlite3

GPIO.setmode(GPIO.BCM)

addr = [[0xe8,0xe8,0xf0,0xf0, 0xe1],[0xf0,0xf0,0xf0,0xf0,0xe1]]

radio = NRF24(GPIO,spidev.SpiDev())
radio.begin(0,25)
radio.setPayloadSize(32)
radio.setChannel(0x76)
radio.setDataRate(NRF24.BR_1MBPS)
radio.setPALevel(NRF24.PA_MIN)

radio.setAutoAck(True)
radio.enableDynamicPayloads()
radio.enableAckPayload()

radio.openWritingPipe(addr[0])
radio.openReadingPipe(1,addr[1])
radio.printDetails()
radio.stopListening()

#inicializacion del sensor
CMD_START = list('a')
CMD_ACTIV_RELE = 0x02
TIME_OUT = 3
db = sqlite3.connect('../db.sqlite3')
radio.write(CMD_START)
radio.startListening()
print("(INFO) Sensor inicializado")
try:
    while(1):
        time_ini = time.time()
        print("Recibiendo datos del sensor...")
        while( not radio.available()):
            if (time.time()-time_ini) > TIME_OUT:
                print("(WARNING) tiempo de espera agotado!")
                print("(INFO) intentando inicializacion de sensores")
                radio.stopListening()
                radio.write(CMD_START)
                radio.startListening()
                time_ini = time.time()
        recv_msg = []
        radio.read(recv_msg,22)
        recvb=pack('=22B',*recv_msg)
        result = unpack('=Lhhhhffcc',recvb )
        print("momento de la captura: ",str(result[0]))
        print("acelerometro x: ",str(result[1]))
        print("acelerometro y: ",str(result[2]))
        print("acelerometro z: ",str(result[3]))
        print("distancia : ",str(result[4]))
        print("temperatura : ",str(result[5]))
        print("humedad : ",str(result[6]))
        print("movimiento: ",str(result[7]))
        print("reles : ",str(result[8]))

        #base de datos
        dbc = db.cursor()
        date_muestreo = time.strftime('%Y-%m-%d %H:%M:%S')
        dbc.execute('''INSERT INTO appSensores_sensormuestreo (fechaMuestreo,origenMuestreo) VALUES(?,?)''',(date_muestreo,"sensorX_test"))
        dbc.execute('''SELECT id from appSensores_sensormuestreo where id=(select max(id) from appSensores_sensormuestreo)''')
        idm=dbc.fetchone()
        dbc.execute('''INSERT INTO appSensores_sensoracelerometro (idMuestreo_id,ejeX,ejeY,ejeZ) VALUES(?,?,?,?)''',(idm[0],float(result[1]),float(result[2]),float(result[3])))
        dbc.execute('''INSERT INTO appSensores_sensordistancia (idMuestreo_id,distancia) VALUES(?,?)''',(idm[0],float(result[4])))
        dbc.execute('''INSERT INTO appSensores_sensortemperatura (idMuestreo_id,temperatura) VALUES(?,?)''',(idm[0],result[5]))
        dbc.execute('''INSERT INTO appSensores_sensorhumedad (idMuestreo_id,humedad) VALUES(?,?)''',(idm[0],result[6]))
        if result[7]==b'\x0f':
            mov=False
        else:
            mov=True
        dbc.execute('''INSERT INTO appSensores_sensormovimiento (idMuestreo_id,movimiento) VALUES(?,?)''',(idm[0],mov))
        db.commit()

        dbc.execute('''SELECT actuadorUno from appSensores_sensoractuador where id=(select max(id) from appSensores_sensoractuador)''')
        rele1 = dbc.fetchone()
        dbc.execute('''SELECT actuadorDos from appSensores_sensoractuador where id=(select max(id) from appSensores_sensoractuador)''')
        rele2 = dbc.fetchone()
        dbc.execute('''SELECT actuadorTres from appSensores_sensoractuador where id=(select max(id) from appSensores_sensoractuador)''')
        rele3 = dbc.fetchone()
        dbc.execute('''SELECT actuadorCuatro from appSensores_sensoractuador where id=(select max(id) from appSensores_sensoractuador)''')
        rele4 = dbc.fetchone()
        rele = rele1[0] | rele2[0]<<1 | rele3[0] <<2 | rele4[0]<<3
        print("reles db: ",str(rele))
        cmd_rele = [CMD_ACTIV_RELE,rele]
        radio.stopListening()
        radio.write(cmd_rele)
        radio.startListening()
        print("estado rele 1: "+str(rele1[0]))
        print("estado rele 2: "+str(rele2[0]))
        print("estado rele 3: "+str(rele3[0]))
        print("estado rele 4: "+str(rele4[0]))

except KeyboardInterrupt:
    print("cerrando base de datos...")    
    db.close()
    pass
        
