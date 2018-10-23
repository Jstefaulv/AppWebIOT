#include "DHT.h"
#include <SPI.h>
#include "nRF24L01.h"
#include "RF24.h"
//#include "printf.h"
#include "reles.h"
#include "acelerometro.h"
#include "distancia.h"
#include "movimiento.h"

//definicion de estados
#define ST_STOP       0
#define ST_RUN        3

//longitud del buffer
#define LEN_CMD     2
#define LEN_DATA    10

//tiempo en mS entre lecturas de los sensores
#define TIME_RD_SENS    1500

//definicion de comandos
#define CMD_START       'a'
#define CMD_RUN         1
#define CMD_ACTIV_RELE  2

//pines del rele
#define PIN_RELE4   7
#define PIN_RELE3   6
#define PIN_RELE2   5
#define PIN_RELE1   4
//pin del sensor de movimiento
#define PIN_MOV     3
//pin y tipo de sensor de temperatura y humedad
#define PIN_TEMP    2
#define TMPTYPE DHT11
//pines del acelerometro
#define PIN_ACELX   A0
#define PIN_ACELY   A1
#define PIN_ACELZ   A2
//pin del sensor de distancia
#define PIN_DIST    A5

//objeto sensor de temperatura y humedad
DHT dht(PIN_TEMP, TMPTYPE);
//objeto transceiver de radio
RF24 radio(9,10);
byte addrs[][6]={{0xe8,0xe8,0xf0,0xf0,0xe1},{0xf0,0xf0,0xf0,0xf0,0xe1}};
//objeto Rele
RELES rele(PIN_RELE1,PIN_RELE2,PIN_RELE3,PIN_RELE4);
//objeto acelerometro
ACELEROMETRO acel(PIN_ACELX,PIN_ACELY,PIN_ACELZ);
//objeto sensor de movimiento
MOVIMIENTO mov(PIN_MOV);
//objeto sensor de distancia
DISTANCIA dist(PIN_DIST);

struct DatoSensores{
   unsigned long time_on;
   int acelx, acely, acelz;
   int distancia;
   float temperatura;
   float humedad;
   char movimiento;
   char reles;
} sensores;

unsigned int state, state_next;
unsigned long time_ini, time_aux; 

char buffer_rx[32];
char buffer_tx[32];

void setup() {
  Serial.begin(115200);
  //iniciacion sensor de movimiento
  mov.begin();
  //iniciacion del sensor de temperatura
  dht.begin();
  //iniciacion del rele
  rele.begin();
  //iniciacion del acelerometro
  acel.begin(ACEL_SCALE_1_5);
  
  //inicializacion de la radio
  radio.begin();
  //radio.Retries(0,15);                 // Smallest time between retries, max no. of retries
  radio.setChannel(0x76);
  radio.setPALevel(RF24_PA_LOW);
  radio.openWritingPipe(0xF0F0F0F0E1LL);
  radio.openReadingPipe(1,0xE8E8F0F0E1LL);
//  radio.printDetails();
  radio.enableDynamicPayloads();
  radio.powerUp();
  radio.startListening();
  
  state = ST_STOP;
  Serial.println("Setup end!");
}

void loop() {
  // put your main code here, to run repeatedly:
  char *buff;
  int acelx, acely, acelz;
  int cm;
  
  state_next = state;
  
  switch(state){
    case ST_STOP:
      if(radio.available()){
        Serial.println("ST_STOP Recv msg...");
        buff = buffer_rx;
        while(radio.available())
          radio.read(buff++,1);
        if(buffer_rx[0]==CMD_START){
          Serial.println("ST_STOP go to RUN...");
          time_ini = millis();
          state_next = ST_RUN;
        }
      }
    break;
    case ST_RUN:
      
      //recepcion de un comando
      if(radio.available()){
        Serial.println("Recv msg...");
        buff = buffer_rx;
        while(radio.available())
          radio.read(buff++,2);
        if(buffer_rx[0]==CMD_ACTIV_RELE){
          Serial.print("Rele Activar con ");
          Serial.println(buffer_rx[1],DEC);
          rele.activar(buffer_rx[1]);          
        }
      }
      //envio de lecturas de sensores
      time_aux = (millis()-time_ini);
      if( time_aux > TIME_RD_SENS){
        
        Serial.print("Send Sensors...");
        sensores.time_on = millis();
        sensores.acelx=acel.leerX();
        sensores.acely=acel.leerY();
        sensores.acelz=acel.leerZ();
        sensores.distancia=dist.leerMilimetros();
        sensores.temperatura=dht.readTemperature();
        sensores.humedad=dht.readHumidity();
        sensores.movimiento= (mov.hayMovimiento()==true) ? 0x0A : 0x0F;
        sensores.reles = rele.leer();

        Serial.print("Tiempo: ");
        Serial.println(sensores.time_on);
        Serial.print("acelx: ");
        Serial.println(sensores.acelx);
        Serial.print("acely: ");
        Serial.println(sensores.acely);
        Serial.print("acelz: ");
        Serial.println(acelz);
        Serial.print("distancia: ");
        Serial.println(sensores.distancia);
        Serial.print("temperatura: ");
        Serial.println(sensores.temperatura);
        Serial.print("humedad: ");
        Serial.println(sensores.humedad);
        Serial.print("movimiento: ");
        Serial.println(sensores.movimiento,HEX); 
        Serial.print("reles: ");
        Serial.println(sensores.reles,HEX);
        //preparando la transmision
        radio.stopListening();
        Serial.print("Txing sens...");
        Serial.println(sizeof(sensores));
        if(!radio.write(&sensores,sizeof(sensores)))
          Serial.println("Error!! Txing Sens");
        //
        radio.startListening();
        time_ini = millis();
      }
      
    
  }
  state = state_next;
  
}
