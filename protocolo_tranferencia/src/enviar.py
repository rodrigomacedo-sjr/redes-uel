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

    for seq in range(1, TOTAL + 1):
        # Garante que o payload não exceda o tamanho total do pacote
        payload_size = tamanho - MAIN_HEADER_SIZE - HASH_SIZE - 4  # 4 bytes para o seq
        if payload_size < 0:
            payload_size = 0
        payload = os.urandom(payload_size)

        # Monta o pacote sem o checksum
        dados_sem_checksum = (
            seq.to_bytes(4, "big") + MAIN_HEADER.encode("utf-8") + payload
        )

        # Calcula o checksum dos dados
        checksum = utils.calcula_checksum(dados_sem_checksum)

        # Anexa o checksum ao final para formar o pacote completo
        dados_para_envio = dados_sem_checksum + checksum.encode("utf-8")

        sock.sendto(dados_para_envio, destino)

    sock.close()

    return TOTAL
