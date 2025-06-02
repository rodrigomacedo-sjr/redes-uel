import socket

from src.protocolo_tranferencia.config import MAIN_HEADER

DESTINO = (ip_destino, porta_destino)

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
    dados = encode(MAIN_HEADER)
    sock.sendto(dados, DESTINO)
    print("enviando...")
