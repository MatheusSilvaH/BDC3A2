from datetime import date

import pandas as pd
from bson import ObjectId

from reports.relatorios import Relatorio

from model.parcelas import Parcelas
from model.conta import Conta

from controller.controller_conta import Controller_Conta
from conexion.mongo_queries import MongoQueries


class Controller_Parcelas:
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
        conta = self.valida_conta(id_conta)
        if conta == None:
            return None

        dia = int(input("Informe a dia de vencimento da parcela (DD): "))
        mes = int(input("Informe a mes de vencimento da parcela (MM): "))
        ano = int(input("Informe a ano de vencimento da parcela (AAAA): "))
        vencimento = date(ano, mes, dia)
        data_pagamento = None
        num_parcela = float(input(f"Informe onúmero da parcela: "))
        valor = float(input(f"Informe o valor unitário de cada parcela: "))

        proxima_parcela = self.mongo.db["parcelas"].aggregate([
            {
                '$group': {
                    '_id': '$parcelas',
                    'proxima_parcela': {
                        '$max': '$id'
                    }
                }
            }, {
                '$project': {
                    'proxima_parcela': {
                        '$sum': [
                            '$proxima_parcela', 1
                        ]
                    },
                    '_id': 0
                }
            }
        ])

        proxima_parcela = int(list(proxima_parcela)[0]['proxima_parcela'])
        # Cria um dicionário para mapear as variáveis de entrada e saída
        data = dict(id=proxima_parcela, id_conta=int(conta.get_codigo_conta()), data_vencimento=vencimento,
                    data_pagamento=data_pagamento, numero_parcela=num_parcela, valor=valor)
        # Insere e Recupera o código do novo item de pedido
        id_parcela = self.mongo.db["parcelas"].insert_one(data)
        # Recupera os dados do novo item de pedido criado transformando em um DataFrame
        df_parcela = self.recupera_parcela(id_parcela.inserted_id)
        # Cria um novo objeto Item de Pedido
        nova_parcela = Parcelas(df_parcela.id.values[0], conta, df_parcela.data_vencimento.values[0],
                                df_parcela.data_pagamento.values[0], df_parcela.numero_parcela.values[0],
                                df_parcela.valor_unitario.values[0])
        # Exibe os atributos do novo Item de Pedido
        print(nova_parcela.to_string())
        self.mongo.close()
        # Retorna o objeto novo_item_pedido para utilização posterior, caso necessário
        return nova_parcela

    def atualizar_parcela(self) -> Parcelas:
        # Cria uma nova conexão com o banco que permite alteração
        self.mongo.connect()

        # Solicita ao usuário o código do item de pedido a ser alterado
        id = int(input("Id de Parcela que irá alterar: "))

        # Verifica se o item de pedido existe na base de dados
        if not self.verifica_existencia_parcela(id):

            # Lista os pedido existentes para inserir no item de pedido
            self.relatorio.get_relatorio_contas()
            id_conta = int(str(input("Digite o número da conta: ")))
            conta = self.valida_conta(id_conta)
            if conta == None:
                return None

            diav = int(input("Informe a dia de vencimento da parcela (DD): "))
            mesv = int(input("Informe a mes de vencimento da parcela (MM): "))
            anov = int(input("Informe a ano de vencimento da parcela (AAAA): "))
            vencimento = date(anov, mesv, diav)
            diap = int(input("Informe a dia de vencimento da parcela (DD): "))
            mesp = int(input("Informe a mes de vencimento da parcela (MM): "))
            anop = int(input("Informe a ano de vencimento da parcela (AAAA): "))
            data_pagamento = date(anop, mesp, diap)
            num_parcela = float(input(f"Informe o número da parcela: "))
            valor = float(input(f"Informe o valor unitário de cada parcela: "))

            # Atualiza o item de pedido existente
            self.mongo.db["[parcela]"].update_one({"id": id},
                                                     {"$set": {"id_conta": id_conta,
                                                               "data_vencimento": vencimento,
                                                               "data_pagamento": data_pagamento,
                                                               "numero_parcela": num_parcela,
                                                               "valor": valor
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
                # Revome a parcela da tabela
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
        df_parcela = self.recupera_parcela(id=id)
        return df_parcela.empty

    def recupera_parcela(self, id: int = None) -> bool:
        # Recupera os dados do novo pedido criado transformando em um DataFrame
        df_parcela = pd.DataFrame(list(self.mongo.db["parcelas"].find({"id": id}, {"id": 1, "id_conta": 1,
                                                                                   "data_vencimento": 1,
                                                                                   "data_pagamento": 1,
                                                                                   "numero_parcela": 1,
                                                                                   "valor": 1,
                                                                                   "_id": 0})))
        return df_parcela

    def valida_conta(self, id: int = None) -> Conta:
        if self.ctrl_conta.verifica_existencia_conta(id, external=True):
            print(f"O Id da Conta {id} informado não existe na base.")
            return None
        else:
            df_conta = self.ctrl_conta.recupera_id_conta(id, external=True)
            # Cria um novo objeto conta
            conta = Conta(df_conta.id.values[0], df_conta.tipo.values[0], df_conta.data_quitacao.values[0])
            return conta
