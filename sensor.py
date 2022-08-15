import paho.mqtt.client as paho
from paho import mqtt
import RPi.GPIO as GPIO
import time

# define static variable
# broker = "localhost" # for local connection
broker = "broker.mqttdashboard.com"  # for online version
port = 1883
timeout = 60

username = ''
password = ''
topic = "sensor/ultrasonic"

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
 
def on_publish(client,userdata,result):
	print("data published \n")
	


client1 = paho.Client("altisimo",userdata=None,protocol=paho.MQTTv5)
client1.username_pw_set(username=username,password=password)
client1.on_connect = on_connect
client1.on_publish = on_publish
client1.connect(broker,port,timeout)

#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)
 
#set GPIO Pins
GPIO_TRIGGER = 20
GPIO_ECHO = 21
 
#set GPIO direction (IN / OUT)
GPIO.setwarnings(False)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

def distance():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
 
    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = ((TimeElapsed * 34300) / 2)
 
    return distance

while True:
	ultrasonic = "%.1f" % distance()
	print(ultrasonic)
	ret = client1.publish(topic,payload=ultrasonic,qos=0)
	time.sleep(1)
