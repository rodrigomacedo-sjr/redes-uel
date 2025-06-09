# Trabalho 05 - Teste de Rede

## Especificações
1. Implementar dois sistemas (scripts) separados: um baseado em TCP e
outro em UDP.
2. Os scripts devem ter dois modos de execução: upload e download.
3. Pacotes devem ter um tamanho fixo de 500 bytes.
4. O payload dos pacotes deve ser composto por sequências da string
“teste de rede \*2025\*”.
5. Um teste deve executar por aproximadamente 20 segundos.
6. Apresentar as métricas de transferência:
    - Total de bytes;
    - Total de pacotes;
    - (G,M,K) bit/s;
    - pacotes/s;
    - Perda de pacotes.  
    Obs: separar milhar por ponto (ex: 15.000 Kbit/s)

## Apresentações de Resultados
- Testar para o meio cabeado e o meio sem fio:
    - Testar para TCP e UDP:
        - A -> B (2x)
            - Tabelar métricas.
        - B -> A (2x)
            - Tabelar métricas.
    Total de execuções = 2 x 2 x (2 + 2) = 16.
- Apresentar o sistema funcionando e o seu ﬂuxograma.
- Entregar o código, o ﬂuxograma e as tabelas de resultados.
- Mostrar os pacotes transferidos utilizando a ferramenta Wireshark.