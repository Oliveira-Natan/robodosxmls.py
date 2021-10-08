from datetime import datetime
import os
import pandas as pd

def criaReports(path_report, reportrobodeindividualizacao, reportdosrobos_erros, reportrobodospdfs, reportrobodosemails, reportrobodoarquivei):
    if os.path.exists(path_report + reportrobodospdfs):
        robo_data = pd.read_csv(path_report + reportrobodospdfs)
        print("Report do robo de pdfs existente")
    else:
        robo_data = pd.DataFrame(columns=['time', 'nomedorobo', 'acao', 'path'])
        robo_data.to_csv(path_report + reportrobodospdfs, index=False)
        print("Report do robo de pdfs criado")

    if os.path.exists(path_report + reportrobodosemails):
        robo_data = pd.read_csv(path_report + reportrobodosemails)
        print("Report do robo de emails existente")
    else:
        robo_data = pd.DataFrame(columns=['time', 'nomedorobo', 'acao', 'path'])
        robo_data.to_csv(path_report + reportrobodosemails, index=False)
        print("Report do robo de emails criado")

    if os.path.exists(path_report + reportrobodeindividualizacao):
        robo_data = pd.read_csv(path_report + reportrobodeindividualizacao)
        print("Report do robo de individualizacao existente")
    else:
        robo_data = pd.DataFrame(columns=['time', 'nomedorobo', 'acao', 'path'])
        robo_data.to_csv(path_report + reportrobodeindividualizacao, index=False)
        print("Report do robo de individualizacao criado")

    if os.path.exists(path_report + reportrobodoarquivei):
        robo_data = pd.read_csv(path_report + reportrobodoarquivei)
        print("Report do robo do arquivei existente")
    else:
        robo_data = pd.DataFrame(columns=['time', 'nomedorobo', 'acao', 'path'])
        robo_data.to_csv(path_report + reportrobodoarquivei, index=False)
        print("Report do robo do arquivei criado")

    if os.path.exists(path_report + reportdosrobos_erros):
        robo_data_error = pd.read_csv(path_report + reportdosrobos_erros)
        print("Report dos erros dos robos existente")
    else:
        robo_data_error = pd.DataFrame(columns=['time', 'nomedorobo', 'acao', 'path'])
        robo_data_error.to_csv(path_report + reportdosrobos_erros, index=False)
        print("Report dos erros dos robos criado")

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
path_report = r"C:\Users\felipe.rosa\Desktop\New folder\report"
path_centraldenotas = r'C:\Users\felipe.rosa\Desktop\centraldenotas'
path_temp_original = r'C:\Users\felipe.rosa\Desktop\New folder\temp_original'
path_temp_individualizados = r'C:\Users\felipe.rosa\Desktop\New folder\temp_individualizados'
path_temp_individualizados_enviados = r'C:\Users\felipe.rosa\Desktop\New folder\temp_individualizados_enviados'
path_arquivei = r'C:\Users\felipe.rosa\Desktop\arquivei'
path_cloudFiscal = r'C:\Users\felipe.rosa\Desktop\cloudfiscal_fit'

# reports names
reportrobodeindividualizacao = '\\robodeindividualizacao_' + str(currentYear) + '_' + str(currentMonth) + '.csv'
reportdosrobos_erros = '\\errosdosrobos_' + str(currentYear) + '_' + str(currentMonth) + '.csv'
reportrobodospdfs = '\\robodospdfs_' + str(currentYear) + '_' + str(currentMonth) + '.csv'
reportrobodosemails = '\\robodosemails_' + str(currentYear) + '_' + str(currentMonth) + '.csv'
reportrobodoarquivei = '\\robodoarquivei_' + str(currentYear) + '_' + str(currentMonth) + '.csv'

# start process
criaReports(path_report, reportrobodeindividualizacao, reportdosrobos_erros, reportrobodospdfs, reportrobodosemails, reportrobodoarquivei)
