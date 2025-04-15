import socket
import threading
import time
from menu import init, teste

ativo = True

def ouvir(ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    s.bind((ip, int(port)))

    s.listen()

    conn, addr = s.accept()
    print("Conexão (recebimento) [OK]")

    while ativo:
        a = conn.recv(1024)
        ativo = teste(a)
        print(f"Recebido: {a.decode()}\n")
    return


def enviar(ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    s.connect((ip, int(port)))
    print("Conexão envio [OK]")

    while ativo:
        a = input()
        ativo = teste(a)
        print()
        s.send(a.encode())
    return


def aguardar(tempo):
    print("Aguardando")
    for i in range(int(tempo)):
        print(i + 1)
        time.sleep(1)


def main():
    username, porta_receber, porta_destino, ip_destino = init()
    IP = "0.0.0.0"

    print(f"Ouvindo em {IP} {porta_receber}")
    print(f"Enviando para {ip_destino} {porta_destino}")

    thread_ouvir = threading.Thread(
        target=ouvir, args=(IP, porta_receber), daemon=True
    )
    thread_enviar = threading.Thread(
        target=enviar, args=(ip_destino, porta_destino), daemon=True
    )

    thread_ouvir.start()
    aguardar(5)
    thread_enviar.start()

    thread_ouvir.join()
    thread_enviar.join()


if __name__ == "__main__":
    main()
    print("Programa encerrado...")
