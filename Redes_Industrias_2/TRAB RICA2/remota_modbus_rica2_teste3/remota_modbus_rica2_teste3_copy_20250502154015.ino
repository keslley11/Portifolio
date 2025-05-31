//#include <WiFi.h> 
#include <ModbusIP_ESP8266.h> 
 
/*
Modscan teste:

IP : [serial]
Device Id:1
Addr: 0001
Len: 5
Function: 03

*/

/* Obs:
    - verifique a rede que irá conectar para comunicar via TCP/IP (linha 60)
    - Após conectar a remota ao modscan, escreva "1" no primeiro registro do modscan para habilitar a remota;
    - Apenas a leitura analógica é feita sem estar habilitada;
    - A interrupção assossiada ao botão de alarme as vezes trava a ESP32, neste caso reinicie tudo.
 */ 
 
#define SLAVE_ID 1 

#define HREG_BASE_ADDRESS                                    40001 
 
#define LED_VERMELHO_ON_OFF_COIL_ADRESS                     (40001 - HREG_BASE_ADDRESS)
#define LED_VERDE_OXIGENIO_HREG_ADRESS                      (40002 - HREG_BASE_ADDRESS)  
#define LED_AMARELO_GAS_HREG_ADRESS                         (40003 - HREG_BASE_ADDRESS)
#define BOTAO_ALARME_INPUT_COIL_LOCAL_ADRESS                (40004 - HREG_BASE_ADDRESS)
#define POT_TEMPERATURA_IREG_ADRESS                         (40005 - HREG_BASE_ADDRESS)  


 
/* Pinout */ 
#define BOTAO_ALARME_PIN                                    25 //DI --> BT Alarme
#define LED_VERMELHO_ON_OFF_PIN                             33 //DO --> LED ON_OFF modbus
#define POT_TEMPERATURA_PIN                                 34 //AI --> Potenciometro (temperatura)
#define LED_VERDE_OXIGENIO_PIN                              32 //AO --> LED pwm (Valvula O2)
#define LED_AMARELO_GAS_PIN                                 27 //AO --> LED pwm (Valvula Gas) 


/* Global variables*/   
ModbusIP mb; 
size_t timestamp; 
size_t holdingStartTime = 0; // Tempo de início do estado HOLDING 
 
bool sys_on = false;
//bool alarme = false;

uint16_t temperatura;

volatile bool alarme = false;
volatile unsigned long lastInterruptTime = 0; // Guarda o tempo da última interrupção
const unsigned long debounceDelay = 1000;      // Tempo de debounce em milissegundos

/* ISR Callback functions */ 
void IRAM_ATTR ISR_bt_sensor() {
  
  unsigned long currentTime = millis();
  if ((currentTime - lastInterruptTime) > debounceDelay) {
    alarme = !alarme;
    if (alarme) {
      Serial.println("Alarme!");
    } else {
      Serial.println("Alarme off");
    }
    lastInterruptTime = currentTime;
  }
} 
 
void setup() { 
  /* Connect to network*/ 
  Serial.begin(9600); 
  WiFi.begin("INDUSTRIA", "industria50");
  //WiFi.begin("PINGO", "palio6635");
  //WiFi.begin("LASEC", "lasecca123");
   
  while (WiFi.status() != WL_CONNECTED) { 
    delay(500); 
    Serial.println("Connecting to WiFi.."); 
  } 
 
  Serial.println(""); 
  Serial.println("WiFi connected");  
  Serial.print("IP address: "); 
  Serial.println(WiFi.localIP()); 
 
  //**configura pinos de entradas e saidas** 

  // Entrada Digital (DI): configura Botão como pulldown, interrupção
  pinMode(BOTAO_ALARME_PIN, INPUT_PULLDOWN);
  attachInterrupt(digitalPinToInterrupt(BOTAO_ALARME_PIN), ISR_bt_sensor, 
FALLING); 
 
  // Saída Digital (DO): configura LEDs e define os estado inicial para 0 
  pinMode(LED_VERMELHO_ON_OFF_PIN, OUTPUT);
  digitalWrite(LED_VERMELHO_ON_OFF_PIN, LOW); 
 
  // configura AI
  pinMode(POT_TEMPERATURA_PIN,INPUT);

  // configura AO
  pinMode(LED_VERDE_OXIGENIO_PIN, OUTPUT);
  pinMode(LED_AMARELO_GAS_PIN, OUTPUT);
  // Configura os canais PWM para controlar os leds
  ledcSetup(0, 5000, 8); // Canal 0, frequência 5000 Hz, resolução de 8 bits
  ledcAttachPin(LED_VERDE_OXIGENIO_PIN, 0);// Associa o canal PWM ao pino
  ledcSetup(1, 5000, 8); // Canal 1, frequência 5000 Hz, resolução de 8 bits
  ledcAttachPin(LED_AMARELO_GAS_PIN, 1);// Associa o canal PWM ao pino
 
  /* Add and set holding registers */ 
  mb.addHreg(BOTAO_ALARME_INPUT_COIL_LOCAL_ADRESS); 
  mb.Hreg(BOTAO_ALARME_INPUT_COIL_LOCAL_ADRESS, LOW);
  
  mb.addHreg(LED_VERMELHO_ON_OFF_COIL_ADRESS); 
  mb.Hreg(LED_VERMELHO_ON_OFF_COIL_ADRESS, LOW);
 
  mb.addHreg(POT_TEMPERATURA_IREG_ADRESS); 
  mb.Hreg(POT_TEMPERATURA_IREG_ADRESS, 25);
 
  mb.addHreg(LED_VERDE_OXIGENIO_HREG_ADRESS); 
  mb.Hreg(LED_VERDE_OXIGENIO_HREG_ADRESS, 0);
  
  mb.addHreg(LED_AMARELO_GAS_HREG_ADRESS); 
  mb.Hreg(LED_AMARELO_GAS_HREG_ADRESS, 0);
  
 
  //initialize modbus connection 
  mb.server(); 
} 
 
