import os
from utils import criar_socket, aguardar_ack_udp, enviar_ack_udp
from config import DURACAO_SEGUNDOS, MAX_TENTATIVAS, STRING_TESTE, TAMANHO_BYTES
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
    sock.settimeout(1.0)  # Tempo máximo de espera

    retransmissoes = 0
    perdidos = 0
    pacotes_enviados = 0

    print("Iniciando envio de pacotes...")

    inicio = time.perf_counter()
    tempo_limite = inicio + DURACAO_SEGUNDOS

    while time.perf_counter() < tempo_limite:
        pacotes_enviados += 1

        sequencia_bytes = pacotes_enviados.to_bytes(4, "big")
        string_bytes = STRING_TESTE.encode()
        tamanho_payload = TAMANHO_BYTES - len(sequencia_bytes) - len(string_bytes)
        payload = os.urandom(tamanho_payload)
        dados = sequencia_bytes + string_bytes + payload

        sock.sendto(dados, destinatario)

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
    sock.settimeout(30.0)  # Tempo máximo de espera

    try:
        sock.bind(remetente)
        print(f"Servidor UDP escutando em {remetente[0]}:{remetente[1]}")
    except Exception as e:
        print(f"Erro ao criar servidor para escuta: {e}")
        sock.close()
        return {}

    recebidos = set()
    stats_final_bytes = b""

    print("Aguardando pacotes...")
    fim_recepcao = 0
    inicio_recepcao = time.perf_counter()

    while True:
        try:
            data, addr = sock.recvfrom(1024)

            if data == b"FIM":
                print("Sinal de FIM recebido.")
                fim_recepcao = time.perf_counter()
                enviar_ack_udp(sock, addr, 0)
                break

            try:
                # É o pacote de estatísticas?
                data_str = data.decode("utf-8")

                # Válido
                if "," in data_str:
                    partes = data_str.split(",")
                    if len(partes) >= 4:
                        try:
                            # Converte formato
                            int(partes[0])  # pacotes
                            int(partes[1])  # retransmissões
                            int(partes[2])  # perdidos
                            float(partes[3])  # tempo

                            print("Estatísticas finais recebidas.")
                            stats_final_bytes = data
                            enviar_ack_udp(sock, addr, 0)
                            break
                        except Exception:
                            # Não é um pacote de estatísticas válido
                            pass

                # É um pacote normal
                seq = int.from_bytes(data[:4], "big")
                recebidos.add(seq)
                enviar_ack_udp(sock, addr, seq)
            except Exception:
                print("Pacote inválido recebido")

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

    tempo_recepcao = fim_recepcao - inicio_recepcao

    sock.close()
    print("Conexão fechada.")

    stats_final = {}
    if stats_final_bytes:
        try:
            stats_str = stats_final_bytes.decode("utf-8")

            if stats_str:
                dados = stats_str.split(",")
                if len(dados) >= 4:
                    stats_final = {
                        "quantidade_enviados": int(dados[0]),
                        "retransmissoes": int(dados[1]),
                        "perdidos_remetente": int(dados[2]),
                        "tempo": float(dados[3]),
                    }
                else:
                    print("Formato de estatísticas inválido")
                    raise Exception
        except Exception as e:
            print(f"Erro ao decodificar estatísticas: {e}")
            stats_final = {}

    perdidos_receptor = stats_final.get("quantidade_enviados", 0) - len(recebidos)

    # Garante que o tempo nunca seja zero para evitar divisão por zero
    tempo_recepcao_final = max(tempo_recepcao, 0.001)
    tempo_envio_final = max(stats_final.get("tempo", 0), 0.001)

    return {
        "quantidade_recebidos": len(recebidos),
        "quantidade_enviados": stats_final.get("quantidade_enviados", 0),
        "retransmissoes_remetente": stats_final.get("retransmissoes", 0),
        "perdidos": perdidos_receptor,
        "tempo": tempo_recepcao_final,
        "tempo_envio": tempo_envio_final,
    }
