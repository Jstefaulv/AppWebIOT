#include "Arduino.h"

class RELES{
  public:
  RELES(int R1, int R2, int R3, int R4): pin_r1(R1), pin_r2(R2), pin_r3(R3),
  pin_r4(R4){

  }

  void begin(){
    pinMode(pin_r1,OUTPUT);
    pinMode(pin_r2,OUTPUT);
    pinMode(pin_r3,OUTPUT);
    pinMode(pin_r4,OUTPUT);

    activar(0x00);
  }

  void activar(char R){
    digitalWrite(pin_r1,(R & 0x01) ? LOW : HIGH);
    digitalWrite(pin_r2,(R & 0x02) ? LOW : HIGH);
    digitalWrite(pin_r3,(R & 0x04) ? LOW : HIGH);
    digitalWrite(pin_r4,(R & 0x08) ? LOW : HIGH);
  }
  
  char leer(){
    char r = 0;
    r = (digitalRead(pin_r1)==HIGH) ? r : (r | 0x01);
    r = (digitalRead(pin_r2)==HIGH) ? r : (r | 0x02);
    r = (digitalRead(pin_r3)==HIGH) ? r : (r | 0x04);
    r = (digitalRead(pin_r4)==HIGH) ? r : (r | 0x08);
    return r;
  }
  
  private:
  int pin_r1, pin_r2, pin_r3, pin_r4;
};

