from decouple import config
from pymongo import MongoClient

# acesso ao db via impostosretidos@mcsmarkup.com.br

def consultadeversao():
    client = MongoClient(config("DB_VERSAO_URL"))
    db = client.get_database(config("DB_VERSAO_NAME"))
    records = db.db_versao.find_one()
    controle_de_versao = records['versao']
    if controle_de_versao == '01':
        return 'versao_atualizada'
    else:
        return 'versao_desatualizada'
