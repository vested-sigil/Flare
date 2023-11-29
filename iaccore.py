import socket
import threading

class IACCore:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.adhoc_ssid = None
        self.adhoc_password = None
        self.clients = {}

    def start(self):
        server_thread = threading.Thread(target=self.run_server)
        server_thread.start()

    def run_server(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind((self.host, self.port))
            server_socket.listen(1)
            print(f"IAC core is listening on {self.host}:{self.port}")

            while True:
                client_socket, addr = server_socket.accept()
                print(f"Connection established with {addr}")

                # Handle client verification
                if self.verify_client(client_socket):
                    # Get the client's MAC address
                    mac_address = self.get_mac_address(client_socket)

                    # Store the client's MAC address and associated socket
                    self.clients[mac_address] = client_socket

                    # Send the adhoc SSID and password to the client
                    self.send_adhoc_details(client_socket)
                else:
                    client_socket.sendall(b"Unauthorized client")
                    client_socket.close()

    def verify_client(self, client_socket):
        # Implement your client verification logic here
        # You can verify the client based on their MAC address, adlib identifier, or any other method
        # Return True if the client is verified, otherwise False
        return True

    def get_mac_address(self, client_socket):
        # Retrieve the MAC address of the client from the socket
        # Implement the logic to extract and return the MAC address
        mac_address = "<MAC_ADDRESS>"
        return mac_address

    def send_adhoc_details(self, client_socket):
        if self.adhoc_ssid is not None and self.adhoc_password is not None:
            adhoc_details = f"SSID: {self.adhoc_ssid}, Password: {self.adhoc_password}"
            client_socket.sendall(adhoc_details.encode())
        else:
            client_socket.sendall(b"No adhoc details available")

        client_socket.close()

    def arm_security_system(self):
        # Code to arm the security system
        print("Arming the security system")

    def disarm_security_system(self):
        # Code to disarm the security system
        print("Disarming the security system")

    def main_menu(self):
        while True:
            print("MAIN MENU")
            print("1. Arm Security System")
            print("2. Disarm Security System")
            print("3. Exit")
            choice = input("Enter your choice: ")

            if choice == "1":
                self.arm_security_system()
            elif choice == "2":
                self.disarm_security_system()
            elif choice == "3":
                break
            else:
                print("Invalid choice. Please try again.")


# Example usage
if __name__ == '__main__':
    host = '192.168.0.1'  # Replace with the IP address of the core
    port = 8000  # Replace with the desired port number

    core = IACCore(host, port)
    core.start()
    core.main_menu()
i
mport random
import subprocess
import time
import socket
import threading
import hashlib
from adlibs import adv, adj, verb, object

KEY_LENGTH = 16
SSID_NAME = "Central_Intelligence"
RENEW_PASSWORD_INTERVAL = 3600  # Refresh the password every 1 hour

class IACCore:
    """A class representing the IAC core server and handling its various network operations."""
    
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.authorized_devices = {}
        self.kvp = [adv.list, adj.list, verb.list, object.list]
        self.seeds = {}

    def start(self):
        """Start the IAC core server."""
        self.setup_adhoc_network()
        server_thread = threading.Thread(target=self.run_server)
        server_thread.start()

    def setup_adhoc_network(self):
        """Set up the adhoc network and refresh password every hour."""
        password = self.generate_adlib_key()
        subprocess.call(['netsh', 'wlan', 'set', 'hostednetwork', 'mode=allow', f'ssid={SSID_NAME}', f'key={password}'])
        subprocess.call(['netsh', 'wlan', 'start', 'hostednetwork'])

        while True:
            time.sleep(RENEW_PASSWORD_INTERVAL)
            password = self.generate_adlib_key()
            subprocess.call(['netsh', 'wlan', 'set', 'hostednetwork', f'key={password}'])

    @staticmethod
    def generate_adlib_key():
        """Generate a random adlib key."""
        characters = string.ascii_letters + string.digits
        return ''.join(random.choice(characters) for _ in range(KEY_LENGTH))

    def run_server(self):
        """Run the server and handle incoming connections."""
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
        """Verify if the client is authorized."""
        client_id = self.get_client_id(client_socket)
        if client_id is None:
            return False

        received_key = client_socket.recv(1024).decode()  # Note: You'll need to have client send this.
        if self.authenticate(client_id, received_key):
            return True
        else:
            seed = self.register(client_id)
            client_socket.sendall(seed.encode())
            return False

    def handle_authorized_client(self, client_socket):
        """Handle authorized client by sending welcome message."""
        client_socket.sendall(b"Welcome to the IAC system.")
        # handle your authorized client
        client_socket.close()

    def get_client_id(self, client_socket):
        """Implement your own method to retrieve client ID."""
        pass

    def register(self, client_id):
        """Register a new client and return the seed."""
        seed = hashlib.sha256(str(random.randint(0, 99999999)).encode()).hexdigest()
        self.seeds[client_id] = seed
        return seed

    def authenticate(self, client_id, received_key):
        """Authenticate the client using the received key."""
        seed = self.seeds.get(client_id)
        if seed is None:
           

   def authenticate(self, client_id, received_key):
        """Authenticate the client using the received key."""
        seed = self.seeds.get(client_id)
        if seed is None:
            return False
        expected_key = self.generate_key(seed)
        return received_key == expected_key

    def generate_key(self, seed):
        """Generate a key based on a given seed."""
        random.seed(seed)
        key = [self.kvp[i][random.randint(0, 99)] for i in range(4)]
        return ' '.join(key)

