El script test_getdata.py obtiene las mediciones hechas por el sensor arduino y las guarda en una base de datos sqlite. Este script necesita las librerias de python SpiDev, sqlite3 y lib_nrf24 (ya incluida).

El directorio incluye los siguientes archivos:
- test_getdata.py
- lib_nrf24.py

### Instalacion de libreria SpiDev:
```
wget https://github.com/Gadgetoid/py-spidev/archive/master.zip
unzip master.zip
cd py-spidev-master
sudo python setup.py install
```
