from datetime import datetime
from movimentacao import Movimentacao

class ContaCorrente:
    def __init__(self, conexao, numero):
        self.conexao = conexao
        self.cursor = self.conexao.cursor()
        self.cursor.execute("SELECT * FROM contas WHERE numero = ?", (numero,))
        conta = self.cursor.fetchone()
        if conta:
            self.numero, self.saldo, self.especial, self.limite_saque_diario, self.flag_ativo, self.tipo_conta, self.data_criacao = conta
        else:
            raise ValueError("Conta inexistente.")

    def sacar(self, valor):
        if not self.flag_ativo:
            raise ValueError("Não pode sacar de uma conta inativa.")
        if valor > self.saldo:
            raise ValueError("Não pode sacar se não tiver saldo suficiente.")
        self.saldo -= valor
        self.cursor.execute("UPDATE contas SET saldo = ? WHERE numero = ?", (self.saldo, self.numero))
        self.conexao.commit()
        self.registrar_movimentacao('Saque', 'S', valor)
        

    def depositar(self, valor):
        if valor <= 0:
            raise ValueError("O valor do depósito deve ser positivo.")
        self.saldo += valor
        self.cursor.execute("UPDATE contas SET saldo = ? WHERE numero = ?", (self.saldo, self.numero))
        self.conexao.commit()
        self.registrar_movimentacao('Depósito', 'D', valor)
        

    def transferir(self, conta_destino, valor):
        if self.saldo < valor:
            raise ValueError("Saldo insuficiente para transferência.")
        if not conta_destino.flag_ativo:
            raise ValueError("Conta de destino inativa.")
        self.sacar(valor)
        conta_destino.depositar(valor)
        self.registrar_movimentacao('Transferência Enviada', 'T', valor)
        conta_destino.registrar_movimentacao('Transferência Recebida', 'T', valor)
        
        
    def registrar_movimentacao(self, descricao, tipo, valor):
        data_movimentacao = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.cursor.execute('''
            INSERT INTO movimentacoes (numero_conta, descricao, tipo, valor, data_movimentacao)
            VALUES (?, ?, ?, ?, ?)
        ''', (self.numero, descricao, tipo, valor, data_movimentacao))
        self.conexao.commit()


    def emitir_extrato(self):
        self.cursor.execute("SELECT * FROM movimentacoes WHERE numero_conta = ?", (self.numero,))
        movimentacoes = self.cursor.fetchall()
        extrato = f"Extrato da Conta {self.numero}:\n"
        for mov in movimentacoes:
            extrato += f"{mov[1]} - {mov[2]} - TIPO {mov[3]} - R${mov[4]} - Data: {mov[5]}\n"
        return extrato
