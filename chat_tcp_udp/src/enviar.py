import os                                                           # Usado para gerar dados aleatórios (payload).
import time                                                         # Usado para medir o tempo de envio dos pacotes.
from utils import criar_socket, aguardar_ack_udp, MAX_TENTATIVAS    # Importa funções e constantes de um módulo local 'utils'.
                                                                    # - criar_socket: Cria um socket TCP ou UDP.
                                                                    # - aguardar_ack_udp: Espera por uma confirmação (ACK) em UDP.
                                                                    # - MAX_TENTATIVAS: Número máximo de tentativas de envio para um pacote UDP.

def enviar_pacotes(ip, porta, protocolo, total):
    """
    Envia uma quantidade 'total' de pacotes para o 'ip' e 'porta' especificados,
    usando o 'protocolo' (TCP ou UDP).

    Retorna um dicionário com estatísticas da transmissão.
    """
    sock = criar_socket(protocolo)      # Cria o socket com base no protocolo fornecido.
    retransmissoes = 0                  # Contador para o número de vezes que pacotes foram reenviados.
    perdidos = 0                        # Contador para o número de pacotes que não foram confirmados (ACK)
                                        # após todas as tentativas (relevante para UDP).

    if protocolo.lower() == "tcp":
        sock.connect((ip, porta))       # Se for TCP, estabelece a conexão com o servidor.
    else: # Protocolo UDP
                                        # Se for UDP, o bind é feito em uma porta local aleatória ("", 0)
                                        # para poder receber os ACKs. O envio dos dados será para o (ip, porta) de destino.
        sock.bind(("", 0))

    inicio = time.perf_counter()        # Marca o tempo de início do envio.

    for seq in range(1, total + 1):     # Loop para enviar cada um dos 'total' pacotes.
        payload = os.urandom(50)        # Gera 50 bytes de dados aleatórios como carga útil.
        dados = seq.to_bytes(4, "big") + payload  # Constrói o pacote:
                                                                    # - Número de sequência (seq) convertido para 4 bytes (big-endian).
                                                                    # - Seguido pelo payload.
        tent = 0        # Contador de tentativas para o pacote atual.
        ack_ok = False  # Flag para indicar se o ACK do pacote atual foi recebido.

        while tent < MAX_TENTATIVAS and not ack_ok:  # Tenta enviar o pacote até MAX_TENTATIVAS ou até receber ACK.
            if protocolo.lower() == "tcp":
                sock.send(dados)    # Em TCP, envia os dados.
                ack_ok = True       # Assume que o 'send' do TCP é confiável e o ACK é gerenciado pelo próprio protocolo.
                                    # Esta é uma simplificação; o TCP garante a entrega, mas um ACK a nível de aplicação
                                    # não está sendo esperado explicitamente aqui. O sistema confia no TCP.
            else:  # Protocolo UDP
                sock.sendto(dados, (ip, porta))     # Envia os dados para o endereço de destino.
                ack_ok = aguardar_ack_udp(sock)     # Espera por uma confirmação (ACK) do receptor.
                                                    # A função 'aguardar_ack_udp' (do módulo utils) deve ter um timeout.
            if not ack_ok:  # Se o ACK não foi recebido (relevante principalmente para UDP).
                tent += 1  # Incrementa o contador de tentativas para este pacote.
                retransmissoes += 1  # Incrementa o contador global de retransmissões.

        if not ack_ok:  # Se, após todas as tentativas, o ACK não foi recebido (para UDP).
            perdidos += 1  # Incrementa o contador de pacotes perdidos.

    fim = time.perf_counter()  # Marca o tempo de fim do envio.
    sock.close()  # Fecha o socket.

    return {  # Retorna um dicionário com as estatísticas da transmissão.
        "enviados": total,  # Número total de pacotes que se tentou enviar (corresponde ao 'total' solicitado).
        "retransmissoes": retransmissoes,  # Total de retransmissões ocorridas (principalmente para UDP).
        "perdidos": perdidos,  # Total de pacotes considerados perdidos (principalmente para UDP).
        "tempo": fim - inicio,  # Tempo total decorrido para o envio de todos os pacotes.
    }