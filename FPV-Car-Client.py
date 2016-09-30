#!/bin/python3

import socket, logging, time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
chan_list = [5,6,13,19]
GPIO.setup(chan_list, GPIO.OUT)
global restart
restart = 0

def Main():
    if restart == 1:
        global restart
        restart = 0
        print("Restarted Client Succesfully")
    host = '10.0.0.6'
    port = 5000

    mySocket = socket.socket()
    mySocket.connect((host,port))
    move_list = []

    while True:
        data = mySocket.recv(1024).decode()
        move_list = str(data).split()
        N1 = move_list[len(move_list)-2]
        N2 = move_list[len(move_list)-1]
        if N1 == -1 or 0 or 1:
            lor = float(N2)
            fab = float(N1)
        else:
            logging.warning("Bad Value detected, Removing...")
            logging.info("Trying again")



        if fab == -1:
            #print("Backwards")
            GPIO.output(19, GPIO.LOW)
            GPIO.output(13, GPIO.HIGH)
        elif fab == 1:
            #print("Forwards")
            GPIO.output(13, GPIO.LOW)
            GPIO.output(19, GPIO.HIGH)
        else:
            #print("Idle")
            GPIO.output(13, GPIO.LOW)
            GPIO.output(19, GPIO.LOW)

        if lor < -0.3:
            #print("Left")
            GPIO.output(6, GPIO.LOW)
            GPIO.output(5, GPIO.HIGH)
        elif lor > 0.3:
            #print("Right")
            GPIO.output(5, GPIO.LOW)
            GPIO.output(6, GPIO.HIGH)
        else:
            #print("Straight")
			GPIO.output(5, GPIO.LOW)
            GPIO.output(6, GPIO.LOW)

try:
if __name__ == '__main__':
    Main()
except ValueError:
    print("Value Error Detected attempting restart!")
    GPIO.cleanup()
    time.sleep(1)
    GPIO.setmode(GPIO.BCM)
    chan_list = [5,6,13,19]
    GPIO.setup(chan_list, GPIO.OUT)
    Main()
