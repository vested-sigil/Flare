import random
import hashlib
import subprocess
import time
import socket
import threading
import uuid
from adlibs import adv, adj, verb, object

KEY_LENGTH = 16
SSID_NAME = "Central_Intelligence"
RENEW_PASSWORD_INTERVAL = 3600  # Refresh the password every 1 hour

class SecretRecipe:
    def __init__(self):
        self.kvp = [adv.list, adj.list, verb.list, object.list]
        self.seeds = {}

    def register(self, client_id):
        seed = hashlib.sha256(str(random.randint(0, 99999999)).encode()).hexdigest()
        self.seeds[client_id] = seed
        return seed

    def authenticate(self, client_id, received_key):
        seed = self.seeds.get(client_id)
        if seed is None:
            return False
        expected_key = self.generate_key(seed)
        return received_key == expected_key

    def generate_key(self, seed):
        random.seed(seed)
        key = [self.kvp[i][random.randint(0, 99)] for i in range(4)]
        return key

    def shuffle(self, seed):
        random.seed(seed)
        for list in self.kvp:
            random.shuffle(list)

class IACCore:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.authorized_devices = {}
        self.security = SecretRecipe()

    def start(self):
        self.setup_adhoc_network()
        server_thread = threading.Thread(target=self.run_server)
        server_thread.start()

    def setup_adhoc_network(self):
        password = self.generate_adlib_key()
        subprocess.call(['netsh', 'wlan', 'set', 'hostednetwork', 'mode=allow', f'ssid={SSID_NAME}', f'key={password}'])
        subprocess.call(['netsh', 'wlan', 'start', 'hostednetwork'])

        while True:
            time.sleep(RENEW_PASSWORD_INTERVAL)
            password = self.generate_adlib_key()
            subprocess.call(['netsh', 'wlan', 'set', 'hostednetwork', f'key={password}'])

    def generate_adlib_key(self):
        characters = string.ascii_letters + string.digits
        return ''.join(random.choice(characters) for _ in range(KEY_LENGTH))

    def run_server(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind((self.host, self.port))
            server_socket.listen(1)

            while True:
                client_socket, addr = server_socket.accept()
                if self.verify_client(client_socket):
                    self.handle_authorized_client(client_socket)
                else:
                    client_socket.sendall(b"Unauthorized client")
                    client_socket.close()

    def verify_client(self, client_socket):
        client_id = self.get_client_id(client_socket)
        if client_id is None:
            return False

        received_key = client_socket.recv(1024).decode()  # Note: You'll need to have client send this.
        if self.security.authenticate(client_id, received_key):
            return True
        else:
            seed = self.security.register(client_id)
            client_socket.sendall(seed.encode())
            return False

    def handle_authorized_client(self, client_socket):
        client_socket.sendall(b"Welcome to the IAC system.")
        # handle your authorized client
        client_socket.close()

    def get_client_id(self, client_socket):
        """Fetch the MAC address as a string."""
        mac_num = hex(uuid.getnode()).replace('0x', '').upper()  #

