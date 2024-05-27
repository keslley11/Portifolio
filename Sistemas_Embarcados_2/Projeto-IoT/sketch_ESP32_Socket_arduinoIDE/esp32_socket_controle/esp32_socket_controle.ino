#include <WebServer.h>
#include <WebSocketsServer.h>
//#include <WiFi.h>

//temperatura em °C  [38,6 - 97,7 °C] --> necessário garantir que a temperatura esteja neste intervalo!

//=============================================================================
//    Prototipo das funções
//=============================================================================

void webSocketEvent(uint8_t num, WStype_t type, uint8_t * payload, size_t length);
float resistanceTemperature(float V_in, float R_serie);
void incpulso ();
float controlador(float r, float y);




#define pwm_out 32   //[ESP] Saída PWM
//#define pwm_out 5   //[Arduino]
#define resistencia  33      // [ESP] Ativa resistencia (transistor queimou --> ligar direto)
//#define resistencia  7    //[Arduino]
//#define sensorPin 0    //[Arduino] (analogRead-> A0-> ADC0)
//#define interruptPin 3; //[Arduino] pino de interrupção

//#define ledPin 33 //[ESP]Led indicador de conexão (--> 'resistencia' )
#define sensorPin 34 //[ESP]leitura porta analogica




//=============================================================================
//    Controle PI - temperatura
//=============================================================================



// Variaveis gerais
float V_cc=5.0; // Valor da fonte de Alimentação  
#define nSamples 3 // Set the number of samples of the mean at the aquisition 

#define T_amostragem 1000 //periodo de amostragem : 1s 
//unsigned long t1=0;
//unsigned long t2=0;
//unsigned long loop_web=0;
//unsigned long elapsedTime = 0;
unsigned long n_amostra=0;
unsigned long start_time;
float t1=0;
float t2=0;
float loop_web=0;
float elapsedTime = 0;

//float RPM=0.0; 
//float RPM1=0.0;

volatile unsigned int contaPulso; //Variável para a quantidade de pulsos (por interrupção)


//Variaveis de controle 

float valor = 0.0;
int duty_cycle = 0;
int sp=40; //SetPoint 
float Temperatura=0.0; //Variavel de temperatura
bool ligar_controle = true;

//Controlador 
float u = 0.0, ek = 0.0, uk_1 = 0.0, ek_1 = 0.0; 
float b0 = -67.5; 
float b1 = 66.5;



//Funções
float resistanceTemperature(float V_in, float R_serie) {         // Caracterizado em range de temperatura 38,6 - 97,7 °C
  float x1 = log((V_cc*R_serie)/V_in - R_serie);  //determina a resistência do termistor
  float A,B,C;

  A=0.001218;
  B=0.0002175;
  C=1.641e-07;

 
  float T = 1/(A + (B*x1) + (C*x1*x1*x1)) - 273.15;
  return T;// retorna temperatura em °C
}

void incpulso ()  {
 contaPulso++; //Incrementa a variável de pulsos
}

//Implementação do PI Digital
float controlador(float r, float y){

  ek = r-y;
  u = uk_1 + b0*ek + b1*ek_1;

  //Serial.println(ek);
  //Serial.println(u);

  if (u>255) u=255;     // limitador superior
  else if (u<0) u=0;    // limitador inferior

  ek_1 = ek;
  uk_1 = u;

  return u;
}




//=============================================================================
//    Conexão via Socket
//=============================================================================


//Parâmetros do Wifi
/* (wifi) --> atualizar IP no script index.html (acoes.js)
const char* ssid = "..." ;
const char* password = "...";
*/


/* (wifi lab - domotica)
const char* ssid = "Domotica" ;
const char* password = "domotica1c203a";
//*/
/* (wifi 1)
const char* ssid = "PINGO" ;
const char* password = "palio6635";
//*/
/* (wifi 2)
const char* ssid = "Joao " ;
const char* password = "123k56k8";
//*/
///* (wifi)
const char* ssid = "Redmi 13C";  //"iPhone de Amanda" ;
const char* password = "Senha1234";  //"amandinha123";
//*/

// --> 'ws:// ... :81/' (wifi) --> atualizar no script
// --> 'ws://192.168.0.10?:81/' (wifi lab - domotica)
// --> 'ws://192.168.100.10:81/' (wifi casa 1)
// --> 'ws://192.168.1.10:81/' (wifi casa 2)


  
//Parâmetros dos servidores
WebSocketsServer webSocket = WebSocketsServer(81);



//Função que recebe as mensagens do site e chama os comandos
void webSocketEvent(uint8_t num, WStype_t type, uint8_t * payload, size_t length) {
  Serial.print("Mensagem recebida: ");
  Serial.println((char*)payload);


  if(type == WStype_TEXT){

    if (strcmp((char*)payload, "temp") == 0) {
      // Se receber "temp", enviar a leitura de temperatura
      
      String resposta = String(Temperatura)+"° |"+String(sp)+"° |"+String(duty_cycle*100/255);
      webSocket.sendTXT(num, resposta);
      Serial.print("Mensagem enviada: ");
      Serial.println(resposta);
    }else if (strcmp((char*)payload, "ligar") == 0){
      ligar_controle = true;
    }else if (strcmp((char*)payload, "desligaligar") == 0){
      ligar_controle = false;
    }
    
  }
}


