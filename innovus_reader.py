import os
import logging
import re

class InnovusPowerParser():
    def __init__(self):
        self.POWER_FILE = ""
        self.nets = {}

    def update_nets(self,file):
        self.POWER_FILE = file
        header = 106
        tail = 15
        try:
            with open(self.POWER_FILE) as file:
                lines = file.readlines()[header:-tail]
                for line in lines:
                    line = " ".join(line.split()).split(" ")
                    name = line[0]
                    if name in self.nets:
                        label = self.nets[name]['label']
                    else:
                        label = 'inactive'
                    self.nets[name] = {'internal' : float(line[3]), 
                                       'switching' : float(line[4]), 
                                       'leakage' : float(line[5]), 
                                       'label' : label}
            inactive = 0
            total = 0
            active = 0
            for name in self.nets:
                net = self.nets[name]
                label = net['label']
                if (label == 'inactive'):
                    inactive += 1
                else:
                    active += 1
                total += 1
        except FileNotFoundError:
            logging.error(f"File {self.POWER_FILE} not found")


    def label_nets(self,signals):
        count = 0
#        logging.info('Signals: %s', signals)
        for signal in signals:
            signal_substrings = signal.split('*')
            for name in self.nets:
                net = self.nets[name]
                label = net['label']
                if (label == 'inactive'):
                    if all(substring in name for substring in signal_substrings):
                        #logging.info(name)
                        self.nets[name]['label'] = signal
                            #Log the net name if the switching power is not 0
#                            if (net['switching'] != 0):
#                                logging.info('Net: %s', name)
                        count += 1


    def get_count_of_inactive_labels(self,signals):
        count = 0
        for signal in signals:
            signal_substrings = signal.split('*')
            for name in self.nets:
                net = self.nets[name]
                label = net['label']
                if (label == 'inactive'):
                    if all(substring in name for substring in signal_substrings):
                        count += 1



    def remove_labels(self,signals):
        count = 0
        for signal in signals:
            signal_substrings = signal.split('*')
            for name in self.nets:
                net = self.nets[name]
                label = net['label']
                if (label == signal):
                    if all(substring in name for substring in signal_substrings):
                        self.nets[name]['label'] = 'inactive'
                        count += 1


    def get_power(self, signals):
        count = 0
        internal_power = 0
        switching_power = 0
        leakage_power = 0
        for signal in signals:
            for name in self.nets:
                net = self.nets[name]
                if(net['label'] == signal):
                    internal_power += net['internal']
                    switching_power += net['switching']
                    leakage_power += net['leakage']
                    count += 1
        power = {'internal': internal_power, 
                    'switching': switching_power,
                    'leakage': leakage_power
                    }
        return(power,count)

    def get_remaining_power(self,tiles):
        internal_power = 0
        switching_power = 0
        leakage_power = 0
        count = 0
        print("Tiles: ", tiles)
        for name in self.nets:
            net = self.nets[name]
            for tile in tiles:
                if tile in name:
                    if(net['label'] == 'inactive'):
                        logging.info('Net: %s', name)
                        internal_power += net['internal']
                        switching_power += net['switching']
                        leakage_power += net['leakage']
                        count += 1
        power = {'internal': internal_power, 
                    'switching': switching_power,
                    'leakage': leakage_power
                    }
        logging.info('Remaining nets: %s', count)
#        print("Inactive net count: ", count)
        return(power,count)


    def get_cell_power(self,tiles):
        internal_power = 0
        switching_power = 0
        leakage_power = 0
        count = 0
        for name in self.nets:
            for tile in tiles:
                if tile in name:
                    net = self.nets[name]
                    internal_power += net['internal']
                    switching_power += net['switching']
                    leakage_power += net['leakage']
                    count += 1
        power = {'internal': internal_power, 
                    'switching': switching_power,
                    'leakage': leakage_power
                    }
        logging.info('Total nets: %s', count)
#        print("Total net count: ", count)
        return(power,count)


    def log_remaining_nets(self,tiles):
        count = 0
        for name in self.nets:
            for tile in tiles:
                if tile in name:
                    net = self.nets[name]
                    if(net['label'] == 'inactive'):
                        logging.info('Net: %s', name)
                        count += 1
        logging.info('Remaining nets: %s', count)
