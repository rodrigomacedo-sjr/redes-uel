import os
from utils import criar_socket, aguardar_ack_udp, enviar_ack_udp
from config import DURACAO_SEGUNDOS, MAX_TENTATIVAS, STRING_TESTE
import time


def enviar_pacotes(destinatario):
    """
    Envia uma quantidade 'total' de pacotes para o 'ip' e 'porta' especificados

    Cada pacote tem 500 butes e contém a string "teste de rede *2025*"

    Retorna um dicionário com estatísticas da transmissão

    destinatario - tupla de ip & porta
    """
    sock = criar_socket("UDP")
    retransmissoes = 0
    perdidos = 0

    sock.bind(("", 0))

    inicio = time.perf_counter()
    fim = time.perf_counter()
    duracao = fim - inicio

    pacotes_enviados = 0
    while duracao < DURACAO_SEGUNDOS:
        pacotes_enviados += 1

        payload = os.urandom(500 - len(STRING_TESTE) - 2)
        dados = pacotes_enviados.to_bytes(4, "big") + STRING_TESTE.encode() + payload
        tentativas_reenvio = 0
        ack_recebido = False

        while tentativas_reenvio < MAX_TENTATIVAS and not ack_recebido:
            sock.sendto(dados, destinatario)
            ack_recebido = aguardar_ack_udp(sock)
            if not ack_recebido:
                tentativas_reenvio += 1
                retransmissoes += 1

        duracao = fim - inicio

        if not ack_recebido:
            perdidos += 1

    dados_envio = """
    {pacotes_enviados},
    {retransmissoes},
    {perdidos},
    {tempo},
    """.format(
        pacotes_enviados, retransmissoes, perdidos, duracao
    )
    ack_recebido = False
    while not ack_recebido:
        sock.sendto("FIM".encode(), destinatario)
        ack_recebido = aguardar_ack_udp(sock)
        sock.sendto(dados_envio.encode(), destinatario)
        ack_recebido = aguardar_ack_udp(sock)

    sock.close()

    return {
        "quantidade_enviados": pacotes_enviados,
        "retransmissoes": retransmissoes,
        "perdidos": perdidos,
        "tempo": duracao,
    }


def receber_pacotes(remetente):
    """
    Recebe pacotes do remetente até receber um "FIM"

    Retorna o número de pacotes únicos recebidos
    """
    sock = criar_socket("UDP")
    recebidos = set()

    sock.bind(remetente)
    print(f"Servidor UDP escutando em {remetente[0]}:{remetente[1]}")
    recv_sock = sock

    print(f"Aguardando pacotes...")
    dados = ""
    while True:
        try:
            data, addr = recv_sock.recvfrom(500)

            seq = int.from_bytes(data[:4], "big")
            recebidos.add(seq)

            enviar_ack_udp(sock, addr, seq)

            if data.decode("utf-8") == "FIM":
                data, addr = recv_sock.recvfrom(500)

            dados = data.decode("utf-8").split(",")

        except Exception as e:
            print(f"Erro ao receber pacote: {e}")
            break

    sock.close()

    return {
        "quantidade_recebidos": len(recebidos),
        "quantidade_enviados": dados[0] or 0,
        "retransmissoes": dados[1] or 0,
        "perdidos": dados[2] or 0,
        "tempo": dados[3] or 0,
    }
