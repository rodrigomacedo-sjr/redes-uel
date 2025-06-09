# Sockets

Referente aos trabalho 1 e 2, [`chat TCP UDP`](src/chat_tcp_udp/).

## Objetivos do trabalho:

- Criar uma aplicação em Python para tornar disponível um Chat entre dois computadores via TCP/IP
  - Utilizar a API de Socket para a camada de transporte
- Apresentar documentação da ferramenta, incluindo um fluxograma operacional
- Permitir envio via UDP, também utilizando a API do Python
- Testar ambos os protocolos para perda de pacotes e tempo de execução, documentar os achados

# Instruções de uso
1. Ter Python 3.10+ instalado
2. Rodar o programa com `main.py --ip {ip_de_envio}` em dois computadores conectados na mesma rede

# Teoria

## O que são Sockets

- Sockets são como “tomadas” usadas para a comunicação entre computadores em uma rede.
- Eles permitem que programas enviem e recebam dados, como acontece em um chat ou ao acessar um site.
- Cada socket tem um **endereço IP** (para identificar o computador) e uma **porta** (para identificar o programa).
- Existem dois tipos principais:
  - **TCP (SOCK_STREAM)**: garante que os dados cheguem completos e na ordem correta.
  - **UDP (SOCK_DGRAM)**: mais rápido, mas sem garantia de entrega.
- São usados em jogos online, aplicativos de mensagens, servidores web e muito mais.

## Sockets em Python

Sockets em Python são usados para estabelecer comunicação entre diferentes processos, seja no mesmo computador ou em diferentes dispositivos em uma rede. Eles são criados e manipulados utilizando o módulo `socket` da linguagem. Este módulo permite que você crie conexões de rede utilizando protocolos como TCP (orientado à conexão) ou UDP (sem conexão). Ao usar sockets, programas podem enviar e receber dados entre si, o que é essencial para a criação de servidores e clientes em aplicações de rede.

### Métodos

Os métodos fornecidos pelo módulo `socket` permitem criar, gerenciar e finalizar conexões de rede, além de enviar e receber dados. Eles são fundamentais para permitir a comunicação entre computadores e dispositivos em uma rede local ou na internet.

#### **socket()**:

O método `socket()` cria um novo socket, ou ponto de comunicação entre processos. Ele exige dois parâmetros:

- **Família de endereços**: Especifica o tipo de protocolo de rede.
  - `AF_INET` para IPv4.
  - `AF_INET6` para IPv6.
- **Tipo de socket**: Define o tipo de comunicação.
  - `SOCK_STREAM` para comunicação orientada à conexão (TCP).
  - `SOCK_DGRAM` para comunicação sem conexão (UDP).

Exemplo:

```Python
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
```

#### **bind()**:

O método `bind()` associa um socket a um endereço e uma porta específicos, permitindo que ele escute conexões. Ele requer um único parâmetro:

- **Endereço e porta**: Uma tupla com o **host** (geralmente `'localhost'` ou `'0.0.0.0'` para todas as interfaces) e a **porta** (número da porta que o servidor usará).

Exemplo:

```Python
s.bind(('localhost', 50000))
```

#### **listen()**:

O método `listen()` coloca o socket no modo de escuta para aceitar conexões de clientes. Ele requer um único parâmetro:

- **Backlog**: Um número inteiro que define a quantidade máxima de conexões que podem ficar em espera antes de serem aceitas. Normalmente, valores como 5 ou 10 são usados.

Exemplo:

```Python
s.listen(5)
```

#### **accept()**:

O método `accept()` aceita uma conexão de um cliente e retorna dois valores:

- **conn**: Um novo objeto socket para a comunicação com o cliente.
- **addr**: O endereço do cliente, geralmente uma tupla contendo o IP e a porta.

Exemplo:

```Python
conn, addr = s.accept()
```

#### **connect()**:

O método `connect()` é utilizado pelo cliente para estabelecer uma conexão com um servidor. Ele exige um único parâmetro:

- **Endereço e porta**: Uma tupla com o **host** e a **porta** do servidor.

Exemplo:

```Python
s.connect(('localhost', 50000))
```

#### **sendall()**:

O método `sendall()` envia todos os dados através do socket. Ele exige um único parâmetro:

- **Dados**: Os dados a serem enviados, que devem ser do tipo bytes.

