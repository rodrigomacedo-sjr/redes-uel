import argparse
from enviar import enviar_pacotes
from config import TOTAL


def main():
    parser = argparse.ArgumentParser(description="Envia pacotes UDP para um destino.")
    parser.add_argument("--ip", default="127.0.0.1", help="IP de destino.")
    parser.add_argument("--port", type=int, default=9001, help="Porta de destino.")
    parser.add_argument(
        "--tamanho",
        type=int,
        choices=[500, 1000, 1500],
        required=True,
        help="Tamanho do pacote (500, 1000 ou 1500).",
    )

    args = parser.parse_args()

    destino = (args.ip, args.port)
    tamanho_pacote = args.tamanho

    print(
        f"Enviando {TOTAL} pacotes de {tamanho_pacote} bytes para {args.ip}:{args.port}..."
    )

    pacotes_enviados = enviar_pacotes(destino, tamanho_pacote)

    print(f"\nEnvio concluído. Total de {pacotes_enviados} pacotes enviados.")


if __name__ == "__main__":
    main()
