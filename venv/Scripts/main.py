#test om te zien of git commit werkt
import paho.mqtt.client as mqtt #import the client
import matplotlib.pyplot as plt
import numpy as np
import math

file1 = open("test.txt", "r+")

stralen0 = []
stralen1 = []
stralen2 = []

fig= plt.figure(figsize=(7,7))
def plot(metingen):
    circle0 = plt.Circle((2, 0), metingen[0], color='r', fill=False, linewidth=10)
    circle00 = plt.Circle((2, 0), metingen[0], color='black', fill=False, linewidth=1)
    circle1 = plt.Circle((0, 2.1), metingen[1], color='y', fill=False, linewidth=10)
    circle11 = plt.Circle((0, 2.1), metingen[1], color='black', fill=False, linewidth=1)
    circle2 = plt.Circle((2, 2), metingen[2], color='g', fill=False, linewidth=10)
    circle22 = plt.Circle((2, 2), metingen[2], color='black', fill=False, linewidth=1)
    plt.pause(0.05)
    plt.cla()
    plt.axis((-3,3 , -3, 3))
    plt.gca().add_patch(circle0)
    plt.gca().add_patch(circle00)
    plt.gca().add_patch(circle1)
    plt.gca().add_patch(circle11)
    plt.gca().add_patch(circle2)
    plt.gca().add_patch(circle22)
    plt.hlines(1, 0, 1, color='black', linewidth=1)
    plt.hlines(0, 0, 2, color='black')
    plt.vlines(1, 0, 1, color='black')
    plt.vlines(0, 0, 1, color='black')
    plt.hlines(2, 0, 2, color='black')
    plt.vlines(2, 0, 2, color='black')
    plt.vlines(0, 0, 2, color='black')
    for i in stralen0:
        plt.gca().add_patch(i)
    for i in stralen1:
        plt.gca().add_patch(i)
    for i in stralen2:
        plt.gca().add_patch(i)
    print(metingen)

def calculateDistance(getal, power):
    return pow(10, (power-getal)/(10*2))

metingen = [0,0,0]
def plotCircle(straal, x,y, max, stralen):
    if (straal < max):
        circle = plt.Circle((x, y), straal, color='black', fill=False, linewidth=1)
        stralen.append(circle)
        for i in (stralen):
            plt.gca().add_patch(i)

# Function to process recieved message
def process_message(client, userdata, message):
    bericht = str(message.payload.decode("utf-8"))
    print(bericht)
    gesplitst = bericht.split("_")
    RSSI = gesplitst[0]
    print(RSSI)
    if (gesplitst[1] == "0"):
        straal = calculateDistance(float(RSSI),-35.53947368)
        metingen[0] = straal
        lijn = str(RSSI),",", "0",",", "0" , "\n"
        file1.writelines(lijn)
        print(file1.read())
        plotCircle(straal,2,0,2,stralen0)
    if (gesplitst[1] == "1"):
        straal = calculateDistance(float(RSSI),-27.78481013)
        metingen[1] = straal
        lijn = "0", ",", str(RSSI), ",", "0", "\n"
        file1.writelines(lijn)
        print(file1.read())
        plotCircle(straal,0,2.1,2.1,stralen1)
    if (gesplitst[1] == "2"):
        straal = calculateDistance(float(RSSI),-31.37209302)
        metingen[2] = straal
        lijn = "0", ",", "0", ",", str(RSSI), "\n"
        file1.writelines(lijn)
        print(file1.read())
        plotCircle(straal, 2, 2, 2, stralen2)
    plot(metingen)

# Create client
client = mqtt.Client(client_id="subscriber-1")

# Assign callback function
client.on_message = process_message

# Connect to broker
client.connect("192.168.0.137",1883,60)

# Subscriber to topic
client.subscribe("esp32/rssi/nathan")

# Run loop
client.loop_forever()