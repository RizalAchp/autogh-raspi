import string
import json
import os
from configparser import ConfigParser

class ConfigJson:
    instance = None
    def __init__(self, file:str = "config.json") -> None:
        if type(self).instance is None:
            # Initialization
            type(self).instance = self
        else:
            raise RuntimeError("hanya satu instance 'ConfigJson' yang dapat berjalan")

        self.file = os.path.join('./config', file)
        self.filebak = "{}.bak".format(self.file)

    def _read_config(self):
        with open(self.file) as f:
            datajson = json.load(f)
            f.close()

        return datajson

    def get_kondisi_config(self):
        return self._read_config()['kondisi']

    def get_server_config(self):
        return self._read_config()['server_connection']

    def new_config(self, data:dict) -> None:
        os.rename(self.file, self.filebak)
        return self._new_config(data, indent=4)

    def default_config(self):
        os.replace(self.filebak, self.file)
        return None

    def _new_config(self, data:dict, indent:int):
        with open(self.file, 'w') as f:
            json.dump(data, f, indent=indent)
            f.close()

            return None

    @classmethod
    def reset(cls):
        cls.instance = None
        cls.instance = ConfigJson()


class ConfigIni(ConfigParser):
    '''
    DEPRECATED! karena config menggunakan Json,
    gunakan `ConfigJson` saja
    '''
    kondisi_config = {
        'temp_hi': 0.0, 'temp_lo': 0.0,
        'humadity_hi': 0.0, 'humadity_lo': 0.0,
        'moisture_hi': 0, 'moisture_lo': 0,
        'water_hi': 0, 'water_lo': 0
    }

    def __init__(self, file="config/sensor_config.ini", *args, **kwargs):
        ConfigParser.__init__(self, *args, **kwargs)
        self.file = file
        self.read(self.file)

    def fromStr(self, x):
        return x.isalpha() and x or x.isdigit() \
            and int(x) or x.isalnum() and x or \
            len(set(string.punctuation).intersection(x)) == 1 \
            and x.count('.') == 1 and float(x) or x

    def read_config(self) -> dict:
        kond = self["KONDISI_SENSOR"]
        for k in self.kondisi_config:
            self.kondisi_config[k] = self.fromStr(kond[k])
        return self.kondisi_config

    def ubah_config(self):
        pass

    def default_config(self):
        pass


template_data = {
    "kondisi": {
        "humid-hi": 80,
        "humid-lo": 70,
        "temp-hi": 33.0,
        "temp-lo": 25.0,
        "soil-hi": 100,
        "soil-lo": 0,
        "water-hi": 33,
        "water-lo": 25
    },
    "server-connection": {
        "ip": "0.0.0.0",
        "port": 5000,
        "use_reloader": False,
        "debug": False
    }
}

if __name__ == "__main__":
    config = ConfigJson()
    data = config._read_config()
    print(data)
    print(type(data))
