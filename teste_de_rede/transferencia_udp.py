import os
from utils import criar_socket
from config import MAX_TENTATIVAS
import time


def transferir_dados():
    """
    1. enviar string com tamanho único de 500 bytes contendo "teste de rede *2025*"
    2. inserir um contador de pacotes enviados
    """
    pass


def enviar_pacotes(ip, porta, total):
    """
    Envia uma quantidade 'total' de pacotes para o 'ip' e 'porta' especificados

    Retorna um dicionário com estatísticas da transmissão.
    """
    sock = criar_socket("UDP")
    retransmissoes = 0 
    perdidos = 0 

    sock.bind(("", 0))

    inicio = time.perf_counter()

    for seq in range(1, total + 1):  # Loop para enviar cada um dos 'total' pacotes.
        payload = os.urandom(50)  
        dados = seq.to_bytes(4, "big") + payload
        tentativas_reenvio = 0 
        ack_recebido = False 

        while (
            tentativas_reenvio < MAX_TENTATIVAS and not ack_recebido
        ):  # Tenta MAX_TENTATIVAS vezes até receber ACK.
            sock.sendto(dados, (ip, porta))
            ack_recebido = aguardar_ack_udp(sock) 
            if not ack_recebido:
                tentativas_reenvio += 1
                retransmissoes += 1

        if not ack_recebido:
            perdidos += 1

    fim = time.perf_counter()
    sock.close()

    return { 
        "quantidade_enviados": total,
        "retransmissoes": retransmissoes,  # Total de retransmissões ocorridas (principalmente para UDP).
        "perdidos": perdidos,  # Total de pacotes considerados perdidos (principalmente para UDP).
        "tempo": fim - inicio,
    }


def receber_dados():
    pass


def avaliar_taxa_de_transferencia():
    """
    (coletar)
    1. quantos pacotes enviados
    2. quantos pacotes perdidos
    3. quantos bytes enviados
    4. qual a velocidade em Giga/mega/kilo/bit por segundo (separar milhar por ponto)
    5. quantos pacotes por segundo
    """
    pass


"""
no final da comunicação
    enviar dados de recebimento para o enviador (ou durante (ack)) 
    enviar dados de envio para o recebedor
    para os dois computadores conseguirem fazer as estatisticas
"""
