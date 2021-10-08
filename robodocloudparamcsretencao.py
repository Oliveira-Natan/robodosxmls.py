from PyPDF2 import PdfFileReader, PdfFileWriter
import os.path
import shutil
from datetime import datetime
import pandas as pd

start = datetime.now()
def uploadingReport(action_list, reportrobodocloudparamcsretencao):
    robo_data = pd.read_csv(path_report + reportrobodocloudparamcsretencao)

    # appending action to reportdosrobos
    action_list = pd.Series(action_list, index=robo_data.columns)
    robo_data = robo_data.append(action_list, ignore_index=True)
    robo_data.to_csv(path_report + reportrobodocloudparamcsretencao, index=False)
    robo_data = pd.read_csv(path_report + reportrobodocloudparamcsretencao)

def uploadingReportError(action_list, reportdosrobos_erros):
    robo_data_error = pd.read_csv(path_report + reportdosrobos_erros)

    # appending error to reportdosrobos_erros
    action_list = pd.Series(action_list, index=robo_data_error.columns)
    robo_data_error = robo_data_error.append(action_list, ignore_index=True)
    robo_data_error.to_csv(path_report + reportdosrobos_erros, index=False)
    robo_data_error = pd.read_csv(path_report + reportdosrobos_erros)

def listingfilestocopy(path_cloudfiscalparamcsretencao, path_report, reportrobodocloudparamcsretencao):
    df = pd.read_csv(path_report + reportrobodocloudparamcsretencao)
    list_of_path_file_reportrobodocloudparamcsretencao = df['path'].to_list()

    # listing files path on cloudfiscal na rede
    print('listing files path on cloudfiscal na rede')
    list_of_path_of_files_cloudparamcsretencao= []
    paths_cloudfiscal = [f.path + '\\' + str(currentYear) for f in os.scandir(path_cloudfiscalparamcsretencao) if f.is_dir()]  # listing folders names with current month
    for path_cloudfiscal in paths_cloudfiscal:  # accessing each folder on CentraldeNotas
        for root, dirs, files in os.walk(path_cloudfiscal):
            for file in files:
                list_of_path_of_files_cloudparamcsretencao.append(os.path.join(root, file))

    path_files_to_copy = [value for value in list_of_path_of_files_cloudparamcsretencao if value not in list_of_path_file_reportrobodocloudparamcsretencao]
    print('CONCLUDED: listing files path on cloudfiscal na rede')
    return path_files_to_copy

def cloudparamcsretencao(list_filestocopy):
    shutil.copy(list_filestocopy, path_cloudFiscal)  # copying pdfs from CentraldeNotas to temp_original
    print('copied from cloudfiscal para mcsretencao: ', list_filestocopy)

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

# start process
try:
    list_filestocopy = listingfilestocopy(path_cloudfiscalparamcsretencao, path_report, reportrobodocloudparamcsretencao)
    if len(list_filestocopy) != 0:
        for file_in_cloudfiscal in list_filestocopy:  # for each file to copy from CentraldeNotas to temp_original
            try:
                cloudparamcsretencao(file_in_cloudfiscal)
                action_list = [datetime.now(), 'robodocloudparamcsretencao', 'cloud para mcsretencao', file_in_cloudfiscal]
                uploadingReport(action_list, reportrobodocloudparamcsretencao)
                print('Report do Robo do Cloud para MCSRetencao atualizado com sucesso')
            except:
                action_list = [datetime.now(), 'robodocloudparamcsretencao', 'ERROR: cloud para mcsretencao', file_in_cloudfiscal]
                uploadingReportError(action_list)
                print('ERROR: Report de erro dos robos atualizado com sucesso')
    else:
        print('Não há arquivos novos a serem copiados')
except:
    action_list = [datetime.now(), 'robodocloudparamcsretencao', 'ERROR: problemas ao listar arquivos do cloud na rede', path_cloudfiscalparamcsretencao]
    uploadingReportError(action_list, reportdosrobos_erros)
    print('ERROR: Report de erro dos robos atualizado com sucesso (problemas ao listar arquivos do cloud na rede)')

end = datetime.now()
print(end-start)
