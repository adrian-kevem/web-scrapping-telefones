import re
import threading

import requests
from bs4 import BeautifulSoup



DOMINIO = "https://django-anuncios.solyd.com.br"
URL_SITE_AUTOMOVEIS = "https://django-anuncios.solyd.com.br"
LINKS_ANUNCIOS_AUTOMOVEIS = []
TELEFONES_ANUNCIOS_AUTOMOVEIS = []

def fazer_requisicao(url):
    try:
        resposta_requisicao = requests.get(url)
        if resposta_requisicao.status_code == 200:
            return resposta_requisicao.text
        else:
            print("Erro ao fazer a requisição!")

    except Exception as error:
        print(f"Erro ao fazer a requisição: {error}")

def parsin_resposta_requisicao(resposta_requisicao):
    try:
        soup_resposta_requisicao = BeautifulSoup(resposta_requisicao, "html.parser")
        return soup_resposta_requisicao
    except Exception as error:
        print(f"Erro ao fazer a conversão: {error}")
        
def imprimir_titulo_da_pagina(soup):
    print(soup.title.get_text().strip())

def buscar_elementos_HTML_na_pagina(soup):
    nome_tag = input("Digite o nome da tag desejada: ")
    menu = input("Gostaria de buscar por tags com atributos específicos? (1 - SIM / 2 - NÃO): ")
    if (menu == "1"):
        nome_atributo = input("Digite o nome do atributo desejado: ")
        elementos = soup.find_all(nome_tag, nome_atributo=True)
    else:
        elementos = soup.find_all(nome_tag)
    for indice, elemento in enumerate(elementos, 1):
        print(f"{indice} - {elemento}")

def encontrar_links_anuncios_automoveis(soup_resposta_requisicao):
    card_pai = soup_resposta_requisicao.find("div", class_="ui three doubling link cards")
    cards = card_pai.find_all("a", class_="card")
    for link in cards:
        try:
            LINKS_ANUNCIOS_AUTOMOVEIS.append(DOMINIO+link["href"])
        except:
            pass

def encontrar_telefones():
    for link in LINKS_ANUNCIOS_AUTOMOVEIS:
        resposta_requisicao = fazer_requisicao(link)
        soup_resposta_requisicao = parsin_resposta_requisicao(resposta_requisicao)
        descricao_anuncio = soup_resposta_requisicao.find_all("div", class_="sixteen wide column")[2].p.get_text().strip()
        regex = re.findall(r"\(?(?:\d{2})\)?[-. ]?(?:9)?(?:\d{4})[-. ]?(?:\d{4})", descricao_anuncio)
        TELEFONES_ANUNCIOS_AUTOMOVEIS.append(regex)
    
def encontrar_telefones_multithreading():
    while True:
        try:
            link = LINKS_ANUNCIOS_AUTOMOVEIS.pop(0)
        except:
            break
    
        resposta_requisicao = fazer_requisicao(link)    
        soup_resposta_requisicao = parsin_resposta_requisicao(resposta_requisicao)
        descricao_anuncio = soup_resposta_requisicao.find_all("div", class_="sixteen wide column")[2].p.get_text().strip()
        regex = re.findall(r"\(?(?:\d{2})\)?[-. ]?(?:9)?(?:\d{4})[-. ]?(?:\d{4})", descricao_anuncio)
        if regex:
            TELEFONES_ANUNCIOS_AUTOMOVEIS.append(regex)
            for telefone in regex:
                salvar_telefones(telefone + " \n ")

def salvar_telefones(telefone):
    try:
        with open("telefones.csv", "a") as arquivo:
            arquivo.write(telefone)
    except Exception as error:
        print(f"Erro ao salvar telefone: {error}")

def main():
    resposta_requisicao = fazer_requisicao(URL_SITE_AUTOMOVEIS)
    if resposta_requisicao:
        soup_resposta_requisicao = parsin_resposta_requisicao(resposta_requisicao)
    # imprimir_titulo_da_pagina(soup)
    # buscar_elementos_HTML_na_pagina(soup)
    encontrar_links_anuncios_automoveis(soup_resposta_requisicao)
    # encontrar_telefones()

    # thread_1 = threading.Thread(target=encontrar_telefones_multithreading)
    # thread_2 = threading.Thread(target=encontrar_telefones_multithreading)
    # thread_3 = threading.Thread(target=encontrar_telefones_multithreading)

    # thread_1.start()
    # thread_2.start()
    # thread_3.start()

    # thread_1.join()
    # thread_2.join()
    # thread_3.join()

    threads = []
    for i in range(3):
        thread = threading.Thread(target=encontrar_telefones_multithreading)
        threads.append(thread)

    for thread in threads:
        thread.start()
    
    for thread in threads:
        thread.join()




if __name__ == "__main__":
    main()
    
 