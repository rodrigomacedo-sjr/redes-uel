import socket
from config import TIMEOUT


def criar_socket(protocolo):
    """
    Cria e retorna um objeto socket com base no protocolo especificado.

    Args:
        protocolo: "tcp" ou "udp".

    Retorna:
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

    Retorna:
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


def formatar_numero(numero, casas_decimais=2):
    """
    Formata número com pontos como separadores de milhares e vírgula para decimais
    Exemplo: 1234567.89 -> "1.234.567,89"
    """
    # Arredonda o número para o número especificado de casas decimais
    numero_arredondado = round(numero, casas_decimais)

    # Separa parte inteira e decimal
    if casas_decimais > 0:
        parte_inteira = int(numero_arredondado)
        parte_decimal = numero_arredondado - parte_inteira
        parte_decimal_str = f"{parte_decimal:.{casas_decimais}f}"[2:]  # Remove "0."
    else:
        parte_inteira = int(numero_arredondado)
        parte_decimal_str = ""

    # Formata parte inteira com pontos como separadores de milhares
    parte_inteira_str = f"{parte_inteira:,}".replace(",", ".")

    # Junta parte inteira e decimal
    if casas_decimais > 0:
        return f"{parte_inteira_str},{parte_decimal_str}"
    else:
        return parte_inteira_str


def formatar_velocidades(velocidades_dict, casas_decimais=2):
    """
    Formata o dicionário de velocidades com formatação brasileira
    """
    velocidades_formatadas = {}
    for unidade, valor in velocidades_dict.items():
        velocidades_formatadas[unidade] = formatar_numero(valor, casas_decimais)
    return velocidades_formatadas
