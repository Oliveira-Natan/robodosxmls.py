import os
from PyPDF2 import PdfFileReader, PdfFileWriter

path_temp_original = r'C:\Users\felipe.rosa\Documents\GitHub\mcstoolsretencoes\sandbox\versao_27.10.2021'
path_temp_individualizados = r'C:\Users\felipe.rosa\Documents\GitHub\mcstoolsretencoes\sandbox\versao_27.10.2021'

def individualizacao(file_in_original):
    # for file_in_original in os.listdir(path_temp_original):  # on for each file on temp_original
    if file_in_original.endswith(".pdf"):  # if file ends with .pdf
        path_original_and_filename = os.path.join(path_temp_original, file_in_original)  # creating file path
        with open(path_original_and_filename, 'rb') as pdf_file:  # read file as pdf_file

            pdfFile = PdfFileReader(pdf_file)
            if pdfFile.isEncrypted:
                pdf_file.close()
                print('encripted')
                from pikepdf import Pdf
                with Pdf.open(path_original_and_filename, password='', allow_overwriting_input=True) as pdf:
                    pdf.save(path_original_and_filename)
                    print('File Decrypted (PyPDF2)')

        with open(path_original_and_filename, 'rb') as pdf_file:  # read file as pdf_file
            pdfFile = PdfFileReader(pdf_file)
            if pdfFile.isEncrypted:
                pdf_file.close()
                print('encripted')
            try:
                number_of_pages = PdfFileReader(pdf_file).getNumPages()  # get number of pages from pdf
                print(number_of_pages)
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

                file_base_name = file_in_original.replace('.pdf', '')  # getting pdf name
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

individualizacao('000 NF BRUNO SANTOS 50156.PDF')