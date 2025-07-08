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
            destinatario = (IP_ENVIO, PORT_ENVIO)
            pc_enviados, retransmissoes, perdidos, tempo = transferencia_tcp.enviar_pacotes(destinatario)
        else: # Download
            destinatario = (IP_RECEBIMENTO, PORT_RECEBIMENTO)
            pc_recebidos, pc_enviados, retransmissoes, perdidos, tempo = transferencia_tcp.receber_pacotes(destinatario)
    
    else: # UDP
        if tipo_transf == 1: # Upload
            destinatario = (IP_ENVIO, PORT_ENVIO)
            pc_enviados, retransmissoes, perdidos, tempo = transferencia_udp.enviar_pacotes(destinatario)
        else: # Download
            destinatario = (IP_RECEBIMENTO, PORT_RECEBIMENTO)
            pc_recebidos, pc_enviados, retransmissoes, perdidos, tempo = transferencia_udp.receber_pacotes(destinatario)

    menu.output_estatisticas(pc_enviados, perdidos)

if __name__ == "__main__":
    main()