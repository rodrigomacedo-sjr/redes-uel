import estatisticas


def inicializa():
    """
    Printa um menu simples e coleta o protocolo e tipo de tranferência.
        - protocolo: [1] TCP ou [2] UDP
        - tranferência: [1] upload ou [2] download
    Retorna os dois valores como int.
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
    if protocolo == 1: protocolo_str = "TCP"
    elif protocolo == 2: protocolo_str = "UDP"
    else: 
        print("Opção não suportada")
        return None, None

    print("""
    - - - - Selecione o tipo de transferência - - - -
    [1] Upload
    [2] Download
    """
    )
    transferencia = int(input())
    if transferencia == 1: transferencia_str = "Upload"
    elif transferencia == 2: transferencia_str = "Download"
    else: 
        print("Opção não suportada")
        return None, None
    
    print(f"""
    =================================================
    - - - - - - Confirmação de Dados - - - - - -
    Protocolo de transferência: {protocolo_str}
    Tipo de tranferência: {transferencia_str}

    Aperte Enter para confirmar ou Ctrl+C para reiniciar programa...
    """
    )
    input()    

    return (protocolo, transferencia)


def output_estatisticas(pacotes, perdidos):
    """
    Printa os resultados do teste de tranferência.
        - Pacotes enviados: número de pacotes enviados na transferência, passado como parâmetro
        - Pacotes recebidos: número de pacotes recebidos na transferência, passado como parâmetro
        - Bytes enviados: quantidade de bytes enviados
        - Velocidade: velocidade da tranferência, em Kb, Mb e Gb por segundo
        - Pacotes/segundo: velocidade de pacotes por segundo 
    Retorna os dois valores como int.
    """

    velocidades = estatisticas.calcula_velocidade(pacotes)
    print(
    f"""
    ================ ESTATÍSTICAS ===================
    PACOTES ENVIADOS: {pacotes}
    - - - - - - - - - - - - - - - - - - - - - - - - -
    PACOTES PERDIDOS: {perdidos}
    - - - - - - - - - - - - - - - - - - - - - - - - -
    BYTES ENVIADOS: {estatisticas.calcula_bytes_enviados(pacotes)} B
    - - - - - - - - - - - - - - - - - - - - - - - - -
    VELOCIDADE (Kb, Mb, Gb):
        > {str(velocidades[0]).replace('.', ',')} Kb/s
        > {str(velocidades[1]).replace('.', ',')} Mb/s
        > {str(velocidades[2]).replace('.', ',')} Gb/s
    - - - - - - - - - - - - - - - - - - - - - - - - -
    PACOTES/SEGUNDO: {estatisticas.calcula_pacotes_segundo(pacotes)}
    =================================================
    """
    )

'''
- TESTES PARA MENU -

def main():
    protocolo, transferencia = inicializa()
    confirma_infos(protocolo, transferencia)
    output_estatisticas(5000, 4500)

if __name__ == "__main__":
    main()
'''