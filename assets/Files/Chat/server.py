import socket
import select
import threading
from chat_util import Hall, Room, Player
import chat_util

class ServerNode:
    client_sockets = set()
    connection_list = []
    READ_BUFFER = 4096

    def __init__(self):
        port_and_ip = ('0.0.0.0', 12345)
        self.separator_token = "<SEP>"
        self.node = chat_util.create_socket((port_and_ip[0], port_and_ip[1]))

    def listen_for_client(self, cs):
        while True:
            try:
                msg = cs.recv(1024).decode()
            except Exception as e:
                print(f"[!] Error: {e}")
                self.client_sockets.remove(cs)
            else:
                msg = msg.replace(self.separator_token, ": ")
            for client_socket in self.client_sockets:
                client_socket.send(msg.encode())
    

    def main(self):
        while True:
            client_socket, client_address = self.node.accept()
            print(f"[+] {client_address} connected.")
            self.client_sockets.add(client_socket)
            t = threading.Thread(target=self.listen_for_client, args=(client_socket,))
            t.daemon = True
            t.start()

server = ServerNode()
server.main()
server.node.close()
