# Checksum:
#   - Função de criar Checksum:
#       - Pega dados
#       - Calcula usando hash e retorna
#   - Função verificar Checksum:
#       - Recebe hash e dados
#       - Usa função de calcular
#       - Compara e retorna se é igual ou não

import hashlib

def calcula_checksum(dados):
    """
    CALCULA CHECKSUM
        - O parâmetro 'dados' deve ser uma string no modelo 'b"string"'
        - Retorna o hash da string 'dados'
    """
    sum = hashlib.sha256(dados).hexdigest()
    return sum

def checksum(sum, dados) -> bool:
    new_sum = calcula_checksum(dados)
    if(sum == new_sum): return True
    else: return False