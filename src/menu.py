"""
Arquivo responsável por gerir o menu do usuário (Cliente).
Este módulo contém funções para exibir opções e interagir com o usuário.

Funções:
    init() -- Função de inicialização do menu (ainda não implementada).
"""
def init():
    username = input("Digite seu nome de usuário: ")
    porta_receber = int(input("Digite a sua porta para receber mensagens: "))
    porta_enviar = int(input("Digite a sua porta para enviar mensagens: "))
    ip_amigo = int(input("Insira o IP do seu amigo que quer se conectar: "))
    return username, porta_receber, porta_enviar, ip_amigo

def enviarMsg():
    pass
