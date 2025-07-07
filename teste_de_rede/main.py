import menu
import transferencia_tcp
import transferencia_udp
from config import IP_ENVIO, PORT_ENVIO, IP_RECEBIMENTO, PORT_RECEBIMENTO

def main():
    """
    1. pegar dados do menu
    2. rodar funções de acordo
    ida e volta
    3. rodar estatisticas
    """

    prot, tipo_transf = menu.inicializa()
    
    if prot == 1: # TCP
        if tipo_transf == 1: # Upload
            pc_enviados, retransmissoes, perdidos, tempo = transferencia_tcp.enviar_pacotes(IP_ENVIO, PORT_ENVIO)
        else: # Download
            pc_recebidos, pc_enviados, retransmissoes, perdidos, tempo = transferencia_tcp.receber_pacotes(IP_RECEBIMENTO, PORT_RECEBIMENTO)
    
    else: # UDP
        if tipo_transf == 1: # Upload
            pc_enviados, retransmissoes, perdidos, tempo = transferencia_udp.enviar_pacotes(IP_ENVIO, PORT_ENVIO)
        else: # Download
            pc_recebidos, pc_enviados, retransmissoes, perdidos, tempo = transferencia_udp.receber_pacotes(IP_RECEBIMENTO, PORT_RECEBIMENTO)

    menu.output_estatisticas(pc_enviados, perdidos)
