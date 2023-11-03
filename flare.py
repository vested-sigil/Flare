from helper import load_config, save_config, grab, update_cells

class Flare:
    def __init__(self, signal_type, config_file='config.json'):
        self.signal_type = signal_type
        self.config_file = config_file
        self.init()
        self.plans = {}  # To store plans
        self.config = load_config(self.config_file)
        self.connect()

    # Initialize buffer and stage
    def init(self):
        self.buffer = {}
        self.stage = {}

    # Connect to server
    def connect(self):
        print("Connected to server.")

    # Load data into buffer, stage, or return as string
    def chaku(self, a, dest):
        data = grab(a)
        if dest == 'buffer':
            self.buffer[a] = data
        elif dest == 'stage':
            self.stage[a] = data
        elif dest == 'string':
            return str(data)

    # Plan a sequence of actions or objects
    def plan(self, name, seq):
        self.plans[name] = seq.split('°')

    # Execute a plan using chaku-chaku
    def chaku2(self, name):
        if name not in self.plans:
            print(f"Plan {name} not found.")
            return
        for action in self.plans[name]:
            self.chaku(action, 'buffer')

    # Update cells from server
    def update(self):
        updated_data = update_cells()
        for cell, data in updated_data.items():
            self.chaku(data, cell)

# Example usage
flare = Flare(signal_type=1)
flare.plan("ex", "a°b°c")
flare.chaku2("ex")
flare.update()

print("Buffer:", flare.buffer)
print("Stage:", flare.stage)
print("Plans:", flare.plans)
from helper import load_config, save_config, grab, update_cells

import os

import shutil

class Flare:

    def __init__(self, signal_type, config_file='config.json'):

        self.signal_type = signal_type

        self.config_file = config_file

        self.init()

        self.plans = {}  # To store plans

        self.config = load_config(self.config_file)

        self.connect()

        self.signals = [Signal(i) for i in range(1, 4)]  # Initialize 3 signals

    # Initialize buffer and stage

    def init(self):

        self.buffer = {}

        self.stage = {}

    # Connect to server

    def connect(self):

        print("Connected to server.")

    # Load data into buffer, stage, or return as string

    def chaku(self, a, dest):

        data = grab(a)

        if dest == 'buffer':

            self.buffer[a] = data

        elif dest == 'stage':

            self.stage[a] = data

        elif dest == 'string':

            return str(data)

    # Plan a sequence of actions or objects

    def plan(self, name, seq):

        self.plans[name] = seq.split('°')

    # Execute a plan using chaku-chaku

    def chaku2(self, name):

        if name not in self.plans:

            print(f"Plan {name} not found.")

            return

        for action in self.plans[name]:

            self.chaku(action, 'buffer')

    # Update cells from server

    def update(self):

        updated_data = update_cells()

        for cell, data in updated_data.items():

            self.chaku(data, cell)

    # File handling and data manipulation methods

    def read_file(self, file_path):

        try:

            with open(file_path, 'r') as f:

                return f.read()

        except FileNotFoundError:

            return "File not found."

    def write_file(self, file_path, content):

        with open(file_path, 'w') as f:

            f.write(content)

    def append_file(self, file_path, content):

        with open(file_path, 'a') as f:

            f.write(content)

    def delete_file(self, file_path):

        try:

            os.remove(file_path)

        except FileNotFoundError:

            return "File not found."

    def list_dir(self, dir_path):

        try:

            return os.listdir(dir_path)

        except FileNotFoundError:

            return "Directory not found."

    def move_file(self, src, dest):

        try:

            shutil.move(src, dest)

        except FileNotFoundError:

            return "File or directory not found."

    def copy_file(self, src, dest):

        try:

            shutil.copy(src, dest)

        except FileNotFoundError:

            return "File not found."

    def execute_signal(self, signal_index):

        self.signals[signal_index].execute()

class Signal:

    def __init__(self, signal_type):

        self.signal_type = signal_type

    def execute(self):

        print(f"Executing signal {self.signal_type}")

