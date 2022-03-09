import psutil as p

class SystemStatus:
    def __init__(self) -> None:
        self.p = p
        pass

    def size(self, byte):
        for x in ["B", "KB", "MB", "GB", "TB"]:
            if byte < 1024:
                return f"{byte:.2f}{x}"
            byte = byte/1024

    def memory(self):
        mem = self.p.virtual_memory()
        swmem = self.p.swap_memory()
        return {
            'mem':{
                'total':self.size(mem.total),
                'available':self.size(mem.available),
                'used':self.size(mem.used),
                'percentage':mem.percent
            },
            'swap':{
                'total':self.size(swmem.total),
                'available':self.size(swmem.free),
                'used':self.size(swmem.used),
                'percentage':mem.percent
            }
        }

    def cpu(self):
        freq = self.p.cpu_freq()
        return {
            'cpu':{
                'core':self.p.cpu_count(logical=False),
                'max-freq':freq.max,
                'min-freq':freq.min,
                'cur-freq':freq.current,
                'cpu-perc':self.p.cpu_percent()
            }
        }

# Driver Function
if __name__ == "__main__":
    pass
