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
    sock = criar_socket("TCP")
    retransmissoes = 0
    perdidos = 0

    sock.connect(destinatario)

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
            sock.send(dados)
            ack_recebido = True
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
        sock.send("FIM".encode())
        sock.send(dados_envio.encode())

    sock.close()

    return {
        "quantidade_enviados": pacotes_enviados,
        "retransmissoes": retransmissoes,
        "perdidos": perdidos,
        "tempo": duracao,
    }


def receber_pacotes(remetente: tuple):
    """
    Recebe pacotes do remetente até receber um "FIM"

    Retorna o número de pacotes únicos recebidos
    """
    sock = criar_socket("TCP")
    recebidos = set()


    sock.bind(remetente)
    sock.listen(1)
    print(f"Servidor TCP escutando em {remetente[0]}:{remetente[1]}")
    conn, _ = sock.accept()
    recv_sock = conn

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

    if 'conn' in locals():
        conn.close()
    sock.close()

    return {
        "quantidade_recebidos": len(recebidos),
        "quantidade_enviados": dados[0] or 0,
        "retransmissoes": dados[1] or 0,
        "perdidos": dados[2] or 0,
        "tempo": dados[3] or 0,
    }
