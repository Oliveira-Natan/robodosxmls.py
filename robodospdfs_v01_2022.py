# -*- encoding: utf-8 -*-
import os.path
import shutil
import time
from datetime import datetime
import pandas as pd
import win32api
from subprocess import call
import getpass

def robodospdfs():
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

    def listaarquivosjaprocessadosnafaseatual(reportdafaseatual):
        print('Iniciando listagem de listaarquivosjaprocessadosnafaseatual')
        df = pd.read_csv(reportdafaseatual)
        arquivosjaprocessadosnafaseatual_list = df['path'].to_list()  # quero a coluna do report onde registrei a origem do que já copiei da central de notas
        print('total de listaarquivosjaprocessadosnafaseatual: ', len(arquivosjaprocessadosnafaseatual_list))
        return arquivosjaprocessadosnafaseatual_list

    def listaarquivosprocessadosnafaseanterior(reportdafaseanterior):
        print('Iniciando listagem de listaarquivosprocessadosnafaseanterior')
        df = pd.read_csv(reportdafaseanterior)
        arquivosprocessadosnafaseanterior_list = df.loc[:, ['id', 'destiny']].values.tolist()  # quero a coluna do report do onedrive onde registrei o destino da copia na central
        print('total de listaarquivosprocessadosnafaseanterior: ', len(arquivosprocessadosnafaseanterior_list))
        return arquivosprocessadosnafaseanterior_list

    def listaarquivosparaprocessarnafaseatual(arquivosprocessadosnafaseanterior_list, arquivosjaprocessadosnafaseatual_list, path_origem_atual, path_destino_atual, robo_path):
        print('Iniciando listagem de listaarquivosparaprocessarnafaseatual')
        path_files_to_copy = []
        for id, item in arquivosprocessadosnafaseanterior_list:
            if item not in arquivosjaprocessadosnafaseatual_list:
                item = robo_path + item
                path_files_to_copy.append([id, item, item.replace('centraldosrobos', 'temp_original')]) # id, origem, destino
        print('total de listaarquivosparaprocessarnafaseatual: ', len(path_files_to_copy))
        return path_files_to_copy

    def processamento(origem, destino, tentativa):
        print(tentativa)
        shutil.copy(origem, destino)  # copiando pdfs da CentraldosRobos para temp_original
        # print('Copiado da centraldosrobos para temp_original: ', origem)

    def uploadingReport(action_list, reportdafaseatual):
        robo_data = pd.read_csv(reportdafaseatual)
        action_list = pd.Series(action_list, index=robo_data.columns)  # convertendo lista de acao em serie
        robo_data = robo_data.append(action_list, ignore_index=True)  # appending serie no report
        robo_data.to_csv(reportdafaseatual, index=False)  # salvando report
        time.sleep(1)

    def uploadingReportError(action_list, reportdosrobos_erros):
        robo_data_error = pd.read_csv(reportdosrobos_erros)
        action_list = pd.Series(action_list, index=robo_data_error.columns)  # convertendo lista de acao em serie
        robo_data_error = robo_data_error.append(action_list, ignore_index=True)  # appending serie no report
        robo_data_error.to_csv(reportdosrobos_erros, index=False)  # salvando report

    # path and reports names
    username = getpass.getuser()
    onedrive_path = r'C:\Users\{}\OneDrivedosRetidos\OneDrive - MCS MARKUP AUDITORIA E CONSULTORIA EMPRESARIAL LTDA\CentraldeNotas'.format(username)
    robo_path = r'C:\Users\{}\Desktop\rede\robodepdfs'.format(username)

    centraldosrobos_path = r'{}\centraldosrobos'.format(robo_path)
    temp_original_path = r'{}\temp_original'.format(robo_path)
    temp_individualizados_path = r'{}\temp_individualizados'.format(robo_path)
    temp_enviados_path = r'{}\temp_enviados'.format(robo_path)

    # reportdosrobos_erros = r'{}\reports\errosdosrobos.csv'.format(robo_path)
    # report_robodoonedrive = r'{}\reports\robodoonedrive.csv'.format(robo_path)
    # report_robodospdfs = r'{}\reports\robodospdfs.csv'.format(robo_path)
    # report_robodeindividualizacao = r'{}\reports\robodeindividualizacao.csv'.format(robo_path)
    # report_robodosemailsparaarquivei = r'{}\reports\robodosemails.csv'.format(robo_path)

    reportdosrobos_erros = r'{}\reports\errosdosrobos.csv'.format(onedrive_path)
    report_robodoonedrive = r'{}\reports\robodoonedrive.csv'.format(onedrive_path)
    report_robodospdfs = r'{}\reports\robodospdfs.csv'.format(onedrive_path)
    report_robodeindividualizacao = r'{}\reports\robodeindividualizacao.csv'.format(onedrive_path)
    report_robodosemailsparaarquivei = r'{}\reports\robodosemails.csv'.format(onedrive_path)

    reportdafaseanterior = report_robodoonedrive
    reportdafaseatual = report_robodospdfs
    path_origem_atual = centraldosrobos_path
    path_destino_atual = temp_original_path

    # ## TRATAMENTO DE FOLDERS: clonando estrutura da fase anterior para a fase atual
    # diretorios_do_path_origem_atual = listardiretorios(path_origem_atual)  # listar estrutura de pasta da fase anterior
    # diretorios_da_path_destino_atual = listardiretorios(path_destino_atual)  # listar estrutura de pasta da fase atual
    # diretoriosparacriar_list = diretoriosparacriar(diretorios_do_path_origem_atual, diretorios_da_path_destino_atual)  # identifica novas pastas na estrutura atual
    # if diretoriosparacriar_list != 0:
    #     criardiretorios(path_destino_atual, diretoriosparacriar_list)  # cria novas pastas na estrutura atual

    ## TRATAMENTO DE ARQUIVOS
    print('----------')
    arquivosjaprocessadosnafaseatual_list = listaarquivosjaprocessadosnafaseatual(reportdafaseatual)  # lista arquivosjaprocessadosnafaseatual
    print('----------')
    arquivosprocessadosnafaseanterior_list = listaarquivosprocessadosnafaseanterior(reportdafaseanterior)  # listar arquivosprocessadosnafaseanterior
    print('----------')
    arquivosparaprocessarnafaseatual_list = listaarquivosparaprocessarnafaseatual(arquivosprocessadosnafaseanterior_list, arquivosjaprocessadosnafaseatual_list, path_origem_atual, path_destino_atual, robo_path)  # listar arquivosparaprocessarnafaseatual

    n = 0
    e = 0
    if len(arquivosparaprocessarnafaseatual_list) > 0:
        # iniciar copia
        for id, origem, destino in arquivosparaprocessarnafaseatual_list:
            try:
                processamento(origem, destino, 'tentativa01')  # copiando arquivos (arquivosparaprocessarnafaseatual) da central dos robos para a temp_original (path_destino_atual)
                action_list = [id, "", datetime.now(), 'robodospdfs', 'centraldenotas to temp_original', origem.replace(robo_path, '').replace("\\?\\", "").replace("\\\\", "\\"), destino.replace(robo_path, '').replace("\\?\\", "").replace("\\\\", "\\")]
                uploadingReport(action_list, reportdafaseatual)
                print(n, 'Processado item: ', id, 'serie: ', '')
                n += 1
            except:
                try:  # TENTANDO NOVAMENTE, MAS COM REDUCAO DO NOME DO DIRETORIO
                    processamento("\\\\?\\" + origem, "\\\\?\\" + destino, 'tentativa02')
                    action_list = [id, "",  datetime.now(), 'robodospdfs', 'centraldenotas to temp_original', origem.replace(robo_path, '').replace("\\?\\", "").replace("\\\\", "\\"), destino.replace(robo_path, '').replace("\\?\\", "").replace("\\\\", "\\")]
                    uploadingReport(action_list, reportdafaseatual)
                    print(n, 'Processado item: ', id, 'serie: ', '')
                    n += 1
                except:
                    try:  # TENTANDO NOVAMENTE, MAS COM OUTRA TECNICA DE REDUCAO DO NOME DO DIRETORIO
                        destino_curto = os.path.dirname(os.path.abspath(destino))  # pega o diretorio do arquivo, sem o nome
                        destino_curto = win32api.GetShortPathName(destino_curto)  # deixa o diretorio do arquivo menor

                        filename = origem.split('\\')[-1]  # pega o nome do arquivo
                        origem_curto = os.path.dirname(os.path.abspath(origem))  # pega o diretorio do arquivo, sem o nome
                        origem_curto = win32api.GetShortPathName(origem_curto)  # deixa o diretorio do arquivo menor
                        origem_curto = origem_curto + '\\' + filename  # remonta a origem: diretorio menor + nome do arquivo

                        processamento("\\\\?\\" + origem_curto, "\\\\?\\" + destino_curto, 'tentativa03')

                        action_list = [id, "", datetime.now(), 'robodospdfs', 'centraldenotas to temp_original', origem.replace(robo_path, '').replace("\\?\\", "").replace("\\\\", "\\"), destino.replace(robo_path, '').replace("\\?\\", "").replace("\\\\", "\\")]
                        uploadingReport(action_list, reportdafaseatual)
                        print(n, 'Processado item: ', id, 'serie: ', '')
                        n += 1
                    except:
                        try:  # TENTANDO NOVAMENTE, MAS COM OUTRA TECNICA DE REDUCAO DO NOME DO DIRETORIO (robocopy)
                            print('tentativa04')
                            destiny_path = os.path.dirname(os.path.abspath(destino))  # pega o diretorio do arquivo, sem o nome
                            origin_path = os.path.dirname(os.path.abspath(origem))  # pega o diretorio do arquivo, sem o nome
                            filename = origem.split('\\')[-1]  # pega o nome do arquivo
                            call(["robocopy",
                                  "{origin}".format(origin=origin_path),
                                  "{destiny}".format(destiny=destiny_path),
                                  "{filename}".format(filename=filename),
                                  "/z"])

                            action_list = [id, "", datetime.now(), 'robodospdfs', 'centraldenotas to temp_original', origem.replace(robo_path, '').replace("\\?\\", "").replace("\\\\", "\\"), destino.replace(robo_path, '').replace("\\?\\", "").replace("\\\\", "\\")]
                            uploadingReport(action_list, reportdafaseatual)
                            print(n, 'Processado id: ', id, 'serie: ', '')
                            n += 1
                        except:
                            action_list = [id, "", datetime.now(), 'robodospdfs', 'ERROR: centraldenotas to temp_original', origem.replace(robo_path, '').replace("\\?\\", "").replace("\\\\", "\\"), destino.replace(robo_path, '').replace("\\?\\", "").replace("\\\\", "\\")]
                            uploadingReportError(action_list, reportdosrobos_erros)
                            print('ERROR: Report de erro dos robos atualizado com sucesso: ',  id, "diretorio: ", origem.replace(robo_path, '').replace("\\?\\", "").replace("\\\\", "\\"))
                            e += 1
    else:
        print('Não há arquivos novos a serem copiados')
    print('Total de arquivos na central conforme reportdorobodoonedrive: ', len(arquivosparaprocessarnafaseatual_list))
    print('Total de arquivos antigos no report: ', len(arquivosjaprocessadosnafaseatual_list))
    print('Total de arquivos novos copiados para o report: ', n)
    print('Total de erros: ', e)

    end = datetime.now()
    print('Time running: ', end-start)

if __name__ == "__main__":
    robodospdfs()