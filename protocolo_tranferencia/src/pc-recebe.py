import argparse
from receber import receber_pacotes
from interface import menu_relatorio
from config import TOTAL


def main():
    parser = argparse.ArgumentParser(
        description="Recebe pacotes UDP e gera um relatório."
    )
    parser.add_argument(
        "--ip", default="0.0.0.0", help="IP para escutar ('0.0.0.0' para todos)."
    )
    parser.add_argument("--port", type=int, default=9001, help="Porta para escutar.")
    parser.add_argument(
        "--tamanho",
        type=int,
        choices=[500, 1000, 1500],
        required=True,
        help="Tamanho do pacote esperado (500, 1000 ou 1500).",
    )

    args = parser.parse_args()

    ip_escuta = args.ip
    porta_escuta = args.port
    tamanho_pacote = args.tamanho

    print(
        f"Receptor iniciado em {ip_escuta}:{porta_escuta}. Aguardando {TOTAL} pacotes de {tamanho_pacote} bytes..."
    )

    # A função receber_pacotes já tem um timeout, então ela não ficará presa para sempre.
    recebidos, desordenados, corrompidos = receber_pacotes(
        ip_escuta, porta_escuta, TOTAL, tamanho_pacote
    )

    # Calcula as estatísticas finais
    pacotes_enviados = TOTAL
    pacotes_perdidos = pacotes_enviados - recebidos

    print("\nRecepção finalizada. Gerando relatório...")

    # Exibe o relatório
    menu_relatorio(
        tamanho_pacote,
        recebidos,
        pacotes_enviados,
        pacotes_perdidos,
        desordenados,
        corrompidos,
    )


if __name__ == "__main__":
    main()
