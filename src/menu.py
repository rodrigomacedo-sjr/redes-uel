"""
Arquivo responsável por gerir o menu do usuário (Cliente).
Este módulo contém funções para exibir opções e interagir com o usuário.

Funções:
    init() -- Função de inicialização do menu (ainda não implementada).
"""
def init():
    username = input("Digite seu nome de usuário: ")
    porta_receber = (input("Digite a sua porta para receber mensagens: "))
    porta_destino = (input("Digite a sua porta de destino das mensagens: "))
    ip_destino = (input("Insira o IP de destino: "))
    return username, porta_receber, porta_enviar, ip_destino

def enviarMsg():
    pass

def teste(mensagem):
    return not mensagem == "fim"
