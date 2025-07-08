"""
rotina do computador de recebimento
"""
import transferencia_tcp
import transferencia_udp

def download(prot, ip, porta):
    if prot == 1:
        return transferencia_tcp.receber_pacotes((ip, porta))
    else:
        return transferencia_udp.receber_pacotes((ip, porta))
