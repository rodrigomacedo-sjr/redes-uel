import socket

def receber_pacotes(teste, ip, porta, total):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    recebidos = set()
    sock.bind((ip, porta))

    tamanhos_teste = [500, 1000, 1500]
    if(teste < 1 or teste > 3): return "Número de teste inválido."

    while len(recebidos) < total:
        data = (sock.recvfrom(tamanhos_teste[teste-1]))        
        seq = int.from_bytes(data[:4], "big")
        recebidos.add(seq)

    sock.close()
    return len(recebidos)
