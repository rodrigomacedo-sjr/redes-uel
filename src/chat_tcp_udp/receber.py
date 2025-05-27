from utils import criar_socket, enviar_ack_udp


def receber_pacotes(ip, porta, protocolo, total):
    sock = criar_socket(protocolo)
    recebidos = set()

    if protocolo.lower() == "tcp":
        sock.bind((ip, porta))
        sock.listen(1)
        conn, _ = sock.accept()
        recv_sock = conn
    else:
        sock.bind((ip, porta))
        recv_sock = sock

    while len(recebidos) < total:
        data, addr = (
            recv_sock.recvfrom(54)
            if protocolo.lower() == "udp"
            else (recv_sock.recv(54), None)
        )
        seq = int.from_bytes(data[:4], "big")
        recebidos.add(seq)
        if protocolo.lower() == "udp":
            enviar_ack_udp(sock, addr, seq)

    sock.close()
    return len(recebidos)
