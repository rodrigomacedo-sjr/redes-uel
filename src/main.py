import socket
import threading
import time
import sys
from threading import Thread

def ouvir(ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    s.bind((ip, int(port)))

    print("Ouvindo por conexão...")
    s.listen()

    conn, addr = s.accept()
    print("Conectei (recebimento)...")

    a = ""
    while a != "fim":
        a = conn.recv(1024)
        print(f"Recebido: {a.decode()}\n")
    sys.exit()


def enviar(ip, port):
    s = socket.socket(
        socket.AF_INET, socket.SOCK_STREAM 
    )

    s.connect((ip, int(port))) 
    print("Conectei (envio)...")

    a = "x"
    while a != "fim":
        a = input()
        print()
        s.send(a.encode()) 
    sys.exit()


def main():
    args = sys.argv[1:]
    print(f"args = {args}")
    L_PORT = args[0]
    # L_IP = args[x]
    L_IP = "0.0.0.0"
    print(f"listening on {L_IP} {L_PORT}")

    S_PORT = args[1]
    # S_IP = args[y]
    S_IP = "10.90.69.80" # colocar o ip da outra pessoa aqui
    print(f"sending to {S_IP} {S_PORT}")

    listen_thread = threading.Thread(target=ouvir, args=(L_IP, L_PORT), daemon=True)
    send_thread = threading.Thread(target=enviar, args=(S_IP, S_PORT), daemon=True)
    listen_thread.start()
    print("Waiting")
    for i in range(5):
        print(i+1)
        time.sleep(1)
    send_thread.start()
    listen_thread.join()
    send_thread.join()


if __name__ == "__main__":
    main()
    print("Programa encerrado...")
