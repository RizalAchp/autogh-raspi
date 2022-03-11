#!/usr/bin/env python3
import sys
from log import log_exception, log_info
from flask_socketio import SocketIO
from flask import Flask, render_template, request
from systemsinfo import getResource

import eventlet
eventlet.monkey_patch()

from sensor_gpio_raspi import Sensors

async_mode = 'eventlet'
app = Flask(__name__)
app.config['SECRET_KEY'] = "secret!"
sock = SocketIO(app, async_mode=async_mode)

class AutoghErrorHandler(Exception):
    pass

class Worker(Sensors):
    instance = None
    def __init__(self, socketio: SocketIO):
        super().__init__()

        self.socketio = socketio
        self.switch = True
        self.mode = True

    def do_work_thread(self):
        log_info("background thread dijalankan")
        try:
            while self.switch:
                try:
                    sock.emit('data_sensor', self.semua_value())
                    if self.mode:
                        self.relay_fb(self.relay())
                    sock.emit('status', {'sts':'ini thread'})
                    sock.sleep(5)

                except IndexError:
                    continue

        except (
            RuntimeError, Exception, AutoghErrorHandler
        ) as e:
            log_exception(e)
            sock.emit('logs', { 'log': str(e) })

    def relay_fb(self, status:list):
        sock.emit('relay_feedback', {'value': status})

    def start(self):
        self.switch = True

    def restart(self):
        self.switch = False
        self.tutupSensor()
        super().__init__()
        self.switch = True


@app.route('/')
def main(): return render_template('index.html', async_mode=sock.async_mode)

@sock.event
def connect():
    global worker, config
    if async_mode:
        sock.start_background_task(worker.do_work_thread)

    sock.emit('mode', {'value': config['moderelay']})

@sock.event
def onrelaychange(msg):
    # ser.sending_data(f'{msg["num"]}')
    status = worker.relay(msg['value'])
    worker.relay_fb(status)

@sock.event
def get_resource():
    sock.emit('resource', getResource())

@sock.event
def modemanual(msg):
    global worker
    if worker.mode:
        worker.mode = False
    worker.relay(msg['value'])
    worker.restart()

@sock.event
def modeauto():
    global worker
    worker.mode = True
    worker.restart()

@sock.event
def setting_change(msg):
    sock.emit('status', {'msg':msg})

@sock.event
def setting_default():
    sock.emit('status', {'sts': 'setting_default'})


worker = Worker(sock)
worker.start()
config = worker._config.get_server_config()
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
