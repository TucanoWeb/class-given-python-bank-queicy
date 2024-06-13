class Movimentacao:
    def __init__(self, conexao, descricao, tipo, valor, numero_conta):
        self.conexao = conexao
        self.cursor = self.conexao.cursor()
        self.descricao = descricao
        self.tipo = tipo
        self.valor = valor
        self.numero_conta = numero_conta
        self.registrar_movimentacao()

    def registrar_movimentacao(self):
        self.cursor.execute('''
            INSERT INTO movimentacoes (descricao, tipo, valor, numero_conta)
            VALUES (?, ?, ?, ?)
        ''', (self.descricao, self.tipo, self.valor, self.numero_conta))
        self.conexao.commit()
