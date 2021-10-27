//-------------Controle INMOOV-----------------
//Arquivo para Download no Arduino  
//Autor: Daniel Formiga
//---------------------------------------------
#include <Servo.h>
Servo servopolegar;         
Servo servoindicador;         
Servo servomeio;
Servo servoanelar;
Servo servomindinho;
//------------------Setup---------------------
//Baudrate na linha
//Saída PWM do Arduíno
int outPolegar = 44;
int outIndicador = 11;
int outMeio = 6;
int outAnelar = 5;
int outMindinho = 4;
//Valores de abre e fecha dos servos de cada dedo
int IndAbre = 20;
int IndFecha = 150;
int MeioAbre = 55;
int MeioFecha = 160;
int AnelAbre = 20;
int AnelFecha = 120;
int MinAbre = 150;
int MinFecha = 50;
int PolAbre = 130;
int PolFecha = 50;
//--------------------------------------------
char number[50];
char c;
int state = 0;
String myStringRec;
int stringCounter = 0;
bool stringCounterStart = false;
String myRevivedString;
int stringLength = 6;
int servoMindinho,servoMeio,servoIndicador,servoPolegar,servoAnelar;
int myVals[] ={0,0,0,0,0} ;
 
void setup() {
 
  Serial.begin(115200);
  servopolegar.attach(44); 
  servoindicador.attach(11); 
  servomindinho.attach(4);
  servoanelar.attach(5);
  servomeio.attach(6);
  delay(500);
   
}
 
void loop() {
receiveData();
if (servoMindinho ==1){  servomindinho.write(MinAbre);}else{servomindinho.write(MinFecha);}
if (servoIndicador ==1){  servoindicador.write(IndAbre);}else{servoindicador.write(IndFecha);}
if (servoMeio ==1){  servomeio.write(MeioAbre);}else{servomeio.write(MeioFecha);}
if (servoPolegar ==1){  servopolegar.write(PolAbre);}else{servopolegar.write(PolFecha);}
if (servoAnelar ==1){  servoanelar.write(AnelAbre);}else{servoanelar.write(AnelFecha);}
}

void receiveData() {
  int i = 0;
  while (Serial.available()) {
   char c = Serial.read();
   
    if (c == '$') {
      stringCounterStart = true;
    }
    if (stringCounterStart == true )
    {
      if (stringCounter < stringLength)
      {
        myRevivedString = String(myRevivedString + c);
        stringCounter++;
      }
      if (stringCounter >= stringLength) {
        stringCounter = 0; stringCounterStart = false;
        servoMindinho = myRevivedString.substring(1, 2).toInt();
        servoAnelar = myRevivedString.substring(2, 3).toInt();
        servoMeio = myRevivedString.substring(3, 4).toInt();
        servoIndicador = myRevivedString.substring(4, 5).toInt();
        servoPolegar = myRevivedString.substring(5, 6).toInt();
//--------------DEBUG-----------------        
//        Serial.print(servoMindinho);
//        Serial.print(" ");
//        Serial.print(servoAnelar);
//        Serial.print(" ");
//        Serial.print(servoMeio);
//        Serial.print(" ");
//        Serial.print(servoIndicador);
//        Serial.print(" ");
//        Serial.println(servoPolegar);
//-------------------------------------
          delay(90); //Delay para evitar erro de escrita serial     
        myRevivedString = "";
      }
    }
  }
}
