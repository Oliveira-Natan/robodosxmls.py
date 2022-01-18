import time

from PyPDF2 import PdfFileReader, PdfFileWriter
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
    print('total de listaarquivosjaprocessadosnafaseatual: ', len(arquivosprocessadosnafaseanterior_list))
    return arquivosprocessadosnafaseanterior_list

def listaarquivosparaprocessarnafaseatual(arquivosprocessadosnafaseanterior_list, arquivosjaprocessadosnafaseatual_list, path_origem_atual, path_destino_atual):
    print('Iniciando listagem de listaarquivosparaprocessarnafaseatual')
    path_files_to_copy = []
    for id, item in arquivosprocessadosnafaseanterior_list:
        if item not in arquivosjaprocessadosnafaseatual_list:
            path_files_to_copy.append([id, item, item.replace(path_origem_atual, path_destino_atual)]) # id, origem, destino
    print('total de listaarquivosparaprocessarnafaseatual: ', len(path_files_to_copy))
    return path_files_to_copy

def processamento(origem, destino, path_destino_atual, tentativa):
    print('iniciando ', tentativa)
    if origem.upper().endswith(".PDF"):  # if file ends with .pdf
        path_original_and_filename = origem  # creating file path
        with open(path_original_and_filename, 'rb') as pdf_file:  # read file as pdf_file
            try:
                number_of_pages = PdfFileReader(pdf_file, strict=False).getNumPages()  # get number of pages from pdf
            except:
                pdf_file.close()  # closing file and adjusting file with EOF error

                def reset_eof_of_pdf_return_stream(pdf_stream_in: list):
                    # find the line position of the EOF
                    for i, x in enumerate(txt[::-1]):
                        if b'%%EOF' in x:
                            actual_line = len(pdf_stream_in) - i
                            break
                    # return the list up to that point
                    return pdf_stream_in[:actual_line]

                # opens the file for reading
                with open(path_original_and_filename, 'rb') as p:
                    txt = (p.readlines())

                # get the new list terminating correctly
                txtx = reset_eof_of_pdf_return_stream(txt)

                # write to new pdf
                with open(path_original_and_filename, 'wb') as f:
                    f.writelines(txtx)

                with open(path_original_and_filename, 'rb') as pdf_file:  # read file as pdf_file
                    number_of_pages = PdfFileReader(pdf_file).getNumPages()  # get number of pages from pdf

            arquivos_criados_ou_movidos_list = []
            if number_of_pages > 1:  # if more than 01 page, then try to split and delete original on temp_original
                file_base_name = origem.split("\\")[-1].replace('.PDF', '').replace('.pdf', '')  # getting pdf name
                pdf = PdfFileReader(path_original_and_filename, strict=False)
                destino = os.path.dirname(os.path.abspath(destino))
                for page_number in range(pdf.getNumPages()):  # for each page of this pdf
                    pdfWriter = PdfFileWriter()
                    pdfWriter.addPage(pdf.getPage(page_number))
                    new_pdf_name = os.path.join(destino, '{0}_page{1}.pdf'.format(file_base_name, page_number + 1))
                    with open(new_pdf_name, 'wb') as new_pdf:  # save new pdf for this page
                        pdfWriter.write(new_pdf)
                        new_pdf.close()
                        arquivos_criados_ou_movidos_list.append(new_pdf_name)
                        # print('Criado from temp_original to temp_individualizados: ', new_pdf_name)
                pdf_file.close()
                # os.remove(path_original_and_filename)
                return arquivos_criados_ou_movidos_list
            else:  # if do not have more than 01 page, then create this file on temp_individualizados and delete original on temp_original
                pdf = PdfFileReader(pdf_file, strict=False)  # lendo o pdf e incluindo numa variavel pdfWriter
                pdfWriter = PdfFileWriter()
                pdfWriter.addPage(pdf.getPage(0))
                with open(destino, 'wb') as new_pdf:  # criando pdf vazio no destino
                    pdfWriter.write(new_pdf)  # salvando pdfWriter no pdf vazio criado no destino
                    new_pdf.close()
                    arquivos_criados_ou_movidos_list.append(destino)  # inserindo "destino" em lista para identificacao de serie
                    # print('Criado from temp_original to temp_individualizados: ', destino)
                pdf_file.close()
                # os.remove(path_original_and_filename)
                return arquivos_criados_ou_movidos_list
                #
                #
                #
                # pdf_file.close()
                # arquivos_criados_ou_movidos_list.append(destino)
                # shutil.copy(origem, destino)
                # print('Moved from temp_original to temp_individualizados: ', path_destino_atual + "\\" + origem)
                # return arquivos_criados_ou_movidos_list

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
onedrive_path = r'C:\Users\felipe.rosa\OneDrive - MCS MARKUP AUDITORIA E CONSULTORIA EMPRESARIAL LTDA\CentraldeNotas'
# centraldosrobos_path = r'F:\robodepdfs\centraldosrobos'
# temp_original_path = r'F:\robodepdfs\temp_original'
# temp_individualizados_path = r'F:\robodepdfs\temp_individualizados'
# temp_enviados_path = r'F:\robodepdfs\temp_enviados'
#
# reportdosrobos_erros = r'F:\robodepdfs\reports\errosdosrobos.csv'
# report_robodoonedrive = r'F:\robodepdfs\reports\robodoonedrive.csv'
# report_robodospdfs = r'F:\robodepdfs\reports\robodospdfs.csv'
# report_robodeindividualizacao = r'F:\robodepdfs\reports\robodeindividualizacao.csv'
# report_robodosemailsparaarquivei = r'F:\robodepdfs\reports\robodosemails.csv'

