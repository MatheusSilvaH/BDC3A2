from datetime import date
from model.conta import Conta


class Parcelas:
    def __init__(self, 
                 id: int=None,
                 id_conta: Conta=None,
                 data_vencimento: date=None,
                 data_pagamento: date=None,
                 numero_parcela: int=None,
                 valor: float=None
                 ):
        self.set_id(id)
        self.set_id_conta(id_conta)
        self.set_data_vencimento(data_vencimento)
        self.set_data_pagamento(data_pagamento)
        self.set_numero_parcela(numero_parcela)
        self.set_valor(valor)

    def set_id(self, id:int):
        self.id = id

    def set_id_conta(self, id_conta:Conta):
        self.id_conta = id_conta

    def set_data_vencimento(self, data_vencimento:date):
        self.data_vencimento = data_vencimento

    def set_data_pagamento(self, data_pagamento:date):
        self.data_pagamento = data_pagamento

    def set_numero_parcela(self, numero_parcela:int):
        self.numero_parcela = numero_parcela

    def set_valor(self, valor:float):
        self.valor = valor

    def get_id(self) -> int:
        return self.id

    def get_id_conta(self) -> Conta:
        return self.id_conta

    def get_data_vencimento(self) -> date:
        return self.data_vencimento

    def get_data_pagamento(self) -> date:
        return self.data_pagamento

    def get_numero_parcela(self) -> int:
        return self.numero_parcela

    def get_valor(self) -> float:
        return self.valor

    def to_string(self) -> str:
        return f"Id: {self.get_id()} | Id Conta: {self.get_id_conta()} | Data de Vencimento: {self.get_data_vencimento()} " \
               f"| Data de Pagamaneto: {self.get_data_pagamento()} | Numero da Parcela: {self.get_numero_parcela()} " \
               f"| Valor: {self.get_valor()}"