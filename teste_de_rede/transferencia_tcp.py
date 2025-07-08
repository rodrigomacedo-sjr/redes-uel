import os
from utils import criar_socket
from config import DURACAO_SEGUNDOS, STRING_TESTE, TAMANHO_BYTES
import time


def enviar_pacotes(destinatario: tuple):
    """
    Envia pacotes para o destinatário usando TCP por um tempo determinado

<<<<<<< HEAD
    Argumentos:
        destinatario (tuple): ip, port
=======
    Cada pacote tem 500 bytes e contém a string "teste de rede *2025*"
>>>>>>> prs-develop

    Retorna:
        Um dicionário com estatísticas da transmissão
    """
    sock = criar_socket("TCP")
    retransmissoes = 0
    perdidos = 0

    try:
        print(f"Conectando em {destinatario[0]}:{destinatario[1]}...")
        sock.connect(destinatario)
        print(f"Conectado! Iniciando envio de pacotes...")
    except Exception as e:
        print(f"Erro na conexão: {e}")
        return None

    pacotes_enviados = 0

    inicio = time.perf_counter()

    while (time.perf_counter() - inicio) < DURACAO_SEGUNDOS:
        pacotes_enviados += 1

        sequecia_bytes = pacotes_enviados.to_bytes(4, "big")
        string_bytes = STRING_TESTE.encode()
        tamanho_payload = TAMANHO_BYTES - len(sequecia_bytes) - len(string_bytes)
        payload = os.urandom(tamanho_payload)
        dados = sequecia_bytes + string_bytes + payload

        try:
            sock.sendall(dados)
        except Exception as e:
            print(f"Erro ao enviar dados: {e}")
            break

    duracao = time.perf_counter() - inicio
    dados_envio = f"{pacotes_enviados}, {retransmissoes}, {perdidos}, {duracao},"

    try:
        sock.sendall(b"FIM")
        time.sleep(0.1)
        print(f"Enviando estatisticas de envio...")
        sock.sendall(dados_envio.encode())
    except Exception as e:
        print(f"Erro ao finalizar: {e}")

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

    Argumentos:
        remetente (tuple): ip, port

    Retorna:
        Um dicionário com as estatísticas da recepção
    """
    sock = criar_socket("TCP")
    sock.bind(remetente)
    sock.listen(1)
    print(f"Servidor TCP escutando em {remetente[0]}:{remetente[1]}")

    conn, addr = sock.accept()
    print(f"Conexão aceita de {addr[0]}:{addr[1]}")

    try:
        recebidos = set()
        stats = []

        # Lógica de buffer para lidar com TCP
        # Garante que pacotes sejam processados corretamente, mesmo em pedaços
        buffer = b""
        stats_bruto = b""
        fim_recebido = False

        print(f"Aguardando pacotes...")
        while not fim_recebido:
            # 1. Processa o que já está no buffer
            while len(buffer) >= TAMANHO_BYTES:
                pacote = buffer[:TAMANHO_BYTES]
                buffer = buffer[TAMANHO_BYTES:]

                seq = int.from_bytes(pacote[:4], "big")
                recebidos.add(seq)

            # 2. Lê mais dados da rede
            dados = conn.recv(4096)  # Lê em chunks maiores para eficiência
            if not dados:
                print("Conexão fechada inesperadamente.")
                break

            buffer += dados

            # 3. Verifica se o sinal de FIM chegou
            if b"FIM" in buffer:
                print("Sinal de finalização recebido")
                # Separa o que veio antes do FIM do que veio depois (as estatísticas)
                partes = buffer.split(b"FIM", 1)
                buffer = partes[0]  # Processa o resto dos pacotes
                stats_bruto = partes[1]
                fim_recebido = True

        # Processa qualquer pacote restante que ficou no buffer antes do "FIM"
        while len(buffer) >= TAMANHO_BYTES:
            pacote = buffer[:TAMANHO_BYTES]
            buffer = buffer[TAMANHO_BYTES:]
            seq = int.from_bytes(pacote[:4], "big")
            recebidos.add(seq)

        stats_bruto += conn.recv(1024)
        stats_decodificado = stats_bruto.strip().decode()
        if stats_decodificado:
            stats = stats_decodificado.split(",")

    except Exception as e:
        print(f"Ocorreu um erro durante a recepção: {e}")
    finally:
        if "conn" in locals():
            conn.close()
        sock.close()
        print("Conexão fechada.")

    if len(stats) >= 2:
        enviados = int(stats[0])
        tempo = float(stats[1])
        perdidos = enviados - len(recebidos)
    else:
        print(
            "Erro no recebimento das estatísticas ou conexão encerrada prematuramente."
        )
        enviados = 0
        tempo = 0
        perdidos = 0

    return {
        "quantidade_recebidos": len(recebidos),
        "quantidade_enviados": enviados,
        "retransmissoes": 0,  # Métrica não calculada aqui
        "perdidos": perdidos,
        "tempo": tempo,
    }
