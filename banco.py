import sqlite3
from datetime import datetime
from conta_corrente import ContaCorrente

class Banco:
    def __init__(self, nome):
        self.nome = nome
        self.conexao = sqlite3.connect('banco.db')
        self.cursor = self.conexao.cursor()
        self.criar_tabelas()

    def criar_tabelas(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS contas (
                numero INTEGER PRIMARY KEY,
                saldo REAL,
                especial BOOLEAN,
                limite_saque_diario REAL,
                flag_ativo BOOLEAN,
                tipo_conta INTEGER,
                data_criacao TEXT
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS movimentacoes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                numero_conta INTEGER,
                descricao TEXT,
                tipo CHAR(1),
                valor REAL,
                data_movimentacao TEXT,
                FOREIGN KEY (numero_conta) REFERENCES contas (numero)
            )
        ''')
        self.conexao.commit()

    def criar_conta_corrente(self, numero, saldo_inicial):
        if saldo_inicial < 0:
            raise ValueError("Não pode criar uma conta com saldo negativo.")
        self.cursor.execute("SELECT numero FROM contas WHERE numero = ?", (numero,))
        if self.cursor.fetchone():
            raise ValueError("Um banco não pode ter duas contas com o mesmo número.")
        self.cursor.execute('''
            INSERT INTO contas (numero, saldo, especial, limite_saque_diario, flag_ativo, tipo_conta, data_criacao)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (numero, saldo_inicial, False, 1000.0, True, 1, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        self.conexao.commit()

    def transferir(self, conta_origem, conta_destino, valor):
        try:
            conta_o = ContaCorrente(self.conexao, conta_origem)
            conta_d = ContaCorrente(self.conexao, conta_destino)
            conta_o.transferir(conta_d, valor)
            print("Transferência realizada com sucesso.")
        except ValueError as e:
            raise ValueError(f"Erro ao realizar transferência: {e}")

    def emitir_extrato(self, numero_conta):
        try:
            conta = ContaCorrente(self.conexao, numero_conta)
            return conta.emitir_extrato()
        except ValueError as e:
            raise ValueError(f"Erro ao emitir extrato: {e}")

    def __del__(self):
        self.conexao.close()
