import socket  # Biblioteca para comunicação em rede
import threading  # Biblioteca para trabalhar com múltiplas threads

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
    while True:
        try:
            mensagem = cliente.recv(1024)  # Recebe dados do cliente
            if mensagem:  # Se recebeu mensagem, envia para os outros
                broadcast(mensagem, cliente)
            else:
                raise Exception("Cliente desconectado")
        except:
            print("Cliente desconectado.")
            if cliente in clientes:
                clientes.remove(cliente)  # Remove da lista
            cliente.close()
            break

def main():
    """ Função principal. Cria o socket e fica aguardando conexões. """
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Cria o socket TCP
    servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    servidor.bind((HOST, PORT))  # Associa o socket ao IP e porta
    servidor.listen()  # Coloca o servidor em modo de escuta
    print(f"Servidor rodando em {HOST}:{PORT}")

    while True:
        # Aceita uma nova conexão
        cliente, endereco = servidor.accept()
        print(f"Novo cliente conectado: {endereco}")
        clientes.append(cliente)  # Adiciona o cliente à lista

        # Cria uma thread para atender esse cliente
        thread = threading.Thread(
            target=handle_cliente,
            args=(cliente,)
        )
        thread.start()  # Inicia a thread

# Executa o programa
if __name__ == "__main__":
    main()
