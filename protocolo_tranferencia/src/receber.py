import socket


def receber_pacotes(ip, porta, total, tamanho):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((ip, porta))

    recebidos = set()
    corrompidos = 0
    desordenados = 0

    for i in range(total):
        data, _ = sock.recvfrom(tamanho)
        seq = int.from_bytes(data[:4], "big")
        recebidos.add(seq)

        if seq != i:  # Recebido fora de ordem
            desordenados += 1
            i = seq  # Corrige o "esperado" para não flagar os próximos pacotes

    sock.close()
    return len(recebidos), desordenados, corrompidos
