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
                #Criar uma thread para cada requisição de um cliente
                thread = threading.Thread(target=self._handle_request,args=(peer, request, msg,))
                thread.start()

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
        print()
        peer_address, peer_port = peer
        file_lst = msg.strip()
        self.peers[peer] = file_lst.split(',')
        print(f"Peer [{peer_address}]:{peer_port} adicionado com arquivos {file_lst}")
        self.UDPServerSocket.sendto(b"JOIN_OK\n",peer)

    def _handle_leave(self, peer):
        if peer in self.peers:
            self.peers.pop(peer)
            self.UDPServerSocket.sendto(b"LEAVE_OK\n",peer)
        else:
            self.UDPServerSocket.sendto(b"Primeiro de JOIN",peer)



    def broadcast(self):
        pass
    
    def _broadcast_alive(self):

        pass


if __name__ == "__main__":

    server = Servidor()
    print(server.HOST)
    server._receive()