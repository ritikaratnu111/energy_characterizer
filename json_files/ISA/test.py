import json

def load_json_file(filename):
    with open(filename, 'r') as file:
        return json.load(file)

def print_data_from_main():
    instructions = load_json_file('instructions.json')
    for key, value in instructions.items():
        print(f"Instruction {key}:")
        data = load_json_file(value)
        print(json.dumps(data, indent=2))  # Print data with indentation for readability

if __name__ == "__main__":
    print_data_from_main()
