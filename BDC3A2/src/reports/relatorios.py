from conexion.mongo_queries import MongoQueries
import pandas as pd
from pymongo import ASCENDING, DESCENDING

class Relatorio:
    def __init__(self):
        pass

    def get_relatorio_conta(self):
        # Cria uma nova conexão com o banco
        mongo = MongoQueries()
        mongo.connect()
        # Recupera os dados transformando em um DataFrame
        query_result = mongo.db["conta"].find({},
                                                 {"id": 1,
                                                  "tipo": 1,
                                                  "data_quitacao": 1,
                                                  "_id": 0
                                                 }).sort("id", ASCENDING)
        df_conta = pd.DataFrame(list(query_result))
        # Fecha a conexão com o Mongo
        mongo.close()
        # Exibe o resultado
        print(df_conta)
        input("Pressione Enter para Sair do Relatório de Contas")

    def get_relatorio_parcelas(self):
        # Cria uma nova conexão com o banco
        mongo = MongoQueries()
        mongo.connect()
        # Recupera os dados transformando em um DataFrame
        query_result = mongo.db["parcelas"].find({},
                                                 {"id": 1,
                                                  "id_conta": 1,
                                                  "data_vencimento": 1,
                                                  "data_pagamento": 1,
                                                  "numero_parcela": 1,
                                                  "valor": 1,
                                                  "_id": 0
                                                 }).sort("id_conta", ASCENDING)
        df_parcelas = pd.DataFrame(list(query_result))
        # Fecha a conexão com o mongo
        mongo.close()
        # Exibe o resultado
        print(df_parcelas)
        input("Pressione Enter para Sair do Relatório de Parcelas")

    def get_valor_conta(self):
        # Cria uma nova conexão com o banco
        mongo = MongoQueries()
        mongo.connect()

        # Realiza uma consulta no mongo e retorna o cursor resultante para a variável
        query_result = mongo.db["parcelas"].aggregate([{'$group': {'_id':"id_conta", 'valor_conta': {'$sum':'valor'}}}])

        # Converte o cursos em lista e em DataFrame
        df_parcelas = pd.DataFrame(list(query_result))
        # Fecha a conexão com o mongo
        mongo.close()
        # Exibe o resultado
        print(df_parcelas[["id_conta", "valor"]])
        input("Pressione Enter para Sair do Relatório de Itens de Pedidos")
