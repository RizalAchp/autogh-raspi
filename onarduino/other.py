import socket
from shutil import which
from subprocess import Popen, PIPE

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0)
    try:
        s.connect(('1.1.1.1', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'

    s.close()
    return IP

def buka_browser():
    global BROWSER, SERVER, PORT, stdout, stderr
    wis = [
        which(a) if which(a) is not None else None for a in [
            "google-chrome",
            "chrome",
            "chromium",
            "chromium-browser",
            "firefox"
        ]
    ]
    for i in range(len(wis)):
        if wis[i] is not None:
            BROWSER = wis[i]

    command = "%s --app=http://%s:%s" % (BROWSER, SERVER, PORT)
    proses = Popen(
        command.split(),
        stdout=PIPE, stderr=PIPE
    )
    stdout, stderr = proses.communicate()

stdout, stderr = None, None
BROWSER = "$BROWSER"
SERVER =get_ip()
PORT = 5000

if __name__ == "__main__":
    print(get_ip())
