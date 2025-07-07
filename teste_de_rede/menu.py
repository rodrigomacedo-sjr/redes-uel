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


def confirma_infos(protocolo, transferencia):
    print(
    f"""
    - - - - - - Confirmação de Dados - - - - - -
    Protocolo de transferência: {protocolo}
    Tipo de tranferência: {transferencia}

    Aperte Enter para confirmar ou Ctrl+C para reiniciar programa...
    """
    )
    input()



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


def main():
    protocolo, transferencia = inicializa()
    confirma_infos(protocolo, transferencia)
    output_estatisticas(50)

if __name__ == "__main__":
    main()