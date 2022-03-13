#!/bin/env python3
import time
import string

from RPi import GPIO
import board
import adafruit_dht

from configparser import ConfigParser


class Config(ConfigParser):
    kondisi_config = {
        'temp_hi': 0.0, 'temp_lo': 0.0,
        'humadity_hi': 0.0, 'humadity_lo': 0.0,
        'moisture_hi': 0, 'moisture_lo': 0,
        'water_hi': 0, 'water_lo': 0
    }

    def isStr(self, x):
        return x.isalpha() and x or x.isdigit() \
            and int(x) or x.isalnum() and x or \
            len(set(string.punctuation).intersection(x)) == 1 \
            and x.count('.') == 1 and float(x) or x

    def __init__(self, *args, **kwargs):
        ConfigParser.__init__(
            self, *args, **kwargs
        )
        self.file = "sensor_config.ini"
        self.read(self.file)

    def read_config(self) -> dict:
        kond = self["KONDISI_SENSOR"]
        for k in self.kondisi_config:
            self.kondisi_config[k] = self.isStr(kond[k])
        return self.kondisi_config

    def ubah_config(self):
        pass

    def default_config(self):
        pass


class Relay:
    RELAY_GPIO = {"1": 5, "2": 6, "3": 19, "4": 26}
    _status_relay = {"humid": 0, "temp": 0, "soil": 0, "tinggiair": 0}

    def __init__(self, auto: bool = True, jalan: bool = True):
        self._auto = auto
        self._jalan = jalan

    def _whatMode(self):
        if self._auto:
            return True
        return False

    def _modeauto(self):
        if not self._auto:
            self._auto = True
        return True

    def _modemanual(self):
        if self._auto:
            self._auto = False
        return True

    def _get_status_relay(self):
        return self._status_relay

    def _perkondisian_status(self, kondisi: list):
        for kond, b in zip(kondisi, self._status_relay):
            self._status_relay[b] = kond


class Sensors(Relay):
    TRIG = 28
    ECHO = 29
    PINSOIL = 12
    DHT11_PIN = board.D13

    data = {'humid': 0, 'temp': 0.0, 'soil': 0, 'tinggiair': 0}

    def __init__(self):
        Relay.__init__(self)
        self.gpio = GPIO
        self.dht = adafruit_dht.DHT11(self.DHT11_PIN, use_pulseio=False)
        self.gpio.setmode(self.gpio.BCM)
        self.gpio.setup(self.TRIG, self.gpio.OUT)
        self.gpio.setup(self.ECHO, self.gpio.IN)
        self.gpio.setup(self.PINSOIL, self.gpio.IN)
        for r in self.RELAY_GPIO:
            self.gpio.setup(self.RELAY_GPIO[r], self.gpio.OUT)

        self.config = Config()
        self.read_config()

    def _relay(self):
        status = self.get_status_relay()
        for a, b in zip(self.RELAY_GPIO, status):
            self.gpio.output(self.RELAY_GPIO[a], status[b])
        return self._status_relay

    def _baca_soil(self):
        if GPIO.input(self.PINSOIL):
            return 1
        return 0

    def _baca_tinggi_air(self):
        GPIO.output(self.TRIG, True)
        time.sleep(0.00001)
        GPIO.output(self.TRIG, False)

        while GPIO.input(self.ECHO) == 0:
            StartTime = time.time()
        while GPIO.input(self.ECHO) == 1:
            StopTime = time.time()

        return round(((StopTime - StartTime) * 34300) / 2, None)

    def _baca_dhthumid(self) -> int:
        return round(self.dht.humidity(), None)

    def _baca_dhttemp(self) -> float:
        return round(self.dht.temperature(), 2)

    def semua_value(self) -> dict:
        try:
            self.data['soil'] = self._baca_soil()
            self.data['tinggiair'] = self._baca_tinggi_air()
            self.data['humid'] = self._baca_dhthumid()
            self.data['temp'] = self._baca_dhttemp()
            return self.data

        except RuntimeError:
            pass
        return self.data

    def relay(self, jalan: bool = True, idx: dict = None) -> dict:
        if jalan:
            self._modeauto()
            self._status_relay['humid'] = 1 if self.data['humid'] >= 80 else 0
            self._status_relay['temp'] = 1 if self.data['temp'] >= 80 else 0
            self._status_relay['soil'] = 0 if self.data['soil'] else 1
            if self.data['tinggiair'] >= 80:
                self._status_relay['tinggiair'] = 1
            elif self.data['tinggiair'] <= 30:
                self._status_relay['tinggiair'] = 0
            return self._relay()
        else:
            if idx:
                self._modemanual()
                self._perkondisian_status([idx[x] for x in idx])
                return self._relay()
            else:
                raise Exception

    def tutupSensor(self) -> None:
        self.dht.exit()
        self.gpio.cleanup()


if __name__ == "__main__":
    sensor = Sensors()
    relay = Relay()
    for i in range(10):
        try:
            # print(sensor.bacaDHT())
            # print("tinggi air : {} cm".format(sensor.distance()))
            # print(sensor.bacaSOIL())
            time.sleep(2.0)

        except RuntimeError as error:
            print(error.args[0])
            time.sleep(2.0)
            continue
        except (Exception, KeyboardInterrupt) as error:
            print(f'Measurement stopped by User | {error}')
        time.sleep(2.0)
