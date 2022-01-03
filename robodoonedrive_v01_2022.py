# -*- encoding: utf-8 -*-
import os.path
import shutil
from datetime import datetime
import pandas as pd
import win32api
from subprocess import call

start = datetime.now()

def listardiretorios(path):
    listadediretorios = []
    print('Iniciando listagem de diretorios')
    for root, dirs, files in os.walk(path):  # PARA cada raiz, diretorio, NO arvore gerada a partir do diretorio da central de notas
        root_sem_prefixo = root.replace(str(path), "")
        for dir in dirs:  # PARA cada diretorio na lista de diretorios
            listadediretorios.append(os.path.join(root_sem_prefixo, dir))  # raiz do diretorio + diretorio
    return listadediretorios


def diretoriosparacriar(diretorios_do_path_origem_atual, diretorios_da_path_destino_atual):
    print('Iniciando criacao diretorios_da_path_destino_atual')
    diretorios_para_criar_list = []
    for item in diretorios_do_path_origem_atual:
        if item not in diretorios_da_path_destino_atual:
            # print('criar diretorio: ', item)
            diretorios_para_criar_list.append(item)
    print('total de diretorios_para_criar_na_fase_atual: ', len(diretorios_para_criar_list))
    return diretorios_para_criar_list


def criardiretorios(path_destino_atual, diretoriosparacriar_list):
    for diretoriosparacriar in diretoriosparacriar_list:
        nome_do_novo_diretorio = path_destino_atual + "\\" + diretoriosparacriar
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
        ultimo_id_do_report = df['id'].max()
        if str(ultimo_id_do_report) == "nan":
            ultimo_id_do_report = 0
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
centraldosrobos_path = r'F:\robodepdfs\centraldosrobos'
temp_original_path = r'F:\robodepdfs\temp_original'
temp_individualizados_path = r'F:\robodepdfs\temp_individualizados'

reportdosrobos_erros = r'F:\robodepdfs\reports\errosdosrobos.csv'
report_robodoonedrive = r'F:\robodepdfs\reports\robodoonedrive.csv'
report_robodospdfs = r'F:\robodepdfs\reports\robodospdfs.csv'
report_robodeindividualizacao = r'F:\robodepdfs\reports\robodeindividualizacao.csv'


path_origem_atual = onedrive_path
path_destino_atual = centraldosrobos_path
reportdafaseatual = report_robodoonedrive
reportdafaseanterior = None

start = datetime.now()
## TRATAMENTO DE FOLDERS
# Clonando estrutura de pastas da Central no OneDrive para a Central do Robo na Rede
diretorios_do_path_origem_atual = listardiretorios(path_origem_atual)  # listar estrutura de pasta da Central de Notas no OneDrive
diretorios_da_path_destino_atual = listardiretorios(path_destino_atual)  # listar estrutura de pasta na central do robo na rede
diretoriosparacriar_list = diretoriosparacriar(diretorios_do_path_origem_atual, diretorios_da_path_destino_atual)  # criar pastas na central dos robos
if diretoriosparacriar_list != 0:
    criardiretorios(path_destino_atual, diretoriosparacriar_list)

## TRATAMENTO DE ARQUIVOS
# Listando arquivos na Central do OneDrive
arquivosdoonedrive_list = listararquivosnaspastas(path_origem_atual)  # listar arquivos na Central de Notas do OneDrive
arquivosjacopiados_list = arquivosjacopiados(reportdafaseatual)
robodoonedrive_report_list = arquivosjacopiados_list[0]  # listando arquivos já registrados no report
ultimo_id_do_report = arquivosjacopiados_list[1]  # pegando o último id já registrado no report do robodoonedrive

# criando lista de arquivos do onedrive ainda não registrados no report do robo
print('Iniciando listagem de arquivosnaocopiados')
arquivosnaocopiados_list = []
for arquivos in arquivosdoonedrive_list:
    if arquivos.replace(path_origem_atual, '') not in robodoonedrive_report_list:
        arquivosnaocopiados_list.append(arquivos)
print('total de serem processados: ', len(arquivosnaocopiados_list))

# criando lista de não copiados com sufixo da central de nota: isso ajuda a identificar o destino
arquivosnaocopiados_comsufixodacentral_list = []
for arquivosnaocopiados in arquivosnaocopiados_list:
    arquivosnaocopiados_comsufixodacentral_list.append(arquivosnaocopiados.replace(path_origem_atual, path_destino_atual))

# iniciando looping de cópia de arquivos da Central do OneDrive para a Central do Robo
n = 0
e = 0
id = ultimo_id_do_report

