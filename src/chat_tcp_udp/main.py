import argparse
from enviar import enviar_pacotes
from receber import receber_pacotes


def parse_args():
    parser = argparse.ArgumentParser(description="Envio de pacotes TCP/UDP")
    parser.add_argument("--ip", default="127.0.0.1", help="IP de destino e recepção")
    parser.add_argument("--porta-envio", type=int, default=9000, help="Porta de envio")
    parser.add_argument(
        "--porta-recebe", type=int, default=9001, help="Porta de recepção"
    )
    parser.add_argument(
        "--protocolo", choices=["tcp", "udp"], default="udp", help="Protocolo"
    )
    parser.add_argument(
        "--testes",
        nargs="+",
        type=int,
        default=[10, 100, 1000],
        help="Lista de tamanhos de teste",
    )
    return parser.parse_args()


def main():
    args = parse_args()

    for n in args.testes:
        print(f"\n=== Teste com {n} pacotes ({args.protocolo.upper()}) ===")

        # Iniciar receptor em background
        import threading

        resultado_receber = {}

        def thread_receber():
            recebido = receber_pacotes(args.ip, args.porta_recebe, args.protocolo, n)
            resultado_receber["qtd"] = recebido

        t = threading.Thread(target=thread_receber, daemon=True)
        t.start()

        # Aguarda receptor subir
        import time

        time.sleep(1)

        # Envia pacotes
        stats = enviar_pacotes(args.ip, args.porta_recebe, args.protocolo, n)

        t.join()

        print(f"Pacotes enviados:       {stats['enviados']}")
        print(f"Retransmissões:         {stats['retransmissoes']}")
        print(f"Pacotes não confirmados:{stats['perdidos']}")
        print(f"Pacotes recebidos:      {resultado_receber.get('qtd',0)}")
        print(f"Tempo total:            {stats['tempo']:.3f}s")


if __name__ == "__main__":
    main()
