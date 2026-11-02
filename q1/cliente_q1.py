import socket  # Comunicação em rede
import threading  # Execução simultânea (threads)

HOST = '127.0.0.1'  # Endereço do servidor (localhost)
PORT = 5000  # Porta do servidor

def receber_mensagens(cliente):
    """ Thread responsável por receber mensagens do servidor """
    while True:
        try:
            mensagem = cliente.recv(1024).decode()  # Recebe mensagem do servidor
            if not mensagem:
                break
            print(mensagem)
        except:
            print("Erro ao receber mensagem. Conexão encerrada.")
            cliente.close()
            break

def enviar_mensagens(cliente, nome):
    """ Thread responsável por enviar mensagens digitadas pelo usuário """
    while True:
        try:
            msg = input()
            mensagem = f"{nome}: {msg}"
            cliente.send(mensagem.encode())  # Envia a mensagem para o servidor
        except:
            break

def main():
    """ Função principal do cliente. Conecta ao servidor e inicia as threads """
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Cria socket TCP
    cliente.connect((HOST, PORT))  # Conecta ao servidor
    nome = input("Digite seu nome: ")  # Solicita nome do usuário

    # Thread para receber mensagens
    thread_receber = threading.Thread(
        target=receber_mensagens,
        args=(cliente,)
    )
    thread_receber.daemon = True
    thread_receber.start()

    # Thread para enviar mensagens
    thread_enviar = threading.Thread(
        target=enviar_mensagens,
        args=(cliente, nome)
    )
    thread_enviar.start()

# Executa o cliente
if __name__ == "__main__":
    main()