Exemplo:

```Python
s.sendall(b'Hello, Server!')
```

#### **recv()**:

O método `recv()` recebe dados do socket. Ele exige um único parâmetro:

- **Tamanho**: O número máximo de bytes que podem ser recebidos de uma vez.

Exemplo:

```Python
data = s.recv(1024)
```

#### **close()**:

O método `close()` fecha o socket, encerrando a comunicação. Ele não requer parâmetros.

Exemplo:

```Python
s.close()
```

---

### Exemplo de Código

#### Servidor

```python
import socket  # Importa a biblioteca socket para comunicação em rede

# Função para configurar o servidor
def configurar_servidor(host, porta):
    servidor_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor_socket.bind((host, porta))  # Associa o socket ao endereço e porta
    servidor_socket.listen()  # Coloca o servidor no modo de escuta
    print(f"Servidor aguardando conexão em {host}:{porta}...")
    return servidor_socket

# Função para aceitar a conexão de um cliente
def aceitar_conexao(servidor_socket):
    conn, endereco = servidor_socket.accept()  # Aceita a conexão
    print(f"Conectado com: {endereco}")
    return conn

# Função para lidar com a comunicação do servidor
def comunicar_com_cliente(conn):
    try:
        while True:
            dados = conn.recv(1024)  # Recebe dados do cliente
            if not dados:
                break  # Encerra a conexão se não houver dados

            mensagem_cliente = dados.decode()  # Decodifica os dados recebidos
            print(f"Recebido: {mensagem_cliente}")

            if mensagem_cliente.lower() == "off":
                conn.sendall("Servidor encerrado.".encode())  # Envia mensagem de encerramento
                break  # Encerra o loop de comunicação

            # Envia de volta a resposta para o cliente
            resposta = "Mensagem recebida."
            conn.sendall(resposta.encode())
    finally:
        conn.close()  # Fecha a conexão após a comunicação

# Função principal para rodar o servidor
def main():
    HOST = '127.0.0.1'  # Definir o endereço do servidor
    PORT = 50000  # Definir a porta do servidor

    servidor_socket = configurar_servidor(HOST, PORT)
    conn = aceitar_conexao(servidor_socket)
    comunicar_com_cliente(conn)

# Executa a função principal se o script for rodado diretamente
if __name__ == '__main__':
    main()
```

#### Cliente

```python
import socket  # Importa a biblioteca socket para comunicação em rede

# Função para configurar o cliente
def configurar_cliente(host, porta):
    cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliente_socket.connect((host, porta))  # Conecta-se ao servidor
    return cliente_socket

# Função para enviar dados ao servidor e receber a resposta
def comunicar_com_servidor(cliente_socket):
    try:
        while True:
            mensagem = input("Digite algo para o servidor (ou 'off' para desconectar): ")
            cliente_socket.sendall(mensagem.encode())  # Envia a mensagem para o servidor

            # Recebe a resposta do servidor
            dados = cliente_socket.recv(1024)
            print(f"Resposta do servidor: {dados.decode()}")  # Exibe a resposta

            if mensagem.lower() == "off":
                break  # Encerra o loop se o cliente enviar "off"
    finally:
        cliente_socket.close()  # Fecha a conexão

# Função principal para rodar o cliente
def main():
    HOST = '127.0.0.1'  # Definir o endereço do servidor
    PORT = 50000  # Definir a porta do servidor

    cliente_socket = configurar_cliente(HOST, PORT)
    comunicar_com_servidor(cliente_socket)

# Executa a função principal se o script for rodado diretamente
if __name__ == '__main__':
    main()
```

### Explicação:

- **Servidor**:

  - O servidor aguarda uma conexão e começa a comunicação.
  - Ele recebe a mensagem do cliente e, se a mensagem for "off", ele responde com "Servidor encerrado." e encerra a comunicação.
  - Se a mensagem não for "off", o servidor responde com "Mensagem recebida."

- **Cliente**:
  - O cliente envia uma mensagem digitada pelo usuário para o servidor.
  - O cliente aguarda a resposta do servidor e a exibe.
  - Se o cliente digitar "off", ele encerra a comunicação e fecha a conexão.

Esse código garante que o servidor continuará recebendo mensagens do cliente até que o usuário digite "off", momento em que o servidor será encerrado.
