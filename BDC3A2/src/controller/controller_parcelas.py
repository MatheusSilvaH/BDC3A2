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
        self.relatorio.get_relatorio_conta()
        id_conta = int(str(input("Digite o id da Conta: ")))
        conta = self.valida_conta(id_conta)
        if conta == None:
            return None

        id = int(input("Informe o Id da parcela: "))

        if self.verifica_existencia_parcela(id, id_conta):
            data_vencimento = str(input("Informe a data de vencimento da parcela (DD-MMM-AAAA): "))
            data_pagamento = None
            num_parcela = float(input(f"Informe o número da parcela: "))
            valor = float(input(f"Informe o valor da parcela: "))
            # Insere e Recupera o código do novo item de pedido
            self.mongo.db["parcelas"].insert_one({"id": id, "id_conta": id_conta,
                                                  "data_vencimento": data_vencimento,
                                                  "data_pagamento": data_pagamento,
                                                  "numero_parcela": num_parcela,
                                                  "valor": valor})
            # Recupera os dados do novo item de pedido criado transformando em um DataFrame
            df_parcela = self.recupera_parcela(id, id_conta)
            # Cria um novo objeto Item de Pedido
            nova_parcela = Parcelas(df_parcela.id.values[0], df_parcela.id_conta.values[0],
                                    df_parcela.data_vencimento.values[0],
                                    df_parcela.data_pagamento.values[0],
                                    df_parcela.numero_parcela.values[0],
                                    df_parcela.valor.values[0])
            # Exibe os atributos do novo Item de Pedido
            print(nova_parcela.to_string())
            self.mongo.close()
            # Retorna o objeto novo_item_pedido para utilização posterior, caso necessário
            return nova_parcela
        else:
            self.mongo.close()
            print(f"Ja existe uma parcela com id {id} para a conta {id_conta}")
            return None

    def atualizar_parcela(self) -> Parcelas:
        # Cria uma nova conexão com o banco que permite alteração
        # self.mongo.connect()

        self.relatorio.get_relatorio_conta()
        id_conta = int(str(input("Digite o id da conta: ")))
        conta = self.valida_conta(id_conta)
        if conta == None:
            return None

        self.mongo.connect()

        id = int(input("Id de Parcela que irá alterar: "))

        # Verifica se o item de pedido existe na base de dados
        if not self.verifica_existencia_parcela(id, id_conta):

            data_vencimento = str(input("Informe a data de vencimento da parcela (DD-MMM-AAAA): "))
            data_pagamento = str(input("Informe a data de pagamento da parcela (DD-MMM-AAAA): "))
            num_parcela = float(input(f"Informe o número da parcela: "))
            valor = float(input(f"Informe o valor unitário da parcela: "))

            # Atualiza o item de pedido existente
            self.mongo.db["parcelas"].update_one({"id": id, "id_conta": id_conta},
                                                  {"$set": {"id_conta": id_conta,
                                                            "data_vencimento": data_vencimento,
                                                            "data_pagamento": data_pagamento,
                                                            "numero_parcela": num_parcela,
                                                            "valor": valor
                                                            }
                                                   })
            # Recupera os dados do novo item de pedido criado transformando em um DataFrame
            df_parcela = self.recupera_parcela(id, id_conta)
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

    def excluir_parcela(self):
        self.mongo.connect()

        self.relatorio.get_relatorio_conta()
        id_conta = int(str(input("Digite o id da Conta: ")))
        conta = self.valida_conta(id_conta)
        if conta == None:
            return None

        id = int(input("Id da Parcela que irá excluir: "))

        # Verifica se a Parcela existe na base de dados
        if not self.verifica_existencia_parcela(id, id_conta):
            # Recupera os dados da parcela criada transformando em um DataFrame
            df_parcela = self.recupera_parcela(id, id_conta)
            # id_conta = self.valida_conta(int(df_parcela.id_conta.values[0]))

            opcao_excluir = input(f"Tem certeza que deseja excluir a parcela {id} da conta {id_conta}[S ou N]: ")
            if opcao_excluir.lower() == "s":
                # Revome a parcela da tabela
                self.mongo.db["parcelas"].delete_many({"id": id, "id_conta": id_conta})
                # Cria um novo objeto Item de Pedido para informar que foi removido
                parcela_excluida = Parcelas(df_parcela.id.values[0],
                                            df_parcela.id_conta.values[0],
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


    def verifica_existencia_parcela(self, id=None, id_conta=None) -> bool:
        # Recupera os dados do novo pedido criado transformando em um DataFrame
        df_parcela = self.recupera_parcela(id=id, id_conta=id_conta)
        return df_parcela.empty

    def recupera_parcela(self, id: int = None, id_conta=None) -> bool:
        # Recupera os dados do novo pedido criado transformando em um DataFrame
        df_parcela = pd.DataFrame(
            list(self.mongo.db["parcelas"].find({"id": id, "id_conta": id_conta}, {"id": 1, "id_conta": 1,
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
            df_conta = self.ctrl_conta.recupera_conta(id, external=True)
            # Cria um novo objeto conta
            conta = Conta(df_conta.id.values[0], df_conta.tipo.values[0], df_conta.data_quitacao.values[0])
            return conta
