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
    except ConnectionRefusedError:
        print(f"Erro: Conexão recusada. Verifique se o servidor está rodando em {destinatario[0]}:{destinatario[1]}")
        sock.close()
        return None
    except Exception as e:
        print(f"Erro na conexão: {e}")
        sock.close()
        return None

    pacotes_enviados = 0

    inicio = time.perf_counter()
    tempo_limite = inicio + DURACAO_SEGUNDOS

    while time.perf_counter() < tempo_limite:
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

    fim_envio = time.perf_counter()
    duracao = fim_envio - inicio
    dados_envio = f"{pacotes_enviados}, {retransmissoes}, {perdidos}, {duracao},"

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
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Permite reutilizar a porta
    sock.settimeout(30)  # Timeout para operações de socket
    
    try:
        sock.bind(remetente)
        sock.listen(1)
        print(f"Servidor TCP escutando em {remetente[0]}:{remetente[1]}")
    except OSError as e:
        print(f"Erro ao fazer bind na porta {remetente[1]}: {e}")
        sock.close()
        return None

    try:
        conn, addr = sock.accept()
        print(f"Conexão aceita de {addr[0]}:{addr[1]}")
    except socket.timeout:
        print("Timeout: Nenhuma conexão recebida")
        sock.close()
        return None
    except Exception as e:
        print(f"Erro ao aceitar conexão: {e}")
        sock.close()
        return None

    try:
        recebidos = set()
        stats = []

        # Lógica de buffer para lidar com TCP
        # Garante que pacotes sejam processados corretamente, mesmo em pedaços
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

        # Se não há dados suficientes no stats_bruto, tenta ler mais uma vez
        if len(stats_bruto) < 10:  # Tamanho mínimo esperado para as estatísticas
            try:
                dados_adicionais = conn.recv(1024)
                if dados_adicionais:
                    stats_bruto += dados_adicionais
            except:
                pass  # Ignora erros na leitura adicional
        
        stats_decodificado = stats_bruto.strip().decode()
        if stats_decodificado:
            stats = stats_decodificado.split(",")

        fim_recepcao = time.perf_counter()  # Marca o fim da recepção
        tempo_recepcao = fim_recepcao - inicio_recepcao  # Calcula o tempo total de recepção

    except Exception as e:
        print(f"Ocorreu um erro durante a recepção: {e}")
        tempo_recepcao = 0  # Em caso de erro, define tempo como 0
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

    return {
        "quantidade_recebidos": len(recebidos),
        "quantidade_enviados": enviados,
        "retransmissoes": 0,  # Métrica não calculada aqui
        "perdidos": perdidos,
        "tempo": tempo_recepcao,  # Usa o tempo de recepção medido localmente
        "tempo_envio": tempo_envio,  # Tempo de envio recebido do remetente
    }
