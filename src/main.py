import socket
import threading
import time
import sys
from menu import init


def ouvir(ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    s.bind((ip, int(port)))

    s.listen()

    conn, addr = s.accept()
    print("Conexão (recebimento) [OK]")

    a = ""
    while a != "fim":
        a = conn.recv(1024)
        print(f"Recebido: {a.decode()}\n")
    return


def enviar(ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    s.connect((ip, int(port)))
    print("Conexão envio [OK]")

    a = ""
    while a != "fim":
        a = input()
        print()
        s.send(a.encode())
    return


def aguardar(tempo):
    print("Aguardando")
    for i in range(int(tempo)):
        print(i + 1)
        time.sleep(1)


def main():
    username, porta_receber, porta_enviar, ip_amigo = init()
    meu_ip = "0.0.0.0"

    print(f"Ouvindo em {meu_ip} {porta_receber}")
    print(f"Enviando para {ip_amigo} {porta_enviar}")

    thread_ouvir = threading.Thread(
        target=ouvir, args=(meu_ip, porta_receber), daemon=True
    )
    thread_enviar = threading.Thread(
        target=enviar, args=(ip_amigo, porta_enviar), daemon=True
    )

    thread_ouvir.start()
    aguardar(5)
    thread_enviar.start()

    thread_ouvir.join()
    thread_enviar.join()


if __name__ == "__main__":
    main()
    print("Programa encerrado...")
