import os
import time
from utils import criar_socket, aguardar_ack_udp, MAX_TENTATIVAS


def enviar_pacotes(ip, porta, protocolo, total):
    sock = criar_socket(protocolo)
    retransmissoes = 0
    perdidos = 0

    if protocolo.lower() == "tcp":
        sock.connect((ip, porta))
    else:
        sock.bind(("", 0))

    inicio = time.perf_counter()

    for seq in range(1, total + 1):
        payload = os.urandom(50)
        dados = seq.to_bytes(4, "big") + payload
        tent = 0
        ack_ok = False

        while tent < MAX_TENTATIVAS and not ack_ok:
            if protocolo.lower() == "tcp":
                sock.send(dados)
                ack_ok = True  # no TCP, confiamos no send
            else:
                sock.sendto(dados, (ip, porta))
                ack_ok = aguardar_ack_udp(sock)
            if not ack_ok:
                tent += 1
                retransmissoes += 1

        if not ack_ok:
            perdidos += 1

    fim = time.perf_counter()
    sock.close()

    return {
        "enviados": total,
        "retransmissoes": retransmissoes,
        "perdidos": perdidos,
        "tempo": fim - inicio,
    }