centraldosrobos_path = r'C:\Users\felipe.rosa\Desktop\rede\robodepdfs\centraldosrobos'
temp_original_path = r'C:\Users\felipe.rosa\Desktop\rede\robodepdfs\temp_original'
temp_individualizados_path = r'C:\Users\felipe.rosa\Desktop\rede\robodepdfs\temp_individualizados'
temp_enviados_path = r'C:\Users\felipe.rosa\Desktop\rede\robodepdfs\temp_enviados'

reportdosrobos_erros = r'C:\Users\felipe.rosa\Desktop\rede\robodepdfs\reports\errosdosrobos.csv'
report_robodoonedrive = r'C:\Users\felipe.rosa\Desktop\rede\robodepdfs\reports\robodoonedrive.csv'
report_robodospdfs = r'C:\Users\felipe.rosa\Desktop\rede\robodepdfs\reports\robodospdfs.csv'
report_robodeindividualizacao = r'C:\Users\felipe.rosa\Desktop\rede\robodepdfs\reports\robodeindividualizacao.csv'
report_robodosemailsparaarquivei = r'C:\Users\felipe.rosa\Desktop\rede\robodepdfs\reports\robodosemails.csv'

reportdafaseanterior = report_robodospdfs
reportdafaseatual = report_robodeindividualizacao
path_origem_atual = temp_original_path
path_destino_atual = temp_individualizados_path

## TRATAMENTO DE FOLDERS: clonando estrutura da fase anterior para a fase atual
diretorios_do_path_origem_atual = listardiretorios(path_origem_atual)  # listar estrutura de pasta da fase anterior
diretorios_da_path_destino_atual = listardiretorios(path_destino_atual)  # listar estrutura de pasta da fase atual
diretoriosparacriar_list = diretoriosparacriar(diretorios_do_path_origem_atual, diretorios_da_path_destino_atual)  # identifica novas pastas na estrutura atual
if diretoriosparacriar_list != 0:
    criardiretorios(path_destino_atual, diretoriosparacriar_list)  # cria novas pastas na estrutura atual

## TRATAMENTO DE ARQUIVOS
arquivosjaprocessadosnafaseatual_list = listaarquivosjaprocessadosnafaseatual(reportdafaseatual)  # lista arquivosjaprocessadosnafaseatual
arquivosprocessadosnafaseanterior_list = listaarquivosprocessadosnafaseanterior(reportdafaseanterior)  # listar arquivosprocessadosnafaseanterior
arquivosparaprocessarnafaseatual_list = listaarquivosparaprocessarnafaseatual(arquivosprocessadosnafaseanterior_list, arquivosjaprocessadosnafaseatual_list, path_origem_atual, path_destino_atual)  # listar arquivosparaprocessarnafaseatual
# print(arquivosparaprocessarnafaseatual_list)

