import threading
import time
from config import setup, TOTAL, RECEIVE_PORT
from enviar import enviar_pacotes
from interface import menu_relatorio
from receber import receber_pacotes


def main():
    setup()

    # Configurações do teste
    ip_destino = "127.0.0.1"
    porta_destino = int(RECEIVE_PORT)
    tamanhos_de_teste = [500, 1000, 1500]

    for tamanho in tamanhos_de_teste:
        print(f"\nIniciando teste com pacotes de {tamanho} bytes...")

        # Dicionário para armazenar resultados da thread receptora
        resultados_receber = {}

        def thread_receber():
            # A thread chama receber_pacotes e armazena o resultado
            recebidos, desordenados, corrompidos = receber_pacotes(
                "0.0.0.0", porta_destino, TOTAL, tamanho
            )
            resultados_receber["recebidos"] = recebidos
            resultados_receber["desordenados"] = desordenados
            resultados_receber["corrompidos"] = corrompidos

        # Inicia a thread receptora
        t = threading.Thread(target=thread_receber)
        t.start()

        # Pequena pausa para garantir que o socket receptor está pronto
        time.sleep(1)

        # Chama a função de envio na thread principal
        pacotes_enviados = enviar_pacotes((ip_destino, porta_destino), tamanho)

        # Espera a thread receptora terminar seu trabalho
        t.join()

        # Coleta e calcula os resultados
        pacotes_recebidos = resultados_receber.get("recebidos", 0)
        pacotes_desordenados = resultados_receber.get("desordenados", 0)
        pacotes_corrompidos = resultados_receber.get("corrompidos", 0)
        pacotes_perdidos = pacotes_enviados - pacotes_recebidos

        # Exibe o relatório para o teste atual
        menu_relatorio(
            tamanho,
            pacotes_recebidos,
            pacotes_enviados,
            pacotes_perdidos,
            pacotes_desordenados,
            pacotes_corrompidos,
        )


if __name__ == "__main__":
    main()
