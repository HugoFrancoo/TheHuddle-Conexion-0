import select
import socket
# variables constantes
HOST = "127.0.0.1"
PORT = 5050
BUFFER = 1024 #la capacidad en bytes que puede recibir 
lista_clientes = []

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
server.bind((HOST,PORT))

def run_server():

    server.listen()

    print(f"[SERVER]Servidor escuchando en {HOST}, {PORT}...")

    lista_clientes.append(server)
    while True:
        lectura_socket,_,_ = select.select(lista_clientes,[],[]) #investigar los corchetes

        for socket in lectura_socket:
            if socket == server:
                conn, addr = server.accept()
                lista_clientes.append(conn)
                print(f"[SERVER] Nuevo cliente conectado {addr}")
            else: #El cliente ya conectado mando datos
                # manejar_mensaje(socket)
                pass

def manejar_clientes(socket):
    try:
        datos = socket.recv(BUFFER)

        if not datos: # recv vacio
            socket.close()
            mensaje = mensaje.decode("utf-8")
            print("[SERVER] Mensaje recibido",mensaje)
            broadcast
            
    except(ConnectionError,OSError):






                






#   FUNCIÓN principal():
#     server_sock = crear_socket(TCP)
#     server_sock.opcion(SO_REUSEADDR = true)
#     server_sock.bind(HOST, PORT)
#     server_sock.listen(max_conexiones = 10)
#     imprimir("Servidor escuchando en PORT")

#     MIENTRAS true:
#       # select() bloquea hasta que haya actividad en algún socket
#       readable = select([server_sock] + lista_clientes)

#       PARA cada sock EN readable:

#         SI sock == server_sock:
#           # Nuevo cliente quiere conectarse
#           cliente_sock, direccion = server_sock.accept()
#           lista_clientes.agregar(cliente_sock)
#           imprimir("Nuevo cliente conectado:", direccion)

#         SINO:
#           # Un cliente ya conectado mandó datos
#           manejar_mensaje(sock)

#   ─────────────────────────────────────────
#   FUNCIÓN manejar_mensaje(sock):
#     INTENTAR:
#       datos = sock.recv(BUFFER_SIZE)

#       SI datos está vacío:
#         # Cliente cerró conexión limpiamente
#         desconectar(sock)
#         RETORNAR

#       mensaje = decodificar(datos)
#       imprimir("[SERVIDOR] Mensaje recibido:", mensaje)
#       broadcast(mensaje, origen = sock)

#     EN CASO DE ERROR (ConnectionError, OSError):
#       # Conexión rota de forma inesperada
#       desconectar(sock)

#   ─────────────────────────────────────────
#   FUNCIÓN broadcast(mensaje, origen):
#     PARA cada cliente EN lista_clientes:
#       SI cliente != origen:
#         INTENTAR:
#           cliente.send(codificar(mensaje))
#         EN CASO DE ERROR:
#           # El cliente remoto ya no responde
#           desconectar(cliente)

#   ─────────────────────────────────────────
#   FUNCIÓN desconectar(sock):
#     SI sock EN lista_clientes:
#       lista_clientes.eliminar(sock)
#     INTENTAR:
#       sock.close()
#     IGNORAR errores al cerrar
#     imprimir("Cliente desconectado")

# FIN PROGRAMA