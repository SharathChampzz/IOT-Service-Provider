#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>

const char* ssid="MADHU_MOBILE"; // Wifi Name
const char* password="madhuthepower"; // Wifi Password



int httpPort = 80;    // This is for over internet Connection. 
String host = "champzz-iot-service.herokuapp.com";
HTTPClient http; 

//int httpPort = 5000;  // I think this is over wlan required, change this port basis on which port you are running the website on
//String host = "192.168.43.99"; // Change IP of destination
//
int r1, r2;

int ledPin = LED_BUILTIN;
void setup() 
{

  pinMode(ledPin, OUTPUT); 
  digitalWrite(ledPin, LOW);
  
  Serial.begin(9600);
  WiFi.begin(ssid, password);
  while(WiFi.status() != WL_CONNECTED)
  {
    delay(200);
    Serial.print("..");
  }
  Serial.println();
  Serial.println("NodeMCU is connected!");
  digitalWrite(ledPin, HIGH);
  Serial.println(WiFi.localIP());

}

void loop() 
{

  r1 = random(1,100);
  r2 = random(1,100);

  String url = "/fyp-healthapp-project-firebase-adminsdk-40qfo-f8fc938674/PM-branch1-branch2/"; // JSON ID and Branch
  String data = (String)r1 + "_" + (String) r2;  // Pass Data here
  Serial.print("Data = ");
  Serial.println(data);
  
  url = url + data;
  http.begin(host,httpPort,url); 
  int httpCode = http.GET();
  Serial.println(httpCode);
  String payload = http.getString();

  // {'fan': 'on'} 
  Serial.println(payload); //Print request response payload

  payload = preprocessing(payload);
  Serial.print("Total Data Arrived : ");
  int count = getcount(payload, ',') + 1;
  Serial.println(count);

for(int i=0;i<count;i++){
  String keyvalue = getValue(payload, ',', i);
  String key = getValue(keyvalue, ':', 0);
  String value = getValue(keyvalue, ':', 1);
  Serial.println("Key : " + key);
  Serial.println("Value : " + value + " \n");
  
  if(key.equals("led") && value.equals("ON")){
    digitalWrite(ledPin, LOW);
  }
  else if(key.equals("led") && value.equals("OFF")){
    digitalWrite(ledPin, HIGH);
  }
  else{
    Serial.println("Ignore For Time Being");
  }
}
  delay(2000);

}









String preprocessing(String inp){
  inp.replace(" ","");
//  Serial.println(inp);  // "{'fan':'off','motor':'on','n0':'HaiMCU'}" // send Hai_MCU
  inp.replace("'","");
//  Serial.println(inp);  // "{"fan":"off","motor":"on","n0":"HaiMCU"}"

  inp.remove(0, 1);  // remove opening and closing bracket
  inp.remove(inp.length()-1, 1);
  Serial.println(inp);  // ""fan":"off","motor":"on","n0":"HaiMCU""
  return inp;
}

int getcount(String string, char character){
  int count = 0;
  for(int i =0; i < string.length() ; i++ ) {
  if(string[i] == character){
    count += 1;
  }
}
return count;
}

String getValue(String data, char separator, int index)
{
  int found = 0;
  int strIndex[] = {0, -1};
  int maxIndex = data.length()-1;

  for(int i=0; i<=maxIndex && found<=index; i++){
    if(data.charAt(i)==separator || i==maxIndex){
        found++;
        strIndex[0] = strIndex[1]+1;
        strIndex[1] = (i == maxIndex) ? i+1 : i;
    }
  }

  return found>index ? data.substring(strIndex[0], strIndex[1]) : "";
}
