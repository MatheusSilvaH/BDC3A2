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

    # def get_valor_conta(self):
    #     # Cria uma nova conexão com o banco
    #     mongo = MongoQueries()
    #     mongo.connect()
    #
    #     # Realiza uma consulta no mongo e retorna o cursor resultante para a variável
    #     query_result = mongo.db['conta'].aggregate([{
    #                                                 {
    #                                                     '$lookup': {
    #                                                         'from': 'parcelas',
    #                                                         'localField': 'id',
    #                                                         'foreignField': 'id_conta',
    #                                                         'as': 'parcelas'
    #                                                     }
    #                                                 }, {
    #                                                     '$unwind': {
    #                                                         'path': '$parcelas'
    #                                                     }
    #                                                 }, {
    #                                                     '$group': {
    #                                                         'id': 1,
    #                                                         'valor': $sum:{'$parcelas'},
    #                                                         'tipo': 1,
    #                                                         '_id': 0
    #                                                     }}}])
    #
    #     # Converte o cursos em lista e em DataFrame
    #     df_parcelas = pd.DataFrame(list(query_result))
    #     # Fecha a conexão com o mongo
    #     mongo.close()
    #     # Exibe o resultado
    #     print(df_parcelas[["id_conta", "valor"]])
    #     input("Pressione Enter para Sair do Relatório de Itens de Pedidos")

    def get_relatorio_contas_a_pagar (self):
        # Cria uma nova conexão com o banco
        mongo = MongoQueries()
        mongo.connect()
        # Recupera os dados transformando em um DataFrame
        query_result = mongo.db["pedidos"].aggregate([
                                                    {
                                                        '$lookup': {
                                                            'from': 'fornecedores',
                                                            'localField': 'cnpj',
                                                            'foreignField': 'cnpj',
                                                            'as': 'fornecedor'
                                                        }
                                                    }, {
                                                        '$unwind': {
                                                            'path': '$fornecedor'
                                                        }
                                                    }, {
                                                        '$project': {
                                                            'codigo_pedido': 1,
                                                            'data_pedido': 1,
                                                            'empresa': '$fornecedor.nome_fantasia',
                                                            'cpf': 1,
                                                            '_id': 0
                                                        }
                                                    }, {
                                                        '$lookup': {
                                                            'from': 'clientes',
                                                            'localField': 'cpf',
                                                            'foreignField': 'cpf',
                                                            'as': 'cliente'
                                                        }
                                                    }, {
                                                        '$unwind': {
                                                            'path': '$cliente'
                                                        }
                                                    }, {
                                                        '$project': {
                                                            'codigo_pedido': 1,
                                                            'data_pedido': 1,
                                                            'empresa': 1,
                                                            'cliente': '$cliente.nome',
                                                            '_id': 0
                                                        }
                                                    }, {
                                                        '$lookup': {
                                                            'from': 'itens_pedido',
                                                            'localField': 'codigo_pedido',
                                                            'foreignField': 'codigo_pedido',
                                                            'as': 'item'
                                                        }
                                                    }, {
                                                        '$unwind': {
                                                            'path': '$item', 'preserveNullAndEmptyArrays': True
                                                        }
                                                    }, {
                                                        '$project': {
                                                            'codigo_pedido': 1,
                                                            'data_pedido': 1,
                                                            'empresa': 1,
                                                            'cliente': 1,
                                                            'item_pedido': '$item.codigo_item_pedido',
                                                            'quantidade': '$item.quantidade',
                                                            'valor_unitario': '$item.valor_unitario',
                                                            'valor_total': {
                                                                '$multiply': [
                                                                    '$item.quantidade', '$item.valor_unitario'
                                                                ]
                                                            },
                                                            'codigo_produto': '$item.codigo_produto',
                                                            '_id': 0
                                                        }
                                                    }, {
                                                        '$lookup': {
                                                            'from': 'produtos',
                                                            'localField': 'codigo_produto',
                                                            'foreignField': 'codigo_produto',
                                                            'as': 'produto'
                                                        }
                                                    }, {
                                                        '$unwind': {
                                                            'path': '$produto', 'preserveNullAndEmptyArrays': True
                                                        }
                                                    }, {
                                                        '$project': {
                                                            'codigo_pedido': 1,
                                                            'data_pedido': 1,
                                                            'empresa': 1,
                                                            'cliente': 1,
                                                            'item_pedido': 1,
                                                            'quantidade': 1,
                                                            'valor_unitario': 1,
                                                            'valor_total': 1,
                                                            'produto': '$produto.descricao_produto',
                                                            '_id': 0
                                                        }
                                                    }, {
                                                        '$sort': {
                                                            'cliente': 1,
                                                            'item_pedido': 1
                                                        }
                                                    }
                                                ])
        df_pedido = pd.DataFrame(list(query_result))
        # Fecha a conexão com o Mongo
        mongo.close()
        print(df_pedido[["codigo_pedido", "data_pedido", "cliente", "empresa", "item_pedido", "produto", "quantidade", "valor_unitario", "valor_total"]])
        input("Pressione Enter para Sair do Relatório de Pedidos")
