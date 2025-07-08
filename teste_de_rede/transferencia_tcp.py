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
    sock = criar_socket("TCP")
    recebidos = set()
    sock.bind(remetente)
    sock.listen(1)
    print(f"Servidor TCP escutando em {remetente[0]}:{remetente[1]}")
    conn, addr = sock.accept()
    print(f"Conexão aceita de {addr}")

    dados_finais = []
    while True:
        try:
            # 1. Usar conn.recv() que é o correto para TCP
            data = conn.recv(500)

            # 2. Se recv retornar vazio, o cliente desconectou
            if not data:
                print("Cliente desconectou.")
                break

            # 3. Verificar se é a mensagem de controle "FIM"
            if data == "FIM":
                print("Recebido sinal de FIM. Aguardando estatísticas...")
                # Recebe o próximo pacote que deve conter as estatísticas
                stats_data = conn.recv(500)
                dados_finais = stats_data.decode("utf-8").split(",")
                break  # Sai do loop principal após receber as estatísticas

            # Se não for FIM, é um pacote de dados normal
            seq = int.from_bytes(data[:4], "big")
            recebidos.add(seq)
            # 4. Não precisa enviar ACK manual em TCP

        except Exception as e:
            print(f"Erro durante a recepção: {e}")
            break

    conn.close()
    sock.close()

    # Proteção contra o IndexError caso algo dê errado
    if len(dados_finais) < 4:
        dados_finais = [0, 0, 0, 0.0]

    return {
        "quantidade_recebidos": len(recebidos),
        "quantidade_enviados": int(dados_finais[0]),
        "retransmissoes": int(dados_finais[1]),
        "perdidos": int(dados_finais[2]),
        "tempo": float(dados_finais[3]),
    }