import RPi.GPIO as GPIO 
from pirc522 import RFID
import time 
import time
import paho.mqtt.client as paho
broker ="192.168.43.140"

def on_message(client, userdata, message):
    time.sleep(1)
    print("received message =",str(message.payload.decode("utf-8")))

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)  

rc522 = RFID() 

print('En attente d\'un badge (pour quitter, Ctrl + c): ') 

while True :
    rc522.wait_for_tag() 
    (error, tag_type) = rc522.request()  
    

    if not error : 
        (error, uid) = rc522.anticoll() 
       
        if not error : 
            print('Vous avez passé le badge avec l\'id : {}'.format(uid)) 
            time.sleep(1)   
            break

client= paho.Client("client-001") 
client.on_message=on_message
#####
print("connecting to broker ",broker)
client.connect(broker)
client.loop_start() 
print("subscribing ")
client.subscribe(tag_type)
time.sleep(2)
print("publishing ")
client.publish("tag_id",tag_type)
time.sleep(4)
client.disconnect() 
client.loop_stop() 
