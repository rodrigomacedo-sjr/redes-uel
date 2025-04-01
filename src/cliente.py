"""
Arquivo responsável para gerenciar o menu do Usuário (Cliente)
"""
import socket
import random

HOST = '127.0.0.1'

class Cliente:
    """Representa um cliente que pode se conectar a um servidor e gerenciar uma sala."""

    def __init__(self):
        """Inicializa os sockets para comunicação com o servidor e para criação de salas."""
        self.cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sala_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def configurar_cliente(self, host: str, port: int):
        """Estabelece conexão com um servidor.

        Args:
            host (str): Endereço IP do servidor.
            port (int): Porta do servidor.
        """
        self.cliente_socket.connect((host, port))

    def configurar_sala(self):
        """Cria uma sala com um código aleatório e começa a escutar conexões."""
        cod = random.randint(10000, 99999)
        self.sala_socket.bind((HOST, cod))
        self.sala_socket.listen(5)
        print(f"Sala criada\nCódigo da sala: {cod}")

    def monitorar_pedidos(self):
        """Monitora conexões de clientes enquanto a sala estiver aberta."""
        pass

    def utilizar_sala(self):
        """Monitora o recebimento de dados dos clientes enquanto a sala estiver aberta.

        Encerra a sala quando finalizado.
        """
        try:
            pass
        finally:
            self.fechar_conexao_sala()

    def fechar_conexao_cliente(self):
        """Fecha a conexão do cliente com o servidor."""
        self.cliente_socket.close()

    def fechar_conexao_sala(self):
        """Fecha a conexão da sala."""
        self.sala_socket.close()
