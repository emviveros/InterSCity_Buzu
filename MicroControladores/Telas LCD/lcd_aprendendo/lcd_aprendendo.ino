//========================================================================================================
//     Código referente a tela LCD com módulo I2C para obra Buzu (2019)
//     13/09/2019
//     
//      Referências:
//        https://www.losant.com/blog/how-to-connect-lcd-esp8266-nodemcu
// 
//========================================================================================================



//========================================================================================================
// Bibliotecas Tela LCD
//========================================================================================================

#include <LiquidCrystal_I2C.h>


//========================================================================================================
// Bibliotecas WiFi ESP8266
//========================================================================================================

#include <ESP8266WiFi.h>
#include <WiFiUdp.h>


//========================================================================================================
// Biblioteca OSC
//========================================================================================================

#include <OSCBundle.h>


//========================================================================================================
// Rede WiFi, senha, endereço UDP e porta UDP
//========================================================================================================

#ifndef STASSID
#define STASSID "wi-fi"
#define STAPSK  "senha"
#endif

unsigned int localPort = 8888;      // local port to listen on

WiFiUDP Udp;


//========================================================================================================
// Inicialização do display LCD
//========================================================================================================

LiquidCrystal_I2C lcd(0x27, 16, 2);


//========================================================================================================
// Configuração do Programa
//========================================================================================================

void setup()
{
  Serial.begin(115200);
  WiFi.mode(WIFI_STA);
  WiFi.begin(STASSID, STAPSK);
  while (WiFi.status() != WL_CONNECTED) {
    Serial.print('.');
    delay(500);
  }
  Serial.print("Connected! IP address: ");
  Serial.println(WiFi.localIP());
  Serial.printf("UDP server on port %d\n", localPort);
  Udp.begin(localPort);

  
  // The begin call takes the width and height. This
  // Should match the number provided to the constructor.
  lcd.begin(16,2);
  lcd.init();

  // Turn on the backlight.
  lcd.backlight();

  // Move the cursor characters to the right and
  // zero characters down (line 1).
  lcd.setCursor(5, 0);

  // Print HELLO to the screen, starting at 5,0.
  lcd.print("ENTAUm");

  // Move the cursor to the next line and print
  // WORLD.
  lcd.setCursor(5, 1);      
  lcd.print("VAMOS LA");
}


//========================================================================================================
// Loop do Programa
//========================================================================================================

void loop()
{
  
}


//========================================================================================================
//                     ---------------------- fim do programa --------------------------           
//========================================================================================================
