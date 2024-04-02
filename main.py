from energy_characterizer import EnergyCharacterizer

def main():
    energy_estimator = EnergyCharacterizer()
    energy_estimator.get_fabric()
    energy_estimator.get_testbenches()
    energy_estimator.generate_characterization()
    return

if __name__ == "__main__":
    main()