//=============================================================================
//    Setup
//=============================================================================

  void  setup(){

    Serial.begin(115200); //web
    //Serial.begin(9600); //controle

    //=== Setup Controle ===
    pinMode(resistencia, OUTPUT);                  
    digitalWrite(resistencia, HIGH);//HIGH LOW // Saída resistencia
    /*
    //Arduino
    pinMode(interruptPin, INPUT_PULLUP);
    attachInterrupt(digitalPinToInterrupt(interruptPin),incpulso, RISING);//RISING FALLING
    */

    pinMode(pwm_out, OUTPUT);
    ledcSetup(0, 5000, 8); // [ESP32] Inicializa o PWM com frequência de 5000 Hz no pino pwm_out:  Canal 0, frequência 5000 Hz, resolução de 8 bits
    // Associa o canal PWM ao pino ledPin
    ledcAttachPin(pwm_out, 0);
    //======================


    //=== Setup Socket ===
    //pinMode(ledPin, OUTPUT);
    pinMode(sensorPin,INPUT); //Arduino: 0-->1023  //ESP32: 0-->4095 

    //Configurações do Wifi
    WiFi.persistent(false);
    WiFi.mode(WIFI_STA);
    WiFi.begin(ssid, password);
    
    while (WiFi.status() != WL_CONNECTED) {
      delay(1000);
      Serial.println("Conectando ao WiFi...");
    }
    
    Serial.println("Conectado ao WiFi");
    Serial.print("Endereço IP: ");
    Serial.println(WiFi.localIP()); // --> 'ws://:81/' (wifi) --> atualizar no script
                                    // --> 'ws://192.168.0.10?:81/' (wifi lab - domotica)
                                    // --> 'ws://192.168.100.10:81/' (wifi casa 1)
                                    // --> 'ws://192.168.1.10/' (wifi casa 2)

    //Configuração dos servidores
    webSocket.begin();
    webSocket.onEvent(webSocketEvent);
    //======================
    
  }
   
  void loop(){

    // entrada anologica (em bits)
    Temperatura=0; // de 0 a 4095[ESP32]

    for (int j = 1; j <= nSamples; ++j) {// Calcula a média de n leituras
      Temperatura += analogRead(sensorPin)/nSamples; //Leitura do canal selecionado
    }
    Serial.print ("sensor:");
    Serial.print (Temperatura); //funciona só para [38,6 - 97,7 °C]--> [2588 - 3819]

    //região de operação NTC: [38,6 °C - 97,7 °C] ==> Funciona corretamente apenas p/ Entrada analogica entre [2588 - 3819] 

    ///* //==> grampear temperaturas fora de [38,6 °C - 97,7 °C]
    if(Temperatura<2588) Temperatura = 2588;
    else if(Temperatura>3819) Temperatura = 3819;
    //*/ 
    Temperatura =  resistanceTemperature(Temperatura*V_cc/4095, 9970);// NTC: entrada analog --> temperatura em °C  [38,6 - 97,7 °C]

    //=== Loop Socket ===
    t1= millis(); // Inicia tempo de LOOP repetição.
    webSocket.loop();
    t2 = millis();
    loop_web= t2-t1;
    Serial.print("Loop web: ");
    Serial.println(loop_web); // ms
    //Serial.println("ms');


    //=== Loop controle === 
    t1= millis(); // Inicia tempo de LOOP 

    if (Serial.available() > 0) { //
    //Leitura de Setpoint   
    String va = Serial.readStringUntil('\n');
    sp=va.toInt();
    }
  


    //Leitura da rotação do cooler
/*
    contaPulso = 0;//Zera a variável 
    attachInterrupt(digitalPinToInterrupt(interruptPin), incpulso, FALLING); // habilita entrada contador pulsos 
    delay (500); //Aguarda 0.5 segundo
    //start_time = millis(); //substituir delay()
    //while((millis() - start_time) < 500){
    //}
    detachInterrupt(digitalPinToInterrupt(interruptPin)); // Desactiva entrada contador pulsos

    RPM=33*(duty_cycle*100/255) + 500; //rotação esperada do cooler (0-330)+500 -->(500-830)
    RPM1 = (contaPulso/0.5)* 60 / 2; // frequencia dos pulsos
*/


    //Controlador

    valor = controlador(sp,Temperatura);
    duty_cycle = int(valor); 
    //duty_cycle = map(valor, 0, 4095, 0, 255); // teste cooler: analog --> duty_cycle (regra de 3)
    //analogWrite(pwm_out,duty_cycle); //Arduino
    if(ligar_controle) ledcWrite(0, duty_cycle);          //ESP32
    else {
      ledcWrite(0, 0);
      digitalWrite(resistencia, LOW);
    }


    //Monitorar pela serial

    Serial.print (" |sp:");
    Serial.print (sp);
    Serial.print (" |T:");
    Serial.print (Temperatura);
    Serial.print (" |u:");
    Serial.print (u);
    Serial.print (" |%:");
    Serial.print(duty_cycle*100/255);
    //Serial.print(" ");
    //Serial.print(RPM);
    //Serial.print(" ");
    //Serial.print(RPM1);
    Serial.print(" |n:");
    Serial.println(n_amostra);

    
    if(n_amostra > 360){ //  6min --> 360s (1 amostra por seg)
      ledcWrite(0, 0); 
      digitalWrite(resistencia, LOW);
    }
    
    //Tempo 
    t2 = millis();
    elapsedTime = t2- t1;
    Serial.print("loop Controle: ");
    Serial.println(elapsedTime);
    n_amostra +=1;  
    //delay(T_amostragem-elapsedTime);

    // o loop não pode ser maior que T_amostragem
    ///*
    if((loop_web + elapsedTime)> T_amostragem){
      Serial.println("estouro do tempo de amostragem!");
    }else delay(T_amostragem-(loop_web+elapsedTime));
    //*/
    
  }