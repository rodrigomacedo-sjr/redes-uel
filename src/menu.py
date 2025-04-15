def init():
    porta_receber = input("Digite a sua porta para receber mensagens: ")
    porta_destino = input("Digite a sua porta para enviar mensagens: ")
    ip_destino = input("Insira o IP do computador de destino: ")
    return porta_receber, porta_destino, ip_destino

def teste(mensagem):
    return not mensagem == "fim"
