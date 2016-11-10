import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
input_list = [7,11]
output_list = [12,13]
GPIO.setup(input_list, GPIO.IN)
GPIO.setup(output_list, GPIO.OUT)

def get_cont():
    a = 0
    while a != 4:
        if a == 0:
            fwd = GPIO.input(7)
            a += 1
        elif a == 1:
            bwd = GPIO.input(11)
            a += 1
        elif a == 2:
            fab = fwd - bwd
            a = 1
        elif a == 3:
            if fab == -1:
                #print("Backwards")
                GPIO.output(15, GPIO.LOW)
                GPIO.output(13, GPIO.HIGH)
            elif fab == 1:
                #print("Forwards")
                GPIO.output(13, GPIO.LOW)
                GPIO.output(15, GPIO.HIGH)
            else:
                #print("Idle")
                GPIO.output(13, GPIO.LOW)
                GPIO.output(15, GPIO.LOW)
            a = 0
