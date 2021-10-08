from datetime import datetime
import os
import shutil
from PyPDF2 import PdfFileReader, PdfFileWriter

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

# path to pdf

path_temp_original = 'F:\\robodepdfs\\temp_original\\'
path_temp_unificado = 'F:\\robodepdfs\\temp_unificados\\'
path_temp_unificado_enviados = 'F:\\robodepdfs\\temp_unificados_enviados\\'
path_relatorio_de_erros = 'F:\\robodepdfs\\relatorio_de_erros\\'

dirname = 'F:\CentralDeNotas\\'
paths_centraldenotas_folders = [f.path for f in os.scandir(dirname) if f.is_dir()]  # getting folder names
paths_centraldenotas = []
for path_centraldenotas_folders in paths_centraldenotas_folders:
    paths_centraldenotas.append(path_centraldenotas_folders + '\\' + str(currentYear) + '\\' + str(currentMonth) + '\\' + str(currentDay) + '\\')  # complementing folder names with current year, month and day

for path_centraldenotas in paths_centraldenotas:
    print('acessing: ', path_centraldenotas)
    for file in os.listdir(path_centraldenotas):
        if file.endswith(".pdf"):
            try:
                path_centraldenotas_and_filename = os.path.join(path_centraldenotas, file)
                shutil.copy(path_centraldenotas_and_filename, path_temp_original)   # copying pdfs from central de notas to temp_original
                print('copied from central_de_notas to temp_original: ', path_temp_original, file)
            except:
                relatorio_de_erros = open(path_relatorio_de_erros + 'relatorio_de_erros.txt', "a")
                relatorio_de_erros.write('\nerror on copy from central_de_notas to temp_original: ', path_temp_original, file)
                relatorio_de_erros.close()
                pass

            # copying pdfs from temp_original to temp_unificados splitting if more than 01 page
            for file_in_original in os.listdir(path_temp_original):
                if file_in_original.endswith(".pdf"):
                    path_original_and_filename = os.path.join(path_temp_original, file_in_original)
                    with open(path_original_and_filename, 'rb') as f1:
                        pdf = PdfFileReader(f1)
                        number_of_pages = pdf.getNumPages()

                        if number_of_pages > 1:  # splitting pdf if more than 01 page
                            try:
                                file_base_name = file_in_original.replace('.pdf', '')
                                pdf = PdfFileReader(path_original_and_filename)

                                for page_number in range(pdf.getNumPages()):
                                    pdfWriter = PdfFileWriter()
                                    pdfWriter.addPage(pdf.getPage(page_number))

                                    with open(os.path.join(path_temp_unificado, '{0}_page{1}.pdf'.format(file_base_name, page_number+1)),'wb') as f:
                                        pdfWriter.write(f)
                                        f.close()
                                        print('copied from temp_original to temp_unificados: ', path_temp_unificado, '{0}_page{1}.pdf'.format(file_base_name, page_number+1))
                                f1.close()
                                os.remove(path_original_and_filename)
                            except:
                                relatorio_de_erros = open(path_relatorio_de_erros + 'relatorio_de_erros.txt', "a")
                                relatorio_de_erros.write('\n' + str(datetime.now()) + "," + 'error on copy temp_original to temp_unificados' + "," + path_temp_unificado + file_in_original)
                                relatorio_de_erros.close()
                                pass
                        else:
                            try:
                                shutil.move(path_original_and_filename, path_temp_unificado)
                                print('moved from temp_original to temp_unificados: ', path_temp_unificado + file_in_original)
                                f1.close()
                            except:
                                relatorio_de_erros = open(path_relatorio_de_erros + 'relatorio_de_erros.txt', "a")
                                relatorio_de_erros.write('\n' + str(datetime.now()) + "," + 'error on copy temp_original to temp_unificados' + "," + path_temp_unificado + file_in_original)
                                relatorio_de_erros.close()
                                pass

# import os
# os.startfile("C:\Documents and Settings\flow_model\flow.exe")