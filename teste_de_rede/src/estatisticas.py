"""
(exibir)
1. quantos pacotes enviados [X]
2. quantos pacotes perdidos [X]
3. quantos bytes enviados [X]
4. qual a velocidade em Giga/mega/kilo/bit por segundo (separar milhar por ponto) [X]
5. quantos pacotes por segundo [X]
"""

from config import TAMANHO_BYTES


def calcula_bytes_enviados(pacotes):
    return pacotes * TAMANHO_BYTES


def calcula_velocidade(pacotes, tempo):
    """
    Calcula velocidade em Giga, Mega e Kilo bits
    Retorna -> tuple : (Kb, Mb, Gb)
    """
    # Evita divisão por zero
    if tempo <= 0:
        return {"Kb/s": 0, "Mb/s": 0, "Gb/s": 0}

    bits = calcula_bytes_enviados(pacotes) * 8

    Kb = bits / 1024
    Mb = Kb / 1024
    Gb = Mb / 1024

    return {"Kb/s": Kb / tempo, "Mb/s": Mb / tempo, "Gb/s": Gb / tempo}


def calcula_pacotes_por_segundo(pacotes, tempo):
    """
    Calcula quantos pacotes por segundo foram transmitidos
    """
    # Evita divisão por zero
    if tempo <= 0:
        return 0

    return pacotes / tempo

