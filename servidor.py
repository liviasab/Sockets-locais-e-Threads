import socket # Módulo para criação do socket
import threading # Módulo para criar uma threading
import os # Módulo para acessar o sistema operacional

# Caminho do socket local
SOCKET_PATH = "/tmp/socket_server"

# Função para tratar cada cliente conectado
def handle_client(conn, addr):
    try:
        # Recebe o identificador do cliente: A função handle_client recebe a
        # conexão (conn) e lê a primeira mensagem enviada pelo cliente, que 
        # é o identificador único. Esse identificador é armazenado na variável client_id e 
        # impresso no console para que o servidor saiba quem está conectado.
        client_id = conn.recv(1024).decode()
        print(f"[CONEXÃO ESTABELECIDA] Cliente: {client_id} (Endereço: {addr})")
        
        # Loop para receber mensagens: Dentro da função handle_client, o servidor entra em um loop 
        # infinito recebendo mensagens enviadas pelo cliente conectado. O loop é encerrado se o 
        # cliente desconectar.
        while True:
            data = conn.recv(1024)
            if not data:
                break 
                # Conexão encerrada pelo cliente: Toda mensagem recebida do cliente
                # é decodificada e impressa no console junto com o identificador único do cliente. 
                # Isso satisfaz o requisito de identificar qual cliente enviou a mensagem.
            
            print(f"[MENSAGEM] Cliente {client_id}: {data.decode()}")
    except ConnectionResetError:
        print(f"[ERRO] Conexão com o cliente {addr} foi interrompida.")
    finally:
        print(f"[DESCONECTADO] Cliente {addr} desconectado.")
        conn.close()

# Configurando o servidor: remove para garantir que não terá comflitos
if os.path.exists(SOCKET_PATH):
    os.remove(SOCKET_PATH)

server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
server.bind(SOCKET_PATH)
server.listen(5)
print(f"[SERVIDOR] Servidor iniciado no socket: {SOCKET_PATH}")

try:
    while True:
        # Aceitar conexão de um cliente:O servidor usa o método accept() para aceitar conexões de clientes.
        # Para cada cliente, uma nova thread é iniciada utilizando a função handle_client, 
        # permitindo o atendimento simultâneo de múltiplos clientes.
        
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print("[CONEXÃO] Nova conexão aceita.")
except KeyboardInterrupt:
    print("\n[ENCERRANDO] Encerrando o servidor.")
finally:
    server.close()
    os.remove(SOCKET_PATH)
