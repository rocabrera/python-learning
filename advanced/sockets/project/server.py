import socket
import threading
#running locally

class Servidor:
    HOST = socket.gethostbyname(socket.gethostname())
    PORT = 10098
    BUFFERSIZE = 1024

    def __init__(self):
        self.UDPServerSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.UDPServerSocket.bind((self.HOST,self.PORT))
        self.peers = {}

        print("Servidor criado!")

    def _receive(self):
        while True:
            try:
                data, peer = self.UDPServerSocket.recvfrom(self.BUFFERSIZE)
                request, msg = data.decode('utf-8').split(':')
                response = self._handle_request(peer, request, msg)
                self.UDPServerSocket.sendto(response,peer)
                
            except KeyboardInterrupt as e:
                """
                No futuro eu devo tirar o client se algum erro acontecer
                """
                print()
                print("#"*64)
                print(self.peers)
                print("#"*64)
                self.UDPServerSocket.close()
                break

    def _handle_request(self,peer,request,msg):
        if request == "JOIN":
            return self._handle_join(peer,msg)

        elif request == "LEAVE":
            return self._handle_leave(peer)
        
    def _handle_join(self,peer,msg):
        self.peers[peer] = msg.strip().split(',')
        return b"JOIN_OK"

    def _handle_leave(self, peer):
        self.peers.pop(peer)
        return b"LEAVE_OK"



    def broadcast(self):
        pass
    
    def _broadcast_alive(self):

        pass


if __name__ == "__main__":

    server = Servidor()
    print(server.HOST)
    server._receive()