"""
rotina do computador e envio
"""
import transferencia_tcp
import transferencia_udp

def upload(prot, ip, porta):
    if prot == 1:
       return transferencia_tcp.enviar_pacotes((ip, porta))
    else:
        return transferencia_udp.enviar_pacotes((ip, porta))

