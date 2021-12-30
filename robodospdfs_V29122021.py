# -*- encoding: utf-8 -*-
import os.path
import shutil
from datetime import datetime
import pandas as pd

# path_centraldenotas = r'C:\Users\felipe.rosa\Desktop\rede\CentralDeNotas'
# for root, dirs, files in os.walk(path_centraldenotas):  # PARA cada raiz, diretorio, NO arvore gerada a partir do diretorio da central de notas
#     # for dir in dirs:  # PARA cada diretorio na lista de diretorios
#     #     print(os.path.join(root, dir))  # raiz do diretorio + diretorio
#
#     for file in files:  # PARA cada arquivo na lista de arquivos
#         print(os.path.join(root, file))  # raiz do diretorio + nome do arquivo

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

def arquivosjacopiados(reportrobodospdfs):
    print('Iniciando listagem de arquivosjacopiados')
    df = pd.read_csv(reportrobodospdfs)
    list_of_path_file_reportrobodospdfs = df['path'].to_list()  # quero a coluna do report onde registrei a origem do que já copiei da central de notas
    print('total de arquivosjacopiados: ', len(list_of_path_file_reportrobodospdfs))
    return list_of_path_file_reportrobodospdfs

def arquivosdoonedrive(reportrobodoonedrive):
    print('Iniciando listagem de arquivosdoonedrive')
    df = pd.read_csv(reportrobodoonedrive)
    list_of_path_file_reportrobodoonedrive = df.loc[:, ['id', 'destiny']].values.tolist()  # quero a coluna do report do onedrive onde registrei o destino da copia na central
    print('total de arquivosjacopiados: ', len(list_of_path_file_reportrobodoonedrive))
    return list_of_path_file_reportrobodoonedrive

def arquivosnacentral(path_centraldenotas):
    print('Iniciando listagem de arquivos arquivosnacentral')
    list_of_path_of_files_centraldenotas = []
    for root, dirs, files in os.walk(path_centraldenotas):  # PARA cada raiz, diretorio, NO arvore gerada a partir do diretorio da central de notas
        files_list = []
        for file in files:  # PARA cada arquivo na lista de arquivos
            if file.upper().endswith(".PDF"):
                files_list.append(os.path.join(root, file))
                list_of_path_of_files_centraldenotas.append(os.path.join(root, file))  # inclui na lista a raiz do diretorio + nome do arquivo
        print(len(files_list), ";", root)
    print('total de arquivosnacentral: ', len(list_of_path_of_files_centraldenotas))
    return list_of_path_of_files_centraldenotas

def arquivosparacopiar(list_of_path_file_reportrobodospdfs, list_of_path_of_files_do_reportdorobodoonedrive):
    print('Iniciando listagem de arquivosparacopiar')
    path_files_to_copy = []
    for id, item in list_of_path_of_files_do_reportdorobodoonedrive:
        if item not in list_of_path_file_reportrobodospdfs:
            path_files_to_copy.append([id, item])
    print('total de arquivosparacopiar: ', len(path_files_to_copy))
    return path_files_to_copy

def copyingFiles(file_in_centraldenotas, path_temp_original):
    shutil.copy(file_in_centraldenotas, path_temp_original)  # copying pdfs from CentraldeNotas to temp_original
    print('copied from central_de_notas to temp_original: ', file_in_centraldenotas)

# path and reports names
path_centraldenotas = r'C:\Users\felipe.rosa\Desktop\rede\centraldosrobos'
path_temp_original = r'C:\Users\felipe.rosa\Desktop\rede\robodepdfs\temp_original'
reportrobodoonedrive = r'C:\Users\felipe.rosa\Desktop\rede\robodepdfs\reports\robodoonedrive.csv'
reportdosrobos_erros = r'C:\Users\felipe.rosa\Desktop\rede\robodepdfs\reports\errosdosrobos.csv'
reportrobodospdfs = r'C:\Users\felipe.rosa\Desktop\rede\robodepdfs\reports\robodospdfs.csv'

# starting process
list_of_path_file_reportrobodospdfs = arquivosjacopiados(reportrobodospdfs)  # listar arquivos ja copiados
list_of_path_file_reportrobodoonedrive = arquivosdoonedrive(reportrobodoonedrive)  # listar arquivos do relatorio do onedrive
arquivosparacopiar_list = arquivosparacopiar(list_of_path_file_reportrobodospdfs, list_of_path_file_reportrobodoonedrive)  # listar arquivos pendentes de copia

n = 0
e = 0
if len(arquivosparacopiar_list) > 0:
    # iniciar copia
    for id, arquivosparacopiar in arquivosparacopiar_list:
        try:
            copyingFiles(arquivosparacopiar, path_temp_original)
            action_list = [id, datetime.now(), 'robodospdfs', 'centraldenotas to temp_original', arquivosparacopiar, arquivosparacopiar.replace(path_centraldenotas, path_temp_original)]
            uploadingReport(action_list, reportrobodospdfs)
            print('Report do Robo dos Pdfs atualizado com sucesso')
            n += 1
        except:
            action_list = [datetime.now(), 'robodospdfs', 'ERROR: centraldenotas to temp_original', arquivosparacopiar]
            uploadingReportError(action_list, reportdosrobos_erros)
            print('ERROR: Report de erro dos robos atualizado com sucesso: ', arquivosparacopiar)
            e += 1
else:
    print('Não há arquivos novos a serem copiados')
print('Total de arquivos na central conforme reportdorobodoonedrive: ', len(arquivosparacopiar_list))
print('Total de arquivos antigos no report: ', len(list_of_path_file_reportrobodospdfs))
print('Total de arquivos novos copiados para o report: ', n)
print('Total de erros: ', e)