import time
import board 
import adafruit_dht
 
dhtDevice = adafruit_dht.DHT11(board.D13, use_pulseio=False)
 
def bacaDHT() -> str:
    temperature_c = dhtDevice.temperature
    humidity = dhtDevice.humidity
    
    return "Temp: {:.1f} C  | Humidity: {}% ".format(temperature_c, humidity)


while True:
    try:
        print(bacaDHT())
 
    except RuntimeError: 
        time.sleep(2)
        continue

    except Exception as error:
        dhtDevice.exit()
        raise error
 
    time.sleep(2.0)
