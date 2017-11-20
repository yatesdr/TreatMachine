# TreatMachine
Some code to make the dog treat dispenser work with Alexa voice commands.

Based on an Arduino UNO which runs the treat machine, an ESP-01s module which is used for WiFi access, a remote server running Mosquitto MQTT Broker, and Amazon Alexa Skills Kit with Lambda functionality.

All files are referenced here, but it's not a tutorial and probably won't be useful to anybody else.

Alexa Skills Kit -> AWS Lambda Function Trigger -> Request to CGI script on remote server -> Mosquitto request
                                                -> Formulate response to Alexa Skill
