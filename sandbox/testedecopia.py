import shutil
import win32api
import os
from subprocess import call
from PyPDF2 import PdfFileReader, PdfFileWriter
import pandas as pd

list = [[2526, r'C:\\Users\\felipe.rosa\\Desktop\\rede\\robodepdfs\\temp_original\\OneDriverRestrito\\Segmedic - Central Medic\\2021\\2021\\03.2021\\DANFE`s\\NF CM HOSP SA (RPO) MAT HOSP 05-03.pdf', r'C:\\Users\\felipe.rosa\\Desktop\\rede\\robodepdfs\\temp_original\\OneDriverRestrito\\Segmedic - Central Medic\\2021\\2021\\03.2021\\DANFE`s\\NF CM HOSP SA (RPO) MAT HOSP 05-03.pdf'], [2527, r'C:\\Users\\felipe.rosa\\Desktop\\rede\\robodepdfs\\temp_original\\OneDriverRestrito\\Segmedic - Central Medic\\2021\\2021\\03.2021\\DANFE`s\\NF ESSENCIAL MAT HOSP 05-03.pdf', r'C:\\Users\\felipe.rosa\\Desktop\\rede\\robodepdfs\\temp_original\\OneDriverRestrito\\Segmedic - Central Medic\\2021\\2021\\03.2021\\DANFE`s\\NF ESSENCIAL MAT HOSP 05-03.pdf'], [2528, r'C:\\Users\\felipe.rosa\\Desktop\\rede\\robodepdfs\\temp_original\\OneDriverRestrito\\Segmedic - Central Medic\\2021\\2021\\03.2021\\DANFE`s\\NF ESSENCIAL MAT HOSP 17-03.pdf', r'C:\\Users\\felipe.rosa\\Desktop\\rede\\robodepdfs\\temp_original\\OneDriverRestrito\\Segmedic - Central Medic\\2021\\2021\\03.2021\\DANFE`s\\NF ESSENCIAL MAT HOSP 17-03.pdf'], [2529, r'C:\\Users\\felipe.rosa\\Desktop\\rede\\robodepdfs\\temp_original\\OneDriverRestrito\\Segmedic - Central Medic\\2021\\2021\\03.2021\\DANFE`s\\NF ESSENCIAL MED 17-03.pdf', r'C:\\Users\\felipe.rosa\\Desktop\\rede\\robodepdfs\\temp_original\\OneDriverRestrito\\Segmedic - Central Medic\\2021\\2021\\03.2021\\DANFE`s\\NF ESSENCIAL MED 17-03.pdf'], [2530, r'C:\\Users\\felipe.rosa\\Desktop\\rede\\robodepdfs\\temp_original\\OneDriverRestrito\\Segmedic - Central Medic\\2021\\2021\\03.2021\\DANFE`s\\NF GALANTI MED 05-03.pdf', r'C:\\Users\\felipe.rosa\\Desktop\\rede\\robodepdfs\\temp_original\\OneDriverRestrito\\Segmedic - Central Medic\\2021\\2021\\03.2021\\DANFE`s\\NF GALANTI MED 05-03.pdf'], [2531, r'C:\\Users\\felipe.rosa\\Desktop\\rede\\robodepdfs\\temp_original\\OneDriverRestrito\\Segmedic - Central Medic\\2021\\2021\\03.2021\\DANFE`s\\NF HYGICARE HIG E LIMP 08-03.pdf', r'C:\\Users\\felipe.rosa\\Desktop\\rede\\robodepdfs\\temp_original\\OneDriverRestrito\\Segmedic - Central Medic\\2021\\2021\\03.2021\\DANFE`s\\NF HYGICARE HIG E LIMP 08-03.pdf'], [2532, r'C:\\Users\\felipe.rosa\\Desktop\\rede\\robodepdfs\\temp_original\\OneDriverRestrito\\Segmedic - Central Medic\\2021\\2021\\03.2021\\DANFE`s\\NF HYGICARE.pdf', r'C:\\Users\\felipe.rosa\\Desktop\\rede\\robodepdfs\\temp_original\\OneDriverRestrito\\Segmedic - Central Medic\\2021\\2021\\03.2021\\DANFE`s\\NF HYGICARE.pdf'], [2533, r'C:\\Users\\felipe.rosa\\Desktop\\rede\\robodepdfs\\temp_original\\OneDriverRestrito\\Segmedic - Central Medic\\2021\\2021\\03.2021\\DANFE`s\\NF LAMBERG MAT HOSP 10-03.pdf', r'C:\\Users\\felipe.rosa\\Desktop\\rede\\robodepdfs\\temp_original\\OneDriverRestrito\\Segmedic - Central Medic\\2021\\2021\\03.2021\\DANFE`s\\NF LAMBERG MAT HOSP 10-03.pdf'], [2534, r'C:\\Users\\felipe.rosa\\Desktop\\rede\\robodepdfs\\temp_original\\OneDriverRestrito\\Segmedic - Central Medic\\2021\\2021\\03.2021\\DANFE`s\\NF LAMBERG MAT HOSP 15-03.pdf', r'C:\\Users\\felipe.rosa\\Desktop\\rede\\robodepdfs\\temp_original\\OneDriverRestrito\\Segmedic - Central Medic\\2021\\2021\\03.2021\\DANFE`s\\NF LAMBERG MAT HOSP 15-03.pdf'], [2535, r'C:\\Users\\felipe.rosa\\Desktop\\rede\\robodepdfs\\temp_original\\OneDriverRestrito\\Segmedic - Central Medic\\2021\\2021\\03.2021\\DANFE`s\\NF LAMBERG MAT HOSP 18-03.pdf', r'C:\\Users\\felipe.rosa\\Desktop\\rede\\robodepdfs\\temp_original\\OneDriverRestrito\\Segmedic - Central Medic\\2021\\2021\\03.2021\\DANFE`s\\NF LAMBERG MAT HOSP 18-03.pdf'], [2536, r'C:\\Users\\felipe.rosa\\Desktop\\rede\\robodepdfs\\temp_original\\OneDriverRestrito\\Segmedic - Central Medic\\2021\\2021\\03.2021\\DANFE`s\\NF NET CARE MED 15-03.pdf', r'C:\\Users\\felipe.rosa\\Desktop\\rede\\robodepdfs\\temp_original\\OneDriverRestrito\\Segmedic - Central Medic\\2021\\2021\\03.2021\\DANFE`s\\NF NET CARE MED 15-03.pdf'], [2537, r'C:\\Users\\felipe.rosa\\Desktop\\rede\\robodepdfs\\temp_original\\OneDriverRestrito\\Segmedic - Central Medic\\2021\\2021\\03.2021\\DANFE`s\\NF PAPELEX MAT ESC 09-03.pdf', r'C:\\Users\\felipe.rosa\\Desktop\\rede\\robodepdfs\\temp_original\\OneDriverRestrito\\Segmedic - Central Medic\\2021\\2021\\03.2021\\DANFE`s\\NF PAPELEX MAT ESC 09-03.pdf'], [2538, r'C:\\Users\\felipe.rosa\\Desktop\\rede\\robodepdfs\\temp_original\\OneDriverRestrito\\Segmedic - Central Medic\\2021\\2021\\03.2021\\DANFE`s\\NF PAPELEX MAT ESC 12-03.pdf', r'C:\\Users\\felipe.rosa\\Desktop\\rede\\robodepdfs\\temp_original\\OneDriverRestrito\\Segmedic - Central Medic\\2021\\2021\\03.2021\\DANFE`s\\NF PAPELEX MAT ESC 12-03.pdf'], [2539, r'C:\\Users\\felipe.rosa\\Desktop\\rede\\robodepdfs\\temp_original\\OneDriverRestrito\\Segmedic - Central Medic\\2021\\2021\\03.2021\\DANFE`s\\NF PAPELEX MAT ESC 18-03.pdf', r'C:\\Users\\felipe.rosa\\Desktop\\rede\\robodepdfs\\temp_original\\OneDriverRestrito\\Segmedic - Central Medic\\2021\\2021\\03.2021\\DANFE`s\\NF PAPELEX MAT ESC 18-03.pdf'], [2540, r'C:\\Users\\felipe.rosa\\Desktop\\rede\\robodepdfs\\temp_original\\OneDriverRestrito\\Segmedic - Central Medic\\2021\\2021\\03.2021\\DANFE`s\\NF PAPERPLACE MAT ESC 17-03.pdf', r'C:\\Users\\felipe.rosa\\Desktop\\rede\\robodepdfs\\temp_original\\OneDriverRestrito\\Segmedic - Central Medic\\2021\\2021\\03.2021\\DANFE`s\\NF PAPERPLACE MAT ESC 17-03.pdf'], [2541, r'C:\\Users\\felipe.rosa\\Desktop\\rede\\robodepdfs\\temp_original\\OneDriverRestrito\\Segmedic - Central Medic\\2021\\2021\\03.2021\\DANFE`s\\NF SIEMENS.pdf', r'C:\\Users\\felipe.rosa\\Desktop\\rede\\robodepdfs\\temp_original\\OneDriverRestrito\\Segmedic - Central Medic\\2021\\2021\\03.2021\\DANFE`s\\NF SIEMENS.pdf'], [2542, r'C:\\Users\\felipe.rosa\\Desktop\\rede\\robodepdfs\\temp_original\\OneDriverRestrito\\Segmedic - Central Medic\\2021\\2021\\03.2021\\DANFE`s\\NF THAISSA DE ALMEIDA SOARES 3397690.pdf', r'C:\\Users\\felipe.rosa\\Desktop\\rede\\robodepdfs\\temp_original\\OneDriverRestrito\\Segmedic - Central Medic\\2021\\2021\\03.2021\\DANFE`s\\NF THAISSA DE ALMEIDA SOARES 3397690.pdf'], [2543, r'C:\\Users\\felipe.rosa\\Desktop\\rede\\robodepdfs\\temp_original\\OneDriverRestrito\\Segmedic - Central Medic\\2021\\2021\\03.2021\\DANFE`s\\NF WR SOUZA -  GAZES PARA REFRIGERAÇÃO 09-03.pdf', r'C:\\Users\\felipe.rosa\\Desktop\\rede\\robodepdfs\\temp_original\\OneDriverRestrito\\Segmedic - Central Medic\\2021\\2021\\03.2021\\DANFE`s\\NF WR SOUZA -  GAZES PARA REFRIGERAÇÃO 09-03.pdf'], [2544, r'C:\\Users\\felipe.rosa\\Desktop\\rede\\robodepdfs\\temp_original\\OneDriverRestrito\\Segmedic - Central Medic\\2021\\2021\\03.2021\\DANFE`s\\NF- BLISSY COMERCIO.pdf', r'C:\\Users\\felipe.rosa\\Desktop\\rede\\robodepdfs\\temp_original\\OneDriverRestrito\\Segmedic - Central Medic\\2021\\2021\\03.2021\\DANFE`s\\NF- BLISSY COMERCIO.pdf'], [2545, r'C:\\Users\\felipe.rosa\\Desktop\\rede\\robodepdfs\\temp_original\\OneDriverRestrito\\Segmedic - Central Medic\\2021\\2021\\03.2021\\DANFE`s\\NF- CHATUBA DE NILOPOLIS 284011.pdf', r'C:\\Users\\felipe.rosa\\Desktop\\rede\\robodepdfs\\temp_original\\OneDriverRestrito\\Segmedic - Central Medic\\2021\\2021\\03.2021\\DANFE`s\\NF- CHATUBA DE NILOPOLIS 284011.pdf'], [2546, r'C:\\Users\\felipe.rosa\\Desktop\\rede\\robodepdfs\\temp_original\\OneDriverRestrito\\Segmedic - Central Medic\\2021\\2021\\03.2021\\DANFE`s\\NF- CHATUBA DE NILOPOLIS 372009.pdf', r'C:\\Users\\felipe.rosa\\Desktop\\rede\\robodepdfs\\temp_original\\OneDriverRestrito\\Segmedic - Central Medic\\2021\\2021\\03.2021\\DANFE`s\\NF- CHATUBA DE NILOPOLIS 372009.pdf'], [2547, r'C:\\Users\\felipe.rosa\\Desktop\\rede\\robodepdfs\\temp_original\\OneDriverRestrito\\Segmedic - Central Medic\\2021\\2021\\03.2021\\DANFE`s\\NF- CORPHO COMERCIO PROD.pdf', r'C:\\Users\\felipe.rosa\\Desktop\\rede\\robodepdfs\\temp_original\\OneDriverRestrito\\Segmedic - Central Medic\\2021\\2021\\03.2021\\DANFE`s\\NF- CORPHO COMERCIO PROD.pdf'], [2548, r'C:\\Users\\felipe.rosa\\Desktop\\rede\\robodepdfs\\temp_original\\OneDriverRestrito\\Segmedic - Central Medic\\2021\\2021\\03.2021\\DANFE`s\\NF- COSTA & COUTO CONSULT .pdf', r'C:\\Users\\felipe.rosa\\Desktop\\rede\\robodepdfs\\temp_original\\OneDriverRestrito\\Segmedic - Central Medic\\2021\\2021\\03.2021\\DANFE`s\\NF- COSTA & COUTO CONSULT .pdf'], [2549, r'C:\\Users\\felipe.rosa\\Desktop\\rede\\robodepdfs\\temp_original\\OneDriverRestrito\\Segmedic - Central Medic\\2021\\2021\\03.2021\\DANFE`s\\NF- DELL COMPUTADORES 2859074.pdf', r'C:\\Users\\felipe.rosa\\Desktop\\rede\\robodepdfs\\temp_original\\OneDriverRestrito\\Segmedic - Central Medic\\2021\\2021\\03.2021\\DANFE`s\\NF- DELL COMPUTADORES 2859074.pdf'], [2550, r'C:\\Users\\felipe.rosa\\Desktop\\rede\\robodepdfs\\temp_original\\OneDriverRestrito\\Segmedic - Central Medic\\2021\\2021\\03.2021\\DANFE`s\\NF- ESTAÇÃO D ALUZ 70.PDF', r'C:\\Users\\felipe.rosa\\Desktop\\rede\\robodepdfs\\temp_original\\OneDriverRestrito\\Segmedic - Central Medic\\2021\\2021\\03.2021\\DANFE`s\\NF- ESTAÇÃO D ALUZ 70.PDF'], [2551, r'C:\\Users\\felipe.rosa\\Desktop\\rede\\robodepdfs\\temp_original\\OneDriverRestrito\\Segmedic - Central Medic\\2021\\2021\\03.2021\\DANFE`s\\NF- ESTAÇÃO DA LUZ.pdf', r'C:\\Users\\felipe.rosa\\Desktop\\rede\\robodepdfs\\temp_original\\OneDriverRestrito\\Segmedic - Central Medic\\2021\\2021\\03.2021\\DANFE`s\\NF- ESTAÇÃO DA LUZ.pdf'], [2552, r'C:\\Users\\felipe.rosa\\Desktop\\rede\\robodepdfs\\temp_original\\OneDriverRestrito\\Segmedic - Central Medic\\2021\\2021\\03.2021\\DANFE`s\\NF- Lacrin.pdf', r'C:\\Users\\felipe.rosa\\Desktop\\rede\\robodepdfs\\temp_original\\OneDriverRestrito\\Segmedic - Central Medic\\2021\\2021\\03.2021\\DANFE`s\\NF- Lacrin.pdf'], [2553, r'C:\\Users\\felipe.rosa\\Desktop\\rede\\robodepdfs\\temp_original\\OneDriverRestrito\\Segmedic - Central Medic\\2021\\2021\\03.2021\\DANFE`s\\NF- REAL VIDRO 017935.pdf', r'C:\\Users\\felipe.rosa\\Desktop\\rede\\robodepdfs\\temp_original\\OneDriverRestrito\\Segmedic - Central Medic\\2021\\2021\\03.2021\\DANFE`s\\NF- REAL VIDRO 017935.pdf'], [2554, r'C:\\Users\\felipe.rosa\\Desktop\\rede\\robodepdfs\\temp_original\\OneDriverRestrito\\Segmedic - Central Medic\\2021\\2021\\03.2021\\DANFE`s\\NF- RICARDO DE  ASSIS NASCIMENTO 50024.pdf', r'C:\\Users\\felipe.rosa\\Desktop\\rede\\robodepdfs\\temp_original\\OneDriverRestrito\\Segmedic - Central Medic\\2021\\2021\\03.2021\\DANFE`s\\NF- RICARDO DE  ASSIS NASCIMENTO 50024.pdf'], [2555, r'C:\\Users\\felipe.rosa\\Desktop\\rede\\robodepdfs\\temp_original\\OneDriverRestrito\\Segmedic - Central Medic\\2021\\2021\\03.2021\\DANFE`s\\NF- STUDIO DESSENCES -.pdf', r'C:\\Users\\felipe.rosa\\Desktop\\rede\\robodepdfs\\temp_original\\OneDriverRestrito\\Segmedic - Central Medic\\2021\\2021\\03.2021\\DANFE`s\\NF- STUDIO DESSENCES -.pdf'], [2556, r'C:\\Users\\felipe.rosa\\Desktop\\rede\\robodepdfs\\temp_original\\OneDriverRestrito\\Segmedic - Central Medic\\2021\\2021\\03.2021\\DANFE`s\\NF- STUDIO DESSENCES.pdf', r'C:\\Users\\felipe.rosa\\Desktop\\rede\\robodepdfs\\temp_original\\OneDriverRestrito\\Segmedic - Central Medic\\2021\\2021\\03.2021\\DANFE`s\\NF- STUDIO DESSENCES.pdf'], [2557, r'C:\\Users\\felipe.rosa\\Desktop\\rede\\robodepdfs\\temp_original\\OneDriverRestrito\\Segmedic - Central Medic\\2021\\2021\\03.2021\\DANFE`s\\NF- UNIVESTTE COMERCIO 42.pdf', r'C:\\Users\\felipe.rosa\\Desktop\\rede\\robodepdfs\\temp_original\\OneDriverRestrito\\Segmedic - Central Medic\\2021\\2021\\03.2021\\DANFE`s\\NF- UNIVESTTE COMERCIO 42.pdf'], [2558, r'C:\\Users\\felipe.rosa\\Desktop\\rede\\robodepdfs\\temp_original\\OneDriverRestrito\\Segmedic - Central Medic\\2021\\2021\\03.2021\\DANFE`s\\NF-DanielRosarME-.pdf', r'C:\\Users\\felipe.rosa\\Desktop\\rede\\robodepdfs\\temp_original\\OneDriverRestrito\\Segmedic - Central Medic\\2021\\2021\\03.2021\\DANFE`s\\NF-DanielRosarME-.pdf'], [2559, r'C:\\Users\\felipe.rosa\\Desktop\\rede\\robodepdfs\\temp_original\\OneDriverRestrito\\Segmedic - Central Medic\\2021\\2021\\03.2021\\DANFE`s\\NF-JCM NITEROI REFRIGERACAO LTDA-.pdf', r'C:\\Users\\felipe.rosa\\Desktop\\rede\\robodepdfs\\temp_original\\OneDriverRestrito\\Segmedic - Central Medic\\2021\\2021\\03.2021\\DANFE`s\\NF-JCM NITEROI REFRIGERACAO LTDA-.pdf'], [2560, r'C:\\Users\\felipe.rosa\\Desktop\\rede\\robodepdfs\\temp_original\\OneDriverRestrito\\Segmedic - Central Medic\\2021\\2021\\03.2021\\DANFE`s\\NF-JCM NITEROI REFRIGERACAO LTDA-26032021.pdf', r'C:\\Users\\felipe.rosa\\Desktop\\rede\\robodepdfs\\temp_original\\OneDriverRestrito\\Segmedic - Central Medic\\2021\\2021\\03.2021\\DANFE`s\\NF-JCM NITEROI REFRIGERACAO LTDA-26032021.pdf'], [2561, r'C:\\Users\\felipe.rosa\\Desktop\\rede\\robodepdfs\\temp_original\\OneDriverRestrito\\Segmedic - Central Medic\\2021\\2021\\03.2021\\DANFE`s\\NF-JCM NITEROI REFRIGERACAO LTDA-328631.pdf', r'C:\\Users\\felipe.rosa\\Desktop\\rede\\robodepdfs\\temp_original\\OneDriverRestrito\\Segmedic - Central Medic\\2021\\2021\\03.2021\\DANFE`s\\NF-JCM NITEROI REFRIGERACAO LTDA-328631.pdf'], [2562, r'C:\\Users\\felipe.rosa\\Desktop\\rede\\robodepdfs\\temp_original\\OneDriverRestrito\\Segmedic - Central Medic\\2021\\2021\\03.2021\\DANFE`s\\NF-Kalunga-05032021.pdf', r'C:\\Users\\felipe.rosa\\Desktop\\rede\\robodepdfs\\temp_original\\OneDriverRestrito\\Segmedic - Central Medic\\2021\\2021\\03.2021\\DANFE`s\\NF-Kalunga-05032021.pdf'], [2563, r'C:\\Users\\felipe.rosa\\Desktop\\rede\\robodepdfs\\temp_original\\OneDriverRestrito\\Segmedic - Central Medic\\2021\\2021\\03.2021\\DANFE`s\\NF-REALDISTRUNICARIO-11032021.pdf', r'C:\\Users\\felipe.rosa\\Desktop\\rede\\robodepdfs\\temp_original\\OneDriverRestrito\\Segmedic - Central Medic\\2021\\2021\\03.2021\\DANFE`s\\NF-REALDISTRUNICARIO-11032021.pdf'], [2564, r'C:\\Users\\felipe.rosa\\Desktop\\rede\\robodepdfs\\temp_original\\OneDriverRestrito\\Segmedic - Central Medic\\2021\\2021\\03.2021\\DANFE`s\\SEG MEDIC 26-03.pdf', r'C:\\Users\\felipe.rosa\\Desktop\\rede\\robodepdfs\\temp_original\\OneDriverRestrito\\Segmedic - Central Medic\\2021\\2021\\03.2021\\DANFE`s\\SEG MEDIC 26-03.pdf'], [2565, r'C:\\Users\\felipe.rosa\\Desktop\\rede\\robodepdfs\\temp_original\\OneDriverRestrito\\Segmedic - Central Medic\\2021\\2021\\04.2021\\09.04 a 10.04 Nf 89.PDF', r'C:\\Users\\felipe.rosa\\Desktop\\rede\\robodepdfs\\temp_original\\OneDriverRestrito\\Segmedic - Central Medic\\2021\\2021\\04.2021\\09.04 a 10.04 Nf 89.PDF'], [2566, r'C:\\Users\\felipe.rosa\\Desktop\\rede\\robodepdfs\\temp_original\\OneDriverRestrito\\Segmedic - Central Medic\\2021\\2021\\04.2021\\21NFSE_00120722_RLBA.pdf', r'C:\\Users\\felipe.rosa\\Desktop\\rede\\robodepdfs\\temp_original\\OneDriverRestrito\\Segmedic - Central Medic\\2021\\2021\\04.2021\\21NFSE_00120722_RLBA.pdf'], [2567, r'C:\\Users\\felipe.rosa\\Desktop\\rede\\robodepdfs\\temp_original\\OneDriverRestrito\\Segmedic - Central Medic\\2021\\2021\\04.2021\\boleto_verisure_20210505_3477900.pdf', r'C:\\Users\\felipe.rosa\\Desktop\\rede\\robodepdfs\\temp_original\\OneDriverRestrito\\Segmedic - Central Medic\\2021\\2021\\04.2021\\boleto_verisure_20210505_3477900.pdf'], [2568, r'C:\\Users\\felipe.rosa\\Desktop\\rede\\robodepdfs\\temp_original\\OneDriverRestrito\\Segmedic - Central Medic\\2021\\2021\\04.2021\\boleto_verisure_20210505_3477908.pdf', r'C:\\Users\\felipe.rosa\\Desktop\\rede\\robodepdfs\\temp_original\\OneDriverRestrito\\Segmedic - Central Medic\\2021\\2021\\04.2021\\boleto_verisure_20210505_3477908.pdf'], [3618, r'C:\\Users\\felipe.rosa\\Desktop\\rede\\robodepdfs\\temp_original\\OneDriverRestrito\\Segmedic - Central Medic\\2021\\2021\\09.2021\\20210916\\NF kIOTO AMBIENTAL 112817.pdf', r'C:\\Users\\felipe.rosa\\Desktop\\rede\\robodepdfs\\temp_original\\OneDriverRestrito\\Segmedic - Central Medic\\2021\\2021\\09.2021\\20210916\\NF kIOTO AMBIENTAL 112817.pdf'], [17485, 'F:\\robodepdfs\\temp_original\\OneDriverRestrito\\IMC Saste\\2021\\1001 SERASA - NF 9347500 SENHA 6770685310.pdf', 'F:\\robodepdfs\\temp_individualizados\\OneDriverRestrito\\IMC Saste\\2021\\1001 SERASA - NF 9347500 SENHA 6770685310.pdf'], [17505, 'F:\\robodepdfs\\temp_original\\OneDriverRestrito\\IMC Saste\\2021\\OK - ABIX NF- 147.PDF', 'F:\\robodepdfs\\temp_individualizados\\OneDriverRestrito\\IMC Saste\\2021\\OK - ABIX NF- 147.PDF'], [17506, 'F:\\robodepdfs\\temp_original\\OneDriverRestrito\\IMC Saste\\2021\\OK - AD FORROS - NF 400.pdf', 'F:\\robodepdfs\\temp_individualizados\\OneDriverRestrito\\IMC Saste\\2021\\OK - AD FORROS - NF 400.pdf'], [17507, 'F:\\robodepdfs\\temp_original\\OneDriverRestrito\\IMC Saste\\2021\\OK - ADRIANA BRAGA NF- 05.pdf', 'F:\\robodepdfs\\temp_individualizados\\OneDriverRestrito\\IMC Saste\\2021\\OK - ADRIANA BRAGA NF- 05.pdf'], [17508, 'F:\\robodepdfs\\temp_original\\OneDriverRestrito\\IMC Saste\\2021\\OK - ADRIANA CAMAROTA - NF 82.pdf', 'F:\\robodepdfs\\temp_individualizados\\OneDriverRestrito\\IMC Saste\\2021\\OK - ADRIANA CAMAROTA - NF 82.pdf'], [17509, 'F:\\robodepdfs\\temp_original\\OneDriverRestrito\\IMC Saste\\2021\\OK - ADRIANA CAMAROTA ND- 03.pdf', 'F:\\robodepdfs\\temp_individualizados\\OneDriverRestrito\\IMC Saste\\2021\\OK - ADRIANA CAMAROTA ND- 03.pdf'], [17510, 'F:\\robodepdfs\\temp_original\\OneDriverRestrito\\IMC Saste\\2021\\OK - ADRIANA CAMAROTA NF 80 {1119771,1000}.pdf', 'F:\\robodepdfs\\temp_individualizados\\OneDriverRestrito\\IMC Saste\\2021\\OK - ADRIANA CAMAROTA NF 80 {1119771,1000}.pdf'], [17511, 'F:\\robodepdfs\\temp_original\\OneDriverRestrito\\IMC Saste\\2021\\OK - ADRIANA CAMAROTA NF- 83.pdf', 'F:\\robodepdfs\\temp_individualizados\\OneDriverRestrito\\IMC Saste\\2021\\OK - ADRIANA CAMAROTA NF- 83.pdf'], [17512, 'F:\\robodepdfs\\temp_original\\OneDriverRestrito\\IMC Saste\\2021\\OK - ADRIANA CAMAROTA NF- 86.pdf', 'F:\\robodepdfs\\temp_individualizados\\OneDriverRestrito\\IMC Saste\\2021\\OK - ADRIANA CAMAROTA NF- 86.pdf'], [17513, 'F:\\robodepdfs\\temp_original\\OneDriverRestrito\\IMC Saste\\2021\\OK - ADRIANA QUEIROZ NF 4 {1119764,1000}.pdf', 'F:\\robodepdfs\\temp_individualizados\\OneDriverRestrito\\IMC Saste\\2021\\OK - ADRIANA QUEIROZ NF 4 {1119764,1000}.pdf'], [17514, 'F:\\robodepdfs\\temp_original\\OneDriverRestrito\\IMC Saste\\2021\\OK - ADRIANA QUEIROZ NF- 7.pdf', 'F:\\robodepdfs\\temp_individualizados\\OneDriverRestrito\\IMC Saste\\2021\\OK - ADRIANA QUEIROZ NF- 7.pdf'], [17515, 'F:\\robodepdfs\\temp_original\\OneDriverRestrito\\IMC Saste\\2021\\OK - AILTON JOSE NF- 158.pdf', 'F:\\robodepdfs\\temp_individualizados\\OneDriverRestrito\\IMC Saste\\2021\\OK - AILTON JOSE NF- 158.pdf'], [17516, 'F:\\robodepdfs\\temp_original\\OneDriverRestrito\\IMC Saste\\2021\\OK - AILTON NF 150 {1119838,1000}.pdf', 'F:\\robodepdfs\\temp_individualizados\\OneDriverRestrito\\IMC Saste\\2021\\OK - AILTON NF 150 {1119838,1000}.pdf'], [17517, 'F:\\robodepdfs\\temp_original\\OneDriverRestrito\\IMC Saste\\2021\\OK - AILTON NF- 153.pdf', 'F:\\robodepdfs\\temp_individualizados\\OneDriverRestrito\\IMC Saste\\2021\\OK - AILTON NF- 153.pdf'], [17518, 'F:\\robodepdfs\\temp_original\\OneDriverRestrito\\IMC Saste\\2021\\OK - ALAN JACSON  - NF 202121.pdf', 'F:\\robodepdfs\\temp_individualizados\\OneDriverRestrito\\IMC Saste\\2021\\OK - ALAN JACSON  - NF 202121.pdf']]
for item in list:
    print(item[0])


