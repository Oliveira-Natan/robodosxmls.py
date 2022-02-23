import getpass
from datetime import datetime
import os
import shutil

def report_backup(onedrive_path, reportdosrobos_erros, report_robodoonedrive, report_robodospdfs, report_robodeindividualizacao, report_robodosemailsparaarquivei):
    report_backup_directory = r'{}\Retencao_Gerencial\robosdoretencao_backup'.format(onedrive_path) + '\\backup_'
    now = datetime.now()
    hora = datetime.now().hour
    if (hora <= 12):
        momento = 'manha'
    elif (hora > 12) and (hora <= 18):
        momento = 'tarde'
    elif (hora > 18):
        momento = 'noite'

    directory = report_backup_directory + str(now.strftime("%d-%m-%Y_")) + momento
    print(directory)
    try:
        os.mkdir(directory)
        shutil.copyfile(reportdosrobos_erros, directory + '\\' + 'errosdosrobos.csv')
        shutil.copyfile(report_robodoonedrive, directory + '\\' + 'robodoonedrive.csv')
        shutil.copyfile(report_robodospdfs, directory + '\\' + 'robodospdfs.csv')
        shutil.copyfile(report_robodeindividualizacao, directory + '\\' + 'robodeindividualizacao.csv')
        shutil.copyfile(report_robodosemailsparaarquivei, directory + '\\' + 'robodosemails.csv')
    except:
        print('Diretorio de backup já existente')


# path and reports names
username = getpass.getuser()
onedrive_path = r'C:\Users\{}\OneDrive - MCS MARKUP AUDITORIA E CONSULTORIA EMPRESARIAL LTDA\CentraldeNotas'.format(username)
robo_path = r'C:\Users\{}\Desktop\rede\robodepdfs'.format(username)

reportdosrobos_erros = r'{}\reports\errosdosrobos.csv'.format(robo_path)
report_robodoonedrive = r'{}\reports\robodoonedrive.csv'.format(robo_path)
report_robodospdfs = r'{}\reports\robodospdfs.csv'.format(robo_path)
report_robodeindividualizacao = r'{}\reports\robodeindividualizacao.csv'.format(robo_path)
report_robodosemailsparaarquivei = r'{}\reports\robodosemails.csv'.format(robo_path)


report_backup(onedrive_path, reportdosrobos_erros, report_robodoonedrive, report_robodospdfs, report_robodeindividualizacao, report_robodosemailsparaarquivei)

# import getpass
# user = getpass.getuser()
# print(user)

# def processamento(origem, destino, path_destino_atual, tentativa):
#     print('iniciando ', tentativa)
#     if origem.upper().endswith(".PDF"):  # if file ends with .pdf
#         path_original_and_filename = origem  # creating file path
#         with open(path_original_and_filename, 'rb') as pdf_file:  # read file as pdf_file
#             try:
#                 number_of_pages = PdfFileReader(pdf_file, strict=False).getNumPages()  # get number of pages from pdf
#             except:
#                 number_of_pages = PdfFileReader(pdf_file, strict=False)  # get number of pages from pdf
#                 if number_of_pages.isEncrypted:
#                     print('tentando decriptografar')
#                     # try:
#                     pdf_file.close()  # closing file and adjusting file with EOF error
#                     pdf = pikepdf.open(path_original_and_filename, allow_overwriting_input=True)
#                     pdf.save(path_original_and_filename)
#                     print('Now is unencrypted')
#                     # with open(path_original_and_filename, 'rb') as pdf_file:  # read file as pdf_file
#                     #     number_of_pages = PdfFileReader(pdf_file, strict=False).getNumPages()  # get number of pages from pdf
#                 else:
#                     pdf_file.close()  # closing file and adjusting file with EOF error
#
#         with open(path_original_and_filename, 'rb') as pdf_file:  # read file as pdf_file
#             try:
#                 number_of_pages = PdfFileReader(pdf_file, strict=False).getNumPages()  # get number of pages from pdf
#             except:
#                 pdf_file.close()  # closing file and adjusting file with EOF error
#                 def reset_eof_of_pdf_return_stream(pdf_stream_in: list):
#                     # find the line position of the EOF
#                     for i, x in enumerate(txt[::-1]):
#                         if b'%%EOF' in x:
#                             actual_line = len(pdf_stream_in) - i
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
#     arquivos_criados_ou_movidos_list = []
#     if number_of_pages > 1:  # if more than 01 page, then try to split and delete original on temp_original
#         with open(path_original_and_filename, 'rb') as pdf_file:  # read file as pdf_file
#             file_base_name = origem.split("\\")[-1].replace('.PDF', '').replace('.pdf', '')  # getting pdf name
#             pdf = PdfFileReader(path_original_and_filename, strict=False)
#             destino = os.path.dirname(os.path.abspath(destino))
#             for page_number in range(pdf.getNumPages()):  # for each page of this pdf
#                 pdfWriter = PdfFileWriter()
#                 pdfWriter.addPage(pdf.getPage(page_number))
#                 new_pdf_name = os.path.join(destino, '{0}_page{1}.pdf'.format(file_base_name, page_number + 1))
#                 with open(new_pdf_name, 'wb') as new_pdf:  # save new pdf for this page
#                     pdfWriter.write(new_pdf)
#                     new_pdf.close()
#                     arquivos_criados_ou_movidos_list.append(new_pdf_name)
#             pdf_file.close()
#             return arquivos_criados_ou_movidos_list
#     else:  # if do not have more than 01 page, then create this file on temp_individualizados and delete original on temp_original
#         with open(path_original_and_filename, 'rb') as pdf_file:  # read file as pdf_file
#             pdf = PdfFileReader(pdf_file, strict=False)  # lendo o pdf e incluindo numa variavel pdfWriter
#             pdfWriter = PdfFileWriter()
#             pdfWriter.addPage(pdf.getPage(0))
#             print('origem', origem)
#             print('destino', destino)
#
#             # with open(destino, 'wb') as new_pdf:  # criando pdf vazio no destino
#             #     pdfWriter.write(new_pdf)  # salvando pdfWriter no pdf vazio criado no destino
#             #     new_pdf.close()
#             #     arquivos_criados_ou_movidos_list.append(
#             #         destino)  # inserindo "destino" em lista para identificacao de serie
#             pdf_file.close()
#             return arquivos_criados_ou_movidos_list