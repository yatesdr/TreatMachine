// Outputs
int MOT_ENA = A0;
int MOT_STEP = A1;
int MOT_DIR = A2;
int COM = 5;
int BUZZER = 7;
int V50=A3;

// Inputs
int MOTION_SENSOR=11;
int SWITCH1=8;
int SWITCH2=9;
int SWITCH3=10;
int SOUND_SENSOR=12;
int REMOTE=6;
int ALEXA=13;


unsigned long DISPENSE_DELAY=30000; // How many milliseconds to wait to dispense another treat
unsigned long MOTION_DELAY=60000;
unsigned long BARK_DELAY=1000;
int SOFT=0;
int FORCE=1;
unsigned long treat_dispensed=0;
int remainder=0;

void setup() {
  // put your setup code here, to run once:



  pinMode(A0,OUTPUT);
  digitalWrite(A0,HIGH);
  pinMode(A1,OUTPUT);
  digitalWrite(A1,LOW);
  pinMode(A2,OUTPUT);
  digitalWrite(A2,LOW);
  pinMode(A3,OUTPUT);
  digitalWrite(A3,HIGH);// Use as 5v source for buzzer

  pinMode(0, OUTPUT);
  pinMode(1, OUTPUT);
  pinMode(2, OUTPUT);
  pinMode(3, INPUT);
  pinMode(4, OUTPUT);
  pinMode(5, OUTPUT);
  pinMode(6, INPUT_PULLUP);
  pinMode(7, OUTPUT);
  pinMode(8, INPUT_PULLUP);
  pinMode(9, INPUT_PULLUP);
  pinMode(10, INPUT_PULLUP);
  pinMode(11, INPUT);
  pinMode(12, INPUT);
  pinMode(13, INPUT);

  digitalWrite(BUZZER, 1);
  digitalWrite(4,1);
  digitalWrite(MOT_STEP, 0);
  digitalWrite(MOT_DIR, 0);
  digitalWrite(MOT_ENA, 1); // 1=disabled, 0=enabled
  digitalWrite(COM, 0);

  //Serial.begin(9600);
}

bool motion_enabled(){
  return !digitalRead(SWITCH1);
}

bool bark_enabled(){
  return !digitalRead(SWITCH2);
}

bool mute_enabled(){
  return !digitalRead(SWITCH3);
}

void five_long_beeps(){
  if (! mute_enabled()){
  for(int i=0;i<5;i++){
    digitalWrite(BUZZER,0);
    delay(500);
    digitalWrite(BUZZER,1);
    delay(300);
  }
  }
}

void five_short_beeps(){
  if (! mute_enabled()){
    for (int i=0;i<5;i++){
    digitalWrite(BUZZER,0);
    delay(50);
    digitalWrite(BUZZER,1);
    delay(50);
  }
  }
}
void reject(void){
  five_short_beeps();
}
void do_dispense(void){
  // Alert Twixy Pooh
  five_long_beeps();
  
  // Enable motors
  digitalWrite(MOT_ENA,0);
  
  delay(200);
  
  // Set direction
  digitalWrite(MOT_DIR,0);

  int s=133;
  if (remainder>2){
    s++;
    remainder=0;
  }
  // Step 200 times
  for(int i=0; i<s; i++){
  digitalWrite(MOT_STEP,1);
  delay(1);
  digitalWrite(MOT_STEP,0);
  delay(1);
  }
  
  delay(200);
  // Disable Motors
  digitalWrite(MOT_ENA,1);
  remainder++;
  
}

void dispense(int mode){

  if (mode==FORCE){
    do_dispense();
    treat_dispensed=millis();
  }
  else {
    if (millis()-treat_dispensed < DISPENSE_DELAY){
      reject();
    }
    else {
     do_dispense();
     treat_dispensed=millis();
    }
  }

}
void loop() {

  unsigned long motion_detected=0;
  unsigned long sound_detected=0;

  
  digitalWrite(MOT_ENA,1); // Disable the motors, again.
  
  while (1) {

    if(motion_enabled() && (millis()-treat_dispensed>DISPENSE_DELAY) && (millis()-motion_detected>MOTION_DELAY))
    // If the motion sensor is enabled, watch for motion.
    {
    if (digitalRead(MOTION_SENSOR)==1){
        dispense(SOFT);
        motion_detected=millis();
      }
    }

    // If the sound sensor is activated, listen for sound.
    if(bark_enabled() && (millis()-sound_detected>BARK_DELAY))
    {
      if (digitalRead(SOUND_SENSOR)==0){
        dispense(SOFT);
        sound_detected=millis();
      }
      
    }

    if (digitalRead(REMOTE)==0){
      dispense(FORCE);
    }

    if (digitalRead(ALEXA)==1){
      // give her time to respond
      // delay(3500);
      dispense(FORCE);
    }
  }
}
