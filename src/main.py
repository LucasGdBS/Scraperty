'''
    Script responsável por executar o scraping e 
    filtrar os fundos de acordo com a estratégia definida.
'''
from modelos import Estrategia, Scraperty

scraperty = Scraperty()

strategy = Estrategia(
    cotacao_atual_minima=50.0,
    dividiend_yield_minimo=5,
    p_vp_minimo=0.70,
    valor_mercado_minimo=200000000,
    liquidez_minima=50000,
    qt_imoveis_minimo=5,
    maxima_vacancia_media=10
)

resultado = [elemento for elemento in scraperty.scraping() if strategy.filtering(elemento)]
print(scraperty.tabulating(resultado))