void loop() { 
  mb.task(); 
  if (millis() - timestamp > 100) 
  { 
    timestamp = millis(); 

    //******************************************************* 
    // ativação da remota via modbus
    //*******************************************************
    if(mb.Hreg(LED_VERMELHO_ON_OFF_COIL_ADRESS)!=0) 
    { 
      sys_on = true;
    }   
    else 
    {  
      sys_on = false; 
    }  
    
    //******************************************************* 
    // rotina de atualizacoes de ENTRADAS 
    //*******************************************************  

    //limpa alarme
    /*
    if(mb.Hreg(BOTAO_ALARME_INPUT_COIL_LOCAL_ADRESS) == 0){
      alarme = false;
    }
    */

    // entradas digitais
    if(alarme){
      mb.Hreg(BOTAO_ALARME_INPUT_COIL_LOCAL_ADRESS, HIGH);
    } else{
      mb.Hreg(BOTAO_ALARME_INPUT_COIL_LOCAL_ADRESS, LOW);
    }
    
    // entradas analogicas
    temperatura = int(float(analogRead(POT_TEMPERATURA_PIN))/4095.0*1600.0);  // Regra de 3: 4095 --> 1600
    mb.Hreg(POT_TEMPERATURA_IREG_ADRESS, temperatura); 

    
 
    //******************************************************* 
    // rotina de atualizacoes de SAIDAS 
    //******************************************************* 
 
    // saidas digitais
    if(sys_on) 
    { 
      digitalWrite(LED_VERMELHO_ON_OFF_PIN, HIGH);
    }   
    else 
    {  
      digitalWrite(LED_VERMELHO_ON_OFF_PIN, LOW); 
    }       

    // atualiza saidas PWM conforme o estado do registro no servidor 
    if(sys_on) 
    {  
      //analogWrite(PIN, mb.Hreg(ADRESS));
      // Ajusta os leds de 0 a 255

      //float duty0 = (mb.Hreg(LED_VERDE_OXIGENIO_HREG_ADRESS))/65536.0*255.0; // regra de 3: 65536 --> 255
      
      uint16_t value0 = mb.Hreg(LED_VERDE_OXIGENIO_HREG_ADRESS);
      value0 = (value0 <= 100)? value0 : 100; //grampear valor max da valvula (100%)
      float duty0 = float(value0)/100.0*255.0; // regra de 3: 100 --> 255
      
      ledcWrite(0, int(duty0));
      
      //float duty1 = (mb.Hreg(LED_AMARELO_GAS_HREG_ADRESS))/65536.0*255.0; // regra de 3: 65536 --> 255
      uint16_t value1 = mb.Hreg(LED_AMARELO_GAS_HREG_ADRESS);
      value1 = (value1 <= 100)? value1 : 100; //grampear valor max da valvula (100%)
      float duty1 = float(value1)/100.0*255.0; // regra de 3: 100 --> 255
      
      ledcWrite(1, int(duty1));
    } 
    else 
    {
      //analogWrite(PIN, 0);
      ledcWrite(0, 0);
      ledcWrite(1, 0);
    } 
 
  } 
  yield(); 
} 