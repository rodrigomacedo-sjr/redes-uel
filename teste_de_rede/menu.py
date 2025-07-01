"""
1. perguntar TCP ou UDP
2. pegar o computador de envio da config.py (é mais rápido e fácil)
3. perguntar upload ou download
4. output de estatisticas
"""

import estatisticas

def inicializa():
    """
    Printa um menu simples e coleta o protocolo e tipo de tranferência
        - protocolo: [1] TCP ou [2] UDP
        - tranferência: [1] upload ou [2] download
    Retorna os dois valores como int
    """

    print(
    """
    ========== INICIALIZANDO TESTE DE REDE ==========
    - - - Selecione o protocolo de transferência - - -
    [1] TCP
    [2] UDP
    """
    )
    protocolo = int(input())
    print(
    """
    - - - - Selecione o tipo de transferência - - - -
    [1] Upload
    [2] Download
    """
    )
    transferencia = int(input())
    print("=================================================")

    return (protocolo, transferencia)

def output_estatisticas(pacotes):
    velocidades = estatisticas.calcula_velocidade(pacotes)
    print(
    f"""
    ================ ESTATÍSTICAS ===================
    PACOTES ENVIADOS: 
    - - - - - - - - - - - - - - - - - - - - - - - - -
    PACOTES PERDIDOS:
    - - - - - - - - - - - - - - - - - - - - - - - - -
    BYTES ENVIADOS: {estatisticas.calcula_bytes_enviados(pacotes)} B
    - - - - - - - - - - - - - - - - - - - - - - - - -
    VELOCIDADE (Kb, Mb, Gb):
        > {str(velocidades[0]).replace(',', '.')} Kb
        > {str(velocidades[1]).replace(',', '.')} Mb
        > {str(velocidades[2]).replace(',', '.')} Gb
    - - - - - - - - - - - - - - - - - - - - - - - - -
    PACOTES/SEGUNDO: {estatisticas.calcula_pacotes_segundo(pacotes)}
    =================================================
    """
    )
