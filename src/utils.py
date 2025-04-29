import socket
import time

TIMEOUT = 1.0       # segundos de espera por ACK no UDP
MAX_TENTATIVAS = 5  # tentativas máximas de retransmissão

def criar_socket(protocolo):
    if protocolo.lower() == 'tcp':
        return socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    else:
        return socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def aguardar_ack_udp(sock):
    sock.settimeout(TIMEOUT)
    try:
        data, _ = sock.recvfrom(8)
        return data.decode().startswith('ACK')
    except socket.timeout:
        return False

def enviar_ack_udp(sock, endereco, seq):
    mensagem = f'ACK{seq}'.encode()
    sock.sendto(mensagem, endereco)

