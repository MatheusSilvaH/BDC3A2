from utils import config

class SplashScreen:

    def __init__(self):
        # Nome(s) do(s) criador(es)
        self.created_by = "\n Luana Amy Nakasuga\n Luiz Guilherme Machado Zortea\nMatheus Silva Herculino\n Renato Archajo Rabello\nVictor Isida Hirosse"
        self.professor = "Prof. M.Sc. Howard Roatti"
        self.disciplina = "Banco de Dados"
        self.semestre = "2022/2"

    def get_documents_count(self, collection_name):
        # Retorna o total de registros computado pela query
        df = config.query_count(collection_name=collection_name)
        return df[f"total_{collection_name}"].values[0]

    def get_updated_screen(self):
        return f"""
        ########################################################
        #              Registro de contas e parcelas                     
        #                                                         
        #  TOTAL DE REGISTROS:                                    
        #      1 - CONTAS:         {str(self.get_documents_count(collection_name="contas")).rjust(5)}
        #      2 - PARCELAS:         {str(self.get_documents_count(collection_name="parcelas")).rjust(5)}
        #      
        #
        #  CRIADO POR: {self.created_by}
        #
        #  PROFESSOR:  {self.professor}
        #
        #  DISCIPLINA: {self.disciplina}
        #              {self.semestre}
        ########################################################
        """