for arquivosnaocopiados_comsufixodacentral in arquivosnaocopiados_comsufixodacentral_list:
    arquivo_do_onedrive = arquivosnaocopiados_comsufixodacentral.replace(path_destino_atual, path_origem_atual)  # reincluio o sufixo do onedrive, como origem do arquivo a ser copiado
    try:
        destino = os.path.dirname(os.path.abspath(arquivosnaocopiados_comsufixodacentral))
        copyingfiles(arquivo_do_onedrive, destino)
        id += 1
        action_list = [id, "", datetime.now(), 'robodoonedrive', 'onedrive to centraldenotas', arquivo_do_onedrive.replace(path_origem_atual, ''), arquivosnaocopiados_comsufixodacentral]
        uploadingReport(action_list, reportdafaseatual)
        print(n, 'Processado id: ', id, 'serie: ', '')
        n += 1
    except:
        try:  # TENTANDO NOVAMENTE, MAS COM REDUCAO DO NOME DO DIRETORIO
            destino = os.path.dirname(os.path.abspath(arquivosnaocopiados_comsufixodacentral))
            copyingfiles("\\\\?\\" + arquivo_do_onedrive, "\\\\?\\" + destino)
            id += 1
            action_list = [id, "", datetime.now(), 'robodoonedrive', 'onedrive to centraldenotas',arquivo_do_onedrive.replace(path_origem_atual, ''), arquivosnaocopiados_comsufixodacentral]
            uploadingReport(action_list, reportdafaseatual)
            print(n, 'Processado id: ', id, 'serie: ', '')
            n += 1
        except:
            try:  # TENTANDO NOVAMENTE, MAS COM OUTRA TECNICA DE REDUCAO DO NOME DO DIRETORIO
                destino = os.path.dirname(os.path.abspath(arquivosnaocopiados_comsufixodacentral))  # pega o diretorio do arquivo, sem o nome
                destino_curto = win32api.GetShortPathName(destino)  # deixa o diretorio do arquivo menor

                filename = arquivo_do_onedrive.split('\\')[-1]  # pega o nome do arquivo
                arquivo_do_onedrive_curto = os.path.dirname(os.path.abspath(arquivo_do_onedrive))  # pega o diretorio do arquivo, sem o nome
                arquivo_do_onedrive_curto = win32api.GetShortPathName(arquivo_do_onedrive_curto)  # deixa o diretorio do arquivo menor
                arquivo_do_onedrive_curto = arquivo_do_onedrive_curto + '\\' + filename  # remonta a origem: diretorio menor + nome do arquivo

                copyingfiles("\\\\?\\" + arquivo_do_onedrive_curto, "\\\\?\\" + destino_curto)
                id += 1
                action_list = [id, "", datetime.now(), 'robodoonedrive', 'onedrive to centraldenotas', arquivo_do_onedrive.replace(path_origem_atual, ''), arquivosnaocopiados_comsufixodacentral]
                uploadingReport(action_list, reportdafaseatual)
                print(n, 'Processado id: ', id, 'serie: ', '')
                n += 1
            except:
                try:  # TENTANDO NOVAMENTE, MAS COM OUTRA TECNICA DE REDUCAO DO NOME DO DIRETORIO (robocopy)
                    destiny_path = os.path.dirname(os.path.abspath(arquivosnaocopiados_comsufixodacentral))  # pega o diretorio do arquivo, sem o nome
                    origin_path = os.path.dirname(os.path.abspath(arquivo_do_onedrive))  # pega o diretorio do arquivo, sem o nome
                    filename = arquivo_do_onedrive.split('\\')[-1]  # pega o nome do arquivo
                    call(["robocopy",
                          "{origin}".format(origin=origin_path),
                          "{destiny}".format(destiny=destiny_path),
                          "{filename}".format(filename=filename),
                          "/z"])

                    id += 1
                    action_list = [id, "", datetime.now(), 'robodoonedrive', 'onedrive to centraldenotas', arquivo_do_onedrive.replace(path_origem_atual, ''), arquivosnaocopiados_comsufixodacentral]
                    uploadingReport(action_list, reportdafaseatual)
                    print(n, 'Processado id: ', id, 'serie: ', '')
                    n += 1
                except:
                    action_list = [id, "", datetime.now(), 'robodoonedrive', 'ERROR: onedrive to centraldenotas', arquivo_do_onedrive, arquivosnaocopiados_comsufixodacentral]
                    uploadingReportError(action_list, reportdosrobos_erros)
                    print('ERROR: Report de erro dos robos atualizado com sucesso: ', id, "diretorio: ", arquivo_do_onedrive)
                    e += 1
print('Total de arquivos no onedrive: ', len(arquivosdoonedrive_list))
print('Total de arquivos antigos no report: ', ultimo_id_do_report)
print('Total de arquivos novos copiados para o report: ', n)
print('Total de erros: ', e)
end = datetime.now()
print('time running copyingfiles: ', end-start)

# converter relatorio em base64 e salvar backup no mongodb