import socket
from config import TIMEOUT


def criar_socket(protocolo):
    """
    Cria e retorna um objeto socket com base no protocolo especificado.

    Args:
        protocolo: "tcp" ou "udp".

    Returns:
        socket.socket: O objeto socket criado.
    """
    if protocolo.lower() == "tcp":
        return socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    else:
        return socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


def aguardar_ack_udp(sock):
    """
    Aguarda o recebimento de uma mensagem de ACK (confirmação) em um socket UDP

    Args:
        sock (socket.socket): O socket UDP no qual se espera o ACK.

    Returns:
        bool: True se um ACK for recebido dentro do TIMEOUT, False caso contrário.
    """
    sock.settimeout(TIMEOUT)

    try:
        data, _ = sock.recvfrom(8)
        return data.decode().startswith("ACK")
    except socket.timeout:
        return False
    except Exception:
        return False


def enviar_ack_udp(sock, endereco, seq):
    """
    Envia uma mensagem de ACK (confirmação) via UDP para um endereço específico.

    Args:
        sock (socket.socket): O socket UDP a ser usado para enviar o ACK
        endereco (tuple): Uma tupla (ip, porta) do destino para onde o ACK será enviado
        seq (int): O número de sequência do pacote que está sendo confirmado
    """
    mensagem = f"ACK{seq}".encode()

    sock.sendto(mensagem, endereco)