# report_robodeindividualizacao = r'F:\robodepdfs\reports\robodeindividualizacao.csv'
# df = pd.read_csv(report_robodeindividualizacao)
# print(df)


# dir = r'F:\robodepdfs\2021_backup\temp_individualizados'
# dir_list = os.listdir(dir)
# for item in dir_list:
#     print(item)

# var = r'C:\Users\felipe.rosa\Desktop\rede\robodepdfs\temp_original\OneDrivers\Grupo RG LOG - RG LOG LOGISTICA\RG LOG LOGÍSTICA\112021\CUBATAO\3709_ATLANTIS GJA_R$ 1.750,00_26-11-21_NF E BOLETO - LAVAGENS DE CNTRS REPAROS REUTILIZAÇÃO DE CNTRS REPAROS - REUTILIZAÇÃO DE CARGA RETORNO - ARMADOR COSCO 5X40HC.pdf'
#
# print(len(var))

# origem = r'C:\Users\felipe.rosa\Desktop\rede\robodepdfs\centraldosrobos\OneDrivers\Grupo RG LOG - RG LOG LOGISTICA\RG LOG LOGÍSTICA\112021\CUBATAO\3709_ATLANTIS GJA_R$ 1.750,00_26-11-21_NF E BOLETO - LAVAGENS DE CNTRS REPAROS REUTILIZAÇÃO DE CNTRS REPAROS - REUTILIZAÇÃO DE CARGA RETORNO - ARMADOR COSCO 5X40HC.pdf'
# destiny = r'C:\Users\felipe.rosa\Desktop\rede\robodepdfs\temp_original\OneDrivers\Grupo RG LOG - RG LOG LOGISTICA\RG LOG LOGÍSTICA\112021\CUBATAO\3709_ATLANTIS GJA_R$ 1.750,00_26-11-21_NF E BOLETO - LAVAGENS DE CNTRS REPAROS REUTILIZAÇÃO DE CNTRS REPAROS - REUTILIZAÇÃO DE CARGA RETORNO - ARMADOR COSCO 5X40HC.pdf'
#
# path_original_and_filename = origem  # creating file path
# print(path_original_and_filename)
# arquivos_criados_ou_movidos_list = []
# # with open(path_original_and_filename, 'rb') as pdf_file:  # read file as pdf_file
# file_base_name = origem.split("\\")[-1].replace('.PDF', '').replace('.pdf', '')  # getting pdf name
# pdf = PdfFileReader(path_original_and_filename)
# for page_number in range(pdf.getNumPages()):  # for each page of this pdf
#       pdfWriter = PdfFileWriter()
#       pdfWriter.addPage(pdf.getPage(page_number))
#       destino = os.path.dirname(os.path.abspath(destino))
#       new_pdf_name = os.path.join(destino, '{}.pdf'.format(file_base_name))
#       with open(new_pdf_name, 'wb') as new_pdf:  # save new pdf for this page
#             pdfWriter.write(new_pdf)
#             new_pdf.close()
#             arquivos_criados_ou_movidos_list.append(new_pdf_name)
#             print('Criado from temp_original to temp_individualizados: ', new_pdf_name)
# # pdf_file.close()
# print(arquivos_criados_ou_movidos_list)









# shutil.move(origin,destiny)

# destiny_path = r'C:\Users\felipe.rosa\Desktop\teste'
# origin_path = os.path.dirname(os.path.abspath(origin))
# filename = origin.split('\\')[-1]  # pega o nome do arquivo
# call(["robocopy",
#       "{origin}".format(origin=origin_path),
#       "{destiny}".format(destiny=destiny_path),
#       "{filename}".format(filename=filename),
#       "/z"])
#