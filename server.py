import socket

# Solicitar porta para o seridor ouvir
MY_PORT = int(input("Insira a porta que o servidor deve ouvir: "))

MY_IP = ''

# Criar o socket 
tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Definir o IP e porta para o servidor ouvir
MY_SERVER = (MY_IP, MY_PORT)
tcp.bind(MY_SERVER)  # Faz o bind do IP e da porta para começar a ouvir

tcp.listen(1)  # Começar a ouvir (aguardar conexão)

print(f"Servidor ouvindo na porta {MY_PORT}...")

# Aceitar conexão do cliente
conexao, docliente = tcp.accept()
print("O cliente =", docliente, "se conectou")

# Loop para receber mensagens do cliente
while True:
    mensagem_recebida = conexao.recv(1024)
    if mensagem_recebida:
        # Se houver uma nova mensagem, imprime na tela
        print(f"{mensagem_recebida.decode("utf8")}, - {docliente}")

# Fechar a conexão ao terminar
conexao.close()
