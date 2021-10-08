from PyPDF2 import PdfFileReader, PdfFileWriter
import os.path
import shutil
import pandas as pd
from datetime import datetime
import csv

path_temp_original = r'F:\robodepdfs\temp_original'
path_temp_unificado = r'F:\robodepdfs\temp_unificados'


for file_in_original in os.listdir(path_temp_original):  # on for each file on temp_original
    print(file_in_original)
    if file_in_original.endswith(".pdf"):  # if file ends with .pdf
        path_original_and_filename = os.path.join(path_temp_original, file_in_original)  # creating file path
        with open(path_original_and_filename, 'rb') as pdf_file:  # read file as pdf_file
            pdf = PdfFileReader(pdf_file)

            number_of_pages = pdf.getNumPages()  # get number of pages from pdf

            if number_of_pages > 1:  # if more than 01 page, then try to split and delete original from temp_original

                file_base_name = file_in_original.replace('.pdf', '')  # getting pdf name
                pdf = PdfFileReader(path_original_and_filename)
                for page_number in range(pdf.getNumPages()):  # for each page of this pdf
                    pdfWriter = PdfFileWriter()
                    pdfWriter.addPage(pdf.getPage(page_number))

                    with open(os.path.join(path_temp_unificado,
                                           '{0}_page{1}.pdf'.format(file_base_name, page_number + 1)),
                              'wb') as new_pdf:  # save new pdf for this page
                        pdfWriter.write(new_pdf)
                        new_pdf.close()
                        print('copied from temp_original to temp_unificados: ', path_temp_unificado,
                              '{0}_page{1}.pdf'.format(file_base_name, page_number + 1))
                pdf_file.close()
                os.remove(path_original_and_filename)
            else:  # if do not have more than 01 page, then move file from temp_original to temp_unificados
                print('uma pagina')
                pdf_file.close()
                shutil.move(
                    os.path.join(path_temp_original, file_in_original),
                    os.path.join(path_temp_unificado, file_in_original))
