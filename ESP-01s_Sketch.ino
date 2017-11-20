#include <ESP8266WiFi.h>
#include <DNSServer.h>
#include <ESP8266WebServer.h>
#include <WiFiManager.h>
#include <PubSubClient.h>

const char* mqtt_server = "xxx.xxx.xxx.xxx";

WiFiClient espClient;
PubSubClient client(espClient);
long lastMsg = 0;
char msg[50];
int value = 0;

const char* outTopic = "Treats_out";

// Read these messages and respond by dispensing a treat.
const char* inTopic = "Treats_in";

int dispense_pin = 2;

void setup_wifi() {
  WiFiManager wifiManager;
  // WiFi.disconnect();
  wifiManager.autoConnect("TreatMachineAP");
}

void callback(char* topic, byte* payload, unsigned int length) {
  Serial.print("Message arrived [");
  Serial.print(topic);
  Serial.print("] ");
  for (int i = 0; i < length; i++) {
    Serial.print((char)payload[i]);
  }
  Serial.println();

  if ((char)payload[0]=='d'){
    Serial.println("Dispensing treat");
    digitalWrite(dispense_pin,1);
    delay(500);
    digitalWrite(dispense_pin,0);
  }
  else {
    Serial.printf("Message: '%s'",payload[0]);
  }
}

void reconnect() {
  // Loop until we're reconnected
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    // Attempt to connect
    if (client.connect("TreatClient")) {
      Serial.println("TreatClient connected");
      // Once connected, publish an announcement...
      client.publish(outTopic, "Treat Dispenser Ready.");
      // ... and resubscribe
      client.subscribe(inTopic);
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      // Wait 5 seconds before retrying
      delay(5000);
    }
  }
}



void setup() {
  //EEPROM.begin(512);              // Begin eeprom to store on/off state
  pinMode(dispense_pin, OUTPUT);     // Initialize the relay pin as an output
  digitalWrite(dispense_pin,0);
  
  Serial.begin(115200);
  setup_wifi();                   // Connect to wifi 
  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);
}

void loop() {

  if (!client.connected()) {
    reconnect();
  }
  client.loop();

}
