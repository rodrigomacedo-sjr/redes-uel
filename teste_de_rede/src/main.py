import menu
import transferencia_tcp
import transferencia_udp
from config import IP_CONEXAO, PORT_CONEXAO, IP_LOCAL, PORT_LOCAL

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
            destinatario = (IP_CONEXAO, PORT_CONEXAO)
            resultado = transferencia_tcp.enviar_pacotes(destinatario)
            pc_enviados = resultado["quantidade_enviados"]
            perdidos = resultado["perdidos"]
        else: # Download
            servidor = (IP_LOCAL, PORT_LOCAL)
            resultado = transferencia_tcp.receber_pacotes(servidor)
            pc_enviados = resultado["quantidade_enviados"]
            perdidos = resultado["perdidos"]
    
    else: # UDP
        if tipo_transf == 1: # Upload
            destinatario = (IP_CONEXAO, PORT_CONEXAO)
            resultado = transferencia_udp.enviar_pacotes(destinatario)
            pc_enviados = resultado["quantidade_enviados"]
            perdidos = resultado["perdidos"]
        else: # Download
            servidor = (IP_LOCAL, PORT_LOCAL)
            resultado = transferencia_udp.receber_pacotes(servidor)
            pc_enviados = resultado["quantidade_enviados"]
            perdidos = resultado.get("perdidos_calculado", resultado.get("perdidos", 0))

    menu.output_estatisticas(pc_enviados, perdidos, resultado.get("tempo", 20))

if __name__ == "__main__":
    main()
