# Resolução da atividade 01 - Socket local

import socket
import hashlib
import random

# Caminho do socket local
SOCKET_PATH = "/tmp/socket_server"

def generate_hash_identifier():
    # Gera um hash único baseado em dados aleatórios
    random_data = str(random.random()).encode()
    return hashlib.sha256(random_data).hexdigest()

def main():
    # Criando o identificador único do cliente: A função generate_hash_identifier 
    # cria um identificador único utilizando um hash SHA-256 gerado a partir de dados aleatórios.
    # Este identificador é enviado ao servidor assim que a conexão é estabelecida.
    client_id = generate_hash_identifier()
    print(f"[CLIENTE] Identificador único: {client_id}")

    # Conectando ao servidor: O cliente cria um socket usando o
    # protocolo local (AF_UNIX) e tenta conectar-se ao servidor 
    # utilizando o caminho do socket definido em SOCKET_PATH. Isso satisfaz 
    # o requisito de conexão inicial.
    client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    client.connect(SOCKET_PATH)

    # Enviando o identificador ao servidor
    client.send(client_id.encode())

    try:
        while True:
            # Lendo input do usuário e enviando ao servidor: O cliente entra 
            # em um loop infinito aguardando o input do usuário. Ele permite que 
            # o cliente envie mensagens repetidamente.
            msg = input("Digite uma mensagem (ou 'sair' para encerrar): ")
            
            # A cada input, a mensagem de texto deve ser enviada ao servidor: A mensagem digitada pelo 
            # usuário é enviada ao servidor usando o método send().
            # Caso o input seja "sair", o loop é encerrado, e a conexão é fechada.
            if msg.lower() == "sair":
                print("[CLIENTE] Encerrando conexão.")
                break
            client.send(msg.encode())
    except KeyboardInterrupt:
        print("\n[CLIENTE] Encerrando conexão.")
    finally:
        client.close()

if __name__ == "__main__":
    main()
