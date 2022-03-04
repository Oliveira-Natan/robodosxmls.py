from requests import Session
import base64
import json
import io
import xml.etree.ElementTree as ET
import csv
import os
from os import path
import random
from requests.api import request
from pymongo import MongoClient
import csv
import logging
import time
import datetime

def robodosxmls():
    def test():
        print("ok")


    class GettingAPI:
        r1 = Session()
        headering = {
            "Content-Type": "application/json",
            "x-api-key": "948a78438b7293c001e19c3dd44489a801497ab6",
            "x-api-id": "c7ee8a69beda0c7c64564ea9b88486bcec3543a3",
            "Connection": "keep-alive"
        }
        r1.headers.update(headering)

        def __init__(self, url="https://api.arquivei.com.br/v1/nfse/received?"):
            self.url = url

        def Decoding64(self, content):
            ''' Receive a byte --> Change_to_string --> Select_data part --> decode_64 to byte --> byte_to_string --> format string as XML --> return list of ET(XML)'''

            decoded_64 = base64.b64decode(content['xml'])
            byte_to_string = decoded_64.decode()

            tree = ET.ElementTree(ET.fromstring(byte_to_string))
            return tree

        def Decoding64Manual(self, content):
            ''' Receive a byte --> Change_to_string --> Select_data part --> decode_64 to byte --> byte_to_string --> format string as XML --> return list of ET(XML)'''

            decoded_64 = base64.b64decode(content['json'])
            byte_to_string = decoded_64.decode()

            return byte_to_string

        def WritingManual(self, content):
            data = json.loads(content)['Data']
            with open("ocr_json/NFS_{}_{}.json".format(data['Numero'], data['Prestador']['Cnpj']), "w") as file:
                file.write(content)

        def getNFReceived(self, json_version=False):
            '''return list of TREES of first 50 NF'''

            request = self.r1.get(self.url)
            lista = []
            data = json.load(io.BytesIO(request._content))['data']
            for tree in data:
                lista.append((self.Decoding64(tree)))
            return lista

        def getFullNFReceived(self, json_version=False):
            '''return list of TREES of all the NF's (over count=50)'''
            request = self.r1.get(self.url)
            print(datetime.time.hour)
            print("Lendo todas da API")
            data = json.load(io.BytesIO(request._content))
            lista = []
            cursor = 11500

            while data['count'] == 50:
                time.sleep(2)
                request = self.r1.get("{}&cursor={}".format(self.url, cursor))
                data = json.load(io.BytesIO(request._content))
                with open("print_response.json", "w") as file:
                    json.dump(data, file)
                with open("print_request.json", "w") as file:
                    json.dump(request.request.url, file)
                    json.dump(dict(request.request.headers), file)
                    json.dump(dict(request.headers), file)
                for tree in data['data']:
                    lista.append((self.Decoding64(tree)))

                cursor += 50

            request2 = self.r1.get("{}&cursor={}".format(self.url, cursor))
            for tree in json.load(io.BytesIO(request2._content))['data']:
                lista.append((self.Decoding64(tree)))

            return lista

        def getFullNFReceivedManual(self, json_version=False):
            '''return list of TREES of all the NF's (over count=50)'''
            self.url = "https://api.arquivei.com.br/v1/nfse/received/manual?"
            request = self.r1.get(self.url)
            print("Lendo todas da OCR")
            data = json.load(io.BytesIO(request._content))
            lista = []
            cursor = 1

            while data['count'] == 50:
                request = self.r1.get("{}&cursor={}".format(self.url, cursor))
                data = json.load(io.BytesIO(request._content))

                for tree in data['data']:
                    lista.append((self.Decoding64Manual(tree)))
                    print(self.Decoding64Manual(tree))
                    self.WritingManual(self.Decoding64Manual(tree))
                cursor += 50

            request2 = self.r1.get("{}&cursor={}".format(self.url, cursor))
            for tree in json.load(io.BytesIO(request2._content))['data']:
                lista.append(self.Decoding64Manual(tree))
                print(self.Decoding64Manual(tree))
                self.WritingManual(self.Decoding64Manual(tree))

            return lista

        def WriteNFReceived(self):
            ''' Receive a byte --> Change_to_string --> Select_data part --> decode_64 to byte --> byte_to_string --> format string as XML --> Write file with ID name'''

            request = self.r1.get(self.url)
            for v1 in json.load(io.BytesIO(request._content))['data']:
                tree = self.Decoding64(v1)
                if 'id' in v1:
                    ET.register_namespace('', "http://www.abrasf.org.br/nfse.xsd")
                    with open('{}.xml'.format(v1['id']), 'w') as file:
                        tree.write(file, encoding="unicode", method="html")
                else:
                    ET.register_namespace('', "http://www.w3.org/2000/09/xmldsig#")
                    ET.register_namespace('', "http://www.portalfiscal.inf.br/nfe")
                    # ET.SubElement(tree.findall(), ET.QName("", "http://www.portalfiscal.inf.br/nfe"))
                    with open('{}.xml'.format(v1['access_key']), 'w') as file:
                        tree.write(file, encoding="unicode", method="html")
            return request._content

        def getAllByCnpj(self, cnpj):
            ''' return list of first 50 of Nfse/received - Nfse/emitted - Nfe/received - Nfe/emitted '''

            urls = ["https://api.arquivei.com.br/v1/nfse/emitted", "https://api.arquivei.com.br/v1/nfse/received",
                    "https://api.arquivei.com.br/v1/nfe/emitted", "https://api.arquivei.com.br/v1/nfe/received"]
            lista = []
            for url in urls:
                v1 = GettingAPI("{}?cnpj[]={}".format(url, cnpj)).getNFReceived()
                lista += v1
            return lista

        def WriteAllByCnpj(self, cnpj):
            ''' WRITE first 50 of Nfse/received - Nfse/emitted - Nfe/received - Nfe/emitted '''

            urls = ["https://api.arquivei.com.br/v1/nfse/emitted", "https://api.arquivei.com.br/v1/nfse/received",
                    "https://api.arquivei.com.br/v1/nfe/emitted", "https://api.arquivei.com.br/v1/nfe/received"]
            for url in urls:
                title = "{}_{}d_{}".format(url[-13: -8].replace("1", ""), url[-8:-1], cnpj).replace("/", "")
                os.mkdir(title)
                os.chdir(title)
                GettingAPI("{}?cnpj[]={}".format(url, cnpj)).WriteNFReceived()
                os.chdir("../")


    class Changer():

        def __init__(self, arquivei_tree, manual=False, file=None):
            self.arquivei_tree = arquivei_tree
            self.manual = manual
            self.file = file

        def Arquivei(self, string_elemento_arquivei):
            tree = self.arquivei_tree
            root = tree.getroot()
            lista = []
            for elemento in root.iter():
                if self.Prefixing(string_elemento_arquivei) == elemento.tag:
                    lista.append(elemento)
            return lista

        def Prefixing(self, string):
            if string.startswith("{http"):
                return string.replace("{http://www.abrasf.org.br/nfse.xsd}", "")
            else:
                return '{}{}'.format('{http://www.abrasf.org.br/nfse.xsd}', string)

        def Finding(self, root, string):
            for elemento in root.iter():
                if string == elemento.tag:
                    return elemento

        def FindingAll(self, root, string):
            lista = []
            for elemento in root.iter():
                if string == elemento.tag:
                    lista.append(elemento)
            return lista

        # print(Finding(root, "DataEmissao"))

        def ChangingValue(self, root):

            dicter_api = [
                {"Numero": {"value": "Numero", "done_fit": 0, "done_arq": 0}},
                {"CodigoVerificacao": {"value": "CodigoVerificacao", "done_fit": 0, "done_arq": 0}},
                {"DataEmissao": {"value": "DataEmissao", "done_fit": 0, "done_arq": 0}},  # AGEITAR O FORMATO#
                {"Numero": {"value": "Numero", "done_fit": 1, "done_arq": 1}},
                {"OptanteSimplesNacional": {"value": "OptanteSimplesNacional", "done_fit": 0, "done_arq": 0}},
                {"ValorServicos": {"value": "ValorServicos", "done_fit": 0, "done_arq": 0}},
                {"ValorIss": {"value": "ValorIss", "done_fit": 0, "done_arq": 0}},
                {"BaseCalculo": {"value": "ValorServicos", "done_fit": 0, "done_arq": 0}},
                {"Aliquota": {"value": "Aliquota", "done_fit": 0, "done_arq": 0}},
                {"CodigoTributacaoMunicipio": {"value": "ItemListaServico", "done_fit": 0, "done_arq": 0}},
                {"Discriminacao": {"value": "Discriminacao", "done_fit": 0, "done_arq": 0}},
                {"CodigoMunicipio": {"value": "Numero", "done_fit": 0, "done_arq": 2}},
                {"Cnpj": {"value": "Cnpj", "done_fit": 0, "done_arq": 0}},
                {"InscricaoMunicipal": {"value": "InscricaoMunicipal", "done_fit": 0, "done_arq": 0}},
                {"RazaoSocial": {"value": "RazaoSocial", "done_fit": 0, "done_arq": 0}},
                {"CodigoMunicipio": {"value": "CodigoMunicipio", "done_fit": 1, "done_arq": 0}},
                {"Uf": {"value": "Uf", "done_fit": 0, "done_arq": 0}},  #
                {"Cnpj": {"value": "Cnpj", "done_fit": 1, "done_arq": 2}},  #
                {"RazaoSocial": {"value": "RazaoSocial", "done_fit": 1, "done_arq": 1}},
                {"CodigoMunicipio": {"value": "CodigoMunicipio", "done_fit": 2, "done_arq": 1}},  #
                {"Uf": {"value": "Uf", "done_fit": 1, "done_arq": 1}},  #
            ]

            # DICTER vindo do json da ARQUIVEI para o XML da FIT, com o acressimo do done_arq2 para sinalizar tags dentro de tags do JSON vindo da arquivei
            dicter_api_ocr = [
                {"Numero": {"value": "Numero", "done_fit": 0, "done_arq": 0}},
                {"CodigoVerificacao": {"value": "CodigoVerificacao", "done_fit": 0, "done_arq": 0}},
                {"DataEmissao": {"value": "DataEmissao", "done_fit": 0, "done_arq": 0}},  # AGEITAR O FORMATO#
                {"Numero": {"value": "Numero", "done_fit": 1, "done_arq": "Rps"}},
                {"OptanteSimplesNacional": {"value": "OptanteSimplesNacional", "done_fit": 0, "done_arq": 0}},
                {"ValorServicos": {"value": "ValorServicos", "done_fit": 0, "done_arq": "Servico"}},
                {"ValorIss": {"value": "ValorIss", "done_fit": 0, "done_arq": "Servico"}},
                {"BaseCalculo": {"value": "ValorServicos", "done_fit": 0, "done_arq": "Servico"}},
                {"Aliquota": {"value": "Aliquota", "done_fit": 0, "done_arq": "Servico"}},
                {"CodigoTributacaoMunicipio": {"value": "CodigoServico", "done_fit": 0, "done_arq": "Servico"}},
                # PERGUNTAR
                {"Discriminacao": {"value": "DataDeVencimento", "done_fit": 0, "done_arq": "Servico",
                                   "done_arq2": "Discriminacao"}},
                {"CodigoMunicipio": {"value": "Numero", "done_fit": 1, "done_arq": "Rps"}},
                {"Cnpj": {"value": "Cnpj", "done_fit": 0, "done_arq": "Prestador"}},
                {"InscricaoMunicipal": {"value": "InscricaoMunicipal", "done_fit": 0, "done_arq": "Tomador"}},
                {"RazaoSocial": {"value": "RazaoSocial", "done_fit": 0, "done_arq": "Prestador"}},
                {"CodigoMunicipio": {"value": "CodigoMunicipio", "done_fit": 1, "done_arq": "Prestador",
                                     "done_arq2": "Endereco"}},
                {"Uf": {"value": "Uf", "done_fit": 0, "done_arq": "Prestador", "done_arq2": "Endereco"}},  #
                {"Cnpj": {"value": "Cnpj", "done_fit": 1, "done_arq": "Tomador"}},  #
                {"RazaoSocial": {"value": "RazaoSocial", "done_fit": 1, "done_arq": "Tomador"}},
                {"CodigoMunicipio": {"value": "CodigoMunicipio", "done_fit": 2, "done_arq": "Tomador",
                                     "done_arq2": "Endereco"}},  #
                {"Uf": {"value": "Uf", "done_fit": 1, "done_arq": "Tomador", "done_arq2": "Endereco"}},  #
            ]

            dicter_rede = [
                {"Numero": {"value": "NumeroNFe", "done_fit": 0, "done_arq": 0}},
                {"CodigoVerificacao": {"value": "CodigoVerificacao", "done_fit": 0, "done_arq": 0}},
                {"DataEmissao": {"value": "DataEmissaoNFe", "done_fit": 0, "done_arq": 0}},  # AGEITAR O FORMATO#
                {"Numero": {"value": "NumeroRPS", "done_fit": 1, "done_arq": 0}},
                {"OptanteSimplesNacional": {"value": "OpcaoSimples", "done_fit": 0, "done_arq": 0}},
                {"ValorServicos": {"value": "ValorServicos", "done_fit": 0, "done_arq": 0}},
                {"ValorIss": {"value": "ValorISS", "done_fit": 0, "done_arq": 0}},
                {"BaseCalculo": {"value": "ValorServicos", "done_fit": 0, "done_arq": 0}},
                {"Aliquota": {"value": "AliquotaServicos", "done_fit": 0, "done_arq": 0}},
                {"CodigoTributacaoMunicipio": {"value": "CodigoServico", "done_fit": 0, "done_arq": 0}},
                {"Discriminacao": {"value": "Discriminacao", "done_fit": 0, "done_arq": 0}},
                {"Cnpj": {"value": "CNPJ", "done_fit": 0, "done_arq": 0}},
                {"InscricaoMunicipal": {"value": "InscricaoPrestador", "done_fit": 0, "done_arq": 0}},
                {"RazaoSocial": {"value": "RazaoSocialPrestador", "done_fit": 0, "done_arq": 0}},
                {"CodigoMunicipio": {"value": "Cidade", "done_fit": 1, "done_arq": 0}},
                {"Uf": {"value": "UF", "done_fit": 0, "done_arq": 0}},  #
                {"Cnpj": {"value": "CNPJ", "done_fit": 1, "done_arq": 1}},  #
                {"RazaoSocial": {"value": "RazaoSocialTomador", "done_fit": 1, "done_arq": 0}},
                {"CodigoMunicipio": {"value": "Cidade", "done_fit": 2, "done_arq": 1}},  #
                {"Uf": {"value": "UF", "done_fit": 1, "done_arq": 1}},  #
            ]
            dicter = dicter_api_ocr if self.manual == True else dicter_api
            for o in dicter:
                keys_obj = list(o.keys())
                fit_rep = o[keys_obj[0]]["done_fit"]
                arq_rep = o[keys_obj[0]]["done_arq"]
                value = o[keys_obj[0]]["value"]

                elementos = self.FindingAll(root, self.Prefixing(keys_obj[0]))
                try:
                    if self.manual == True:
                        # print(len(list(o[keys_obj[0]].keys())))
                        if len(list(o[keys_obj[0]].keys())) > 3:
                            arq_rep2 = o[keys_obj[0]]["done_arq2"]
                            elementos[fit_rep].text = self.arquivei_tree['Data'][arq_rep][arq_rep2][value]
                        else:
                            elementos[fit_rep].text = self.arquivei_tree['Data'][arq_rep][value] if arq_rep != 0 else \
                            self.arquivei_tree['Data'][value]
                        print("OK")
                        print(elementos[fit_rep].text)
                    else:
                        elementos[fit_rep].text = (self.Arquivei(o[keys_obj[0]]['value'])[arq_rep].text).strip()
                except IndexError:
                    pass

        def ReturnNome(self):
            numero_nota = self.Arquivei("Numero")[0].text if self.Arquivei("Numero") else "ERROR{}".format(
                random.randint(1, 1000))
            cnpj_prestador = self.Arquivei("Cnpj")[0].text if self.Arquivei("Cnpj") else "ERROR{}".format(
                random.randint(1, 1000))
            nome = "NFS_{}_{}".format(numero_nota, cnpj_prestador)
            return nome

        def ReturnManualNome(self):
            try:
                return "NFS_{}_{}".format(self.arquivei_tree['Data']['Numero'],
                                          self.arquivei_tree['Data']['Prestador']['Cnpj'])
            except Exception:
                return "NFS_ERROR_ERROR"

        def Done(self):
            base_xml = "PENvbnN1bHRhck5mc2VSZXNwb3N0YSB4bWxucz0iaHR0cDovL3d3dy5hYnJhc2Yub3JnLmJyL25mc2UueHNkIgogICAgeG1sbnM6bnMyPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwLzA5L3htbGRzaWcjIj4KICAgIDxMaXN0YU5mc2U+CiAgICAgICAgPENvbXBOZnNlPgogICAgICAgICAgICA8TmZzZT4KICAgICAgICAgICAgICAgIDxJbmZOZnNlPgogICAgICAgICAgICAgICAgICAgIDxOdW1lcm8+PC9OdW1lcm8+CiAgICAgICAgICAgICAgICAgICAgPENvZGlnb1ZlcmlmaWNhY2FvPjwvQ29kaWdvVmVyaWZpY2FjYW8+CiAgICAgICAgICAgICAgICAgICAgPERhdGFFbWlzc2FvPjwvRGF0YUVtaXNzYW8+CiAgICAgICAgICAgICAgICAgICAgPElkZW50aWZpY2FjYW9ScHM+CiAgICAgICAgICAgICAgICAgICAgICAgIDxOdW1lcm8+PC9OdW1lcm8+CiAgICAgICAgICAgICAgICAgICAgICAgIDxTZXJpZT48L1NlcmllPgogICAgICAgICAgICAgICAgICAgICAgICA8VGlwbz48L1RpcG8+CiAgICAgICAgICAgICAgICAgICAgPC9JZGVudGlmaWNhY2FvUnBzPgogICAgICAgICAgICAgICAgICAgIDxEYXRhRW1pc3Nhb1Jwcz48L0RhdGFFbWlzc2FvUnBzPgogICAgICAgICAgICAgICAgICAgIDxOYXR1cmV6YU9wZXJhY2FvPjwvTmF0dXJlemFPcGVyYWNhbz4KICAgICAgICAgICAgICAgICAgICA8UmVnaW1lRXNwZWNpYWxUcmlidXRhY2FvPjwvUmVnaW1lRXNwZWNpYWxUcmlidXRhY2FvPgogICAgICAgICAgICAgICAgICAgIDxPcHRhbnRlU2ltcGxlc05hY2lvbmFsPjwvT3B0YW50ZVNpbXBsZXNOYWNpb25hbD4KICAgICAgICAgICAgICAgICAgICA8SW5jZW50aXZhZG9yQ3VsdHVyYWw+PC9JbmNlbnRpdmFkb3JDdWx0dXJhbD4KICAgICAgICAgICAgICAgICAgICA8TmZzZVN1YnN0aXR1aWRhPjwvTmZzZVN1YnN0aXR1aWRhPgogICAgICAgICAgICAgICAgICAgIDxTZXJ2aWNvPgogICAgICAgICAgICAgICAgICAgICAgICA8VmFsb3Jlcz4KICAgICAgICAgICAgICAgICAgICAgICAgICAgIDxWYWxvclNlcnZpY29zPjwvVmFsb3JTZXJ2aWNvcz4KICAgICAgICAgICAgICAgICAgICAgICAgICAgIDxWYWxvckRlZHVjb2VzPjwvVmFsb3JEZWR1Y29lcz4KICAgICAgICAgICAgICAgICAgICAgICAgICAgIDxWYWxvclBpcz48L1ZhbG9yUGlzPgogICAgICAgICAgICAgICAgICAgICAgICAgICAgPFZhbG9yQ29maW5zPjwvVmFsb3JDb2ZpbnM+CiAgICAgICAgICAgICAgICAgICAgICAgICAgICA8VmFsb3JJbnNzPjwvVmFsb3JJbnNzPgogICAgICAgICAgICAgICAgICAgICAgICAgICAgPFZhbG9ySXI+PC9WYWxvcklyPgogICAgICAgICAgICAgICAgICAgICAgICAgICAgPFZhbG9yQ3NsbD48L1ZhbG9yQ3NsbD4KICAgICAgICAgICAgICAgICAgICAgICAgICAgIDxJc3NSZXRpZG8+PC9Jc3NSZXRpZG8+CiAgICAgICAgICAgICAgICAgICAgICAgICAgICA8VmFsb3JJc3M+PC9WYWxvcklzcz4KICAgICAgICAgICAgICAgICAgICAgICAgICAgIDxWYWxvcklzc1JldGlkbz48L1ZhbG9ySXNzUmV0aWRvPgogICAgICAgICAgICAgICAgICAgICAgICAgICAgPE91dHJhc1JldGVuY29lcz48L091dHJhc1JldGVuY29lcz4KICAgICAgICAgICAgICAgICAgICAgICAgICAgIDxCYXNlQ2FsY3Vsbz48L0Jhc2VDYWxjdWxvPgogICAgICAgICAgICAgICAgICAgICAgICAgICAgPEFsaXF1b3RhPjwvQWxpcXVvdGE+CiAgICAgICAgICAgICAgICAgICAgICAgICAgICA8VmFsb3JMaXF1aWRvTmZzZT48L1ZhbG9yTGlxdWlkb05mc2U+CiAgICAgICAgICAgICAgICAgICAgICAgICAgICA8RGVzY29udG9JbmNvbmRpY2lvbmFkbz48L0Rlc2NvbnRvSW5jb25kaWNpb25hZG8+CiAgICAgICAgICAgICAgICAgICAgICAgICAgICA8RGVzY29udG9Db25kaWNpb25hZG8+PC9EZXNjb250b0NvbmRpY2lvbmFkbz4KICAgICAgICAgICAgICAgICAgICAgICAgPC9WYWxvcmVzPgogICAgICAgICAgICAgICAgICAgICAgICA8SXRlbUxpc3RhU2Vydmljbz48L0l0ZW1MaXN0YVNlcnZpY28+CiAgICAgICAgICAgICAgICAgICAgICAgIDxDb2RpZ29UcmlidXRhY2FvTXVuaWNpcGlvPjwvQ29kaWdvVHJpYnV0YWNhb011bmljaXBpbz4KICAgICAgICAgICAgICAgICAgICAgICAgPERpc2NyaW1pbmFjYW8+PC9EaXNjcmltaW5hY2FvPgogICAgICAgICAgICAgICAgICAgICAgICA8Q29kaWdvTXVuaWNpcGlvPjwvQ29kaWdvTXVuaWNpcGlvPgogICAgICAgICAgICAgICAgICAgIDwvU2Vydmljbz4KICAgICAgICAgICAgICAgICAgICA8UHJlc3RhZG9yU2Vydmljbz4KICAgICAgICAgICAgICAgICAgICAgICAgPElkZW50aWZpY2FjYW9QcmVzdGFkb3I+CiAgICAgICAgICAgICAgICAgICAgICAgICAgICA8Q25waj48L0NucGo+CiAgICAgICAgICAgICAgICAgICAgICAgICAgICA8SW5zY3JpY2FvTXVuaWNpcGFsPjwvSW5zY3JpY2FvTXVuaWNpcGFsPgogICAgICAgICAgICAgICAgICAgICAgICA8L0lkZW50aWZpY2FjYW9QcmVzdGFkb3I+CiAgICAgICAgICAgICAgICAgICAgICAgIDxSYXphb1NvY2lhbD48L1JhemFvU29jaWFsPgogICAgICAgICAgICAgICAgICAgICAgICA8Tm9tZUZhbnRhc2lhPjwvTm9tZUZhbnRhc2lhPgogICAgICAgICAgICAgICAgICAgICAgICA8RW5kZXJlY28+CiAgICAgICAgICAgICAgICAgICAgICAgICAgICA8RW5kZXJlY28+PC9FbmRlcmVjbz4KICAgICAgICAgICAgICAgICAgICAgICAgICAgIDxCYWlycm8+PC9CYWlycm8+CiAgICAgICAgICAgICAgICAgICAgICAgICAgICA8Q29kaWdvTXVuaWNpcGlvPjwvQ29kaWdvTXVuaWNpcGlvPgogICAgICAgICAgICAgICAgICAgICAgICAgICAgPFVmPjwvVWY+CiAgICAgICAgICAgICAgICAgICAgICAgICAgICA8Q2VwPjwvQ2VwPgogICAgICAgICAgICAgICAgICAgICAgICA8L0VuZGVyZWNvPgogICAgICAgICAgICAgICAgICAgIDwvUHJlc3RhZG9yU2Vydmljbz4KICAgICAgICAgICAgICAgICAgICA8VG9tYWRvclNlcnZpY28+CiAgICAgICAgICAgICAgICAgICAgICAgIDxJZGVudGlmaWNhY2FvVG9tYWRvcj4KICAgICAgICAgICAgICAgICAgICAgICAgICAgIDxDcGZDbnBqPgogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIDxDbnBqPjwvQ25waj4KICAgICAgICAgICAgICAgICAgICAgICAgICAgIDwvQ3BmQ25waj4KICAgICAgICAgICAgICAgICAgICAgICAgPC9JZGVudGlmaWNhY2FvVG9tYWRvcj4KICAgICAgICAgICAgICAgICAgICAgICAgPFJhemFvU29jaWFsPjwvUmF6YW9Tb2NpYWw+CiAgICAgICAgICAgICAgICAgICAgICAgIDxFbmRlcmVjbz4KICAgICAgICAgICAgICAgICAgICAgICAgICAgIDxFbmRlcmVjbz48L0VuZGVyZWNvPgogICAgICAgICAgICAgICAgICAgICAgICAgICAgPE51bWVybz48L051bWVybz4KICAgICAgICAgICAgICAgICAgICAgICAgICAgIDxCYWlycm8+PC9CYWlycm8+CiAgICAgICAgICAgICAgICAgICAgICAgICAgICA8Q29kaWdvTXVuaWNpcGlvPjwvQ29kaWdvTXVuaWNpcGlvPgogICAgICAgICAgICAgICAgICAgICAgICAgICAgPFVmPjwvVWY+CiAgICAgICAgICAgICAgICAgICAgICAgICAgICA8Q2VwPjwvQ2VwPgogICAgICAgICAgICAgICAgICAgICAgICA8L0VuZGVyZWNvPgogICAgICAgICAgICAgICAgICAgICAgICA8Q29udGF0bz4KICAgICAgICAgICAgICAgICAgICAgICAgICAgIDxUZWxlZm9uZT48L1RlbGVmb25lPgogICAgICAgICAgICAgICAgICAgICAgICAgICAgPEVtYWlsPjwvRW1haWw+CiAgICAgICAgICAgICAgICAgICAgICAgIDwvQ29udGF0bz4KICAgICAgICAgICAgICAgICAgICA8L1RvbWFkb3JTZXJ2aWNvPgogICAgICAgICAgICAgICAgICAgIDxPcmdhb0dlcmFkb3I+CiAgICAgICAgICAgICAgICAgICAgICAgIDxDb2RpZ29NdW5pY2lwaW8+PC9Db2RpZ29NdW5pY2lwaW8+CiAgICAgICAgICAgICAgICAgICAgICAgIDxVZj48L1VmPgogICAgICAgICAgICAgICAgICAgIDwvT3JnYW9HZXJhZG9yPgogICAgICAgICAgICAgICAgPC9JbmZOZnNlPgogICAgICAgICAgICA8L05mc2U+CiAgICAgICAgPC9Db21wTmZzZT4KICAgIDwvTGlzdGFOZnNlPgo8L0NvbnN1bHRhck5mc2VSZXNwb3N0YT4="
            # tree = ET.parse("xml_fit_blank.xml")
            tree = ET.ElementTree(ET.fromstring(base64.b64decode(base_xml)))
            ET.register_namespace('', "http://www.abrasf.org.br/nfse.xsd")
            root = tree.getroot()

            self.ChangingValue(root)

            save_path = r'F:\Impostos Retidos\Conversor FIT'
            if self.manual == True:
                # with open("allnotes/OCR_{}.xml".format(self.ReturnManualNome()), "w") as file:
                #     tree.write(file, encoding="unicode", method="html")

                tree.write("{}\{}.xml".format(save_path, self.ReturnManualNome()), method="html")
                return self.ReturnManualNome()
            else:
                # with open("allnotes/{}.xml".format(self.ReturnNome()), "w") as file:
                #     tree.write(file, encoding="unicode", method="html")

                tree.write("{}\{}.xml".format(save_path, self.ReturnNome()), method="html")
                return self.ReturnNome()


    class Processing():
        cluster = MongoClient(
            "mongodb+srv://mcsdeclaraki:markup01@cluster0.vb8dc.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
        database = cluster["myFirstDatabase"]
        collection = database["db_ArquiveiRetencao"]

        def ProcessingNFe():
            pass

        def ProcessingNFSe(self):
            # try:
            #     arquivei_florest = GettingAPI().getNFReceived2()
            # except KeyError:
            #     arquivei_florest = GettingAPI("https://api.arquivei.com.br/v1/nfse/received?abrasf=false").getNFReceived2()

            ja_salvas = 0
            try:
                arquivei_florest_xml = GettingAPI().getFullNFReceived()
                # arquivei_florest_json = GettingAPI().getFullNFReceivedManual()
                for arquivei_tree in arquivei_florest_xml:
                    if self.collection.find_one({"nome": Changer(arquivei_tree).ReturnNome()}) == None:
                        print(self.collection.find_one({"nome": Changer(arquivei_tree).ReturnNome()}))
                        fit_way = Changer(arquivei_tree).Done()
                        self.collection.insert_one({"nome": fit_way})
                    else:
                        ja_salvas += 1
                        print(self.collection.find_one({"nome": Changer(arquivei_tree).ReturnNome()}))
                        print("JA TEM {}".format(Changer(arquivei_tree).ReturnNome()))
                print("Foram encontradas {}".format(arquivei_florest_xml.count()))
                print("Ja haviam sido salvas {}".format(ja_salvas))
                print("Foram adicionadas{}")
                time.sleep(2000)
                # for arquivei_tree in arquivei_florest_json:
                #     if self.collection.find_one({"nome": Changer(arquivei_tree).ReturnManualNome()}) != "aloow": #None:
                #         print(self.collection.find_one({"nome": Changer(arquivei_tree).ReturnManualNome()}))
                #         fit_way = Changer(arquivei_tree).Done()
                #         # self.collection.insert_one({"nome": fit_way})
                #     else:
                #         print(self.collection.find_one({"nome": Changer(arquivei_tree).ReturnManualNome()}))
                #         print("JA TEM {}".format(Changer(arquivei_tree).ReturnManualNome()))
            except Exception as e:
                self.Logger(e)

        def ProcessingCTe():
            pass

        def WriteCSV(self):

            with open("allNotes.csv", 'w', newline='', encoding='utf-8') as file:
                writing = csv.writer(file)
                writing.writerow(["numero", "cnpj_prestador", "cnpj_tomador"])
                for xml in GettingAPI().getFullNFReceived():

                    event_data = []
                    root = xml.getroot()
                    for row in root:
                        event_data.append(Changer(xml).Arquivei("Numero")[0].text)
                        event_data.append(Changer(xml).Arquivei("Cnpj")[0].text)
                        event_data.append(Changer(xml).Arquivei("Cnpj")[1].text)
                        writing.writerow(event_data)

        def Logger(self, e):
            # Create a logging instance
            logger = logging.getLogger('my_application')
            logger.setLevel(logging.INFO)  # you can set this to be DEBUG, INFO, ERROR

            # Assign a file-handler to that instance
            fh = logging.FileHandler("ERRROOOOR.txt")
            fh.setLevel(logging.INFO)  # again, you can set this differently

            # Format your logs (optional)
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            fh.setFormatter(formatter)  # This will set the format to the file handler

            # Add the handler to your logging instance
            logger.addHandler(fh)

            try:
                raise ValueError("Some error occurred")
            except ValueError as e:
                logger.exception(e)


    Processing().ProcessingNFSe()
    # Processing().ProcessingManual()
    # Processing().WriteCSV()


    # print(Processing().collection.find_one({"nome": "dqdq"}))


    # def ProcessingManual(self):
    #     all = GettingAPI("https://api.arquivei.com.br/v1/nfse/received/manual?").getFullNFReceivedManual()
    #     for json_object in all:
    #         ChangerManual(json_object).


    # decoded_64 = base64.b64decode(string)
    # byte_to_string = decoded_64.decode()
    # with open("{}.json".format(manual_name), "w+") as file:
    #     file.write(byte_to_string)


    # ALOW
if __name__ == "__main__":
    robodosxmls()
