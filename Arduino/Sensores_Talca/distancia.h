#include "Arduino.h"

class DISTANCIA{
  public:
  DISTANCIA(int pin_sens) : pin(pin_sens){
     
  }

  int leerMilimetros(){
    int medicion,res, i;
    float aux;

    medicion=0;
    for (i=0;i<20;i++)
      medicion += analogRead(pin);
    aux = ((float)i/(float)medicion)*5.4054e+04;
      res = (int) aux;
    return res;
  }

  private:
  int pin;
  float dist;
};

