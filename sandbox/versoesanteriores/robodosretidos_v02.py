import os.path, time
from datetime import datetime
import shutil

# listing files changed in the last 01 hour
source = r'F:\Impostos Retidos\FIT_XML_TERCEIRO'
destiny = r'F:\Impostos Retidos\Conversor FIT'
path_relatorio_de_erros = 'F:\\robodepdfs\\relatorio_de_erros\\'

past = time.time() - 1*60*60  # 1 hours
source_files = []
for p, ds, fs in os.walk(source):
    for fn in fs:
        try:
            filepath = os.path.join(p, fn)
            if os.path.getmtime(filepath) >= past:
                shutil.copy(filepath, destiny)
                print('moved from cloud_fiscal to mcs_retencao: ', os.path.basename(filepath))
        except:
            relatorio_de_erros = open(path_relatorio_de_erros + 'relatorio_de_erros_robodosretidos.txt', "a")
            relatorio_de_erros.write('\n' + str(datetime.now()) + "," + 'error on copy from cloud_fiscal to mcs_retencao: ' + fn)
            relatorio_de_erros.close()
            pass




# try:
# for p, ds, fs in os.walk(source):
#     for fn in fs:
#         filepath = os.path.join(p, fn)
#         if os.path.getmtime(filepath) >= past:
#             source_files.append(filepath)
# print(source_files)
#
# # copying files to new destiny
# for file in source_files:
#     shutil.copy(file, destiny)


