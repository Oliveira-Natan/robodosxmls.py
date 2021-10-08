from PyPDF2 import PdfFileReader, PdfFileWriter
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

    # listing files path on CentraldeNotas
    list_of_path_of_files_centraldenotas = []
    path_centraldenotas_year = path_centraldenotas + '\\' + str(currentYear)  # ..\CentraldeNotas\\2021\\Empresa01\\08'
    paths_centraldenotas = [f.path + '\\' + str(currentMonth) for f in os.scandir(path_centraldenotas_year) if f.is_dir()]  # listing folders names with current month
    for path_centraldenotas in paths_centraldenotas:  # accessing each folder on CentraldeNotas
        for root, dirs, files in os.walk(path_centraldenotas):
            for file in files:
                list_of_path_of_files_centraldenotas.append(os.path.join(root, file))

    path_files_to_copy = [value for value in list_of_path_of_files_centraldenotas if value not in list_of_path_file_reportrobodospdfs]
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
try:
    list_filestocopy = filestocopy(path_centraldenotas, path_report, reportrobodospdfs)
    if len(list_filestocopy) != 0:
        for file_in_centraldenotas in list_filestocopy:  # for each file to copy from CentraldeNotas to temp_original
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
