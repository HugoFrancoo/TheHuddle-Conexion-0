import socket
import threading # trabaja con un hilo por cada uno de los clientes

# lo primero que hay que hacer es definir un puerto y la ip del servidor
HEADER = 64 # el primer mensaje que se reciba del cliente al servidor va a ser de 64 bytes "hello                    " relleno hasta 64 bytes
PORT = 5050 # es un puerto que se asocia comunmente a aplicaciones de comunicacion 
SERVER = socket.gethostbyname(socket.gethostname()) # obtiene la direccion de ip local de mi servidor automaticamente (obtener la direccion IPV4 apartir del hotname de la pc)
ADDR = (SERVER,PORT) #un tupla donde primero tenemos la direccion IP del servidor y el puerto del servidor "192.168.0.X:5050"
FORMAT = 'uft-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # definimos con que tipo de direccion IP vamos a contactar, y como se va a transmitir esos datos
server.bind(ADDR) # enlazamos el socket a la direccion IP y el PORT del servidor

def handle_client(conn,addr):
    print(f"[NEW CONNECTION] {addr} connected.") #informacion de quien se conecto al servidor

    connected = True

    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT) #vamos a recibir un mensaje del cliente, lo recibimos del socket conn (esperamos a que envie un mensaje a traves del socket) formato byte a utf-8
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE: 
                connected = False           #si el mensaje recibido por el servidor es !DISCONNECT entonces se cierra el bucle While, y se deja de recibir mensajes del cliente
            
            print(f"[{addr}] {msg}")
        conn.close() # es para cerrar la conexion  actual una vez que se sale del bucle while


def start():
    server.listen() # servidor escuchando peticiones 
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept() # espera una conexion al servidor, y nosotros almacenamos los valores dentro de conn y de addr CONN es un objeto SOCKET
        thread = threading.Thread(target=handle_client, args=(conn, addr)) # cuando se genere una nueva conexion pasamos los argumentos conn y addr a handle_client
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activecount() - 1}") # es para visualizar la cantidad de hilos que estan activos, la cantidad de hilos representa a la cantidad de clientes

print("[STARTING] server is starting...")
start()









