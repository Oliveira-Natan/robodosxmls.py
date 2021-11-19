# -*- encoding: utf-8 -*-
import PySimpleGUI as sg
import pandas as pd
import numpy as np
import os
from pathlib import Path
from datetime import datetime

pd.set_option('display.max_columns', None)

# planilhao = r'planilhao_original.xlsx'
planilhao = sg.popup_get_file('Escolha o planilhão que deseja aplicar as regras:')
empresas_rj_sp = sg.popup_get_file('Escolha a planilha "empresas_rj_sp.xlsx" atualizada:')
df_base_cepom = sg.popup_get_file('Escolha a planilha "base_cpom.xlsx" atualizada:')
df_aliquota_cpom = sg.popup_get_file('Escolha a planilha "aliquota_cpom.xlsx" atualizada:')

df_planilhao = pd.read_excel(planilhao)
df_planilhao['filial_formatada'] = df_planilhao[df_planilhao.iloc[:, [7]].columns[0]]
df_planilhao['filial_formatada'] = df_planilhao['filial_formatada'].str.replace('.','', regex=True)
df_planilhao['filial_formatada'] = df_planilhao['filial_formatada'].str.replace('-','')
df_planilhao['filial_formatada'] = df_planilhao['filial_formatada'].str.replace('/','')
# print(df_planilhao['filial_formatada'])

# buscando colunas 5 e 6: cnpj e municipio
# empresas_rj_sp = r'empresas_rj_sp.xlsx'
# empresas_rj_sp = sg.popup_get_file('Escolha a planilha "empresas_rj_sp.xlsx" atualizada:')
df_empresas_rj_sp = pd.read_excel(empresas_rj_sp)
df_empresas_rj_sp = df_empresas_rj_sp[[df_empresas_rj_sp.iloc[:, [5]].columns[0],df_empresas_rj_sp.iloc[:, [6]].columns[0]]]
df_empresas_rj_sp = df_empresas_rj_sp.rename(columns={df_empresas_rj_sp.iloc[:, [0]].columns[0]: 'filial_formatada'})
df_empresas_rj_sp[df_empresas_rj_sp.iloc[:, [0]].columns[0]] = df_empresas_rj_sp[df_empresas_rj_sp.iloc[:, [0]].columns[0]].apply(str)
df_empresas_rj_sp[df_empresas_rj_sp.iloc[:, [0]].columns[0]] = df_empresas_rj_sp[df_empresas_rj_sp.iloc[:, [0]].columns[0]].apply(lambda x: x.zfill(14))
# print(df_empresas_rj_sp)

# trazendo municipio do prestador para planilhao
df_planilhao_filial_com_municipio = df_planilhao.merge(df_empresas_rj_sp, on='filial_formatada', how='left')
df_planilhao_filial_com_municipio['check_filial_prest_mun'] = df_planilhao_filial_com_municipio[df_planilhao_filial_com_municipio.iloc[:, [18]].columns[0]] == df_planilhao_filial_com_municipio[df_planilhao_filial_com_municipio.iloc[:, [-1]].columns[0]]
# conferindo colunas municipio prestador, municipio (filial) e check_filial_prest_mun
# print(df_planilhao_filial_com_municipio[[df_planilhao_filial_com_municipio.iloc[:, [15]].columns[0],
#                                          df_planilhao_filial_com_municipio.iloc[:, [16]].columns[0],
#                                          df_planilhao_filial_com_municipio.iloc[:, [18]].columns[0],
#                                          df_planilhao_filial_com_municipio.iloc[:, [-2]].columns[0],
#                                          df_planilhao_filial_com_municipio.iloc[:, [-1]].columns[0]]])

## PRIMEIRO CÁLCULO DE ISS:
# coluna 15 (aliquota ISS), onde coluna -1 (check) for True, recebe 0, senão continua o que era na coluna 15 (aliquota ISS)
df_planilhao_filial_com_municipio[df_planilhao_filial_com_municipio.iloc[:, [15]].columns[0]] = np.where(
df_planilhao_filial_com_municipio[df_planilhao_filial_com_municipio.iloc[:, [-1]].columns[0]]==True, 0, df_planilhao_filial_com_municipio[df_planilhao_filial_com_municipio.iloc[:, [15]].columns[0]]
)

# coluna 16 (retenção ISS), onde coluna -1 (check) for True, recebe 0, senão continua o que era na coluna 16 (retenção ISS)
df_planilhao_filial_com_municipio[df_planilhao_filial_com_municipio.iloc[:, [16]].columns[0]] = np.where(
df_planilhao_filial_com_municipio[df_planilhao_filial_com_municipio.iloc[:, [-1]].columns[0]]==True, 0, df_planilhao_filial_com_municipio[df_planilhao_filial_com_municipio.iloc[:, [16]].columns[0]]
)

