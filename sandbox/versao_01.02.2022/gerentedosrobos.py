import os
from datetime import datetime
import pandas as pd
import time

def centralparatemporiginal(path_centraldenotas, path_report, reportrobodospdfs):
    df = pd.read_csv(path_report + reportrobodospdfs)
    list_of_path_file_reportrobodospdfs = df['path'].to_list()

    # listing files path on CentraldeNotas
    list_of_path_of_files_centraldenotas = []
    path_centraldenotas_year = path_centraldenotas + '\\' + str(currentYear)  # ..\CentraldeNotas\\2021\\Empresa01\\08'
    paths_centraldenotas = [f.path + '\\' + str(currentMonth) for f in os.scandir(path_centraldenotas_year) if f.is_dir()]  # listing folders names with current month
    for path_centraldenotas in paths_centraldenotas:  # accessing each folder on CentraldeNotas
        for root, dirs, files in os.walk(path_centraldenotas):
            for file in files:
                list_of_path_of_files_centraldenotas.append(os.path.join(root, file))

    path_files_to_copy = [value for value in list_of_path_of_files_centraldenotas if value not in list_of_path_file_reportrobodospdfs]
    return len(path_files_to_copy)


def cloudparamcsretencao(path_cloudfiscalparamcsretencao, path_report, reportrobodocloudparamcsretencao):
    df = pd.read_csv(path_report + reportrobodocloudparamcsretencao)
    list_of_path_file_reportrobodocloudparamcsretencao = df['path'].to_list()

    # listing files path on cloudfiscal na rede
    list_of_path_of_files_cloudparamcsretencao= []
    paths_cloudfiscal = [f.path + '\\' + str(currentYear) for f in os.scandir(path_cloudfiscalparamcsretencao) if f.is_dir()]  # listing folders names with current month
    for path_cloudfiscal in paths_cloudfiscal:  # accessing each folder on CentraldeNotas
        for root, dirs, files in os.walk(path_cloudfiscal):
            for file in files:
                list_of_path_of_files_cloudparamcsretencao.append(os.path.join(root, file))

    path_files_to_copy = [value for value in list_of_path_of_files_cloudparamcsretencao if value not in list_of_path_file_reportrobodocloudparamcsretencao]
    return len(path_files_to_copy)

def arquiveiparamcsretencao(path_arquivei, path_report, reportrobodoarquivei):
    df = pd.read_csv(path_report + reportrobodoarquivei)
    list_of_path_file_reportrobodoarquivei = df['path'].to_list()

    # listing files path on arquivei na rede
    list_of_path_of_files_arquivei= []
    # path_arquivei_subfolder = path_arquivei + '\\' + 'Nfse' + '\\' + 'Recebido' + '\\' + str(currentYear)  # ..\CentraldeNotas\\2021\\Empresa01\\08'
    paths_arquivei = [f.path + '\\' + 'Nfse' + '\\' + 'Recebido' + '\\' + str(currentYear) for f in os.scandir(path_arquivei) if f.is_dir()]  # listing folders names with current month
    for path_arquivei in paths_arquivei:  # accessing each folder on CentraldeNotas
        for root, dirs, files in os.walk(path_arquivei):
            for file in files:
                list_of_path_of_files_arquivei.append(os.path.join(root, file))

    path_files_to_copy = [value for value in list_of_path_of_files_arquivei if value not in list_of_path_file_reportrobodoarquivei]
    return len(path_files_to_copy)

# defining year, month and day
currentDay = datetime.now().day
if currentDay < 10:
    currentDay = '0' + str(currentDay)
else:
    currentDay = str(currentDay)

currentMonth = datetime.now().month
if currentMonth < 10:
    currentMonth = '0' + str(currentMonth)
else:
    currentMonth = str(currentMonth)

currentYear = datetime.now().year

# main paths
path_report = r"F:\robodepdfs\reports"
path_centraldenotas = r'F:\CentralDeNotas'
path_temp_original = r'F:\robodepdfs\temp_original'
path_temp_individualizados = r'F:\robodepdfs\temp_individualizados'
path_temp_individualizados_enviados = r'F:\robodepdfs\temp_individualizados_enviados'
path_arquivei = r'F:\Fiscal\Clientes Fiscal\Arquivei - Armazenamento de XML'
path_cloudFiscal = r'F:\Impostos Retidos\Conversor FIT'
path_cloudfiscalparamcsretencao = r'F:\Impostos Retidos\FIT_XML_TERCEIRO'

# reports names
reportrobodeindividualizacao = '\\robodeindividualizacao_' + str(currentYear) + '_' + str(currentMonth) + '.csv'
reportdosrobos_erros = '\\errosdosrobos_' + str(currentYear) + '_' + str(currentMonth) + '.csv'
reportrobodospdfs = '\\robodospdfs_' + str(currentYear) + '_' + str(currentMonth) + '.csv'
reportrobodosemails = '\\robodosemails_' + str(currentYear) + '_' + str(currentMonth) + '.csv'
reportrobodoarquivei = '\\robodoarquivei_' + str(currentYear) + '_' + str(currentMonth) + '.csv'
reportrobodocloudparamcsretencao = '\\robodocloudparamcsretencao_' + str(currentYear) + '_' + str(currentMonth) + '.csv'

# path dos robos
path_robodospdfs = r'C:\Users\felipe.rosa\Desktop\robodospdfs.exe'
path_robodeindividualizacao = r'C:\Users\felipe.rosa\Desktop\robodeindividualizacao.exe'
path_robodosemails = r'C:\Users\felipe.rosa\Desktop\robodosemails.exe'
path_robodocloudparamcsretencao = r'C:\Users\felipe.rosa\Desktop\robodocloudparamcsretencao.exe'
path_robodoarquivei = r'C:\Users\felipe.rosa\Desktop\robodoarquivei.exe'

# starting process
time_to_next_process = 60*3  # sec*(min)

while True:
    if centralparatemporiginal(path_centraldenotas, path_report, reportrobodospdfs) != 0:
        print('executando robo dos pdfs')
        os.startfile(path_robodospdfs)
    else:
        print('não foi necessário executar o robo dos pfs')
    time.sleep(time_to_next_process)

    if len(os.listdir(path_temp_original)) != 0:
        print('executando robo de individualização')
        os.startfile(path_robodeindividualizacao)
    else:
        print('não foi necessário executar o robo de individualização')
    time.sleep(time_to_next_process)

    if len(os.listdir(path_temp_individualizados)) != 0:
        print('executando robo dos emails')
        os.startfile(path_robodosemails)
    else:
        print('não foi necessário executar o robo dos emails')
    time.sleep(time_to_next_process)

    if cloudparamcsretencao(path_cloudfiscalparamcsretencao, path_report, reportrobodocloudparamcsretencao) != 0:
        print('executando robo do cloud para retencao')
        os.startfile(path_robodocloudparamcsretencao)
    else:
        print('não foi necessário executar o robo do cloud para retencao')
    time.sleep(time_to_next_process)

    if arquiveiparamcsretencao(path_arquivei, path_report, reportrobodoarquivei) != 0:
        print('executando robo do arquivei')
        os.startfile(path_robodoarquivei)
    else:
        print('não foi necessário executar o robo do arquivei')
    time.sleep(time_to_next_process)