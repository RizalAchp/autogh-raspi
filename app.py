#!/usr/bin/env python3

from log import log_exception, log_info
from flask_socketio import SocketIO
from flask import Flask, render_template, request
from config import ConfigJson
import socket
import sys
import eventlet
eventlet.monkey_patch()


# in_raspi = True
# if in_raspi:
#     from sensor_gpio_raspi import Sensors
# else:
#     from onarduino.sensor_serial import TheSerial, Data, parseStr, SerialException,\
#         PortNotOpenError, SerialTimeoutException
#     ser = TheSerial()
#     ser.port = None


# import redis
# from other import SERVER, PORT
# db = redis.StrictRedis('localhost', 6379, 0)
async_mode = 'eventlet'
app = Flask(__name__)
app.config['SECRET_KEY'] = "secret!"
sock = SocketIO(app, async_mode=async_mode)
_config = ConfigJson()
config = _config.get_server_config()
workerObject = None

class Worker(object):
    instance = None
    def __init__(self, socketio: SocketIO):
        if type(self).instance is None:
            # Initialization
            type(self).instance = self
        else:
            raise RuntimeError("hanya satu instance 'Worker' yang dapat berjalan")

        self.socketio = socketio
        self.switch = True
        self.mode_default = True

    def do_work_thread(self):
        log_info("background thread dijalankan")
        try:
            while self.switch:
                try:
                    pass

                except IndexError:
                    continue

        except (
            Exception
        ) as e:
            log_exception(e)
            sock.emit('my_response', {
                'value': 'error', 'desc': 'An error has occuired', 'info': str(e)
            })

    def restart(self):
        self.switch = False
        self.switch = True


@app.route('/')
def main(): return render_template('index.html', async_mode=sock.async_mode)

worker = Worker(sock)

@sock.event
def connect():
    global worker
    # worker.start()
    # ser.port = ser.get_serial_name(0)
    # if async_mode:
    #     sock.start_background_task(worker.do_work_thread)

    sock.emit('mode', {'value': worker.mode_default})


@sock.event
def onrelaychange(msg):
    # ser.sending_data(f'{msg["num"]}')
    sock.emit('relay_feedback', {'msg':msg})


@sock.event
def modemanual():
    # ser.sending_data('4') # 3 mode auto | 4 mode manual
    sock.emit('status', {'sts': False})


@sock.event
def modeauto():
    # ser.sending_data('3')
    sock.emit('status', {'sts': True})


@sock.event
def setting_change(msg):
    sock.emit('status', {'sts': 'setting_change', 'msg':msg})


@sock.event
def setting_default():
    sock.emit('status', {'sts': 'setting_default'})


@sock.event
def shutdown_server():
    sock.emit('status', {'sts': 'shutdown_server'})


if __name__ == "__main__":
    try:
        sock.run(
            app,
            host = config['ip'],
            port = config['port'],
            use_reloader = config['use_reloader'],
            debug = config['debug']
        )

    except KeyboardInterrupt:
        sock.stop()
        sys.exit("program ditutup")
