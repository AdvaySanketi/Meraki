import socket
import random
import json
from threading import Thread
from datetime import datetime
from colorama import Fore, init, Back

init()

colors = [Fore.BLUE, Fore.CYAN, Fore.GREEN, Fore.LIGHTBLACK_EX, 
    Fore.LIGHTBLUE_EX, Fore.LIGHTCYAN_EX, Fore.LIGHTGREEN_EX, 
    Fore.LIGHTMAGENTA_EX, Fore.LIGHTRED_EX, Fore.LIGHTWHITE_EX, 
    Fore.LIGHTYELLOW_EX, Fore.MAGENTA, Fore.RED, Fore.YELLOW
]
client_color = random.choice(colors)

class ClientNode:

    READ_BUFFER = 4096

    def __init__(self):
        self.node = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.node.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        port_and_ip = ('127.0.0.1', 12345)
        print(f"[*] Connecting to {port_and_ip[0]}:{port_and_ip[1]}...")
        self.separator_token = "<SEP>"
        self.node.connect(port_and_ip)
        print(f"[+] Connected to {port_and_ip[0]}:{port_and_ip[1]}")
        with open("assets//Files//Active_User.json", 'r') as file:
            data = json.load(file)
        self.name = data['username']

    def listen_for_messages(self):
        while True:
            message = self.node.recv(1024).decode()
            self.message = "\n" + message

    def main(self):
        while True:
            to_send =  input()
            date_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
            to_send = f"{client_color}[{date_now}] {self.name}{self.separator_token}{to_send}{Fore.RESET}"
            self.node.send(to_send.encode())

Client = ClientNode()
always_receive = Thread(target=Client.listen_for_messages)
always_receive.daemon = True
always_receive.start()
Client.main()
Client.node.close()