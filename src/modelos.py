'''Módulo com as classes necessarias para o Scraping de fundos imobiliários'''
import locale
import requests
from tabulate import tabulate
from bs4 import BeautifulSoup

class FundoImobiliario:
    '''Classe para representar um fundo imobiliário'''

    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8') # Define o locale para pt_BR

    def __init__(self, codigo, segmento, cotacao_atual, ffo_yield, dividiend_yield,
                 p_vp, valor_mercado, liquidez, qt_imoveis,
                 preco_m2, aluguel_m2, cap_rate, vacancia_media):
        self.codigo = codigo
        self.segmento = segmento
        self.cotacao_atual = self.__trata_decimal(cotacao_atual)
        self.ffo_yield = self.__trata_porcetagem(ffo_yield)
        self.dividiend_yield = self.__trata_porcetagem(dividiend_yield)
        self.p_vp = self.__trata_decimal(p_vp)
        self.valor_mercado = self.__trata_decimal(valor_mercado)
        self.liquidez = self.__trata_decimal(liquidez)
        self.qt_imoveis = qt_imoveis
        self.preco_m2 = self.__trata_decimal(preco_m2)
        self.aluguel_m2 = self.__trata_decimal(aluguel_m2)
        self.cap_rate = self.__trata_porcetagem(cap_rate)
        self.vacancia_media = self.__trata_porcetagem(vacancia_media)

    def __trata_porcetagem(self, porcetagem_str):
        '''Converte string com % decimal'''
        return locale.atof(porcetagem_str.split('%')[0])

    def __trata_decimal(self, decimal_str):
        '''Converter string para decimal'''
        return locale.atof(decimal_str)


class Estrategia:
    '''Classe para representar uma estratégia de filtro de fundos imobiliários'''

    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8') # Define o locale para pt_BR

    def __init__(self, segmento='', cotacao_atual_minima=0, ffo_yield_minimo=0,
                dividiend_yield_minimo=0, p_vp_minimo=0,
                valor_mercado_minimo=0, liquidez_minima=0, qt_imoveis_minimo=0,
                valor_minimo_preco_m2=0, valor_minimo_aluguel_m2=0,
                valor_minimo_cap_rate=0, maxima_vacancia_media=0):
        self.segmento = segmento
        self.cotacao_atual_minima = cotacao_atual_minima
        self.ffo_yield_minimo = ffo_yield_minimo
        self.dividiend_yield_minimo = dividiend_yield_minimo
        self.p_vp_minimo = p_vp_minimo
        self.valor_mercado_minimo = valor_mercado_minimo
        self.liquidez_minima = liquidez_minima
        self.qt_imoveis_minimo = qt_imoveis_minimo
        self.valor_minimo_preco_m2 = valor_minimo_preco_m2
        self.valor_minimo_aluguel_m2 = valor_minimo_aluguel_m2
        self.valor_minimo_cap_rate = valor_minimo_cap_rate
        self.maxima_vacancia_media = maxima_vacancia_media

    def filtering(self, fundo:FundoImobiliario):
        '''Aplica a estratégia de filtro em um fundo imobiliário'''
        if self.segmento not in ('', self.segmento):
            return False

        if fundo.cotacao_atual < self.cotacao_atual_minima \
                or fundo.ffo_yield < self.ffo_yield_minimo \
                or fundo.dividiend_yield < self.dividiend_yield_minimo \
                or fundo.p_vp < self.p_vp_minimo \
                or fundo.valor_mercado < self.valor_mercado_minimo \
                or fundo.liquidez < self.liquidez_minima \
                or fundo.qt_imoveis < self.qt_imoveis_minimo \
                or fundo.preco_m2 < self.valor_minimo_preco_m2 \
                or fundo.aluguel_m2 < self.valor_minimo_aluguel_m2 \
                or fundo.cap_rate < self.valor_minimo_cap_rate \
                or fundo.vacancia_media > self.maxima_vacancia_media:
            return False

        return True

    def tabulating(self, table):
        '''Tabula os fundos imobiliários
        Recomenda-se filtrar antes de tabular
        :param table: Lista de fundos imobiliários
        :return: Tabela formatada'''
        cabecalho = ['CÓDIGO', 'SEGMENTO', 'COTAÇÃO ATUAL', 'DIVIDEND YIELD']
        content = []
        for elemento in table:
            content.append([elemento.codigo, elemento.segmento,
                            locale.currency(elemento.cotacao_atual),
                            f'{locale.str(elemento.dividiend_yield)}%'])

        return tabulate(content, headers=cabecalho, tablefmt='fancy_grid', showindex=True)

class Scraperty:
    '''Classe responsavel por realizar o web scraping'''
    def __init__(self):
        self.__url = 'https://www.fundamentus.com.br/fii_resultado.php'
        self.__headers = {'User-Agent': 'Mozilla/5.0'}
        self.__response = requests.get(url=self.__url, headers=self.__headers, timeout=10)

    def scraping(self):
        '''Realiza o scraping
        :return: um gerador de Fundo imobiliário'''
        soup = BeautifulSoup(self.__response.text, 'html.parser')

        linhas = soup.find(id='tabelaResultado').find('tbody').find_all('tr')

        resultado = []

        for linha in linhas:
            dados = linha.find_all('td')

            fundo_imobiliario = FundoImobiliario(
                codigo=dados[0].text,
                segmento=dados[1].text,
                cotacao_atual=dados[2].text,
                ffo_yield=dados[3].text,
                dividiend_yield=dados[4].text,
                p_vp=dados[5].text,
                valor_mercado=dados[6].text,
                liquidez=dados[7].text,
                qt_imoveis=int(dados[8].text),
                preco_m2=dados[9].text,
                aluguel_m2=dados[10].text,
                cap_rate=dados[11].text,
                vacancia_media=dados[12].text,
            )

            resultado.append(fundo_imobiliario)

        return resultado
