from datetime import date


class Conta:
    def __init__(self, 
                 id:int=None,
                 tipo:int=None,
                 data_quitacao:date=None
                ):
        self.set_id(id)
        self.set_tipo(tipo)
        self.set_data_quitacao(data_quitacao)

    def set_id(self, id:int):
        self.id = id

    def set_tipo(self, tipo:int):
        self.tipo = tipo

    def set_data_quitacao(self, data_quitacao:date):
        self.data_quitacao = data_quitacao

    def get_id(self) -> int:
        return self.id

    def get_tipo(self) -> int:
        return self.tipo

    def get_data_quitacao(self) -> date:
        return self.data_quitacao

    def to_string(self) -> str:
        return f"Id: {self.get_id()} | Tipo: {self.get_tipo()} | Data Quitacao: {self.get_data_quitacao()}"