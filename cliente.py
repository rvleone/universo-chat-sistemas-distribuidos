import socket  # Comunicação em rede
import threading  # Execução simultânea (threads)
import sys
import os

# Garante compatibilidade de acentuação (UTF-8) no terminal do Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

HOST = '127.0.0.1'  # Endereço do servidor (localhost)
PORT = 5000  # Porta do servidor
conectado = True

def receber_mensagens(cliente):
    """ Thread responsável por receber mensagens do servidor """
    global conectado
    while conectado:
        try:
            mensagem = cliente.recv(1024).decode('utf-8')  # Recebe mensagem do servidor
            if not mensagem:
                break
            print(mensagem)
        except:
            break
    if conectado:
        print("Conexão encerrada pelo servidor.")

def enviar_mensagens(cliente, nome):
    """ Thread responsável por enviar mensagens digitadas pelo usuário """
    global conectado
    while conectado:
        try:
            msg = input()
            # Comando para sair do chat
            if msg.strip() == '/sair':
                conectado = False
                try:
                    cliente.send('/sair'.encode('utf-8'))
                except:
                    pass
                cliente.close()
                print("Você saiu do chat.")
                os._exit(0)

            # Formatação solicitada no padrão: [Nome]: Mensagem
            mensagem = f"[{nome}]: {msg}"
            cliente.send(mensagem.encode('utf-8'))  # Envia a mensagem para o servidor
        except:
            break

def main():
    """ Função principal do cliente. Conecta ao servidor e inicia as threads """
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Cria socket TCP
    try:
        cliente.connect((HOST, PORT))  # Conecta ao servidor
    except Exception as e:
        print(f"Não foi possível conectar ao servidor: {e}")
        return

    nome = input("Digite seu nome: ").strip()  # Solicita nome do usuário
    cliente.send(nome.encode('utf-8'))  # Envia o nome imediatamente ao servidor

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
    thread_enviar.daemon = True
    thread_enviar.start()

    thread_enviar.join()

# Executa o cliente
if __name__ == "__main__":
    main()
