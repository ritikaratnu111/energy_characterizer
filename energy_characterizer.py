import sys,os
import logging
import json
from helper_functions import fabric, tbgen
from helper_functions import VesylaOutput
from innovus_reader import InnovusPowerParser
from measurement import Measurement
import ast
import constants

JSON_FILES = "/media/storage1/ritika/energy_characterizer/json_files/"

class EnergyCharacterizer():
    def __init__(self):
        self.testbenches = {}
        self.FABRIC_PATH = ""
        self.logger = None
        self.estimate = {}
        self.debug = {}
        logging.basicConfig(level=logging.DEBUG)

    def get_fabric(self):
        self.FABRIC_PATH = fabric.set_path()
        os.environ['FABRIC_PATH'] = self.FABRIC_PATH

    def get_testbenches(self):
        self.testbenches = tbgen.set_testbenches("db")

    def update_logger(self, path, name, about):
        LOGFILE = f"{path}/activity_gen.log"
        try:
            with open(LOGFILE, 'w'): pass
            self.logger = logging.getLogger()
            handler = logging.FileHandler(LOGFILE)
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
            self.logger.info(f"Testbench: {name}")
            self.logger.info(f"About: {about}")
        except Exception as e:
            print(f"Failed to set logfile: {e}")
            self.logger = None

    def get_cells(self, tb, start, end):
        activity = json.load(open(f"{tb}/activity.json"))
        c_start, c_end = VesylaOutput.return_execution_cycle(tb)
        T = c_end - c_start
        all = {}
        avg = {}
        
        for i in range(start, end):
            pwr_file = f"{tb}/vcd/iter_{i}.vcd.pwr" 
            reader = InnovusPowerParser()
            reader.update_nets(pwr_file)
            
            for cell, info in activity.items():
                self.estimate[cell] = {}
                total = Measurement()
                nets = 0
                
                for component, component_info in info.items():
                    all[component] = Measurement()
                    avg[component] = Measurement()
                
                for component, component_info in info.items():
                    
                    T_active = int(component_info["active"]) * constants.CLOCK_PERIOD
                    T_inactive = int(component_info["inactive"]) * constants.CLOCK_PERIOD
                    mode = component_info["mode"]

                    current = Measurement()
                    current_active= Measurement()
                    current_inactive = Measurement()
                    
                    signals = ast.literal_eval(component_info["signals"])
                    current.set_measurement(reader, signals, T)
                    inactive_power = json.load(open(f"{JSON_FILES}/primitive_components/{component}.json"))["mode"][mode]["inactive"]
                    current_inactive.update(inactive_power, T_inactive)
                    current_active.energy = current.energy - current_inactive.energy
                    current_active.power = (current.power * T - current_inactive.power * T_inactive) / T_active
                    current_active.update_time(T_active)
                    #current_active.energy.update(current_active.power, T_active)
                    print(component)
                    print(current_active)
                    print(current_inactive)
                    print(current)

                    all[component] = all[component] + current_active
                    avg[component] = all[component] / (end - start)
                    self.estimate[cell][component] = {
                        "cycles"    : T,
                        "power"    : {
                            "internal"  : avg[component].power.internal,
                            "switching"  : avg[component].power.switching,
                            "leakage"  : avg[component].power.leakage
                        },
                        "active_cycles": T_active,
                        "inactve_cycles": T_inactive,
                        "power_active": {
                            "internal"  : avg[component].power.internal,
                            "switching"  : avg[component].power.switching,
                            "leakage"  : avg[component].power.leakage
                        },
                        "power_inactive": {
                            "internal"  : avg[component].power.internal,
                            "switching"  : avg[component].power.switching,
                            "leakage"  : avg[component].power.leakage
                        },
                        "energy"    : {
                            "internal"  : avg[component].energy.internal,
                            "switching"  : avg[component].energy.switching,
                            "leakage"  : avg[component].energy.leakage
                        }
                    }
                    total = total + avg[component]
                self.estimate[cell]["total"] = {
                    "power"    : {
                        "internal"  : total.power.internal,
                        "switching"  : total.power.switching,
                        "leakage"  : total.power.leakage
                    },
                    "energy"    : {
                        "internal"  : total.energy.internal,
                        "switching"  : total.energy.switching,
                        "leakage"  : total.energy.leakage
                    }
            }

    def generate_characterization(self):
        for name, info in self.testbenches.items():
            if info["to_run"] == True:
                tb = info["path"]
                self.update_logger(tb, name, info['about'])
                self.get_cells(tb, 0, 1)
                self.write_energy(tb)
    
    def write_energy(self, tb):
        with open(f"{tb}/estimate.json", "w") as file:
            data = json.dumps(self.estimate, indent = 2)
            file.write(data)
