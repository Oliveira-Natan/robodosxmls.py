from PyPDF2 import PdfFileReader, PdfFileWriter
import os.path
import shutil
from datetime import datetime
import pandas as pd

start = datetime.now()
def uploadingReport(action_list, reportrobodeindividualizacao):
    robo_data = pd.read_csv(path_report + reportrobodeindividualizacao)

    # appending action to reportdosrobos
    action_list = pd.Series(action_list, index=robo_data.columns)
    robo_data = robo_data.append(action_list, ignore_index=True)
    robo_data.to_csv(path_report + reportrobodeindividualizacao, index=False)
    robo_data = pd.read_csv(path_report + reportrobodeindividualizacao)

def uploadingReportError(action_list, reportdosrobos_erros):
    robo_data_error = pd.read_csv(path_report + reportdosrobos_erros)

    # appending error to reportdosrobos_erros
    action_list = pd.Series(action_list, index=robo_data_error.columns)
    robo_data_error = robo_data_error.append(action_list, ignore_index=True)
    robo_data_error.to_csv(path_report + reportdosrobos_erros, index=False)
    robo_data_error = pd.read_csv(path_report + reportdosrobos_erros)

def individualizacao(file_in_original):
    # for file_in_original in os.listdir(path_temp_original):  # on for each file on temp_original
    if file_in_original.endswith(".PDF"):  # if file ends with .pdf
        path_original_and_filename = os.path.join(path_temp_original, file_in_original)  # creating file path
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
                            # print(f'EOF found at line position {-i} = actual {actual_line}, with value {x}')
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

            if number_of_pages > 1:  # if more than 01 page, then try to split and delete original from temp_original

                file_base_name = file_in_original.replace('.PDF', '')  # getting pdf name
                pdf = PdfFileReader(path_original_and_filename)
                for page_number in range(pdf.getNumPages()):  # for each page of this pdf
                    pdfWriter = PdfFileWriter()
                    pdfWriter.addPage(pdf.getPage(page_number))

                    with open(os.path.join(path_temp_individualizados,
                                           '{0}_page{1}.pdf'.format(file_base_name, page_number + 1)),
                              'wb') as new_pdf:  # save new pdf for this page
                        pdfWriter.write(new_pdf)
                        new_pdf.close()
                        print('copied from temp_original to temp_individualizados: ', path_temp_individualizados,
                              '{0}_page{1}.pdf'.format(file_base_name, page_number + 1))

                        # action_list = [datetime.now(), 'robodeindividualizacao',
                        #                'temp_original to temp_individualizados',
                        #                path_temp_individualizados + '{0}_page{1}.pdf'.format(file_base_name, page_number + 1)]
                        # uploadingReport(action_list)
                        # print('Report do Robo de Individualizacao atualizado com sucesso')


                pdf_file.close()
                os.remove(path_original_and_filename)
            else:  # if do not have more than 01 page, then move file from temp_original to temp_individualizados
                pdf_file.close()
                shutil.move(
                    os.path.join(path_temp_original, file_in_original),
                    os.path.join(path_temp_individualizados, file_in_original))
                print('copied from temp_original to temp_individualizados: ',
                      path_temp_individualizados + "\\" + file_in_original)

                # action_list = [datetime.now(), 'robodeindividualizacao', 'temp_original to temp_individualizados',
                #                path_temp_individualizados + "\\" + file_in_original]
                # uploadingReport(action_list)
                # print('Report do Robo de Individualizacao atualizado com sucesso')

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

# path_report = r"C:\Users\felipe.rosa\Desktop\New folder\report"
# path_temp_original = r'C:\Users\felipe.rosa\Desktop\New folder\temp_original'
# path_temp_individualizados = r'C:\Users\felipe.rosa\Desktop\New folder\temp_individualizados'
# path_temp_individualizados_enviados = r'C:\Users\felipe.rosa\Desktop\New folder\temp_individualizados_enviados'

path_arquivei = r'F:\Fiscal\Clientes Fiscal\Arquivei - Armazenamento de XML'
path_cloudFiscal = r'F:\Impostos Retidos\Conversor FIT'

# reports names
reportrobodeindividualizacao = '\\robodeindividualizacao_' + str(currentYear) + '_' + str(currentMonth) + '.csv'
reportdosrobos_erros = '\\errosdosrobos_' + str(currentYear) + '_' + str(currentMonth) + '.csv'
reportrobodospdfs = '\\robodospdfs_' + str(currentYear) + '_' + str(currentMonth) + '.csv'
reportrobodosemails = '\\robodosemails_' + str(currentYear) + '_' + str(currentMonth) + '.csv'
reportrobodoarquivei = '\\robodoarquivei_' + str(currentYear) + '_' + str(currentMonth) + '.csv'

# start process

if len(os.listdir(path_temp_original)) != 0:
    for file in os.listdir(path_temp_original):  # on for each file on temp_original
        print(file)
        individualizacao(file)
        action_list = [datetime.now(), 'robodeindividualizacao', 'temp_original to temp_individualizados',
                       path_temp_original + "\\" + file]
        uploadingReport(action_list, reportrobodeindividualizacao)
        print('Report do Robo de Individualizacao atualizado com sucesso')
#             except:
#                 action_list = [datetime.now(), 'robodeindividualizacao', 'ERROR: temp_original to temp_individualizados', path_temp_original + "\\" + file]
#                 uploadingReportError(action_list, reportdosrobos_erros)
#                 print('ERROR: Report de erro dos robos atualizado com sucesso')
#     else:
#         print('Não há arquivos novos a serem copiados')
# except:
#     action_list = [datetime.now(), 'robodeindividualizacao', 'ERROR: problemas ao processar o robo de individualizacao', path_temp_individualizados]
#     uploadingReportError(action_list, reportdosrobos_erros)
#     print('ERROR: Report de erro dos robos atualizado com sucesso (problemas ao processar o robo de individualizacao)')
#
# end = datetime.now()
# print(end-start)