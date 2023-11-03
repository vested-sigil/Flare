# helper.py

import json

# Load configuration from file
def load_config(file='config.json'):
    try:
        with open(file, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

# Save configuration to file
def save_config(config, file='config.json'):
    with open(file, 'w') as f:
        json.dump(config, f)

# Simulate grabbing object from server
def grab(obj):
    return {"key": f"value from server for {obj}"}

# Simulate updating cells from server
def update_cells():
    return {"cell_a": "new_data_a", "cell_b": "new_data_b"}
