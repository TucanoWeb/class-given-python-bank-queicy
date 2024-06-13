from colorama import Fore, Back, Style, init
from banco import Banco
from conta_corrente import ContaCorrente

def main():
    banco = Banco('Banco Queicy')
    init(autoreset=True)
    
    def solicitar_numero(mensagem):
        while True:
            entrada = input(mensagem)
            try:
                valor = float(entrada)
                return valor
            except ValueError:
                print("Por favor, insira apenas números.")
            
    while True:
        print("\n")
        print(Fore.YELLOW + Back.BLUE + Style.BRIGHT + "Bem-vindo(a) ao Banco Queicy!")
        print(Fore.CYAN + "1. Criar conta corrente")
        print(Fore.CYAN + "2. Depositar")
        print(Fore.CYAN + "3. Sacar")
        print(Fore.CYAN + "4. Transferir")
        print(Fore.CYAN + "5. Emitir extrato")
        print(Fore.CYAN + "6. Sair")
        opcao = input(Fore.GREEN + "Escolha uma opção: ")
        

        if opcao == '1':
            numero = input(Fore.YELLOW + "Digite o número da conta: ")
            if numero.isdigit():
                saldo_inicial = input("Digite o saldo inicial da conta: ")
                if saldo_inicial.replace('.', '', 1).isdigit() and float(saldo_inicial) >= 0:
                    try:
                        banco.criar_conta_corrente(int(numero), float(saldo_inicial))
                        print(Fore.BLUE +"\n> Status")   
                        print(Fore.GREEN + "SUCESSO:")   
                        print("Conta corrente criada com sucesso.")   
                        print("===========================")   
                    except ValueError as e:
                        print(Fore.BLUE +"\n> Status")
                        print(Fore.RED + "ERROR:")
                        print(e)
                        print("===========================")
                else:
                    print(Fore.BLUE +"\n> Status")
                    print(Fore.RED + "ERROR:")
                    print("Por favor, insira um valor numérico positivo para o saldo inicial.")
                    print("===========================")
            else:
                print(Fore.BLUE +"\n> Status")
                print(Fore.RED + "ERROR:")
                print("Por favor, insira apenas números para o número da conta.")
                print("===========================")
            

        elif opcao == '2':
            numero = solicitar_numero(Fore.YELLOW + "Digite o número da conta: ")
            valor = solicitar_numero(Fore.YELLOW + "Digite o valor a ser depositado: ")
            try:
                conta = ContaCorrente(banco.conexao, int(numero))
                conta.depositar(valor)
                print(Fore.BLUE +"\n> Status")
                print(Fore.GREEN + "SUCESSO:")
                print("Depósito realizado com sucesso.")
                print("===========================")
            except ValueError as e:
                print(Fore.BLUE +"\n> Status")
                print(Fore.RED + "ERROR:")
                print(e)
                print("===========================")

        elif opcao == '3':
            numero = solicitar_numero(Fore.YELLOW + "Digite o número da conta: ")
            valor = solicitar_numero(Fore.YELLOW + "Digite o valor a ser sacado: ")
            try:
                conta = ContaCorrente(banco.conexao, int(numero))
                conta.sacar(valor)
                print(Fore.BLUE +"\n> Status")
                print(Fore.GREEN + "SUCESSO:")
                print("Saque realizado com sucesso.")
                print("===========================")
            except ValueError as e:
                print(Fore.BLUE +"\n> Status")
                print(Fore.RED + "ERROR:")
                print(e)
                print("===========================")

        elif opcao == '4':
            numero_origem = solicitar_numero(Fore.YELLOW + "Digite o número da conta de origem: ")
            numero_destino = solicitar_numero(Fore.YELLOW + "Digite o número da conta de destino: ")
            valor = solicitar_numero(Fore.YELLOW + "Digite o valor a ser transferido: ")
            try:
                banco.transferir(int(numero_origem), int(numero_destino), valor)
                print(Fore.BLUE +"\n> Status")
                print(Fore.GREEN + "SUCESSO:")
                print("Transferência realizada com sucesso.")
                print("===========================")
            except ValueError as e:
                print(Fore.BLUE +"\n> Status")
                print(Fore.RED + "ERROR:")
                print(e)
                print("===========================")

        elif opcao == '5':
            numero = solicitar_numero(Fore.YELLOW + "Digite o número da conta: ")
            try:
                conta = ContaCorrente(banco.conexao, int(numero))
                extrato = conta.emitir_extrato()
                print(Fore.BLUE +"\n> Status")
                print(extrato)
                print("===========================")
            except ValueError as e:
                print(Fore.BLUE +"\n> Status")
                print(Fore.RED + "ERROR:")
                print(e)
                print("===========================")

        elif opcao == '6':
            print(Fore.BLUE +"\n> Status")
            print("Obrigado e volte sempre!")
            print("===========================")
            break

        else:
            print("Opção inválida. Tente novamente.")

if __name__ == '__main__':
    main()
