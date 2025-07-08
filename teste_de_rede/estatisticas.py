"""
(exibir)
1. quantos pacotes enviados [-]
2. quantos pacotes perdidos [-]
3. quantos bytes enviados [X]
4. qual a velocidade em Giga/mega/kilo/bit por segundo (separar milhar por ponto) [X]
5. quantos pacotes por segundo [X]
"""
from config import TAMANHO_BYTES


def calcula_bytes_enviados(pacotes):
    return pacotes * TAMANHO_BYTES

def calcula_velocidade(pacotes):
    """
    Calcula velocidade em Giga, Mega e Kilo bits
    Retorna -> tuple : (Kb, Mb, Gb)
    """
    
    bits = calcula_bytes_enviados(pacotes) * 8
    
    Kb = bits/1024
    Mb = Kb/1024
    Gb = Mb/1024

    return {
        "Kb/s": Kb,
        "Mb/s": Mb,
<<<<<<< HEAD
        "Gb/s": Gb,
    }
=======
        "Gb/s": Gb
    }
>>>>>>> prs-develop