# print(df_planilhao_filial_com_municipio[[df_planilhao_filial_com_municipio.iloc[:, [15]].columns[0],
#                                          df_planilhao_filial_com_municipio.iloc[:, [16]].columns[0],
#                                          df_planilhao_filial_com_municipio.iloc[:, [18]].columns[0],
#                                          df_planilhao_filial_com_municipio.iloc[:, [-2]].columns[0],
#                                          df_planilhao_filial_com_municipio.iloc[:, [-1]].columns[0]]])
df_planilhao_filial_com_municipio['LC'] = df_planilhao_filial_com_municipio[df_planilhao_filial_com_municipio.iloc[:, [17]].columns[0]].astype('str').str.split('|',expand=True)[2]
df_planilhao_filial_com_municipio['LC'] = df_planilhao_filial_com_municipio['LC'].str.split(': ',expand=True)[1]
df_planilhao_filial_com_municipio['LC'] = df_planilhao_filial_com_municipio['LC'].apply(lambda x: x.zfill(6))
df_planilhao_filial_com_municipio['LC'] = df_planilhao_filial_com_municipio['LC'].str.replace(" ", "")
# print(df_planilhao_filial_com_municipio['LC'])

df_planilhao_filial_com_municipio['prestador_formatada'] = df_planilhao_filial_com_municipio[df_planilhao_filial_com_municipio.iloc[:, [5]].columns[0]].astype('str')
df_planilhao_filial_com_municipio['prestador_formatada'] = df_planilhao_filial_com_municipio['prestador_formatada'].str.replace('.','', regex=True)
df_planilhao_filial_com_municipio['prestador_formatada'] = df_planilhao_filial_com_municipio['prestador_formatada'].str.replace('-','')
df_planilhao_filial_com_municipio['prestador_formatada'] = df_planilhao_filial_com_municipio['prestador_formatada'].str.replace('/','')
df_planilhao_filial_com_municipio['prestador_formatada'] = df_planilhao_filial_com_municipio['prestador_formatada'].apply(lambda x: x.zfill(14))
# print(df_planilhao_filial_com_municipio['prestador_formatada'])

# se a col 29 (municipio da filial) é de São Paulo e a col 18 (municipio do prestador) não for São Paulo, então sim (deve calcular retenção de iss)
df_planilhao_filial_com_municipio.loc[(df_planilhao_filial_com_municipio[df_planilhao_filial_com_municipio.iloc[:, [29]].columns[0]] == 'São Paulo') &
                                      (df_planilhao_filial_com_municipio[df_planilhao_filial_com_municipio.iloc[:, [18]].columns[0]] != 'São Paulo'),
                                      'analisar_se_calcular_iss'] = 'sim'

df_planilhao_filial_com_municipio.loc[(df_planilhao_filial_com_municipio[df_planilhao_filial_com_municipio.iloc[:, [29]].columns[0]] == 'São Paulo') &
                                      (df_planilhao_filial_com_municipio[df_planilhao_filial_com_municipio.iloc[:, [18]].columns[0]] == 'São Paulo'),
                                      'analisar_se_calcular_iss'] = 'não'

# se a col 29 (municipio da filial) é de São Paulo e a col 18 (municipio do prestador) não for São Paulo, mas não estiver na lista (que exige retenção), então não (deve recalcular retenção de iss)
lista_de_servicos = ["01.01","01.02","01.03","01.04","01.05","01.06","01.07","01.08","01.09","02.01","03.01","03.02","04.01","04.02","04.03","04.04","04.05","04.06","04.07","04.08","04.09","04.10","04.11","04.12","04.13","04.14","04.15","04.16","04.18","04.20","04.21","05.01","05.04","05.05","05.06","05.07","05.08","07.01","07.03","07.06","07.07","07.08","07.13","07.20","07.21","07.22","08.02","09.02","09.03","10.01","10.02","10.03","10.05","10.06","10.07","10.08","10.09","10.10","11.03","12.13","13.02","13.03","13.04","13.05","14.01","14.02","14.03","14.04","14.05","14.06","14.07","14.08","14.09","14.10","14.11","14.12","14.13","14.14","17.01","17.02","17.03","17.04","17.06","17.08","17.09","17.11","17.12","17.13","17.14","17.15","17.16","17.17","17.18","17.19","17.20","17.21","17.22","17.23","17.24","17.25","18.01","19.01","23.01","24.01","25.01","25.03","25.04","25.05","26.01","27.01","28.01","29.01","30.01","31.01","32.01","33.01","34.01","35.01","36.01","37.01","38.01","39.01","40.01"]
df_planilhao_filial_com_municipio.loc[
    (df_planilhao_filial_com_municipio[df_planilhao_filial_com_municipio.iloc[:, [29]].columns[0]] == 'São Paulo') &
    (df_planilhao_filial_com_municipio[df_planilhao_filial_com_municipio.iloc[:, [18]].columns[0]] != 'São Paulo') &
    (df_planilhao_filial_com_municipio['LC'].isin(lista_de_servicos) == False), 'analisar_se_calcular_iss'] = 'não'
