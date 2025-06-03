import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.padding import Padding

console = Console() # Cria uma instância do Console do Rich

@click.command()
@click.option('--recebidos', default=0, help='Número de pacotes recebidos.', type=int)
@click.option('--enviados', default=0, help='Número de pacotes enviados.', type=int)
@click.option('--perdidos', default=0, help='Número de pacotes perdidos.', type=int)
@click.option('--desordenados', default=0, help='Número de pacotes desordenados.', type=int)
@click.option('--corrompidos', default=0, help='Número de pacotes corrompidos.', type=int)
@click.option('--tamanho-dados', default="0B", help='Tamanho total dos dados (ex: 10MB, 2GB).')
def menu_relatorio(recebidos, enviados, perdidos, desordenados, corrompidos, tamanho_dados):
    """
    Exibe um relatório de transmissão de dados com formatação Rich.
    """
    # Criando um título com Panel
    titulo = Panel(
        Text("Relatório de Transmissão", justify="center", style="bold white on blue"),
        padding=(1, 2),
        expand=False
    )
    console.print(titulo)

    # Criando uma tabela para os dados
    tabela = Table(show_header=True, header_style="bold magenta")
    tabela.add_column("Estatísticas", style="dim", width=20)
    tabela.add_column("Valor", justify="right")

    tabela.add_row("Pacotes Recebidos", f"[green]{recebidos}[/green]")
    tabela.add_row("Pacotes Enviados", f"[blue]{enviados}[/blue]")
    tabela.add_row("Pacotes Perdidos", f"[red]{perdidos}[/red]")
    tabela.add_row("Pacotes Desordenados", f"[yellow]{desordenados}[/yellow]")
    tabela.add_row("Pacotes Corrompidos", f"[bold red]{corrompidos}[/bold red]")
    tabela.add_row("Tamanho Total dos Dados", f"[cyan]{tamanho_dados}[/cyan]")

    console.print(Padding(tabela, (1, 0, 1, 0))) # Adiciona um pouco de espaço vertical

    # Exemplo de uso de Text para uma observação
    observacao = Text.assemble(
        ("Nota: ", "italic dim"),
        ("Valores em ", "dim"),
        ("vermelho ", "red"),
        ("indicam problemas.", "dim")
    )
    console.print(observacao)
    console.print("") # Linha em branco


def menu_inicio():
    print("=="*5 + "[Server]" + "=="*5)
    ip_destino = input("Digite o ip destino: ")
    print(ip_destino)
    porta_destino = input("Digite o porta destino: ")
    print(porta_destino)
    tamanho_teste = int(input("Digite o tipo de teste [500|1000|1500]: "))
    print(tamanho_teste)
    print("==" * 14, end="\n\n")
    return ip_destino, porta_destino, tamanho_teste

