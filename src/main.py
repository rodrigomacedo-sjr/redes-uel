import socket
import threading
import time
import sys


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
    sys.exit()


def enviar(ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    s.connect((ip, int(port)))
    print("Conexão envio [OK]")

    a = ""
    while a != "fim":
        a = input()
        print()
        s.send(a.encode())
    sys.exit()


def aguardar(tempo):
    print("Aguardando")
    for i in range(int(tempo)):
        print(i + 1)
        time.sleep(1)


def main():
    args = sys.argv[1:]
    L_PORT = args[0]
    L_IP = "0.0.0.0"  # NÃO MUDA
    print(f"Ouvindo em {L_IP} {L_PORT}")

    S_PORT = args[1]
    S_IP = "191.52.82.222"  # IP DO OUTRO USUÁRIO
    print(f"Enviando para {S_IP} {S_PORT}")

    thread_ouvir = threading.Thread(target=ouvir, args=(L_IP, L_PORT), daemon=True)
    thread_enviar = threading.Thread(target=enviar, args=(S_IP, S_PORT), daemon=True)

    thread_ouvir.start()
    aguardar(5)
    thread_enviar.start()

    thread_ouvir.join()
    thread_enviar.join()


if __name__ == "__main__":
    main()
    print("Programa encerrado...")