n = 0
e = 0
if len(arquivosparaprocessarnafaseatual_list) > 0:
    # iniciar copia
    for id, origem, destino in arquivosparaprocessarnafaseatual_list:
        try:
            arquivos_criados_ou_movidos_list = processamento(origem, destino, path_destino_atual, 'tentativa01')  # copiando arquivos (arquivosparaprocessarnafaseatual) da central dos robos para a temp_original (path_destino_atual)
            serie = 1
            for arquivos_criados_ou_movidos in arquivos_criados_ou_movidos_list:
                action_list = [id, serie, datetime.now(), 'robodeindividualizacao', 'temp_original to temp_individualizados', origem, arquivos_criados_ou_movidos]
                uploadingReport(action_list, reportdafaseatual)
                print(n, 'Processado id: ', id, 'serie: ', serie)
                serie += 1
            n += 1
        except:
            try:  # TENTANDO NOVAMENTE, MAS COM REDUCAO DO NOME DO DIRETORIO
                arquivos_criados_ou_movidos_list = processamento("\\\\?\\" + origem, "\\\\?\\" + destino, path_destino_atual, 'tentativa02')
                serie = 1
                for arquivos_criados_ou_movidos in arquivos_criados_ou_movidos_list:
                    action_list = [id, serie, datetime.now(), 'robodeindividualizacao', 'temp_original to temp_individualizados', origem, arquivos_criados_ou_movidos]
                    uploadingReport(action_list, reportdafaseatual)
                    print(n, 'Processado id: ', id, 'serie: ', serie)
                    serie += 1
                n += 1
            except:
                try:  # TENTANDO NOVAMENTE, MAS COM OUTRA TECNICA DE REDUCAO DO NOME DO DIRETORIO
                    destino_curto = os.path.dirname(os.path.abspath(destino))  # pega o diretorio do arquivo, sem o nome
                    destino_curto = win32api.GetShortPathName(destino_curto)  # deixa o diretorio do arquivo menor

                    filename = origem.split('\\')[-1]  # pega o nome do arquivo
                    origem_curto = os.path.dirname(os.path.abspath(origem))  # pega o diretorio do arquivo, sem o nome
                    origem_curto = win32api.GetShortPathName(origem_curto)  # deixa o diretorio do arquivo menor
                    origem_curto = origem_curto + '\\' + filename  # remonta a origem: diretorio menor + nome do arquivo

                    arquivos_criados_ou_movidos_list = processamento("\\\\?\\" + origem_curto, "\\\\?\\" + destino_curto, path_destino_atual, 'tentativa03')
                    serie = 1
                    for arquivos_criados_ou_movidos in arquivos_criados_ou_movidos_list:
                        action_list = [id, serie, datetime.now(), 'robodeindividualizacao', 'temp_original to temp_individualizados', origem, arquivos_criados_ou_movidos]
                        uploadingReport(action_list, reportdafaseatual)
                        print(n, 'Processado id: ', id, 'serie: ', serie)
                        serie += 1
                    n += 1
                except:
                    action_list = [id, "", datetime.now(), 'robodeindividualizacao', 'ERROR: temp_original to temp_individualizados', origem, destino]
                    uploadingReportError(action_list, reportdosrobos_erros)
                    print('ERROR: Report de erro dos robos atualizado com sucesso: ', id, "diretorio: ", origem)
                    e += 1
else:
    print('Não há arquivos novos a serem copiados')
print('Total de arquivos na central conforme reportdorobodoonedrive: ', len(arquivosparaprocessarnafaseatual_list))
print('Total de arquivos antigos no report: ', len(arquivosjaprocessadosnafaseatual_list))
print('Total de arquivos novos copiados para o report: ', n)
print('Total de erros: ', e)

end = datetime.now()
print('Time running: ', end-start)

