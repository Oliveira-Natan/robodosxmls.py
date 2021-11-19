# -*- encoding: utf-8 -*-
import PySimpleGUI as sg
from pathlib import Path
import pandas as pd
from datetime import datetime
import os
from shutil import copyfile
# import jinja2

pd.set_option('display.max_columns', None)

root_path = sg.popup_get_folder('Escolha o local onde estão as antigas planilhas que deseja atualizar:')

# listar arquivos na pasta
start = datetime.now()
print(start)
today = datetime.now()

# root_path = r'C:\Users\felipe.rosa\Documents\GitHub\mcstoolsretencoes\sandbox\robodasplanilhas\teste_11_11_2021'
# files_in_folder = os.listdir(root_path)

# listando arquivos que sejam excel
files_in_folder = [_ for _ in os.listdir(root_path) if _.endswith('.xlsx')]

files_path = []
for files in files_in_folder:
    files_path.append(root_path + "\\" + files)
print(files_path)

# criando folder para salvar arquivos atualizados
try:
    os.mkdir(root_path + "\\" + "atualizacoes")
except:
    pass

filename_novo = sg.popup_get_file('Agora, escolha o planilhão, com os dados mais atualizados:')
# filename_novo = r'C:\Users\felipe.rosa\Documents\GitHub\mcstoolsretencoes\sandbox\robodasplanilhas\planilhao_original.xlsx'
df2 = pd.read_excel(filename_novo, dtype=object)

# montar lista com path e nome da empresa
for files in files_path:
    try:
        df_2_parcial = df2.iloc[:, 0:27]
        # filename_antigo = r'C:\Users\felipe.rosa\Documents\GitHub\mcstoolsretencoes\dist\Power safe importação.xlsx'
        filename_antigo = files

        file_antigo = Path(filename_antigo)
        directory_to_save = str(file_antigo.parent) + "\\" + "atualizacoes" + "\\"

        # filename = os.path.basename(filename_antigo)

        df1 = pd.read_excel(file_antigo, dtype=object)
        df_1_parcial = df1.iloc[:, 0:27]

        # identificar nome da empresa no presente relatorio
        client_name = df_1_parcial.iloc[[0], [0]]
        client_name = client_name.values.tolist()
        client_name = client_name[0][0]
        # print(client_name)

        # filtrando cliente no planilhão
        df_2_parcial = df_2_parcial[df_2_parcial[df_2_parcial.iloc[:, [0]].columns[0]] == client_name]
        print('planilhao: ', len(df_2_parcial))
        # print('filtrando cliente no planilhão: ', df_2_parcial.iloc[[0], [0]])

        # update da df_1_parcial da planilha antiga com os dados novos que vieram do planilhão (df_2_parcial)
        # df_1_parcial.update(df_2_parcial)
        print('planilha antiga: ', len(df_1_parcial))

        a = df1.set_index(['Número Nota Fiscal', 'CNPJ Prestador'])  # antiga
        b = df_2_parcial.set_index(['Número Nota Fiscal', 'CNPJ Prestador'])  # planilhao

        df_de_dados_novos = (a.combine_first(b).reset_index().reindex(columns=df1.columns))

        # df_de_dados_novos = df_de_dados_novos.drop_duplicates([df_de_dados_novos.iloc[:, [3]].columns[0],
        #                                                        df_de_dados_novos.iloc[:, [5]].columns[0]], keep='last', ignore_index=True)
        # print(df_de_dados_novos)
        # df_de_dados_novos.to_excel('novos.xlsx', index=False, header=True, encoding='utf-8-sig')

        print('quantidade de dados novos no cliente ', client_name, ': ', (len(b) - len(a)))
        if (len(b) - len(a)) != 0:
    #         df_de_dados_novos = df_de_dados_novos.loc[df_de_dados_novos.duplicated([df_de_dados_novos.iloc[:, [3]].columns[0],
    #                                                                                 df_de_dados_novos.iloc[:, [1]].columns[0],
    #                                                                                 df_de_dados_novos.iloc[:, [5]].columns[0]
    #                                                                                 ], keep="first")]  # deixando apenas o que veio do df_2_parcial a partir da coluna do numero da nfse
    #         print(len(df_de_dados_novos))
    #
    #         # incluindo df_de_dados_novos no df1 como df_final
    #         df_final = pd.concat([df1, df_de_dados_novos])
    #
            new_filename = client_name + ' - atualizada em ' + today.strftime("%d-%m-%Y_%H-%M-%S")
            final_directory = str(directory_to_save) + new_filename + '.xlsx'
            df_de_dados_novos.to_excel(final_directory, index=False, header=True, encoding='utf-8-sig')

        else:
            copyfile(files, str(directory_to_save) + "\\" + files.split("\\")[-1])
    except:
        erros_list = []
        erros_list.append(new_filename)
        print('Erro ao processar: ',new_filename )

sg.popup('Seu arquivo foi processado com sucesso e está disponível em: ', directory_to_save,
         'Identificamos erros no processamento dos seguintes arquivos: ',erros_list)