import socket  # Biblioteca para comunicação em rede
import threading  # Biblioteca para trabalhar com múltiplas threads
import sys

# Garante compatibilidade de acentuação (UTF-8) no terminal do Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

HOST = '0.0.0.0'  # Aceita conexões de qualquer IP
PORT = 5000  # Porta do servidor
clientes = []  # Lista para armazenar os clientes conectados

def broadcast(mensagem, cliente_origem):
    """ Envia a mensagem para todos os clientes conectados,
    exceto para quem enviou a mensagem."""
    for cliente in list(clientes):
        if cliente != cliente_origem:  # Evita enviar para quem mandou
            try:
                cliente.send(mensagem)  # Envia a mensagem
            except:
                if cliente in clientes:
                    clientes.remove(cliente)  # Se ocorrer erro, remove o cliente

def handle_cliente(cliente):
    """ Função executada em uma thread separada para cada cliente.
    Responsável por receber mensagens desse cliente. """
    nome = ""
    try:
        # Recebe o nome do usuário logo ao conectar
        nome_bytes = cliente.recv(1024)
        if not nome_bytes:
            if cliente in clientes:
                clientes.remove(cliente)
            cliente.close()
            return
        nome = nome_bytes.decode('utf-8').strip()
        # O servidor exibe a mensagem de conexão no formato solicitado: <Nome> entrou no chat
        print(f"{nome} entrou no chat", flush=True)
    except:
        if cliente in clientes:
            clientes.remove(cliente)
        cliente.close()
        return

    while True:
        try:
            mensagem = cliente.recv(1024)  # Recebe dados do cliente
            if not mensagem:
                # Conexão encerrada pelo cliente
                break
            
            texto = mensagem.decode('utf-8').strip()
            # Comando para sair do chat
            if texto == '/sair':
                break

            # Se recebeu mensagem normal, envia para os demais participantes
            broadcast(mensagem, cliente)
        except:
            break

    # Ao encerrar a conexão, o servidor exibe: <Nome> saiu do chat
    print(f"{nome} saiu do chat", flush=True)
    if cliente in clientes:
        clientes.remove(cliente)  # Remove da lista
    cliente.close()

def main():
    """ Função principal. Cria o socket e fica aguardando conexões. """
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Cria o socket TCP
    # Permite reutilizar a porta imediatamente se o script for reiniciado
    servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    servidor.bind((HOST, PORT))  # Associa o socket ao IP e porta
    servidor.listen()  # Coloca o servidor em modo de escuta
    print(f"Servidor rodando em {HOST}:{PORT}", flush=True)

    while True:
        # Aceita uma nova conexão
        cliente, endereco = servidor.accept()
        clientes.append(cliente)  # Adiciona o cliente à lista

        # Cria uma thread para atender esse cliente
        thread = threading.Thread(
            target=handle_cliente,
            args=(cliente,)
        )
        thread.daemon = True
        thread.start()  # Inicia a thread

# Executa o programa
if __name__ == "__main__":
    main()
