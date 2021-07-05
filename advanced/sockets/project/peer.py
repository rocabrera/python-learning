import os   # Utilitys do sistema operacional
import sys  # Para pegar folder no qual os dados estão
import glob  # Percorre com regex os files de um folder
import json  # Utilizado para fazer parse da mensagem
import time
import socket
import threading

from message import Message


class Peer:

    MY_ADRESS = socket.gethostbyname(socket.gethostname())

    SERVER_ADDRESS = "127.0.1.1"
    SERVER_PORT = 10098
    SERVER = (SERVER_ADDRESS, SERVER_PORT)
    BUFFERSIZE = 4096

    def __init__(self, file_folder_path, files_path, port):
        self.PORT = int(port)
        self.UDPClientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.TCPSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.TCPSocket.bind((self.MY_ADRESS, self.PORT))
        self.TCPSocket.listen()

        self.network_peers = {}
        self.file_folder_path = file_folder_path
        self.files_path = files_path
        self.files = " ".join([os.path.basename(file_name)
                              for file_name in files_path])
        self.menu_str = "Digite a requisição [JOIN, SEARCH, DOWNLOAD, LEAVE]:"

    def _receive_download(self):
        while True:
            client, address = self.TCPSocket.accept()
            msg = client.recv(1024).decode('ascii')
            print(msg)

    def _receive(self):
        while True:
            data, server = self.UDPClientSocket.recvfrom(self.BUFFERSIZE)

            recv_msg = json.loads(data.decode('utf-8'))  # Transforma json em dict
            thread = threading.Thread(target=self._handle_request, args=(server, recv_msg))
            thread.start()
            thread.join()

    def _handle_request(self, server, recv_msg):

        text_msg = recv_msg["message"].strip("\n")

        if recv_msg["type_msg"] == "OK":

            if text_msg == "JOIN_OK":
                self._handle_join()

            elif text_msg == "LEAVE_OK":
                self._handle_leave()  # No futuro preciso desligar o client aqui

            elif text_msg == "ALIVE":
                return self._handle_alive()

        elif recv_msg["type_msg"] == "SEARCH":
            filename = recv_msg["file"]
            self._handle_search(text_msg, filename)

        elif recv_msg["type_msg"] == "DOWNLOAD":
            filename = recv_msg["file"]
            package = recv_msg["info"]
            self._handle_download(filename, package)

    def _handle_join(self):
        print(f"Sou o peer [{self.MY_ADRESS}]:{self.PORT} com arquivos {self.files}\n")

    def _handle_search(self, msg, filename):
        parse_msg = msg.strip('[]').split()
        for peer in parse_msg:
            address, port = peer.split(':')
            self.network_peers[(address, int(port))] = filename
        print(f"Peers com arquivo solicitado: {msg}")

    def _handle_download(self, filename, package):
        client_socket, address = self.TCPSocket.accept()

        # client.send("NICK".encode('ascii'))
        # nickname = client.recv(1024).decode('ascii')

        file_path = os.path.join(self.file_folder_path, filename)
        with open(file_path, "wb") as f:
            while True:
                bytes_read = client_socket.recv(self.BUFFERSIZE)
                if not bytes_read:
                    # nothing is received
                    # file transmitting is done
                    break
                # write to the file the bytes we just received
                f.write(package)

    def _handle_leave(self):
        sys.exit("Desconectado")

    def _handle_alive(self):        
        msg = Message("ALIVE_OK:\n", None)
        self.UDPClientSocket.sendto(msg.to_json("utf-8"), self.SERVER)

    def _request(self):
        while True:
            time.sleep(0.1)
            request = input(self.menu_str)
            thread = threading.Thread(target=self._handle_write, args=(request,))
            thread.start()
            thread.join()

    def _handle_write(self, request):
        command, *msg = request.split()
        command = command.upper()

        if command == "JOIN":
            self.join()

        elif command == "SEARCH":
            msg_len = len(msg)
            if msg_len == 0:
                print("Faltou o nome do arquivo")
            elif msg_len == 1:
                self.search(msg[0])
            else:
                print("Somente 1 arquivo por vez")

        elif command == "DOWNLOAD":
            msg_len = len(msg)
            if msg_len == 0:
                print("Faltou o nome do arquivo")
            elif msg_len == 1:
                self.download(msg[0])
            else:
                print("Somente 1 arquivo por vez")

        elif command == "LEAVE":
            self.leave()
        else:
            print("Comando Invalido.")

    def join(self):
        msg = Message(f"JOIN: {self.files}", "JOIN", None, self.PORT)
        self.UDPClientSocket.sendto(msg.to_json("utf-8"), self.SERVER)

    def search(self, requested_file):
        msg = Message(f"SEARCH: {requested_file}", None)
        self.UDPClientSocket.sendto(msg.to_json("utf-8"), self.SERVER)

    def download(self, requested_file):
        msg = Message(f"DOWNLOAD: {requested_file}", None)
        for peer in self.network_peers:
            if requested_file in self.network_peers[peer]:
                print(peer)
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((peer[0],30000))
                s.sendall(msg.to_json("utf-8"), peer)
                return None

        """
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect(peer)
            file_path = os.path.join(self.file_folder_path, requested_file)
            with open(file_path, "rb") as f:
                while True:
                    # read the bytes from the file
                    bytes_read = f.read(self.BUFFERSIZE)
                    if not bytes_read:
                        # file transmitting is done
                        break
                    # we use sendall to assure transimission in busy networks
                    s.sendall(msg.to_json("utf-8"))
            s.close()
        """

    def leave(self):
        msg = Message("LEAVE:", None)
        self.UDPClientSocket.sendto(msg.to_json("utf-8"), self.SERVER)


if __name__ == "__main__":

    _, file_folder_path, port = sys.argv
    # file_folder_path = "data/peer1"
    files_path = [file_name for file_name in glob.glob(f"{file_folder_path}/*.txt")]

    peer = Peer(file_folder_path, files_path, port)
    print("ONLINE\n")
    listening_thread = threading.Thread(target=peer._receive)
    alive_thread = threading.Thread(target=peer._request)

    listening_thread.start()
    alive_thread.start()
