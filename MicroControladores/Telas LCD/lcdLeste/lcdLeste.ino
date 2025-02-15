//========================================================================================================
//     Código referente a tela LCD com módulo I2C para obra Buzu (2019)
//     18/09/2019
//     
//      Referências:
//        https://www.losant.com/blog/how-to-connect-lcd-esp8266-nodemcu
//
//                                                                                Esteban Viveros
//========================================================================================================

/*
                                      CONEXÕES
                          -------------------------------
                         | Wemos D1 Mini |  LCD c/ I2C   |
                         |---------------|---------------|
                         |     G         |     GND       |
                         |     5V        |     VCC       |
                         |     D2        |     SDA       |
                         |     D1        |     SCL       |
                          -------------------------------
     
 */

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
  Serial.print("Conectando");
  while (WiFi.status() != WL_CONNECTED)
  {
    Serial.print('.');
    delay(500);
  }
  Serial.println();
  Serial.print("Connected! IP address: ");
  Serial.println(WiFi.localIP());
  Serial.printf("UDP server on port %d\n", localPort);
  Udp.begin(localPort);


  lcd.begin(16,2);
  lcd.init();
  lcd.backlight();

  lcd.setCursor(12,0);
  lcd.print("buzu");
  lcd.setCursor(2,1);
  lcd.print("GATO PRETO");
}


//========================================================================================================
// Loop do Programa
//========================================================================================================

void loop()
{
  OSCMsgReceive();    // processa mensagens OSC recebida
}


//========================================================================================================
//                  -----------------------  fim do loop  -----------------------------
//========================================================================================================


                   /******************************************************************\
                    *                      Funções do Programa                       *
                   \******************************************************************/


//========================================================================================================
// Função que processa as mensagens OSC recebidas
//========================================================================================================
/*  As mensagens OSC recebidas são roteadas para funções que efetuarão as
 *   operações desejadas.
 */

void OSCMsgReceive()
{
  OSCMessage msgIN;
  int size;
  if((size = Udp.parsePacket())>0)
  {
    while(size--)
      msgIN.fill(Udp.read());
    if(!msgIN.hasError())
    {
      msgIN.route("/buzu/lcdLeste", imprimeNaTela);
    }
  }
}


//========================================================================================================
// Função imprimeNaTela   -   Imprime na tela LCD
// 
//    msg: /buzu/lcdLeste/String(nome_da_linha_de_onibus)
//========================================================================================================
void imprimeNaTela(OSCMessage &msg, int addrOffset)
{
  char dadoString[20];
  msg.getString(0, dadoString, 16);

  Serial.println(dadoString);

  lcd.clear();
  lcd.setCursor(0,0);
  lcd.print("            buzu");
  lcd.setCursor(0,1);
  lcd.print(dadoString);
}

//========================================================================================================
//                     ---------------------- fim do programa --------------------------           
//========================================================================================================
