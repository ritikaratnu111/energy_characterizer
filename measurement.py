import constants
from innovus_reader import InnovusPowerParser
import logging

class Power():
    def __init__(self):
        self.internal = 0
        self.switching = 0
        self.leakage = 0
        self.total = 0
        self.t = 0
    
    def update(self, power, t):
        self.internal = float(power['internal'])
        self.switching = float(power['switching'])
        self.leakage = float(power['leakage'])
        self.total = float(power['internal']) + float(power['switching']) + float(power['leakage'])
        self.t = t

    def update_time(self, t):
        self.t = t

    def __add__(self, other):
        result = Power()
        result.internal = self.internal + other.internal
        result.switching = self.switching + other.switching
        result.leakage = self.leakage + other.leakage
        result.total = self.total + other.total
        return result

    def __truediv__(self, n):
        result = Power()
        result.internal = self.internal / n
        result.switching = self.switching / n
        result.leakage = self.leakage / n
        result.total = self.total / n
        return result

    def __mul__(self, n): 
        result = Power()
        result.internal = self.internal * n
        result.switching = self.switching * n
        result.leakage = self.leakage * n
        result.total = self.total * n
        return result

    def __sub__(self, other): 
        result = Power()
        result.internal = self.internal - other.internal
        result.switching = self.switching - other.switching
        result.leakage = self.leakage - other.leakage
        result.total = self.total - other.total
        return result

    def __str__(self):
        return f"Power: Internal={self.internal:.8f}, Switching={self.switching:.8f}, Leakage={self.leakage:.8f}, Time={self.t}"

class Energy():
    def __init__(self):
        self.internal =  0
        self.switching = 0
        self.leakage = 0
        self.total = 0
        self.t = 0

    def update(self, power, t):
        self.internal = float(power['internal']) * t
        self.switching = float(power['switching']) * t
        self.leakage = float(power['leakage']) * t
        self.total = (float(power['internal']) + float(power['switching']) + float(power['leakage'])) * t
        self.t = t

    def update_time(self, t):
        self.t = t

    def __add__(self, other):
        result = Energy()
        result.internal = self.internal + other.internal
        result.switching = self.switching + other.switching
        result.leakage = self.leakage + other.leakage
        result.total = self.total + other.total
        return result

    def __truediv__(self, n):
        result = Energy()
        result.internal = self.internal / n
        result.switching = self.switching / n
        result.leakage = self.leakage / n
        result.total = self.total / n
        return result

    def __mul__(self, n): 
        result = Energy()
        result.internal = self.internal * n
        result.switching = self.switching * n
        result.leakage = self.leakage * n
        result.total = self.total * n
        return result
    
    def __sub__(self, other):
        result = Energy()
        result.internal = self.internal - other.internal
        result.switching = self.switching - other.switching
        result.leakage = self.leakage - other.leakage
        result.total = self.total - other.total
        return result

    def __str__(self):
        return f"Energy: Internal={self.internal:.2f}, Switching={self.switching:.2f}, Leakage={self.leakage:.2f}, Time={self.t:.2f}"


class Measurement():
    def __init__(self):
        self.power = Power()
        self.energy = Energy()
        self.nets = 0
        self.signals = []

    def set_measurement(self, reader, signals, t):
        reader.label_nets(signals)
        power, self.nets = reader.get_power(signals)
        self.power.update(power, t)
        self.energy.update(power, t)

    def update(self, power, t):
        self.power.update(power, t)
        self.energy.update(power, t)

    def update_time(self, t):
        self.power.update_time(t)
        self.energy.update_time(t)

    def __add__(self, other):
        result = Measurement()
        result.energy = self.energy + other.energy
        result.power = self.power + other.power
        return result

    def __truediv__(self, n):
        result = Measurement()
        result.energy = self.energy / n
        result.power = self.power / n
        return result

    def __mul__(self, n):
        result = Measurement()
        result.energy = self.energy * n
        result.power = self.power * n
        return result

    def __sub__(self, other):
        result = Measurement()
        result.energy = self.energy - other.energy
        result.power = self.power - other.power
        return result

    def __str__(self):
        return f"Measurement: {self.power}"

