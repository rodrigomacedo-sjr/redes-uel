import hashlib

def calcula_checksum(dados):
    """
    CALCULA CHECKSUM
        - Recebe o parâmetro 
            dados: String no modelo b"string"
        - Retorna o hash da string
    """

    sum = hashlib.sha256(dados).hexdigest()
    return sum

def checksum(sum, dados) -> bool:
    """
    CHECKSUM
        - Recebe os parâmetros 
            sum: Hash de soma (primeiros 64 bytes da mensagem)
            dados: Mensagem em si, sem a soma
        - Verifica se a soma de parâmetro é igual a soma da mensagem recebida
        - Retorna True se sim e False se não 
    """
    
    new_sum = calcula_checksum(dados)
    if(sum == new_sum): return True
    else: return False