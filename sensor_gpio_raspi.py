#!/bin/env python3
from RPi import GPIO
import board
import adafruit_dht
import time

from config import ConfigJson


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
    TRIG = 21
    ECHO = 20
    PINSOIL = 12
    DHT11_PIN = board.D13

    data = {'humid': 0, 'temp': 0.0, 'soil': 0, 'tinggiair': 0}

    def __init__(self):
        Relay.__init__(self)
        self._gpio = GPIO
        self._dht = adafruit_dht.DHT11(self.DHT11_PIN, use_pulseio=False)
        self._gpio.setmode(self._gpio.BCM)
        self._gpio.setup(self.TRIG, self._gpio.OUT)
        self._gpio.setup(self.ECHO, self._gpio.IN)
        self._gpio.setup(self.PINSOIL, self._gpio.IN)
        for r in self.RELAY_GPIO:
            self._gpio.setup(self.RELAY_GPIO[r], self._gpio.OUT)

        self._config = ConfigJson()
        self.config = self._config.get_kondisi_config()

    def _relay(self):
        status = self._get_status_relay()
        for a, b in zip(self.RELAY_GPIO, status):
            self._gpio.output(self.RELAY_GPIO[a], status[b])
        return [status[i] for i in status]

    def _baca_soil(self):
        if self._gpio.input(self.PINSOIL):
            return 1
        return 0

    def _baca_tinggi_air(self):
        self._gpio.output(self.TRIG, True)
        time.sleep(0.00001)
        self._gpio.output(self.TRIG, False)

        StopTime, StartTime = 0.0, 0.0
        while self._gpio.input(self.ECHO) == 0:
            StartTime = time.time()
        while self._gpio.input(self.ECHO) == 1:
            StopTime = time.time()

        return round(((StopTime - StartTime) * 34300) / 2, None)

    def _baca_dhthumid(self):
        return self._dht.humidity if not None else self.data['humid']

    def _baca_dhttemp(self):
        return self._dht.temperature if not None else self.data['temp']

    def semua_value(self) -> dict:
        try:
            self.data['soil'] = self._baca_soil()
            self.data['tinggiair'] = self._baca_tinggi_air()
            self.data['humid'] = self._baca_dhthumid()
            self.data['temp'] = self._baca_dhttemp()
            return self.data

        except RuntimeError:
            pass

        return self.semua_value()

    def relay(self, jalan: bool = True, idx: dict = None) -> list:
        if jalan:
            self._modeauto()
            if self.data['humid'] >= self.config['humid_hi']:
                self._status_relay['humid'] = 1
            elif self.data['humid'] <= self.config['humid_lo']:
                self._status_relay['humid'] = 0

            if self.data['temp'] >= self.config['temp_hi']:
                self._status_relay['temp'] = 1
            elif self.data['temp'] <= self.config['temp_lo']:
                self._status_relay['temp'] = 0

            if self.data['soil'] >= self.config['soil_hi']:
                self._status_relay['temp'] = 1
            elif self.data['temp'] <= self.config['soil_lo']:
                self._status_relay['temp'] = 0

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
                return {'ERROR':"Mode Manual Butuh Inputan Relay"}

    def tutupSensor(self) -> None:
        self._dht.exit()
        self._gpio.cleanup()

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
