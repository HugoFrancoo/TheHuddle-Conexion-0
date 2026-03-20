import socket

HEADER = 64 # el primer mensaje que se reciba del cliente al servidor va a ser de 64 bytes "hello                    " relleno hasta 64 bytes
PORT = 5050 # es un puerto que se asocia comunmente a aplicaciones de comunicacion 
FORMAT = 'uft-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)