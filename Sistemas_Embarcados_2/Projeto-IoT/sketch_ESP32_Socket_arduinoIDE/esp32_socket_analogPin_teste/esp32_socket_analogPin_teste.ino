/*
#include <SocketIOclient.h>
#include <WebSockets.h>
#include <WebSockets4WebServer.h>
#include <WebSocketsClient.h>
#include <WebSocketsServer.h>
#include <WebSocketsVersion.h>
*/


#include <WebServer.h>
#include <WebSocketsServer.h>
//#include <WiFi.h>

//Parâmetros do Wifi
/* (wifi) --> atualizar IP no script index.html (acoes.js)
const char* ssid = "..." ;
const char* password = "...";
*/
/* (wifi casa 1)
const char* ssid = "PINGO" ;
const char* password = "palio6635";
*/
///* (wifi lab - domotica)
const char* ssid = "Domotica" ;
const char* password = "domotica1c203a";
//*/

  
//Parâmetros dos servidores
WebSocketsServer webSocket = WebSocketsServer(81);

//Led indicador de movimento
const int ledPin = 15;
const int sensorPin = 35;

//Função que recebe os comandos de movimento do site
void webSocketEvent(uint8_t num, WStype_t type, uint8_t * payload, size_t length) {
  Serial.print("Mensagem recebida: ");
  Serial.println((char*)payload);

  int valorAnalogico;

  if(type == WStype_TEXT){

    if(strcmp((char*)payload, "acende") == 0){
      digitalWrite(ledPin, HIGH);
      }
    else if(strcmp((char*)payload, "apaga") == 0){
      digitalWrite(ledPin, LOW);
      }
    else if (strcmp((char*)payload, "temp") == 0) {
      // Se receber "ObterTimestamp", enviar a leitura do pino analógico de volta
      valorAnalogico = analogRead(sensorPin);
      String resposta = String(valorAnalogico)+"°";
      webSocket.sendTXT(num, resposta);
      Serial.print("Mensagem enviada: ");
      Serial.println(resposta);
      }

    }
  
  }


   
  void  setup(){
    Serial.begin(115200);

    //Inicialização dos pinos
    pinMode(ledPin, OUTPUT);
    pinMode(sensorPin,INPUT);

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
    Serial.println(WiFi.localIP()); // --> 'ws://192.168.100.10:81/' (wifi casa 1)
                                    // --> 'ws://192.168.0.106:81/' (wifi lab - domotica)
                                    // --> 'ws://192.168.100.10:81/' (wifi casa 2)

    //Configuração dos servidores
    webSocket.begin();
    webSocket.onEvent(webSocketEvent);
    
  }
   
  void loop(){
      webSocket.loop();
  }