import shutil

# # path
# path = 'F:\CentralDeNotas\ClubedeBeneficios'
#
# # Source path
# src = 'F:\CentralDeNotas\ClubedeBeneficios\\2021'
#
# anos = [2023, 2024, 2025]
#
# for ano in anos:
#     dest = 'F:\CentralDeNotas\ClubedeBeneficios\\' + str(ano)
#     print('criando ', ano)
#     destination = shutil.copytree(src, dest)

import os
import shutil
import datetime

now = str(datetime.datetime.now())[:19]
now = now.replace(":","_")

nomes = ['GaboardParticicacoes',
'ImpalaTerminals',
'MontsHoldings',
'TrafiguradoBrasilConsultoria',
'TrafiguradoBrasilImportacaoeExportacao']

for nome in nomes:
    src_dir='F:\CentralDeNotas\\ClubeFlex'
    dst_dir='F:\CentralDeNotas\\'+nome
    shutil.copytree(src_dir, dst_dir)
    print('foi criada a pasta: ', nome)
