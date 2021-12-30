# -*- encoding: utf-8 -*-
import os.path
import shutil
from datetime import datetime
import pandas as pd


def listardiretorios(path):
    listadediretorios = []
    print('Iniciando listagem de diretorios')
    for root, dirs, files in os.walk(
            path):  # PARA cada raiz, diretorio, NO arvore gerada a partir do diretorio da central de notas
        root_sem_prefixo = root.replace(str(path), "")
        for dir in dirs:  # PARA cada diretorio na lista de diretorios
            listadediretorios.append(os.path.join(root_sem_prefixo, dir))  # raiz do diretorio + diretorio
    return listadediretorios


def diretoriosparacriar(diretorios_do_onedrive, diretorios_da_central):
    print('Iniciando criacao de diretorios na central')
    diretorios_para_criar_list = []
    for item in diretorios_do_onedrive:
        if item not in diretorios_da_central:
            # print('criar diretorio: ', item)
            diretorios_para_criar_list.append(item)
    print('total de arquivosparacopiar: ', len(diretorios_para_criar_list))
    return diretorios_para_criar_list


def criardiretorios(path_centraldenotas, diretoriosparacriar_list):
    for diretoriosparacriar in diretoriosparacriar_list:
        nome_do_novo_diretorio = path_centraldenotas + "\\" + diretoriosparacriar
        os.makedirs(nome_do_novo_diretorio)
        print('Criado o diretorio: ', nome_do_novo_diretorio)

def listararquivosnaspastas(path):
    print('Iniciando listagem de arquivos arquivosnacentral')
    listadediretorios = []
    for root, dirs, files in os.walk(path):  # PARA cada raiz, diretorio, NO arvore gerada a partir do diretorio da central de notas
        files_list = []
        for file in files:  # PARA cada arquivo na lista de arquivos
            nome_arquivo_maiusculo = file.upper()
            if file.upper().endswith(".PDF"):
                files_list.append(os.path.join(root, file))
                listadediretorios.append(os.path.join(root, file))  # inclui na lista a raiz do diretorio + nome do arquivo
        # print(len(files_list), ";", root)
    print('total de arquivosnacentral: ', len(listadediretorios))
    return listadediretorios

def arquivosjacopiados(reportrobodospdfs):
    print('Iniciando listagem de arquivosjacopiados')
    df = pd.read_csv(reportrobodospdfs)
    robodoonedrive_path_list = df['path'].to_list()
    try:
        ultimo_id_do_report = df['id'].iloc[-1]
    except:
        ultimo_id_do_report = 0
        robodoonedrive_path_list = []
    print('total de arquivosjacopiados: ', len(robodoonedrive_path_list))
    return robodoonedrive_path_list, ultimo_id_do_report

def copyingfiles(arquivo_do_onedrive, destino_na_central):
    shutil.copy(arquivo_do_onedrive, destino_na_central)  # copying pdfs from CentraldeNotas to temp_original

def uploadingReport(action_list, reportrobodospdfs):
    robo_data = pd.read_csv(reportrobodospdfs)
    action_list = pd.Series(action_list, index=robo_data.columns)  # convertendo lista de acao em serie
    robo_data = robo_data.append(action_list, ignore_index=True)  # appending serie no report
    robo_data.to_csv(reportrobodospdfs, index=False)  # salvando report

def uploadingReportError(action_list, reportdosrobos_erros):
    robo_data_error = pd.read_csv(reportdosrobos_erros)
    action_list = pd.Series(action_list, index=robo_data_error.columns)  # convertendo lista de acao em serie
    robo_data_error = robo_data_error.append(action_list, ignore_index=True)  # appending serie no report
    robo_data_error.to_csv(reportdosrobos_erros, index=False)  # salvando report


