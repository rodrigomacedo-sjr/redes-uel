import socket
import utils
from config import HASH_SIZE


def receber_pacotes(ip, porta, total, tamanho):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((ip, porta))
    sock.settimeout(5.0)  # Adiciona um timeout de 5s para não travar para sempre

    recebidos = set()
    corrompidos = 0
    desordenados = 0
    maior_seq_recebido = 0

    while len(recebidos) < total:
        try:
            data, _ = sock.recvfrom(tamanho)
        except socket.timeout:
            print("Timeout: Nenhum pacote recebido. Encerrando receptor.")
            break

        # 1. Verificar checksum
        dados_pacote = data[:-HASH_SIZE]
        checksum_recebido = data[-HASH_SIZE:].decode("utf-8")

        if not utils.checksum(checksum_recebido, dados_pacote):
            corrompidos += 1
            continue  # Pula para o próximo pacote se estiver corrompido

        # 2. Extrair número de sequência
        seq = int.from_bytes(dados_pacote[:4], "big")

        # 3. Adicionar aos recebidos (se não estiver corrompido)
        recebidos.add(seq)

        # 4. Verificar se está fora de ordem
        # Um pacote está fora de ordem se sua sequência for menor que a maior já vista.
        if seq < maior_seq_recebido:
            desordenados += 1
        else:
            maior_seq_recebido = seq

    sock.close()
    return len(recebidos), desordenados, corrompidos
