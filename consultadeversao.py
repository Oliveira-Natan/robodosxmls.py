from pymongo import MongoClient

# acesso ao db via impostosretidos@mcsmarkup.com.br

def consultadeversao():
    db_password = 'mcstools'
    CONNECTION_STRING = 'mongodb+srv://mcstools:{}@cluster0.addpt.mongodb.net/myFirstDatabase?retryWrites=true&w=majority'.format(db_password)
    client = MongoClient(CONNECTION_STRING)
    db = client.get_database('mcstools')
    records = db.db_versao.find_one()
    controle_de_versao = records['versao']
    if controle_de_versao == '01':
        return 'versao_atualizada'
    else:
        return 'versao_desatualizada'
