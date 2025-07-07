import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.padding import Padding

console = Console()

@click.command()
@click.option('--bytes', default=0, help='Número de bytes enviados.', type=int)
@click.option('--pacotes', default=0, help='Número de pacotes enviados.', type=int)
@click.option('--bits', default=0, help='Número de bit/s.', type=int)
@click.option('--pacotes_s', default=0, help='Envio de pacotes/s.', type=int)
@click.option('--perda', default=0, help='Perda de pacotes.', type=int)
def menu_relatorio(bytes, pacotes, bits, pacotes_s, perda):
    """
    Exibe um relatório de transmissão de dados com formatação Rich.
    """
    # Criando um título com Panel
    titulo = Panel(
        Text("Relatorio de Envio", justify="center", style="bold white on blue"),
        padding=(1, 2),
        expand=False
    )
    console.print(titulo)

    # Criando uma tabela para os dados
    tabela = Table(show_header=True, header_style="bold magenta")
    tabela.add_column("Estatísticas", style="dim", width=20)
    tabela.add_column("Valor", justify="right")

    tabela.add_row("Total de bytes enviados: ", f"[green]{bytes}[/green]")
    tabela.add_row("Total de Pacotes enviados", f"[blue]{pacotes}[/blue]")
    tabela.add_row("Velocidade dos bit/s", f"[red]{bits}[/red]")
    tabela.add_row("Velocidade dos Pacotes/s", f"[yellow]{pacotes_s}[/yellow]")
    tabela.add_row("Pacotes perdidos", f"[bold red]{perda}[/bold red]")

    console.print(Padding(tabela, (1, 0, 1, 0))) # Adiciona um pouco de espaço vertical
