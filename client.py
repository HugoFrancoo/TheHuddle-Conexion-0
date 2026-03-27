import socket
import threading
import time
# configuración
HOST = "127.0.0.1" #ip-server
PORT = 5050 #puerto-server
BUFFER = 1024
DELAY_REINTENTO = 3 #pausa el programa N segundos entre reintentos
# funciones 
def recibir_mensajes(client, cerrar_evento):
    # escucha mensajes del servidor en un hilo separado
    while True:
        try:
            datos = client.recv(BUFFER)
            if not datos:                       # servidor cerró la conexión
                print("[CLIENT] Servidor desconectado.")
                break
            
            print(datos.decode("utf-8")) 
        except (ConnectionError, OSError):      # conexión caída abruptamente
            print("[CLIENT] Conexión perdida.")
            break
    # avisa al hilo de envío que la conexión murió e interrumpe el socket
    cerrar_evento.set() # activa el flag compartido
    try: # desconexion limpia
        client.shutdown(socket.SHUT_RDWR) # corta la conexion de ambos lados del socket
        client.close() #libera espacio recurso, cierra el socket
    except:
        pass

def enviar_mensajes(client, cerrar_evento):
    # lee input del usuario y lo manda al servidor
    while True:
        try:
            texto = input()

            if not texto:
                continue

            if cerrar_evento.is_set():          # conexión ya muerta, no enviar
                break

            client.send(texto.encode("utf-8"))

        except (ConnectionError, OSError):
            break

def conectar():
    # intenta conectar al servidor, reintenta cada N segundos si falla
    while True:
        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect((HOST, PORT))
            print(f"[CLIENT] Conectado a {HOST}:{PORT}")
            return client
        except (ConnectionError, OSError):
            print(f"[CLIENT] Sin servidor. Reintentando en {DELAY_REINTENTO}s...")
            time.sleep(DELAY_REINTENTO)

# loop principal 
def run_client():
    while True:
        client = conectar()
        # evento compartido: se activa cuando la conexión muere
        cerrar_evento = threading.Event()
        # hilo de recepción: escucha mensajes del servidor
        hilo_recepcion = threading.Thread(target=recibir_mensajes, args=(client, cerrar_evento))
        hilo_recepcion.daemon = True
        hilo_recepcion.start()
        # hilo de envío: escucha input del usuario
        hilo_envio = threading.Thread(target=enviar_mensajes, args=(client, cerrar_evento))
        hilo_envio.daemon = True # el programa sale aunque el hilo siga ejecutandose
        hilo_envio.start()
        # espera hasta que el hilo de recepción muera (señal de que el servidor cayó)
        hilo_recepcion.join()
        print(f"[CLIENT] Reconectando en {DELAY_REINTENTO}s...")
        time.sleep(DELAY_REINTENTO)
run_client()