# path and reports names
onedrive_path = r'C:\Users\felipe.rosa\OneDrive - MCS MARKUP AUDITORIA E CONSULTORIA EMPRESARIAL LTDA\CentraldeNotas'
centraldenotasdosrobos_path = r'C:\Users\felipe.rosa\Desktop\rede\centraldosrobos'
reportdosrobos_erros = r'C:\Users\felipe.rosa\Desktop\rede\robodepdfs\reports\errosdosrobos.csv'
reportrobodoonedrive = r'C:\Users\felipe.rosa\Desktop\rede\robodepdfs\reports\robodoonedrive.csv'
start = datetime.now()

## TRATAMENTO DE FOLDERS
# Clonando estrutura de pastas da Central no OneDrive para a Central do Robo na Rede
diretorios_do_onedrive = listardiretorios(onedrive_path)  # listar estrutura de pasta da Central de Notas no OneDrive
diretorios_da_central = listardiretorios(centraldenotasdosrobos_path)  # listar estrutura de pasta na central do robo na rede
diretoriosparacriar_list = diretoriosparacriar(diretorios_do_onedrive, diretorios_da_central)  # criar pastas na central dos robos
if diretoriosparacriar_list != 0:
    criardiretorios(centraldenotasdosrobos_path, diretoriosparacriar_list)

## TRATAMENTO DE ARQUIVOS
# Listando arquivos na Central do OneDrive
arquivosdoonedrive_list = listararquivosnaspastas(onedrive_path)  # listar arquivos na Central de Notas do OneDrive
robodoonedrive_report_list = arquivosjacopiados(reportrobodoonedrive)[0]  # listando arquivos já registrados no report
ultimo_id_do_report = arquivosjacopiados(reportrobodoonedrive)[1]  # pegando o último id já registrado no report do robodoonedrive

# criando lista de arquivos do onedrive ainda não registrados no report do robo
arquivosnaocopiados_list = []
for arquivos in arquivosdoonedrive_list:
    if arquivos.replace(onedrive_path, '') not in robodoonedrive_report_list:
        arquivosnaocopiados_list.append(arquivos)

# criando lista de não copiados com sufixo da central de nota: isso ajuda a identificar o destino
arquivosnaocopiados_comsufixodacentral_list = []
for arquivosnaocopiados in arquivosnaocopiados_list:
    arquivosnaocopiados_comsufixodacentral_list.append(arquivosnaocopiados.replace(onedrive_path, centraldenotasdosrobos_path))

# iniciando looping de cópia de arquivos da Central do OneDrive para a Central do Robo
n = 0
e = 0
id = ultimo_id_do_report
for arquivosnaocopiados_comsufixodacentral in arquivosnaocopiados_comsufixodacentral_list:
    arquivo_do_onedrive = arquivosnaocopiados_comsufixodacentral.replace(centraldenotasdosrobos_path, onedrive_path)  # reincluio o sufixo do onedrive, como origem do arquivo a ser copiado
    try:
        destino = os.path.dirname(os.path.abspath(arquivosnaocopiados_comsufixodacentral))
        copyingfiles(arquivo_do_onedrive, destino)
        id += 1
        action_list = [id, datetime.now(), 'robodoonedrive', 'onedrive to centraldenotas', arquivo_do_onedrive.replace(onedrive_path, ''), arquivosnaocopiados_comsufixodacentral]
        uploadingReport(action_list, reportrobodoonedrive)
        print(n, 'Report do robodoonedrive atualizado com sucesso: ', arquivo_do_onedrive)
        n += 1
    except:
        action_list = [datetime.now(), 'robodoonedrive', 'ERROR: onedrive to centraldenotas', arquivo_do_onedrive]
        uploadingReportError(action_list, reportdosrobos_erros)
        print('ERROR: Report de erro dos robos atualizado com sucesso: ', arquivo_do_onedrive)
        e += 1
print('Total de arquivos no onedrive: ', len(arquivosdoonedrive_list))
print('Total de arquivos antigos no report: ', ultimo_id_do_report)
print('Total de arquivos novos copiados para o report: ', n)
print('Total de erros: ', e)
end = datetime.now()
print('time running copyingfiles: ', end-start)
