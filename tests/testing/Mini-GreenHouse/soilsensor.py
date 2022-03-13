import RPi.GPIO as GPIO
import time
 
PINSOIL = 12

GPIO.setmode(GPIO.BCM)
GPIO.setup(PINSOIL, GPIO.IN)

def bacaSOIL()->str:
    if GPIO.input(PINSOIL) is 1: return "BASAH"
    elif GPIO.input(PINSOIL) is 0: return "KERING"
    else: return "tidak ada status"
 
