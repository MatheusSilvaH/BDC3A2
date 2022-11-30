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
        relatorio.get_relatorio_valor_conta()
    elif opcao_relatorio == 4:
        relatorio.get_relatorio_parcelas_a_pagar()
    elif opcao_relatorio == 5:
        relatorio.get_relatorio_fornecedores()
    elif opcao_relatorio == 6:
        relatorio.get_relatorio_itens_pedidos()

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
            
            print(config.MENU_RELATORIOS)
            opcao_relatorio = int(input("Escolha uma opção: "))
            config.clear_console(1)

            reports(opcao_relatorio)

            config.clear_console(1)

        elif opcao == 2: # Inserir Novos Registros
            
            print(config.MENU_ENTIDADES)
            opcao_inserir = int(input("Escolha uma opção: "))
            config.clear_console(1)

            inserir(opcao_inserir=opcao_inserir)

            config.clear_console()
            print(tela_inicial.get_updated_screen())
            config.clear_console()

        elif opcao == 3: # Atualizar Registros

            print(config.MENU_ENTIDADES)
            opcao_atualizar = int(input("Escolha uma opção: "))
            config.clear_console(1)

            atualizar(opcao_atualizar=opcao_atualizar)

            config.clear_console()

        elif opcao == 4:

            print(config.MENU_ENTIDADES)
            opcao_excluir = int(input("Escolha uma opção: "))
            config.clear_console(1)

            excluir(opcao_excluir=opcao_excluir)

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
