class MOVIMIENTO{
  public:
  MOVIMIENTO(int pin_in) : pin(pin_in){
    
  }

  void begin(){
    pinMode(pin,INPUT);
  }

  bool hayMovimiento(){
    bool res;
    res = (digitalRead(pin)==HIGH);
    return res;  
  }
  
  private:
  int pin;
};

