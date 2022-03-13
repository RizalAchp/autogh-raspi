import RPi.GPIO as GPIO
import time
 
GPIO.setmode(GPIO.BCM)
 
TRIG = 28
ECHO = 29

GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
 
def distance():
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    while GPIO.input(ECHO) == 0: StartTime = time.time()
    while GPIO.input(ECHO) == 1: StopTime = time.time()

    return ((StopTime - StartTime)* 34300) / 2 
 
if __name__ == '__main__':
    try:
        while True:
            print ("Measured Distance = %.1f cm" %(distance()))
            time.sleep(1)
 
        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()
