import os
import socket
from utils import criar_socket
from config import DURACAO_SEGUNDOS, STRING_TESTE, TAMANHO_BYTES
import time


def enviar_pacotes(destinatario: tuple):
    """
    Envia pacotes para o destinatário usando TCP por um tempo determinado

    Argumentos:
        destinatario (tuple): ip, port

    Retorna:
        Um dicionário com estatísticas da transmissão
    """
    sock = criar_socket("TCP")
    sock.settimeout(30)  # Timeout de 30 segundos para conexão
    retransmissoes = 0
    perdidos = 0

    try:
        print(f"Conectando em {destinatario[0]}:{destinatario[1]}...")
        sock.connect(destinatario)
        print(f"Conectado! Iniciando envio de pacotes...")
    except Exception as e:
        print(f"Erro na conexão: {e}")
        sock.close()
        return None

    pacotes_enviados = 0

    inicio = time.perf_counter()
    tempo_limite = inicio + DURACAO_SEGUNDOS

    while time.perf_counter() < tempo_limite:
        pacotes_enviados += 1

        sequencia_bytes = pacotes_enviados.to_bytes(4, "big")
        string_bytes = STRING_TESTE.encode()
        tamanho_payload = TAMANHO_BYTES - len(sequencia_bytes) - len(string_bytes)
        payload = os.urandom(tamanho_payload)
        dados = sequencia_bytes + string_bytes + payload

        try:
            sock.sendall(dados)
        except Exception as e:
            print(f"Erro ao enviar dados: {e}")
            break

    fim_envio = time.perf_counter()
    duracao = fim_envio - inicio
    dados_envio = f"{pacotes_enviados},{retransmissoes},{perdidos},{duracao}"

    try:
        print(f"Enviando sinal de fim e estatisticas...")
        sock.sendall(b"FIM" + dados_envio.encode())
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
    sock.setsockopt(
        socket.SOL_SOCKET, socket.SO_REUSEADDR, 1
    )  # Permite reutilizar a porta
    sock.settimeout(30)  # Timeout para operações de socket

    try:
        sock.bind(remetente)
        sock.listen(1)
        print(f"Servidor TCP escutando em {remetente[0]}:{remetente[1]}")
    except Exception as e:
        print(f"Erro ao criar servidor para escuta: {e}")
        sock.close()
        return None

    try:
        conn, addr = sock.accept()
        print(f"Conexão aceita de {addr[0]}:{addr[1]}")
    except Exception as e:
        print(f"Erro ao aceitar conexão: {e}")
        sock.close()
        return None

    try:
        recebidos = set()
        stats = []

        buffer = b""
        stats_bruto = b""
        fim_recebido = False

        print(f"Aguardando pacotes...")
        inicio_recepcao = time.perf_counter()  # Marca o início da recepção

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
                stats_bruto = partes[1]  # As estatísticas já estão aqui
                fim_recebido = True

        # Processa qualquer pacote restante que ficou no buffer antes do "FIM"
        while len(buffer) >= TAMANHO_BYTES:
            pacote = buffer[:TAMANHO_BYTES]
            buffer = buffer[TAMANHO_BYTES:]
            seq = int.from_bytes(pacote[:4], "big")
            recebidos.add(seq)

        # Tenta ler tudo se não foi possível da primeira vez
        if len(stats_bruto) < 10:
            try:
                dados_adicionais = conn.recv(1024)
                if dados_adicionais:
                    stats_bruto += dados_adicionais
            except:
                pass

        # Decodifica e limpa as estatísticas
        try:
            stats_decodificado = stats_bruto.strip().decode("utf-8")
            if stats_decodificado:
                # Remove vírgulas extras e espaços
                stats_limpo = stats_decodificado.strip(", ")
                stats = stats_limpo.split(",")
                # Remove espaços em branco de cada elemento
                stats = [s.strip() for s in stats if s.strip()]
            else:
                stats = []
        except Exception as e:
            print(f"Erro ao decodificar estatísticas: {e}")
            stats = []

        fim_recepcao = time.perf_counter()
        tempo_recepcao = fim_recepcao - inicio_recepcao

    except Exception as e:
        print(f"Ocorreu um erro durante a recepção: {e}")
        stats = []
        tempo_recepcao = 20
    finally:
        if "conn" in locals():
            conn.close()
        sock.close()
        print("Conexão fechada.")

    if len(stats) >= 4:
        enviados = int(stats[0])
        retransmissoes = int(stats[1])
        perdidos_remetente = int(stats[2])
        tempo_envio = float(stats[3])  # Tempo do remetente
        perdidos = enviados - len(recebidos)
    else:
        print(
            "Erro no recebimento das estatísticas ou conexão encerrada prematuramente."
        )
        enviados = 0
        tempo_envio = 0
        perdidos = 0
        tempo_recepcao = 0

    # Garantir que o tempo não seja 0
    tempo_recepcao_final = max(tempo_recepcao, 0.001)
    tempo_envio_final = max(tempo_envio, 0.001)

    return {
        "quantidade_recebidos": len(recebidos),
        "quantidade_enviados": enviados,
        "retransmissoes": 0,  # TCP não calcula
        "perdidos": perdidos,
        "tempo": tempo_recepcao_final,  # Usa o tempo de recepção medido localmente
        "tempo_envio": tempo_envio_final,  # Tempo de envio recebido do remetente
    }
