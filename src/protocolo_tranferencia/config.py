import os

# Configurações do usuário
IP = "0.0.0.0"
RECEIVE_PORT = "9001"

# Configurações do programa
MAIN_HEADER = "*#@ Redes de Computadores UEL 2025 @#*"
MAIN_HEADER_SIZE = 38
HASH_SIZE = 64
TOTAL = 1000  # q. de pacotes


def setup():
    os.environ["PYTHONHASHSEED"] = "42"
