PROGRAMA servidor

  CONSTANTES:
    HOST = "0.0.0.0"
    PORT = 12345
    BUFFER_SIZE = 4096

  VARIABLES GLOBALES:
    lista_clientes = []          # lista de sockets activos

  ─────────────────────────────────────────
  FUNCIÓN principal():
    server_sock = crear_socket(TCP)
    server_sock.opcion(SO_REUSEADDR = true)
    server_sock.bind(HOST, PORT)
    server_sock.listen(max_conexiones = 10)
    imprimir("Servidor escuchando en PORT")

    MIENTRAS true:
      # select() bloquea hasta que haya actividad en algún socket
      readable = select([server_sock] + lista_clientes)

      PARA cada sock EN readable:

        SI sock == server_sock:
          # Nuevo cliente quiere conectarse
          cliente_sock, direccion = server_sock.accept()
          lista_clientes.agregar(cliente_sock)
          imprimir("Nuevo cliente conectado:", direccion)

        SINO:
          # Un cliente ya conectado mandó datos
          manejar_mensaje(sock)

  ─────────────────────────────────────────
  FUNCIÓN manejar_mensaje(sock):
    INTENTAR:
      datos = sock.recv(BUFFER_SIZE)

      SI datos está vacío:
        # Cliente cerró conexión limpiamente
        desconectar(sock)
        RETORNAR

      mensaje = decodificar(datos)
      imprimir("[SERVIDOR] Mensaje recibido:", mensaje)
      broadcast(mensaje, origen = sock)

    EN CASO DE ERROR (ConnectionError, OSError):
      # Conexión rota de forma inesperada
      desconectar(sock)

  ─────────────────────────────────────────
  FUNCIÓN broadcast(mensaje, origen):
    PARA cada cliente EN lista_clientes:
      SI cliente != origen:
        INTENTAR:
          cliente.send(codificar(mensaje))
        EN CASO DE ERROR:
          # El cliente remoto ya no responde
          desconectar(cliente)

  ─────────────────────────────────────────
  FUNCIÓN desconectar(sock):
    SI sock EN lista_clientes:
      lista_clientes.eliminar(sock)
    INTENTAR:
      sock.close()
    IGNORAR errores al cerrar
    imprimir("Cliente desconectado")

FIN PROGRAMA