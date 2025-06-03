from config import setup
from protocolo_tranferencia.enviar import enviar_pacotes
from protocolo_tranferencia.interface import menu_inicio, menu_relatorio
from protocolo_tranferencia.receber import receber_pacotes

def main():
    setup()
    ip_destino, porta_destino, tamanho_testes = menu_inicio()
    pacotes_enviados = enviar_pacotes()
    pacotes_recebidos, pacotes_desordenados, pacotes_corrompidos = receber_pacotes()
    pacotes_perdidos = pacotes_enviados - pacotes_recebidos;
    pacotes_recebidos, pacotes_enviados, pacotes_perdidos, pacotes_desordenados, pacotes_corrompidos, tamanho_testes = menu_relatorio()

if __name__ = "main":
    main()