# print(df_planilhao_filial_com_municipio['analisar_se_calcular_iss'].value_counts())

df_planilhao_filial_com_municipio.loc[df_planilhao_filial_com_municipio[df_planilhao_filial_com_municipio.iloc[:, [29]].columns[0]] != 'São Paulo', 'analisar_se_calcular_iss'] = 'não'
# print(df_planilhao_filial_com_municipio['analisar_se_calcular_iss'].value_counts())

# # lendo csv do CPOM

# df_base_cepom = sg.popup_get_file('Escolha a planilha "base_cpom.xlsx" atualizada:')
df_base_cepom = pd.read_excel(df_base_cepom, dtype=object)
# criando DF com filial_formatada e LC a partir do CPOM
df_base_cepom = df_base_cepom[[df_base_cepom.iloc[:, [0]].columns[0],df_base_cepom.iloc[:, [-1]].columns[0]]]


df_base_cepom = df_base_cepom.rename(columns={df_base_cepom.iloc[:, [0]].columns[0]: 'prestador_formatada'})
df_base_cepom['LC'] = df_base_cepom[[df_base_cepom.iloc[:, [1]].columns[0]]].astype('str')
df_base_cepom['LC'] = df_base_cepom['LC'].str.split(' -', expand=True)[0]
df_base_cepom_cnpj_lc = df_base_cepom[[df_base_cepom.iloc[:, [0]].columns[0], df_base_cepom.iloc[:, [-1]].columns[0]]]
df_base_cepom_cnpj_lc['cpom'] = 'não'

df_planilhao_filial_com_municipio = df_planilhao_filial_com_municipio.merge(df_base_cepom_cnpj_lc, on=['prestador_formatada', 'LC'], how='left')

df_planilhao_filial_com_municipio.loc[(df_planilhao_filial_com_municipio['analisar_se_calcular_iss'] == 'sim') &
                                      (df_planilhao_filial_com_municipio['cpom'] != 'sim'),
                                      'conclusão_analise_calcular_iss'] = 'sim'

df_planilhao_filial_com_municipio.loc[(df_planilhao_filial_com_municipio['analisar_se_calcular_iss'] == 'sim') &
                                      (df_planilhao_filial_com_municipio['cpom'] == 'não'),
                                      'conclusão_analise_calcular_iss'] = 'zerar'

df_planilhao_filial_com_municipio.loc[(df_planilhao_filial_com_municipio['analisar_se_calcular_iss'] != 'sim') &
                                      (df_planilhao_filial_com_municipio['cpom'] != 'não'),
                                      'conclusão_analise_calcular_iss'] = 'não'

print(df_planilhao_filial_com_municipio['analisar_se_calcular_iss'].value_counts())
print(df_planilhao_filial_com_municipio['cpom'].value_counts())
print(df_planilhao_filial_com_municipio['conclusão_analise_calcular_iss'].value_counts())

# df_planilhao_filial_com_municipio['conclusão_analise_calcular_iss'] = df_planilhao_filial_com_municipio['conclusão_analise_calcular_iss'].replace(np.nan, 'não')

# # lendo csv do CPOM
# df_aliquota_cpom = sg.popup_get_file('Escolha a planilha "aliquota_cpom.xlsx" atualizada:')
df_aliquota_cpom = pd.read_excel(df_aliquota_cpom, dtype=object)
df_planilhao_filial_com_municipio = df_planilhao_filial_com_municipio.merge(df_aliquota_cpom, on=['LC'], how='left')
# print(df_planilhao_filial_com_municipio[df_planilhao_filial_com_municipio.iloc[:, [-1]].columns[0]])

## SEGUNDO CÁLCULO DE ISS:
# ajustar a aliquota conforme o que está na planilha (5%, 2,9%, se não estiver na tabela 0%)
# coluna 15 (aliquota ISS), onde coluna -1 (check) for True, recebe 0, senão continua o que era na coluna 15 (aliquota ISS)
df_planilhao_filial_com_municipio[df_planilhao_filial_com_municipio.iloc[:, [15]].columns[0]] = np.where(
df_planilhao_filial_com_municipio[df_planilhao_filial_com_municipio.iloc[:, [-2]].columns[0]] == 'zerar', 0, df_planilhao_filial_com_municipio[df_planilhao_filial_com_municipio.iloc[:, [15]].columns[0]]
)

