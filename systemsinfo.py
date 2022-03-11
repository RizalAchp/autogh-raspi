import psutil as p
import time

def sizeit(byte):
    for x in ["B", "KB", "MB", "GB", "TB"]:
        if byte < 1024:
            return round(byte, 2)
        byte = byte/1024

def getResource():
    return {
        'cpu':p.cpu_percent() ,
        'mem':sizeit(p.virtual_memory().used)
    }
# Driver Function
if __name__ == "__main__":
    while True:
        print(getresource())
        time.sleep(1)
