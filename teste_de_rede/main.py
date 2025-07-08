import menu
from enviar import upload
from receber import download
from menu import output_estatisticas


def main():
    """
    1. pegar dados do menu
    2. rodar funções de acordo
    ida e volta
    3. rodar estatisticas
    """

    prot, tipo_transf, ip, porta = menu.inicializa()

    if tipo_transf == 1:
        dados = upload(prot, ip, porta)
        output_estatisticas(dados[0], (dados[0] - dados[2]))
    else:
        dados = download(prot, ip, porta)
        output_estatisticas(dados[1], dados[0])


if __name__ == '__main__':
    main()