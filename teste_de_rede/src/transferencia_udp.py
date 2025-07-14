import os
from utils import criar_socket, aguardar_ack_udp, enviar_ack_udp
from config import DURACAO_SEGUNDOS, MAX_TENTATIVAS, STRING_TESTE
import time


def enviar_pacotes(destinatario: tuple):
    """
    Envia pacotes para o destinatário usando UDP por um tempo determinado,
    com controle de retransmissão.

    Argumentos:
        destinatario (tuple): ip, port

    Retorna:
        Um dicionário com estatísticas da transmissão
    """
    sock = criar_socket("UDP")
    sock.bind(("", 0))
    sock.settimeout(1.0)  # Timeout para operações UDP

    retransmissoes = 0
    perdidos = 0
    pacotes_enviados = 0

    print("Iniciando envio de pacotes...")

    inicio = time.perf_counter()
    tempo_limite = inicio + DURACAO_SEGUNDOS
    
    while time.perf_counter() < tempo_limite:
        pacotes_enviados += 1

        header_size = 4 + len(STRING_TESTE.encode())
        payload_size = 500 - header_size

        payload = os.urandom(payload_size)
        dados = pacotes_enviados.to_bytes(4, "big") + STRING_TESTE.encode() + payload

        # Lógica e ACK
        ack_recebido = False
        tentativas_reenvio = 0
        while tentativas_reenvio < MAX_TENTATIVAS and not ack_recebido:
            sock.sendto(dados, destinatario)
            ack_recebido = aguardar_ack_udp(sock)
            if not ack_recebido:
                tentativas_reenvio += 1
                if tentativas_reenvio < MAX_TENTATIVAS:
                    retransmissoes += 1

        if not ack_recebido:
            print(
                f"Pacote {pacotes_enviados} perdido depois de {MAX_TENTATIVAS} tentativas."
            )
            perdidos += 1

    fim_envio = time.perf_counter()
    duracao = fim_envio - inicio
    print("Tempo esgotado. Enviando sinal de finalização...")

    # Lógica de "FIM"
    ack_recebido = False
    tentativas_reenvio = 0
    while tentativas_reenvio < MAX_TENTATIVAS and not ack_recebido:
        sock.sendto(b"FIM", destinatario)
        ack_recebido = aguardar_ack_udp(sock)
        if not ack_recebido:
            tentativas_reenvio += 1
            if tentativas_reenvio < MAX_TENTATIVAS:
                retransmissoes += 1

    # ACK para envio de estatísticas
    dados_envio = f"{pacotes_enviados},{retransmissoes},{perdidos},{duracao}".encode()
    ack_recebido = False
    tentativas_reenvio = 0
    while tentativas_reenvio < MAX_TENTATIVAS and not ack_recebido:
        sock.sendto(dados_envio, destinatario)
        ack_recebido = aguardar_ack_udp(sock)
        if not ack_recebido:
            tentativas_reenvio += 1
            if tentativas_reenvio < MAX_TENTATIVAS:
                retransmissoes += 1

    sock.close()
    print("Conexão fechada.")

    return {
        "quantidade_enviados": pacotes_enviados,
        "retransmissoes": retransmissoes,
        "perdidos": perdidos,
        "tempo": duracao,
    }


def receber_pacotes(remetente: tuple):
    """
    Recebe pacotes do remetente até receber um "FIM"

    Retorna um dicionário com as estatísticas da recepção
    """
    sock = criar_socket("UDP")
    sock.settimeout(30.0)  # Timeout para recepção UDP
    
    try:
        sock.bind(remetente)
        print(f"Servidor UDP escutando em {remetente[0]}:{remetente[1]}")
    except OSError as e:
        print(f"Erro ao fazer bind na porta {remetente[1]}: {e}")
        sock.close()
        return None

    recebidos = set()
    stats_final_bytes = b""

    print("Aguardando pacotes...")
    inicio_recepcao = time.perf_counter()  # Marca o início da recepção
    
    while True:
        try:
            data, addr = sock.recvfrom(1024)

            if data == b"FIM":
                print("Sinal de FIM recebido.")
                enviar_ack_udp(sock, addr, 0)
                break

            try:
                seq = int.from_bytes(data[:4], "big")
                recebidos.add(seq)
                enviar_ack_udp(sock, addr, seq)

            except (ValueError, IndexError):
                print("Enviando ACK e finalizando.")
                stats_final_bytes = data
                enviar_ack_udp(sock, addr, 0)
                break

        except Exception as e:
            print(f"Erro ao receber pacote: {e}")
            break

    if not stats_final_bytes:
        print("Aguardando estatísticas finais...")
        try:
            stats_final_bytes, addr = sock.recvfrom(1024)
            enviar_ack_udp(sock, addr, 0)
        except Exception as e:
            print(f"Erro ao receber estatísticas: {e}")

    fim_recepcao = time.perf_counter()  # Marca o fim da recepção
    tempo_recepcao = fim_recepcao - inicio_recepcao  # Calcula o tempo total de recepção

    sock.close()
    print("Conexão fechada.")

    stats_final = {}
    if stats_final_bytes:
        try:
            stats_str = stats_final_bytes.decode()
            dados = stats_str.split(",")
            if len(dados) >= 4:
                stats_final = {
                    "quantidade_enviados": int(dados[0]),
                    "retransmissoes": int(dados[1]),
                    "perdidos_remetente": int(dados[2]),
                    "tempo": float(dados[3]),
                }
            else:
                raise ValueError("Formato de estatísticas inválido")
        except (ValueError, IndexError, UnicodeDecodeError) as e:
            print(f"Erro ao decodificar estatísticas: {e}")
            stats_final = {}

    perdidos_receptor = stats_final.get("quantidade_enviados", 0) - len(recebidos)

    return {
        "quantidade_recebidos": len(recebidos),
        "quantidade_enviados": stats_final.get("quantidade_enviados", 0),
        "retransmissoes_remetente": stats_final.get("retransmissoes", 0),
        "perdidos": perdidos_receptor,
        "tempo": tempo_recepcao,  
        "tempo_envio": stats_final.get("tempo", 0), 
    }
