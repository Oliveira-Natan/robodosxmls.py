# -*- encoding: utf-8 -*-
import os.path
import shutil
from datetime import datetime
import pandas as pd

start = datetime.now()
def uploadingReport(action_list, reportrobodospdfs):
    robo_data = pd.read_csv(path_report + reportrobodospdfs)

    # appending action to reportdosrobos
    action_list = pd.Series(action_list, index=robo_data.columns)
    robo_data = robo_data.append(action_list, ignore_index=True)
    robo_data.to_csv(path_report + reportrobodospdfs, index=False)
    robo_data = pd.read_csv(path_report + reportrobodospdfs)

def uploadingReportError(action_list, reportdosrobos_erros):
    robo_data_error = pd.read_csv(path_report + reportdosrobos_erros)

    # appending error to reportdosrobos_erros
    action_list = pd.Series(action_list, index=robo_data_error.columns)
    robo_data_error = robo_data_error.append(action_list, ignore_index=True)
    robo_data_error.to_csv(path_report + reportdosrobos_erros, index=False)
    robo_data_error = pd.read_csv(path_report + reportdosrobos_erros)

def filestocopy(path_centraldenotas, path_report, reportrobodospdfs):
    df = pd.read_csv(path_report + reportrobodospdfs)
    list_of_path_file_reportrobodospdfs = df['path'].to_list()
    print('lista de arquivos no report do mes solicitado: ', list_of_path_file_reportrobodospdfs)
    print('total de arquivos no report: ', len(list_of_path_file_reportrobodospdfs))

    # listing files path on CentraldeNotas
    print('Iniciando listagem de arquivos na Central do mes solicitado')
    list_of_path_of_files_centraldenotas = []
    path_centraldenotas_year = path_centraldenotas + '\\' + str(currentYear)  # ..\CentraldeNotas\\2021\\Empresa01\\08'

    # for currentMonth in range(1,13):
    paths_centraldenotas = [f.path + '\\' + str(currentMonth) for f in os.scandir(path_centraldenotas_year) if f.is_dir()]  # listing folders names with current month
    for path_centraldenotas in paths_centraldenotas:  # accessing each folder on CentraldeNotas
        for root, dirs, files in os.walk(path_centraldenotas):
            for file in files:
                list_of_path_of_files_centraldenotas.append(os.path.join(root, file))
                # print('listando arquivos da central', root, file)
    print('lista de arquivos na central do mes solicitado: ', list_of_path_of_files_centraldenotas)
    print('total de arquivos na central: ', len(list_of_path_of_files_centraldenotas))
    # print(list_of_path_file_reportrobodospdfs)

    path_files_to_copy = [value for value in list_of_path_of_files_centraldenotas if value not in list_of_path_file_reportrobodospdfs]
    print('lista de arquivos para copiar do mes solicitado', path_files_to_copy)
    print('total de arquivos para copiar: ', len(path_files_to_copy))
    return path_files_to_copy

def copyingFiles(list_filestocopy):
    shutil.copy(file_in_centraldenotas, path_temp_original)  # copying pdfs from CentraldeNotas to temp_original
    print('copied from central_de_notas to temp_original: ', file_in_centraldenotas)

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

# reports names
reportrobodeindividualizacao = '\\robodeindividualizacao_' + str(currentYear) + '_' + str(currentMonth) + '.csv'
reportdosrobos_erros = '\\errosdosrobos_' + str(currentYear) + '_' + str(currentMonth) + '.csv'
reportrobodospdfs = '\\robodospdfs_' + str(currentYear) + '_' + str(currentMonth) + '.csv'
reportrobodosemails = '\\robodosemails_' + str(currentYear) + '_' + str(currentMonth) + '.csv'
reportrobodoarquivei = '\\robodoarquivei_' + str(currentYear) + '_' + str(currentMonth) + '.csv'

# start process
# listar arquivos ja copiados
# listar arquivos nas pastas
# listar arquivos pendentes de copia

# iniciar copia


try:
    list_filestocopy = filestocopy(path_centraldenotas, path_report, reportrobodospdfs)
    if len(list_filestocopy) != 0:
        for file_in_centraldenotas in list_filestocopy:  # for each file to copy from CentraldeNotas to temp_original
            print('nome do arquivo', file_in_centraldenotas)
            extentions = [".PDF", ".pdf", ".Pdf"]
            for extention in extentions:
                if file_in_centraldenotas.endswith(extention):
                    try:
                        copyingFiles(file_in_centraldenotas)
                        action_list = [datetime.now(), 'robodospdfs', 'centraldenotas to temp_original', file_in_centraldenotas]
                        uploadingReport(action_list, reportrobodospdfs)
                        print('Report do Robo dos Pdfs atualizado com sucesso')
                    except:
                        action_list = [datetime.now(), 'robodospdfs', 'ERROR: centraldenotas to temp_original', file_in_centraldenotas]
                        uploadingReportError(action_list, reportdosrobos_erros)
                        print('ERROR: Report de erro dos robos atualizado com sucesso')
    else:
        print('Não há arquivos novos a serem copiados')
except:
    action_list = [datetime.now(), 'robodospdfs', 'ERROR: problemas ao listar centraldenotas', path_centraldenotas]
    uploadingReportError(action_list, reportdosrobos_erros)
    print('ERROR: Report de erro dos robos atualizado com sucesso (problemas ao listar centraldenotas)')
end = datetime.now()
print(end-start)
