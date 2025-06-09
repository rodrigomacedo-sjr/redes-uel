import socket       # Importa o módulo socket, fundamental para comunicação em rede.

TIMEOUT = 1.0       # Define uma constante para o tempo de espera (em segundos) por um ACK no protocolo UDP.
                    # Se um ACK não for recebido dentro deste tempo, a tentativa é considerada falha (timeout).
MAX_TENTATIVAS = 5  # Define uma constante para o número máximo de vezes que o remetente tentará
                    # reenviar um pacote UDP caso não receba um ACK.

def criar_socket(protocolo):
    """
    Cria e retorna um objeto socket com base no protocolo especificado.

    Args:
        protocolo (str): "tcp" ou "udp".

    Returns:
        socket.socket: O objeto socket criado.
    """
    if protocolo.lower() == "tcp":
        # Se o protocolo for TCP:
        # socket.AF_INET: Indica que será usada a família de endereços IPv4.
        # socket.SOCK_STREAM: Indica que será um socket orientado à conexão (TCP).
        return socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    else:
        # Caso contrário (assume-se UDP ou qualquer outro valor não "tcp"):
        # socket.SOCK_DGRAM: Indica que será um socket para datagramas (UDP).
        return socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


def aguardar_ack_udp(sock):
    """
    Aguarda o recebimento de uma mensagem de ACK (confirmação) em um socket UDP.

    Args:
        sock (socket.socket): O socket UDP no qual se espera o ACK.

    Returns:
        bool: True se um ACK for recebido dentro do TIMEOUT, False caso contrário.
    """
    sock.settimeout(TIMEOUT)  # Configura o socket para não bloquear indefinidamente.
                              # Se nenhuma mensagem for recebida em 'TIMEOUT' segundos, uma exceção socket.timeout será levantada.
    try:
        data, _ = sock.recvfrom(8)  # Tenta receber dados do socket.
                                    # '8' é o tamanho máximo do buffer para o ACK (ex: "ACK" + número de sequência).
                                    # '_' é usado para ignorar o endereço do remetente do ACK, pois só o dado importa aqui.
        # Verifica se a mensagem recebida (decodificada para string) começa com "ACK".
        # Isso confirma que a mensagem é de fato uma confirmação.
        return data.decode().startswith("ACK")
    except socket.timeout:
        # Se o tempo de espera (TIMEOUT) for excedido sem receber dados.
        return False
    except Exception:
        # Captura outras possíveis exceções durante o recvfrom ou decode (ex: erro de decodificação)
        # e considera como falha no recebimento do ACK.
        return False


def enviar_ack_udp(sock, endereco, seq):
    """
    Envia uma mensagem de ACK (confirmação) via UDP para um endereço específico.

    Args:
        sock (socket.socket): O socket UDP a ser usado para enviar o ACK.
        endereco (tuple): Uma tupla (ip, porta) do destino para onde o ACK será enviado.
        seq (int): O número de sequência do pacote que está sendo confirmado.
                   Isso permite que o remetente original saiba qual pacote foi confirmado.
    """
    mensagem = f"ACK{seq}".encode()     # Cria a mensagem de ACK, por exemplo, "ACK1", "ACK2", etc.
                                        # '.encode()' converte a string para bytes, que é o formato necessário para envio via socket.
    sock.sendto(mensagem, endereco)     # Envia a mensagem de ACK para o 'endereco' especificado.