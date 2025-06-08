from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.padding import Padding

console = Console()  # Cria uma instância do Console do Rich


def menu_relatorio(
    tamanho_pacote, recebidos, enviados, perdidos, desordenados, corrompidos
):
    """
    Exibe um relatório de transmissão de dados com formatação Rich.
    """
    # Criando um título com Panel
    titulo = Panel(
        Text(
            f"Relatório de Transmissão - Pacotes de {tamanho_pacote} bytes",
            justify="center",
            style="bold white on blue",
        ),
        padding=(1, 2),
        expand=False,
    )
    console.print(titulo)

    # Criando uma tabela para os dados
    tabela = Table(show_header=True, header_style="bold magenta")
    tabela.add_column("Estatísticas", style="dim", width=25)
    tabela.add_column("Valor", justify="right")

    tamanho_total_dados = f"{(enviados * tamanho_pacote) / 1024:.2f} KB"

    tabela.add_row("Pacotes Enviados", f"[blue]{enviados}[/blue]")
    tabela.add_row("Pacotes Recebidos", f"[green]{recebidos}[/green]")
    tabela.add_row("Pacotes Perdidos", f"[red]{perdidos}[/red]")
    tabela.add_row("Pacotes Fora de Ordem", f"[yellow]{desordenados}[/yellow]")
    tabela.add_row("Pacotes Corrompidos", f"[bold red]{corrompidos}[/bold red]")
    tabela.add_row("Tamanho Total Transmitido", f"[cyan]{tamanho_total_dados}[/cyan]")

    console.print(Padding(tabela, (1, 0, 1, 0)))

    console.print("")  # Linha em branco