# start = datetime.now()
# def uploadingReport(action_list, reportrobodeindividualizacao):
#     robo_data = pd.read_csv(path_report + reportrobodeindividualizacao)
#
#     # appending action to reportdosrobos
#     action_list = pd.Series(action_list, index=robo_data.columns)
#     robo_data = robo_data.append(action_list, ignore_index=True)
#     robo_data.to_csv(path_report + reportrobodeindividualizacao, index=False)
#     robo_data = pd.read_csv(path_report + reportrobodeindividualizacao)
#
# def uploadingReportError(action_list, reportdosrobos_erros):
#     robo_data_error = pd.read_csv(path_report + reportdosrobos_erros)
#
#     # appending error to reportdosrobos_erros
#     action_list = pd.Series(action_list, index=robo_data_error.columns)
#     robo_data_error = robo_data_error.append(action_list, ignore_index=True)
#     robo_data_error.to_csv(path_report + reportdosrobos_erros, index=False)
#     robo_data_error = pd.read_csv(path_report + reportdosrobos_erros)

# def individualizacao(file_in_original):
#     # for file_in_original in os.listdir(path_temp_original):  # on for each file on temp_original
#     if file_in_original.endswith(".PDF"):  # if file ends with .pdf
#         path_original_and_filename = os.path.join(path_temp_original, file_in_original)  # creating file path
#         with open(path_original_and_filename, 'rb') as pdf_file:  # read file as pdf_file
#             try:
#                 number_of_pages = PdfFileReader(pdf_file, strict=False).getNumPages()  # get number of pages from pdf
#             except:
#                 pdf_file.close()  # closing file and adjusting file with EOF error
#
#                 def reset_eof_of_pdf_return_stream(pdf_stream_in: list):
#                     # find the line position of the EOF
#                     for i, x in enumerate(txt[::-1]):
#                         if b'%%EOF' in x:
#                             actual_line = len(pdf_stream_in) - i
#                             # print(f'EOF found at line position {-i} = actual {actual_line}, with value {x}')
#                             break
#                     # return the list up to that point
#                     return pdf_stream_in[:actual_line]
#
#                 # opens the file for reading
#                 with open(path_original_and_filename, 'rb') as p:
#                     txt = (p.readlines())
#
#                 # get the new list terminating correctly
#                 txtx = reset_eof_of_pdf_return_stream(txt)
#
#                 # write to new pdf
#                 with open(path_original_and_filename, 'wb') as f:
#                     f.writelines(txtx)
#
#                 with open(path_original_and_filename, 'rb') as pdf_file:  # read file as pdf_file
#                     number_of_pages = PdfFileReader(pdf_file).getNumPages()  # get number of pages from pdf
#
#             if number_of_pages > 1:  # if more than 01 page, then try to split and delete original from temp_original
#
#                 file_base_name = file_in_original.replace('.PDF', '')  # getting pdf name
#                 pdf = PdfFileReader(path_original_and_filename)
#                 for page_number in range(pdf.getNumPages()):  # for each page of this pdf
#                     pdfWriter = PdfFileWriter()
#                     pdfWriter.addPage(pdf.getPage(page_number))
#
#                     with open(os.path.join(path_temp_individualizados,
#                                            '{0}_page{1}.pdf'.format(file_base_name, page_number + 1)),
#                               'wb') as new_pdf:  # save new pdf for this page
#                         pdfWriter.write(new_pdf)
#                         new_pdf.close()
#                         print('copied from temp_original to temp_individualizados: ', path_temp_individualizados,
#                               '{0}_page{1}.pdf'.format(file_base_name, page_number + 1))
#
#                         # action_list = [datetime.now(), 'robodeindividualizacao',
#                         #                'temp_original to temp_individualizados',
#                         #                path_temp_individualizados + '{0}_page{1}.pdf'.format(file_base_name, page_number + 1)]
#                         # uploadingReport(action_list)
#                         # print('Report do Robo de Individualizacao atualizado com sucesso')
#
#
#                 pdf_file.close()
#                 os.remove(path_original_and_filename)
#             else:  # if do not have more than 01 page, then move file from temp_original to temp_individualizados
#                 pdf_file.close()
#                 shutil.move(
#                     os.path.join(path_temp_original, file_in_original),
#                     os.path.join(path_temp_individualizados, file_in_original))
#                 print('copied from temp_original to temp_individualizados: ',
#                       path_temp_individualizados + "\\" + file_in_original)
#
#                 # action_list = [datetime.now(), 'robodeindividualizacao', 'temp_original to temp_individualizados',
#                 #                path_temp_individualizados + "\\" + file_in_original]
#                 # uploadingReport(action_list)
#                 # print('Report do Robo de Individualizacao atualizado com sucesso')
#
# # defining year, month and day
# currentDay = datetime.now().day
# if currentDay < 10:
#     currentDay = '0' + str(currentDay)
# else:
#     currentDay = str(currentDay)
#
# currentMonth = datetime.now().month
# if currentMonth < 10:
#     currentMonth = '0' + str(currentMonth)
# else:
#     currentMonth = str(currentMonth)
#
# currentYear = datetime.now().year
#
# # main paths
# path_report = r"F:\robodepdfs\reports"
# path_centraldenotas = r'F:\CentralDeNotas'
# path_temp_original = r'F:\robodepdfs\temp_original'
# path_temp_individualizados = r'F:\robodepdfs\temp_individualizados'
# path_temp_individualizados_enviados = r'F:\robodepdfs\temp_individualizados_enviados'
#
# # path_report = r"C:\Users\felipe.rosa\Desktop\New folder\report"
# # path_temp_original = r'C:\Users\felipe.rosa\Desktop\New folder\temp_original'
# # path_temp_individualizados = r'C:\Users\felipe.rosa\Desktop\New folder\temp_individualizados'
# # path_temp_individualizados_enviados = r'C:\Users\felipe.rosa\Desktop\New folder\temp_individualizados_enviados'
#
# path_arquivei = r'F:\Fiscal\Clientes Fiscal\Arquivei - Armazenamento de XML'
# path_cloudFiscal = r'F:\Impostos Retidos\Conversor FIT'
#
# # reports names
# reportrobodeindividualizacao = '\\robodeindividualizacao_' + str(currentYear) + '_' + str(currentMonth) + '.csv'
# reportdosrobos_erros = '\\errosdosrobos_' + str(currentYear) + '_' + str(currentMonth) + '.csv'
# reportrobodospdfs = '\\robodospdfs_' + str(currentYear) + '_' + str(currentMonth) + '.csv'
# reportrobodosemails = '\\robodosemails_' + str(currentYear) + '_' + str(currentMonth) + '.csv'
# reportrobodoarquivei = '\\robodoarquivei_' + str(currentYear) + '_' + str(currentMonth) + '.csv'
#
# # start process
#
# if len(os.listdir(path_temp_original)) != 0:
#     for file in os.listdir(path_temp_original):  # on for each file on temp_original
#         print(file)
#         individualizacao(file)
#         action_list = [datetime.now(), 'robodeindividualizacao', 'temp_original to temp_individualizados',
#                        path_temp_original + "\\" + file]
#         uploadingReport(action_list, reportrobodeindividualizacao)
#         print('Report do Robo de Individualizacao atualizado com sucesso')
# #             except:
# #                 action_list = [datetime.now(), 'robodeindividualizacao', 'ERROR: temp_original to temp_individualizados', path_temp_original + "\\" + file]
# #                 uploadingReportError(action_list, reportdosrobos_erros)
# #                 print('ERROR: Report de erro dos robos atualizado com sucesso')
# #     else:
# #         print('Não há arquivos novos a serem copiados')
# # except:
# #     action_list = [datetime.now(), 'robodeindividualizacao', 'ERROR: problemas ao processar o robo de individualizacao', path_temp_individualizados]
# #     uploadingReportError(action_list, reportdosrobos_erros)
# #     print('ERROR: Report de erro dos robos atualizado com sucesso (problemas ao processar o robo de individualizacao)')
# #
# # end = datetime.now()
# # print(end-start)