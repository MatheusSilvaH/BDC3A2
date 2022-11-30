import pandas as pd
from bson import ObjectId

from reports.relatorios import Relatorio

from model.parcelas import Parcelas
from model.conta import Conta

from controller.controller_conta import Controller_Conta
from conexion.mongo_queries import MongoQueries


class Controller_Parcela:
    def __init__(self):
        self.ctrl_conta = Controller_Conta()
        self.mongo = MongoQueries()
        self.relatorio = Relatorio()

    def inserir_parcelas(self) -> Parcelas:
        # Cria uma nova conexão com o banco
        self.mongo.connect()

        # Lista as contas existentes para inserir na parcela
        self.relatorio.get_relatorio_contas()
        id_conta = int(str(input("Digite o id da Conta: ")))
        conta = self.valida_pedido(id_conta)
        if pedido == None:
            return None

        # Lista os produtos existentes para inserir no item de pedido
        self.relatorio.get_relatorio_produtos()
        codigo_produto = int(str(input("Digite o código do Produto: ")))
        produto = self.valida_produto(codigo_produto)
        if produto == None:
            return None

        # Solicita a quantidade de itens do pedido para o produto selecionado
        quantidade = float(input(f"Informe a quantidade de itens do produto {produto.get_descricao()}: "))
        # Solicita o valor unitário do produto selecionado
        valor_unitario = float(input(f"Informe o valor unitário do produto {produto.get_descricao()}: "))

        proximo_item_pedido = self.mongo.db["itens_pedido"].aggregate([
            {
                '$group': {
                    '_id': '$itens_pedido',
                    'proximo_item_pedido': {
                        '$max': '$codigo_item_pedido'
                    }
                }
            }, {
                '$project': {
                    'proximo_item_pedido': {
                        '$sum': [
                            '$proximo_item_pedido', 1
                        ]
                    },
                    '_id': 0
                }
            }
        ])

        proximo_item_pedido = int(list(proximo_item_pedido)[0]['proximo_item_pedido'])
        # Cria um dicionário para mapear as variáveis de entrada e saída
        data = dict(codigo_item_pedido=proximo_item_pedido, valor_unitario=valor_unitario, quantidade=quantidade,
                    codigo_pedido=int(pedido.get_codigo_pedido()), codigo_produto=int(produto.get_codigo()))
        # Insere e Recupera o código do novo item de pedido
        id_item_pedido = self.mongo.db["itens_pedido"].insert_one(data)
        # Recupera os dados do novo item de pedido criado transformando em um DataFrame
        df_item_pedido = self.recupera_item_pedido(id_item_pedido.inserted_id)
        # Cria um novo objeto Item de Pedido
        novo_item_pedido = ItemPedido(df_item_pedido.codigo_item_pedido.values[0], df_item_pedido.quantidade.values[0],
                                      df_item_pedido.valor_unitario.values[0], pedido, produto)
        # Exibe os atributos do novo Item de Pedido
        print(novo_item_pedido.to_string())
        self.mongo.close()
        # Retorna o objeto novo_item_pedido para utilização posterior, caso necessário
        return novo_item_pedido

    def atualizar_parcela(self) -> Parcelas:
        # Cria uma nova conexão com o banco que permite alteração
        self.mongo.connect()

        # Solicita ao usuário o código do item de pedido a ser alterado
        id = int(input("Id de Parcela que irá alterar: "))

        # Verifica se o item de pedido existe na base de dados
        if not self.verifica_existencia_item_pedido(codigo_item_pedido):

            # Lista os pedido existentes para inserir no item de pedido
            self.relatorio.get_relatorio_pedidos()
            codigo_pedido = int(str(input("Digite o número do Pedido: ")))
            pedido = self.valida_pedido(codigo_pedido)
            if pedido == None:
                return None

            # Lista os produtos existentes para inserir no item de pedido
            self.relatorio.get_relatorio_produtos()
            codigo_produto = int(str(input("Digite o código do Produto: ")))
            produto = self.valida_parcela(codigo_produto)
            if produto == None:
                return None

            # Solicita a quantidade de itens do pedido para o produto selecionado
            quantidade = float(input(f"Informe a quantidade de itens do produto {produto.get_descricao()}: "))
            # Solicita o valor unitário do produto selecionado
            valor_unitario = float(input(f"Informe o valor unitário do produto {produto.get_descricao()}: "))

            # Atualiza o item de pedido existente
            self.mongo.db["[parcela]"].update_one({"id": id},
                                                     {"$set": {"quantidade": quantidade,
                                                               "valor_unitario": valor_unitario,
                                                               "codigo_pedido": int(pedido.get_codigo_pedido()),
                                                               "codigo_produto": int(produto.get_codigo())
                                                               }
                                                      })
            # Recupera os dados do novo item de pedido criado transformando em um DataFrame
            df_parcela = self.recupera_parcela(id)
            # Cria um novo objeto Item de Pedido
            parcela_atualizada = Parcelas(df_parcela.id.values[0],
                                            df_parcela.id_conta.values[0],
                                            df_parcela.data_vencimento.values[0],
                                            df_parcela.data_pagamento.values[0],
                                            df_parcela.numero_parcela.values[0],
                                            df_parcela.valor.values[0])
            # Exibe os atributos do item de pedido
            print(parcela_atualizada.to_string())
            self.mongo.close()
            # Retorna o objeto pedido_atualizado para utilização posterior, caso necessário
            return parcela_atualizada
        else:
            self.mongo.close()
            print(f"O id {id} não existe.")
            return None

    def excluir_item_pedido(self):
        # Cria uma nova conexão com o banco que permite alteração
        self.mongo.connect()

        id = int(input("Id da Parcela que irá excluir: "))

        # Verifica se a Parcela existe na base de dados
        if not self.verifica_existencia_parcela(id):
            # Recupera os dados da parcela criada transformando em um DataFrame
            df_parcela = self.recupera_parcela(id)
            conta = self.valida_conta(int(df_parcela.id_conta.values[0]))

            opcao_excluir = input(f"Tem certeza que deseja excluir a parcela {id} [S ou N]: ")
            if opcao_excluir.lower() == "s":
                # Revome o item de pedido da tabela
                self.mongo.db["parcela"].delete_one({"id": id})
                # Cria um novo objeto Item de Pedido para informar que foi removido
                parcela_excluida = Parcelas(df_parcela.id.values[0],
                                            conta,
                                            df_parcela.data_vencimento.values[0],
                                            df_parcela.data_pagamento.values[0],
                                            df_parcela.numero_parcela.values[0],
                                            df_parcela.valor.values[0])
                self.mongo.close()
                # Exibe os atributos do produto excluído
                print("Parcela Removida com Sucesso!")
                print(parcela_excluida.to_string())
        else:
            self.mongo.close()
            print(f"O id {id} não existe.")

    def verifica_existencia_parcela(self, id= None) -> bool:
        # Recupera os dados do novo pedido criado transformando em um DataFrame
        df_parcela = self.recupera_id_parcela(id=id)
        return df_parcela.empty

    def recupera_parcela(self, _id: ObjectId = None) -> bool:
        # Recupera os dados do novo pedido criado transformando em um DataFrame
        df_parcela = pd.DataFrame(list(self.mongo.db["parcelas"].find({"_id": _id}, {"id": 1, "id_conta": 1,
                                                                                     "data_vencimento": 1,
                                                                                     "data_pagamento": 1,
                                                                                     "numero_parcela": 1,
                                                                                     "valor": 1,
                                                                                     "_id": 0})))
        return df_parcela

    # def recupera_id(self, id=None) -> bool:
    #     # Recupera os dados da nova parcela criada transformando em um DataFrame
    #     df_parcela = pd.DataFrame(
    #         list(self.mongo.db["parcelas"].find({"id": id}, {"id": 1, "id_conta": 1,
    #                                                          "data_vencimento": 1,
    #                                                          "data_pagamento": 1,
    #                                                          "numero_parcela": 1,
    #                                                          "valor": 1,
    #                                                          "_id": 0})))
    #     return df_parcela

    def valida_conta(self, id_conta: int = None) -> Conta:
        if self.ctrl_conta.verifica_existencia_conta(id_conta, external=True):
            print(f"O Id da Conta {id_conta} informado não existe na base.")
            return None
        else:
            df_conta = self.ctrl_conta.recupera_id_conta(id_conta, external=True)
            # Cria um novo objeto conta
            conta = Conta(df_conta.id.values[0], df_conta.tipo.values[0], df_conta.data_quitacao.values[0])
            return conta

    # def valida_produto(self, codigo_produto: int = None) -> Produto:
    #     if self.ctrl_produto.verifica_existencia_produto(codigo_produto, external=True):
    #         print(f"O produto {codigo_produto} informado não existe na base.")
    #         return None
    #     else:
    #         # Recupera os dados do novo produto criado transformando em um DataFrame
    #         df_produto = self.ctrl_produto.recupera_produto_codigo(codigo_produto, external=True)
    #         # Cria um novo objeto Produto
    #         produto = Produto(df_produto.codigo_produto.values[0], df_produto.descricao_produto.values[0])
    #         return produto