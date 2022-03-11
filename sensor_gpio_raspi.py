#!/bin/env python3
from RPi import GPIO
import time

from config import ConfigJson

class HasilDHT:
    'DHT11 sensor result returned by DHT11.read() method'

    ERR_NO_ERROR = 0
    ERR_MISSING_DATA = 1
    ERR_CRC = 2

    error_code = ERR_NO_ERROR
    temperature = -1
    humidity = -1

    def __init__(self, error_code, temperature, humidity):
        self.error_code = error_code
        self.temperature = temperature
        self.humidity = humidity

    def is_valid(self):
        return self.error_code == HasilDHT.ERR_NO_ERROR


class DHT11:
    'DHT11 sensor reader class for Raspberry'

    __pin = 0

    def __init__(self, pin):
        self.__pin = pin

    def read(self):
        GPIO.setup(self.__pin, GPIO.OUT)
        self.__send_and_sleep(GPIO.HIGH, 0.05)
        self.__send_and_sleep(GPIO.LOW, 0.02)
        GPIO.setup(self.__pin, GPIO.IN, GPIO.PUD_UP)
        data = self.__collect_input()

        pull_up_lengths = self.__parse_data_pull_up_lengths(data)

        if len(pull_up_lengths) != 40:
            return HasilDHT(HasilDHT.ERR_MISSING_DATA, 0, 0)

        bits = self.__calculate_bits(pull_up_lengths)
        the_bytes = self.__bits_to_bytes(bits)
        checksum = self.__calculate_checksum(the_bytes)

        if the_bytes[4] != checksum:
            return HasilDHT(HasilDHT.ERR_CRC, 0, 0)

        ''' Data return jika checksum berhasil
        the_bytes[0]: humidity int
        the_bytes[1]: humidity decimal
        the_bytes[2]: temperature int
        the_bytes[3]: temperature decimal
        '''

        temperature = the_bytes[2] + float(the_bytes[3]) / 10
        humidity = the_bytes[0] + float(the_bytes[1]) / 10

        return HasilDHT(HasilDHT.ERR_NO_ERROR, temperature, humidity)

    def __send_and_sleep(self, output, sleep):
        GPIO.output(self.__pin, output)
        time.sleep(sleep)

    def __collect_input(self):
        unchanged_count = 0
        max_unchanged_count = 100
        last = -1
        data = []
        while True:
            current = GPIO.input(self.__pin)
            data.append(current)
            if last != current:
                unchanged_count = 0
                last = current
            else:
                unchanged_count += 1
                if unchanged_count > max_unchanged_count:
                    break
        return data

    def __parse_data_pull_up_lengths(self, data):
        state = 1
        lengths = []
        current_length = 0
        for i in range(len(data)):
            current = data[i]
            current_length += 1
            if state == 1:
                if current == GPIO.LOW:
                    state = 2
                    continue
                else: continue
            if state == 2:
                if current == GPIO.HIGH:
                    state = 3
                    continue
                else: continue
            if state == 3:
                if current == GPIO.LOW:
                    state = 4
                    continue
                else: continue
            if state == 4:
                if current == GPIO.HIGH:
                    current_length = 0
                    state = 5
                    continue
                else: continue
            if state == 5:
                if current == GPIO.LOW:
                    lengths.append(current_length)
                    state = 4
                    continue
                else: continue

        return lengths

    def __calculate_bits(self, pull_up_lengths):
        # find shortest and longest period
        shortest_pull_up = 1000
        longest_pull_up = 0

        for i in range(0, len(pull_up_lengths)):
            length = pull_up_lengths[i]
            if length < shortest_pull_up:
                shortest_pull_up = length
            if length > longest_pull_up:
                longest_pull_up = length

        # use the halfway to determine whether the period it is long or short
        halfway = shortest_pull_up + (longest_pull_up - shortest_pull_up) / 2
        bits = []

        for i in range(0, len(pull_up_lengths)):
            bit = False
            if pull_up_lengths[i] > halfway:
                bit = True
            bits.append(bit)

        return bits

    def __bits_to_bytes(self, bits):
        the_bytes = []
        byte = 0

        for i in range(0, len(bits)):
            byte = byte << 1
            if (bits[i]):
                byte = byte | 1
            else:
                byte = byte | 0
            if ((i + 1) % 8 == 0):
                the_bytes.append(byte)
                byte = 0

        return the_bytes

    def __calculate_checksum(self, the_bytes):
        return the_bytes[0] + the_bytes[1] + the_bytes[2] + the_bytes[3] & 255

class Relay:
    _status_relay = {"humid": 0, "temp": 0, "soil": 0, "tinggiair": 0}

    def __init__(self, auto: bool = True, jalan: bool = True):
        self._config = ConfigJson()
        configpin = self._config.get_pin_config()
        self.config = self._config.get_kondisi_config()
        self.RELAY_GPIO = configpin['relays']
        self.TRIG = configpin['trigger_hcsr']
        self.ECHO = configpin['echo_hcsr']
        self.PINSOIL = configpin['soil_moisture']
        self.DHT11_PIN = configpin['dht']
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

    data = {'humid': 0, 'temp': 0.0, 'soil': 0, 'tinggiair': 0}

    def __init__(self):
        Relay.__init__(self)
        self._gpio = GPIO
        self._dht = DHT11(self.DHT11_PIN)
        self._gpio.setmode(self._gpio.BCM)
        self._gpio.setup(self.TRIG, self._gpio.OUT)
        self._gpio.setup(self.ECHO, self._gpio.IN)
        self._gpio.setup(self.PINSOIL, self._gpio.IN)
        for r in self.RELAY_GPIO:
            self._gpio.setup(self.RELAY_GPIO[r], self._gpio.OUT)

    def _baca_soil(self):
        if self._gpio.input(self.PINSOIL):
            return 100
        return 10

    def _baca_tinggi_air(self):
        self._gpio.output(self.TRIG, True)
        time.sleep(0.00001)
        self._gpio.output(self.TRIG, False)

        stops, starts = 0.0, 0.0
        while self._gpio.input(self.ECHO) == 0:
            starts = time.time()
        while self._gpio.input(self.ECHO) == 1:
            stops = time.time()

        return round(((stops - starts) * 34300) / 2, None)

    def __baca_dht(self):
        instance = self._dht.read()
        if instance.is_valid():
            return (instance.humidity, instance.temperature)
        else:
            return self._baca_dht()

    def _baca_dht(self):
        return (self.data['humid'], self.data['temp'])

    def semua_value(self) -> dict:
        try:
            self.data['soil'] = self._baca_soil()
            self.data['tinggiair'] = self._baca_tinggi_air()
            self.data['humid'], self.data['temp'] = self.__baca_dht()
            return self.data

        except RuntimeError:
            pass

        return self.semua_value()

    def _relay(self):
        status = self._get_status_relay()
        for a, b in zip(self.RELAY_GPIO, status):
            self._gpio.output(self.RELAY_GPIO[a], status[b])
        return [status[i] for i in status]

    def relay(self, idx: list = None) -> list:
        if idx:
            self._modemanual()
            self._perkondisian_status(idx)
            return self._relay()

        else:
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

    def tutupSensor(self) -> None:
        self._gpio.cleanup()

if __name__ == "__main__":
    sensor = Sensors()
    relay = Relay()
    for i in range(10):
        try:
            print(sensor.semua_value())

            time.sleep(5.0)
        except (Exception, KeyboardInterrupt) as error:
            print(f'Measurement stopped by User | {error}')
        time.sleep(2.0)

