import socket
import os
import utils

from config import HASH_SIZE, MAIN_HEADER, MAIN_HEADER_SIZE, TOTAL


def enviar_pacotes(destino, tamanho):
    """
    Parâmetros:
        Destino: tupla de ip/porta de destino
        Tamanho: 500, 1000, 1500, tamanho dos dados a serem enviados
    """
    # Cria socket UDP
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    sock.bind(("", 0))

    for seq in range(1, TOTAL):
        payload = os.urandom(tamanho - MAIN_HEADER_SIZE - HASH_SIZE)
        dados = seq.to_bytes(4, "big") + MAIN_HEADER.encode("utf-8") + payload

        dados = dados + utils.calcula_checksum(dados).encode("utf-8")

        sock.sendto(dados, destino)

    sock.close()

    return TOTAL