# coluna 16 (retenção ISS), onde coluna -1 (check) for True, recebe 0, senão continua o que era na coluna 16 (retenção ISS)
df_planilhao_filial_com_municipio[df_planilhao_filial_com_municipio.iloc[:, [16]].columns[0]] = np.where(
df_planilhao_filial_com_municipio[df_planilhao_filial_com_municipio.iloc[:, [-2]].columns[0]] == 'zerar', 0, df_planilhao_filial_com_municipio[df_planilhao_filial_com_municipio.iloc[:, [16]].columns[0]]
)

# coluna 15 (aliquota ISS), onde coluna -1 (check) for True, recebe 0, senão continua o que era na coluna 15 (aliquota ISS)
df_planilhao_filial_com_municipio[df_planilhao_filial_com_municipio.iloc[:, [15]].columns[0]] = np.where(
df_planilhao_filial_com_municipio[df_planilhao_filial_com_municipio.iloc[:, [-2]].columns[0]] == 'sim', df_planilhao_filial_com_municipio[df_planilhao_filial_com_municipio.iloc[:, [-1]].columns[0]],
    df_planilhao_filial_com_municipio[df_planilhao_filial_com_municipio.iloc[:, [15]].columns[0]]
)

# coluna 16 (retenção ISS), onde coluna -1 (check) for True, recebe 0, senão continua o que era na coluna 16 (retenção ISS)
df_planilhao_filial_com_municipio[df_planilhao_filial_com_municipio.iloc[:, [16]].columns[0]] = np.where(
df_planilhao_filial_com_municipio[df_planilhao_filial_com_municipio.iloc[:, [-2]].columns[0]] == 'sim', df_planilhao_filial_com_municipio[df_planilhao_filial_com_municipio.iloc[:, [15]].columns[0]]/100*df_planilhao_filial_com_municipio[df_planilhao_filial_com_municipio.iloc[:, [13]].columns[0]], df_planilhao_filial_com_municipio[df_planilhao_filial_com_municipio.iloc[:, [16]].columns[0]]
)

# df_planilhao_filial_com_municipio['regra_cpom'] = df_planilhao_filial_com_municipio.loc[
#     (df_planilhao_filial_com_municipio[df_planilhao_filial_com_municipio.iloc[:, [29]].columns[0]] == 'São Paulo') &
#     (df_planilhao_filial_com_municipio[df_planilhao_filial_com_municipio.iloc[:, [18]].columns[0]] != 'São Paulo')]

# df_planilhao_filial_com_municipio.loc[(df_planilhao_filial_com_municipio[df_planilhao_filial_com_municipio.iloc[:, [29]].columns[0]] == 'São Paulo', 'regra_cpom') & (df_planilhao_filial_com_municipio[df_planilhao_filial_com_municipio.iloc[:, [18]].columns[0]] != 'São Paulo', 'regra_cpom')] = 'sim'


# # pesquisando Cepom
# df_base_cepom_cnpj_lc = df_base_cepom_cnpj_lc.loc[(df_base_cepom_cnpj_lc[df_base_cepom_cnpj_lc.iloc[:, [0]].columns[0]] == '00000068000170') & (df_base_cepom_cnpj_lc[df_base_cepom_cnpj_lc.iloc[:, [1]].columns[0]] == '14.01')]
# df_base_cepom_cnpj_lc = df_base_cepom[[df_base_cepom.iloc[:, [0]].columns[0],df_base_cepom.iloc[:, [-1]].columns[0]]]
# print(df_base_cepom_cnpj_lc)

# print(df_planilhao_filial_com_municipio)

#df_planilhao_filial_com_municipio.loc[df_planilhao_filial_com_municipio[df_planilhao_filial_com_municipio.iloc[:, [29]].columns[0]] == 'São Paulo', 'regra_cpom'] = 'sim'


# df_planilhao_filial_com_municipio.to_excel('planilhao_filial_com_municipio2.xlsx', index=False, header=True, encoding='utf-8-sig')

# df_planilhao_atualizado = df_planilhao_filial_com_municipio.iloc[:, 0:28]

file_antigo = Path(planilhao)
directory_to_save = str(file_antigo.parent) + "\\"
today = datetime.now()
new_filename = 'mcsretencao_planilhao - atualizada em ' + today.strftime("%d-%m-%Y_%H-%M-%S")
final_directory = str(directory_to_save) + new_filename + '.xlsx'

df_planilhao_filial_com_municipio.to_excel(final_directory, index=False, header=True, encoding='utf-8-sig')
sg.popup('Seu arquivo foi processado com sucesso e está disponível em: ', directory_to_save)