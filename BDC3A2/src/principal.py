from utils import config
from utils.splash_screen import SplashScreen
from reports.relatorios import Relatorio
from controller.controller_conta import Controller_Conta
from controller.controller_parcelas import Controller_Parcelas

tela_inicial = SplashScreen()
relatorio = Relatorio()
ctrl_conta = Controller_Conta()
ctrl_parcelas = Controller_Parcelas()

def reports(opcao_relatorio:int=0):

    if opcao_relatorio == 1:
        relatorio.get_relatorio_conta()
    elif opcao_relatorio == 2:
        relatorio.get_relatorio_parcelas()
    elif opcao_relatorio == 3:
        relatorio.get_valor_conta()
def inserir(opcao_inserir:int=0):

    if opcao_inserir == 1:                               
        novo_conta = ctrl_conta.inserir_conta()
    elif opcao_inserir == 2:
        novo_Parcelas = ctrl_parcelas.inserir_parcelas()
def atualizar(opcao_atualizar:int=0):

    if opcao_atualizar == 1:
        relatorio.get_relatorio_conta()
        conta_atualizado = ctrl_conta.atualizar_conta()
    elif opcao_atualizar == 2:
        relatorio.get_relatorio_parcelas()
        parcelas_atualizado = ctrl_parcelas.atualizar_parcela()
def excluir(opcao_excluir:int=0):

    if opcao_excluir == 1:
        relatorio.get_relatorio_conta()
        ctrl_conta.excluir_conta()
    elif opcao_excluir == 2:                
        relatorio.get_relatorio_parcelas()
        ctrl_parcelas.excluir_parcela()

def run():
    print(tela_inicial.get_updated_screen())
    config.clear_console()

    while True:
        print(config.MENU_PRINCIPAL)
        opcao = int(input("Escolha uma opção: "))
        config.clear_console(1)
        
        if opcao == 1: # Relatórios
            continua = True
            while continua:
                print(config.MENU_RELATORIOS)
                opcao_relatorio = int(input("Escolha uma opção: "))
                config.clear_console(1)


                reports(opcao_relatorio)
                opcao_continuar = input("Deseja consultar outro relatorio [S ou N]: ")
                if opcao_continuar.lower() == "s":
                    pass
                else:
                    continua = False

            config.clear_console(1)

        elif opcao == 2: # Inserir Novos Registros
            continua = True
            while continua:
                print(config.MENU_ENTIDADES)
                opcao_inserir = int(input("Escolha uma opção: "))
                config.clear_console(1)

                inserir(opcao_inserir=opcao_inserir)

                opcao_continuar = input("Deseja inserir outro registro [S ou N]: ")
                if opcao_continuar.lower() == "s":
                    pass
                else:
                    continua = False

            config.clear_console()
            print(tela_inicial.get_updated_screen())
            config.clear_console()

        elif opcao == 3: # Atualizar Registros
            continua = True
            while continua:
                print(config.MENU_ENTIDADES)
                opcao_atualizar = int(input("Escolha uma opção: "))
                config.clear_console(1)

                atualizar(opcao_atualizar=opcao_atualizar)
                opcao_continuar = input("Deseja atualizar outro registro [S ou N]: ")
                if opcao_continuar.lower() == "s":
                    pass
                else:
                    continua = False

            config.clear_console()

        elif opcao == 4:
            continua = True
            while continua:
                print(config.MENU_ENTIDADES)
                opcao_excluir = int(input("Escolha uma opção: "))
                config.clear_console(1)

                excluir(opcao_excluir=opcao_excluir)
                opcao_continuar = input("Deseja remover outro registro [S ou N]: ")
                if opcao_continuar.lower() == "s":
                    pass
                else:
                    continua = False

            config.clear_console()
            print(tela_inicial.get_updated_screen())
            config.clear_console()

        elif opcao == 5:

            print(tela_inicial.get_updated_screen())
            config.clear_console()
            print("Até mais!")
            exit(0)

        else:
            print("Opção incorreta. Escolha um número de 1 a 5.")
            exit(1)

if __name__ == "__main__":
    run()
