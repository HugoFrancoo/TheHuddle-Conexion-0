import socket
import threading # trabaja con un hilo por cada uno de los clientes

# lo primero que hay que hacer es definir un puerto y la ip del servidor
PORT = 5050 # es un puerto que se asocia comunmente a aplicaciones de comunicacion 
SERVER = socket.gethostbyname(socket.gethostname()) # obtiene la direccion de ip local de mi servidor automaticamente (obtener la direccion IPV4 apartir del hotname de la pc)
ADDR = (SERVER,PORT) #un tupla donde primero tenemos la direccion IP del servidor y el puerto del servidor "192.168.0.X:5050"
print(SERVER)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # definimos con que tipo de direccion IP vamos a contactar, y como se va a transmitir esos datos
server.bind(ADDR) # enlazamos el socket a la direccion IP y el PORT del servidor

def handle_client(conn,addr):
    pass

def start():
    server.listen() # servidor escuchando peticiones 
    while True:
        conn, addr = server.accept() # espera una conexion al servidor, y nosotros almacenamos los valores dentro de conn y de addr CONN es un objeto SOCKET
        thread = threading.Thread(target=handle_client, args=(conn, addr)) # cuando se genere una nueva conexion pasamos los argumentos conn y addr a handle_client
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}") # es para visualizar la cantidad de hilos que estan activos, la cantidad de hilos representa a la cantidad de clientes

print("[STARTING] server is starting...")
start()









