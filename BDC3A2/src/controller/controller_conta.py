from datetime import date

import pandas as pd
from model.conta import Conta
from conexion.mongo_queries import MongoQueries

class Controller_Conta:
    def __init__(self):
        self.mongo = MongoQueries()
        
    def inserir_conta(self) -> Conta:
        # Cria uma nova conexão com o banco que permite alteração
        self.mongo.connect()

        # Solicita ao usuario o novo id de conta
        id = input("id(Novo int): ")

        if self.verifica_existencia_conta(id):
            # Solicita ao usuario a nova data
            tipo = input("Tipo (Novo - 1 = Conta a Pagar  2 = Conta a Receber): ")
            data_quitacao = None
            # Insere e persiste o novo cliente
            self.mongo.db["conta"].insert_one({"id": id, "tipo": tipo, "data_quitacao": data_quitacao})
            # Recupera os dados do novo cliente criado transformando em um DataFrame
            df_conta = self.recupera_conta(id)
            # Cria um novo objeto Cliente
            nova_conta = Conta(df_conta.id.values[0], df_conta.tipo.values[0], df_conta.data_quitacao)[0]
            print(nova_conta.to_string())
            self.mongo.close()
            # Retorna o objeto nova_conta para utilização posterior, caso necessário
            return nova_conta
        else:
            self.mongo.close()
            print(f"O id {id} já está cadastrado.")
            return None

    def atualizar_conta(self) -> Conta:
        # Cria uma nova conexão com o banco que permite alteração
        self.mongo.connect()

        # Solicita ao usuário o código do cliente a ser alterado
        id = input("id da conta que deseja alterar a Data de Quitação: ")

        # Verifica se o cliente existe na base de dados
        if not self.verifica_existencia_conta(id):
            # Solicita a nova data de quitação da conta
            # print("Insira data de quitacao")
            # dia = int(input("Informe a dia de vencimento da parcela (DD): "))
            # mes = int(input("Informe a mes de vencimento da parcela (MM): "))
            # ano = int(input("Informe a ano de vencimento da parcela (AAAA): "))
            # novo_data_quitacao = date(ano, mes, dia)
            novo_data_quitacao = date(input("Informe a Data de Quitacao(AAAA-MM-DD): "))
            # Atualiza a data da conta existente
            self.mongo.db["conta"].update_one({"id": f"{id}"}, {"$setOnInsert": {"data_quitacao": novo_data_quitacao}})
            # Recupera os dados da nova conta criada transformando em um DataFrame
            df_conta = self.recupera_conta(id)
            # Cria um novo objeto cliente
            conta_atualizada = Conta(df_conta.id.values[0], df_conta.tipo.values[0], df_conta.data_quitacao.values[0])
            # Exibe os atributos do novo cliente
            print(conta_atualizada.to_string())
            self.mongo.close()
            # Retorna o objeto cliente_atualizado para utilização posterior, caso necessário
            return conta_atualizada
        else:
            self.mongo.close()
            print(f"O idF {id} não existe.")
            return None

    def excluir_conta(self):
        # Cria uma nova conexão com o banco que permite alteração
        self.mongo.connect()

        # Solicita ao usuário o id da Conta a ser alterado
        id = input("id da conta que irá excluir: ")

        # Verifica se o cliente existe na base de dados
        if not self.verifica_existencia_conta(id):
            # Recupera os dados do novo cliente criado transformando em um DataFrame
            df_conta = self.recupera_conta(id)
            # Revome a conta da tabela
            self.mongo.db["conta"].delete_one({"id":f"{id}"})
            # Cria um novo objeto Conta para informar que foi removido
            conta_excluida = Conta(df_conta.id.values[0], df_conta.tipo.values[0], df_conta.data_quitacao.values[0])
            self.mongo.close()
            # Exibe os atributos do cliente excluído
            print("Conta Removida com Sucesso!")
            print(conta_excluida.to_string())
        else:
            self.mongo.close()
            print(f"O id {id} não existe.")

    def verifica_existencia_conta(self, id=None, external:bool=False) -> bool:
        if external:
            # Cria uma nova conexão com o banco que permite alteração
            self.mongo.connect()

        # Recupera os dados da nova Conta criava transformando em um DataFrame
        df_conta = pd.DataFrame(self.mongo.db["conta"].find({"id":f"{id}"}, {"id": 1, "tipo": 1, "data_quitacao": 1,
                                                                             "_id": 0}))

        if external:
            # Fecha a conexão com o Mongo
            self.mongo.close()

        return df_conta.empty

    def recupera_conta(self, id=None, external:bool=False) -> pd.DataFrame:
        if external:
            # Cria uma nova conexão com o banco que permite alteração
            self.mongo.connect()

        # Recupera os dados do novo cliente criado transformando em um DataFrame
        df_conta = pd.DataFrame(list(self.mongo.db["conta"].find({"id":f"{id}"}, {"id": 1, "tipo": 1,
                                                                                    "data_quitacao": 1, "_id": 0})))
        
        if external:
            # Fecha a conexão com o Mongo
            self.mongo.close()

        return df_conta