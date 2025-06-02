# test_interface.py
import unittest
from unittest.mock import patch
# Ajuste o caminho da importação conforme a estrutura do seu projeto
from src.protocolo_tranferencia.interface import menu_inicio, menu_relatorio # ou o caminho correto

class TestInterface(unittest.TestCase):

    @patch('builtins.input')
    def test_menu_inicio_retorna_valores_corretos(self, mock_input):
        # Configura os valores que o 'input' simulado deve retornar, na ordem em que são chamados
        mock_input.side_effect = ['192.168.0.1', '8080', '500']

        # Chama a função que queremos testar
        ip_destino, porta_destino, tipo_teste = menu_inicio()

        # Verifica se os valores retornados são os esperados
        self.assertEqual(ip_destino, '192.168.0.1')
        self.assertEqual(porta_destino, '8080')
        self.assertEqual(tipo_teste, 500) # tipo_teste é convertido para int na função

    @patch('builtins.input')
    def test_menu_inicio_tipos_de_teste_diferentes(self, mock_input):
        # Testando com outro tipo de teste
        mock_input.side_effect = ['10.0.0.1', '1234', '1000']
        ip_destino, porta_destino, tipo_teste = menu_inicio()
        self.assertEqual(ip_destino, '10.0.0.1')
        self.assertEqual(porta_destino, '1234')
        self.assertEqual(tipo_teste, 1000)

        # Testando com o terceiro tipo de teste
        mock_input.side_effect = ['172.16.0.5', '9999', '1500']
        ip_destino, porta_destino, tipo_teste = menu_inicio()
        self.assertEqual(ip_destino, '172.16.0.5')
        self.assertEqual(porta_destino, '9999')
        self.assertEqual(tipo_teste, 1500)

    # Você também pode querer testar o que acontece se o usuário digitar algo
    # que não pode ser convertido para int em 'tipo_teste'.
    # A função original levantaria um ValueError.
    @patch('builtins.input')
    def test_menu_inicio_entrada_invalida_para_tipo_teste(self, mock_input):
        mock_input.side_effect = ['192.168.0.1', '8080', 'texto_invalido']

        # Verifica se um ValueError é levantado quando 'tipo_teste' não é um número
        with self.assertRaises(ValueError):
            menu_inicio()

    @patch('builtins.input')
    def test_menu_relatorio(self, mock_input):
        mock_input.side_effect = ['10.0.0.1']

        with self.assertRaises(ValueError):
            menu_relatorio()

# Para rodar os testes (adicione isso ao final do arquivo test_interface.py)
if __name__ == '__main__':
    unittest.main()