PROGRAMA cliente

  CONSTANTES:
    HOST = "127.0.0.1"      # IP del servidor
    PORT = 12345
    BUFFER_SIZE = 4096
    MAX_REINTENTOS = 3
    DELAY_REINTENTO = 2     # segundos entre reintentos

  VARIABLES:
    sock = null
    hilo_recepcion = null

  ─────────────────────────────────────────
  FUNCIÓN principal():
    SI NOT conectar_con_reintentos():
      imprimir("No se pudo conectar. Saliendo.")
      SALIR

    # Lanzar hilo separado para recibir mensajes
    hilo_recepcion = Thread(función = recibir_mensajes)
    hilo_recepcion.daemon = true     # muere si el programa termina
    hilo_recepcion.iniciar()

    # Hilo principal: leer input del usuario y enviar
    enviar_mensajes()

  ─────────────────────────────────────────
  FUNCIÓN conectar_con_reintentos():
    intentos = 0
    MIENTRAS intentos < MAX_REINTENTOS:
      INTENTAR:
        sock = crear_socket(TCP)
        sock.connect(HOST, PORT)
        imprimir("Conectado al servidor")
        RETORNAR true
      EN CASO DE ERROR:
        intentos += 1
        imprimir("Reintento", intentos, "de", MAX_REINTENTOS)
        esperar(DELAY_REINTENTO)
    RETORNAR false

  ─────────────────────────────────────────
  FUNCIÓN enviar_mensajes():
    # Corre en el hilo principal (controla stdin)
    MIENTRAS true:
      INTENTAR:
        texto = leer_stdin()         # bloquea esperando input

        SI texto == "" O texto == null:
          CONTINUAR

        sock.send(codificar(texto))

      EN CASO DE ERROR (ConnectionError, OSError):
        imprimir("Error al enviar. Conexión perdida.")
        ROMPER

    sock.close()
    imprimir("Desconectado del servidor.")

  ─────────────────────────────────────────
  FUNCIÓN recibir_mensajes():
    # Corre en un hilo separado (no bloquea al usuario)
    MIENTRAS true:
      INTENTAR:
        datos = sock.recv(BUFFER_SIZE)

        SI datos está vacío:
          # Servidor cerró la conexión
          imprimir("Servidor cerró la conexión.")
          ROMPER

        mensaje = decodificar(datos)
        imprimir(mensaje)            # muestra en stdout

      EN CASO DE ERROR (ConnectionError, OSError):
        imprimir("Conexión con el servidor perdida.")
        ROMPER

    sock.close()

FIN PROGRAMA