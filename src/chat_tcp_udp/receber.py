from utils import criar_socket, enviar_ack_udp  # Importa funções do módulo 'utils':
                                                # - criar_socket: Para criar o socket do servidor.
                                                # - enviar_ack_udp: Para enviar ACKs quando usar UDP.

def receber_pacotes(ip, porta, protocolo, total):
    """
    Recebe uma quantidade 'total' de pacotes únicos no 'ip' e 'porta' especificados,
    usando o 'protocolo' (TCP ou UDP).

    Retorna o número de pacotes únicos recebidos.
    """
    sock = criar_socket(protocolo)  # Cria o socket com base no protocolo fornecido (TCP ou UDP).
    recebidos = set()               # Utiliza um conjunto (set) para armazenar os números de sequência dos pacotes recebidos.
                                    # Usar um conjunto garante que apenas números de sequência únicos sejam contados,
                                    # tratando automaticamente pacotes duplicados.

    if protocolo.lower() == "tcp":
        sock.bind((ip, porta))      # Associa o socket ao endereço IP e porta especificados.
        sock.listen(1)              # Coloca o socket em modo de escuta, aguardando conexões TCP.
                                    # O '1' indica o número máximo de conexões pendentes na fila.
        print(f"Servidor TCP escutando em {ip}:{porta}")
        conn, _ = sock.accept()     # Aceita uma conexão TCP de um cliente.
                                    # 'conn' é um novo objeto socket usado para comunicar-se com este cliente específico.
                                    # '_' armazena o endereço do cliente, que não é usado diretamente aqui após a conexão.
        recv_sock = conn            # O socket para receber dados será o socket da conexão ('conn').
    else:  # Protocolo UDP
        sock.bind((ip, porta))      # Associa o socket UDP ao endereço IP e porta.
        print(f"Servidor UDP escutando em {ip}:{porta}")
        recv_sock = sock            # Em UDP, o mesmo socket é usado para escutar e receber dados de qualquer remetente.

    print(f"Aguardando {total} pacotes...")
    while len(recebidos) < total:  # Continua recebendo até que o número de pacotes únicos esperados ('total') seja alcançado.
        try:
            if protocolo.lower() == "udp":
                # Para UDP, recebe dados e o endereço do remetente.
                # 54 bytes = 4 bytes para o número de sequência + 50 bytes de payload (conforme o script de envio).
                data, addr = recv_sock.recvfrom(54)
            else:  # Protocolo TCP
                # Para TCP, recebe dados do socket de conexão. O endereço já é conhecido pela conexão.
                data = recv_sock.recv(54)
                addr = None  # Não há um 'addr' por pacote em TCP após a conexão estabelecida.

            if not data: # Se recv retorna dados vazios, a conexão pode ter sido fechada (comum em TCP)
                print("Conexão fechada pelo cliente (TCP) ou pacote vazio recebido.")
                break # Sai do loop se a conexão for encerrada ou não houver mais dados.

            # Extrai o número de sequência dos primeiros 4 bytes dos dados recebidos.
            # 'big' indica a ordem dos bytes (big-endian).
            seq = int.from_bytes(data[:4], "big")
            recebidos.add(seq)  # Adiciona o número de sequência ao conjunto de pacotes recebidos.
                                # Se 'seq' já estiver no conjunto, nada acontece (propriedade do set).

            if protocolo.lower() == "udp":
                # Se for UDP, envia um ACK de volta para o remetente ('addr')
                # confirmando o recebimento do pacote com número de sequência 'seq'.
                enviar_ack_udp(sock, addr, seq)

            # Opcional: Imprimir progresso
            # print(f"Recebido pacote {seq}. Total únicos: {len(recebidos)}/{total}")

        except ConnectionResetError:
            print("Conexão TCP resetada pelo cliente.")
            break
        except Exception as e:
            print(f"Erro ao receber pacote: {e}")
            # Dependendo do erro, pode-se querer continuar ou parar.
            # Para robustez, pode ser útil tratar erros específicos de socket.
            break


    print(f"Recebimento concluído. Total de pacotes únicos recebidos: {len(recebidos)}.")
    if protocolo.lower() == "tcp" and 'conn' in locals(): # Garante que conn foi definido
        conn.close() # Fecha o socket da conexão com o cliente específico em TCP.
    sock.close()  # Fecha o socket principal de escuta (para TCP) ou o socket de dados (para UDP).

    return len(recebidos)  # Retorna a contagem de pacotes únicos recebidos.