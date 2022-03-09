#!/usr/bin/python3
import string

from serial import Serial
from dataclasses import dataclass

from serial.tools import list_ports
from serial.serialutil import PortNotOpenError, SerialException, SerialTimeoutException

from log import log_error, log_exception, log_info
from log import DynopyException, DynopyStop, DynopyPortErrorException


def parseStr(x): return \
    x.isalpha() and x or x.isdigit() and int(x) or\
    x.isalnum() and x or len(set(string.punctuation).intersection(x)) == 1\
    and x.count('.') == 1 and float(x) or x


class TheSerial(Serial):
    def __init__(self, port=None, baudrate=115200):
        super().__init__(port=port, baudrate=baudrate)

    def relay_mode(self, data: dict):
        for i in data: self.write(f'{data[i]}')

    def sending_data(self, data:str):
        self.write(bytes(data, 'utf-8'))

    def check_serial(self) -> bool: return True if any(
        port.pid is not None for port in list_ports.comports()
    ) else False

    def get_list_serial(self) -> list[dict]: return [{
        "id": port.pid,
        "name": port.device,
        "desc": port.description
    } for port in list_ports.comports()]

    def stop_serial(self):
        if self.is_open:
            self.reset_input_buffer()
            self.reset_output_buffer()
            self.close()

        else:
            pass

    def get_serial_id(
        self, index: int) -> str: return self.get_list_serial()[index]['id']

    def get_serial_name(
        self, index: int = 0) -> str: return self.get_list_serial()[index]['name']

    def get_serial_desc(
        self, index: int) -> str: return self.get_list_serial()[index]['desc']


@dataclass
class Data:
    '''
    ini adalah data semua sensor yang didapatkan 
    didalam arduino
    '''
    data = {
        'humid': 0.0, 'temp': 0.0, 'tinggiair': 0.0,
        'soil': 0.0, 'ldr': 0.0, 'rel1': 0,
        'rel2':0, 'rel3':0, 'rel4':0
    }
    def callback_data(self, l: list):
        self.data['humid'] = l[0]
        self.data['temp'] = l[1]
        self.data['tinggiair'] = l[2]
        self.data['soil'] = l[3]
        self.data['ldr'] = l[4]
        self.data['rel1'] = l[5]
        self.data['rel2'] = l[6]
        self.data['rel3'] = l[7]
        self.data['rel4'] = l[8]

    def getdata(self) -> dict: return self.data

    def deldata(self):
        for i in self.data.keys():
            self.data[i] = 0.0


BAUDRATE = 115200
if __name__ == "__main__":
    try:
        pass

    except (DynopyException) as e:
        log_exception(e)
