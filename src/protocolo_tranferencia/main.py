from config import setup, TOTAL
from enviar import enviar_pacotes
from interface import menu_inicio, menu_relatorio
from receber import receber_pacotes


def main():
    setup()
    ip_destino, porta_destino, tamanho_testes = menu_inicio()
    pacotes_enviados = enviar_pacotes((ip_destino, int(porta_destino)), tamanho_testes)
    pacotes_recebidos, pacotes_desordenados, pacotes_corrompidos = receber_pacotes(
        ip_destino, porta_destino, TOTAL, tamanho_testes
    )
    pacotes_perdidos = pacotes_enviados - pacotes_recebidos
    (
        pacotes_recebidos,
        pacotes_enviados,
        pacotes_perdidos,
        pacotes_desordenados,
        pacotes_corrompidos,
        tamanho_testes,
    ) = menu_relatorio()

if __name__ == "__main__":
    main()
