import select # permite vigilar multiples sockets al mismo tiempo sin usar un hilo para cada uno
import socket

# ── configuración ──────────────────────────────────────────
HOST = "127.0.0.1"
PORT = 5050
BUFFER = 1024
# ── estado global ──────────────────────────────────────────
lista_clientes = []  # todos los sockets activos (incluye al server)
# ── socket del servidor ────────────────────────────────────
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))
# ── funciones ──────────────────────────────────────────────
def desconectar(sock):
    # saca el socket de la lista y lo cierra limpiamente
    if sock in lista_clientes:
        lista_clientes.remove(sock)
    try:
        sock.close()
    except:
        pass
    print("[SERVER] Cliente desconectado")

def broadcast(mensaje, origen):
    # envía el mensaje a todos los clientes menos al que lo mandó
    for cliente in lista_clientes:
        if cliente != origen and cliente != server:
            try:
                cliente.send(mensaje.encode("utf-8"))
            except:
                desconectar(cliente)

def manejar_cliente(sock):
    # lee el mensaje del cliente y lo distribuye
    try:
        datos = sock.recv(BUFFER)

        if not datos:                           # desconexión limpia (recv vacío)
            desconectar(sock)
            return # salgo de la funcion

        mensaje = datos.decode("utf-8")
        print(f"[SERVER] Mensaje recibido: {mensaje}")
        broadcast(mensaje, origen=sock)

    except (ConnectionError, OSError):          # desconexión abrupta
        desconectar(sock)

# ── loop principal ─────────────────────────────────────────
def run_server():
    server.listen()
    print(f"[SERVER] Escuchando en {HOST}:{PORT}...")

    lista_clientes.append(server)

    while True:
        # select() bloquea hasta que algún socket tenga actividad
        legibles, _, _ = select.select(lista_clientes, [], []) # solo me importa los sockets quen tienen datos para leer

        for sock in legibles:
            if sock == server:
                # conexión nueva entrante
                conn, addr = server.accept()
                lista_clientes.append(conn)
                print(f"[SERVER] Nuevo cliente: {addr}")
            else:
                # mensaje de un cliente ya conectado
                manejar_cliente(sock)
run_server()