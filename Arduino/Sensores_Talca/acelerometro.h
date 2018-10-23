#include "Arduino.h"

#define ACEL_SCALE_1_5  0
#define ACEL_SCALE_6    1

#define mG_MIN_1_5    -2063 //(1000*1650/800)
#define mG_MAX_1_5    3653 //(1000*(5000-1650)/800)

#define mG_MIN_6    -8010 //(1000*1650/206)
#define mG_MAX_6    13835 //(1000*(5000-1650)/206)

#define mVOLT_G_1_5  800
#define mVOLT_G_6    206

#define mVOLT_BIT   5000/1024
#define mVOLT_CERO  1650 //voltaje alimentacion acel / 2
#define mVOLT_ARDUINO 5000

class ACELEROMETRO{
  public:

  ACELEROMETRO(int pX, int pY, int pZ) : pinX(pX), 
  pinY(pY), pinZ(pZ)
  {
    
  }

  void begin(int scal){

    if(scal==ACEL_SCALE_1_5){
      mg_min = mG_MIN_1_5;
      mg_max = mG_MAX_1_5;
    }else if (scal==ACEL_SCALE_6){
      mg_min = mG_MIN_6;
      mg_max = mG_MAX_6;
    }
  }

  int leerX(){
    int val;
    int i;
    for(i=0;i<20;i++)
      val += analogRead(pinX);
    val = val/i;
    val=map(val,0,1023,mg_min,mg_max);
    return val;
  }
  int leerY(){
    int val;
    int i;
    for(i=0;i<20;i++)
      val += analogRead(pinY);
    val = val/i;
    val=map(analogRead(pinY),0,1023,mg_min,mg_max);
    return val;
  }
  int leerZ(){
    int val;
    int i;
    for(i=0;i<20;i++)
      val += analogRead(pinZ);
    val = val/i;
    val=map(analogRead(pinZ),0,1023,mg_min,mg_max);
    return val;
  }
  private:
  int pinX, pinY, pinZ;
  int mg_min, mg_max;  
  
};

