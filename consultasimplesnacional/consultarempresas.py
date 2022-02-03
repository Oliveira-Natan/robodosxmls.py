from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd
import random
from selenium.webdriver.firefox.options import Options

# Ensure mobile-friendly view for parsing
useragent = "Mozilla/5.0 (Linux; Android 8.0.0; Pixel 2 XL Build/OPD1.170816.004) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Mobile Safari/537.36"

# Firefox
# options = Options()
# options.set_preference("general.useragent.override", useragent)
# profile = webdriver.FirefoxProfile()
# profile.set_preference("general.useragent.override", useragent)
# options = webdriver.FirefoxOptions()
options = Options()
options.set_preference("general.useragent.override", useragent)
options.set_preference("dom.webnotifications.serviceworker.enabled", False)
options.set_preference("dom.webnotifications.enabled", False)

driver = webdriver.Firefox(options=options)
driver.get("http://www8.receita.fazenda.gov.br/SimplesNacional/aplicacoes.aspx?id=21")

# informe aqui a lista de cnpjs que deseja pesquisar
cnpj_list = [
    '13507760000131',
    '43786738000139',
    '01996284000180',
    '05305671000184'
]
result_list = []
erro_list = []
n = 1
round = 1
for cnpj in cnpj_list:
    try:
        time.sleep(2)
        driver.switch_to.frame(driver.find_element(By.XPATH, '//*[@id="frame"]'))  # Muda o foco para o iframe

        # preenche o cnpj
        cnpj_field = driver.find_element(By.XPATH, '//*[@id="Cnpj"]')
        cnpj_field.send_keys(cnpj)

        # clica para pesquisar o cnpj
        cnpj_field = driver.find_element(By.XPATH, '//*[@id="consultarForm"]/button').click()
        time.sleep(4)

        # capta informações do simples referentes ao cnpj
        anteriores_field = driver.find_element(By.XPATH, '/html/body/div/div[2]/div[2]/div[2]/span[1]').text
        situacao_field = driver.find_element(By.XPATH, '/html/body/div/div[2]/div[2]/div[2]/span[2]').text

        # Retorna para a janela principal (fora do iframe)
        driver.switch_to.default_content()

        # salva informações no banco de dados
        info = [cnpj, anteriores_field, situacao_field]
        result_list.append([cnpj, anteriores_field, situacao_field])
        n += 1
        round += 1
        df = pd.DataFrame(result_list)
        df.to_csv('empresasnosimples_encontrado.csv')

        # retorna a tela inicial
        driver.get("http://www8.receita.fazenda.gov.br/SimplesNacional/aplicacoes.aspx?id=21")

        # aguarda entre 10 e 15 segundos para efetuar nova pesquisa
        random_number = random.randint(10, 15)
        print(n, random_number, cnpj, anteriores_field, situacao_field)
        time.sleep(random_number)
    except:
        print('erro no cnpj: ', cnpj)
        erro_list.append(cnpj)
        df = pd.DataFrame(erro_list)
        df.to_csv('empresasnosimples_erro.csv')
        driver.close()
        time.sleep(120)
        round = 0
        driver = webdriver.Firefox(options=options)
        driver.get("http://www8.receita.fazenda.gov.br/SimplesNacional/aplicacoes.aspx?id=21")
driver.close()
