import os   # Utilitys do sistema operacional
import sys  # Para pegar folder no qual os dados estão
import glob # Percorre com regex os files de um folder

import socket
import threading



class Client:

    SERVER_ADDRESS = "127.0.1.1"
    SERVER_PORT = 10098
    SERVER_ID = (SERVER_ADDRESS,SERVER_PORT)
    BUFFER_SIZE = 1024

    def __init__(self,files_path):
        self.UDPClientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.files_path = files_path
        self.files = ",".join([os.path.basename(file_name) for file_name in files_path])
        print("Client criado")

    def _receive(self):
        pass

    def join(self):
        self.UDPClientSocket.sendto(f"JOIN: {self.files}".encode("utf-8"), self.SERVER_ID)
        data, server =self.UDPClientSocket.recvfrom(self.BUFFER_SIZE)
        print(data.decode("utf-8"))

    def leave(self):
        self.UDPClientSocket.sendto(f"LEAVE:", self.SERVER_ID)

        

if __name__ == "__main__":

    #file_folder_path = sys.argv[1]
    file_folder_path = "data/files"
    files_path = [file_name for file_name in glob.glob(f"{file_folder_path}/*.txt")]
    client = Client(files_path)
    print(client.files)
    print(client.files_path)
    client.join()