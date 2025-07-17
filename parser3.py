import ply.yacc as yacc
from lexer import tokens

# --------------------------------------------------------------------
# ETAPA 1: DEFINIÇÃO DAS CLASSES DA ÁRVORE DE SINTAXE ABSTRATA (AST)
# --------------------------------------------------------------------

class ASTNode:
    """ Classe base para todos os nós da AST. """
    def __repr__(self):
        # Uma forma simples de visualizar os nós para depuração
        return f"{self.__class__.__name__}"

class DeclaracaoVar(ASTNode):
    def __init__(self, variaveis, tipo):
        self.variaveis = variaveis
        self.tipo = tipo
    def __repr__(self):
        return f"DeclaracaoVar(vars={self.variaveis}, tipo='{self.tipo}')"

class Variavel(ASTNode):
    def __init__(self, nome):
        self.nome = nome
    def __repr__(self):
        return f"Variavel(nome='{self.nome}')"

class Atribuicao(ASTNode):
    def __init__(self, var, expressao):
        self.var = var
        self.expressao = expressao
    def __repr__(self):
        return f"Atribuicao(var={self.var}, expr={self.expressao})"

class Numero(ASTNode):
    def __init__(self, valor):
        self.valor = valor
    def __repr__(self):
        return f"Numero(valor={self.valor})"

class OperacaoBinaria(ASTNode):
    def __init__(self, esq, op, dir):
        self.esq = esq
        self.op = op
        self.dir = dir
    def __repr__(self):
        return f"OperacaoBinaria(esq={self.esq}, op='{self.op}', dir={self.dir})"

# --------------------------------------------------------------------
# ETAPA 2: PARSER (ANÁLISE SINTÁTICA) E REGRAS DA GRAMÁTICA
# --------------------------------------------------------------------

# Definição da Precedência dos Operadores
precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
)

# Regra inicial
def p_lista_comandos(p):
    '''
    lista_comandos : lista_comandos comando
                   | comando
    '''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]

def p_comando(p):
    '''
    comando : declaracao_var
            | atribuicao
    '''
    p[0] = p[1]

def p_declaracao_var(p):
    '''
    declaracao_var : VAR ID COLON tipo SEMI
    '''
    p[0] = DeclaracaoVar(variaveis=[Variavel(p[2])], tipo=p[4])

def p_tipo(p):
    '''
    tipo : INTEGER
         | REAL
         | STRING
    '''
    p[0] = p[1]

def p_atribuicao(p):
    '''
    atribuicao : ID ATRIB expressao SEMI
    '''
    p[0] = Atribuicao(var=Variavel(p[1]), expressao=p[3])

def p_expressao_binaria(p):
    '''
    expressao : expressao PLUS expressao
              | expressao MINUS expressao
              | expressao TIMES expressao
              | expressao DIVIDE expressao
    '''
    p[0] = OperacaoBinaria(esq=p[1], op=p[2], dir=p[3])

def p_expressao_grupo(p):
    '''
    expressao : LPAREN expressao RPAREN
    '''
    p[0] = p[2]

def p_expressao_numero(p):
    '''
    expressao : NUMERO
    '''
    p[0] = Numero(p[1])

def p_expressao_id(p):
    '''
    expressao : ID
    '''
    p[0] = Variavel(p[1])

# Tratamento de Erros de Sintaxe
def p_error(p):
    if p:
        print(f"Erro de sintaxe no token '{p.value}' (tipo: {p.type}) na linha {p.lineno}")
    else:
        print("Erro de sintaxe: Fim inesperado do arquivo!")

# --------------------------------------------------------------------
# ETAPA 3: ANÁLISE SEMÂNTICA
# --------------------------------------------------------------------

class AnalisadorSemantico:
    def __init__(self):
        self.tabela_simbolos = {}

    def visitar(self, no):
        nome_metodo = f'visitar_{type(no).__name__}'
        visitante = getattr(self, nome_metodo, self.erro_generico)
        return visitante(no)

    def erro_generico(self, no):
        raise Exception(f'Nenhum método visitar_{type(no).__name__} encontrado')

    def visitar_list(self, lista_nos):
        for item in lista_nos:
            self.visitar(item)

    def visitar_DeclaracaoVar(self, no_declaracao):
        tipo = no_declaracao.tipo
        for var in no_declaracao.variaveis:
            nome_var = var.nome
            if nome_var in self.tabela_simbolos:
                raise Exception(f"Erro Semântico: Variável '{nome_var}' já foi declarada.")
            else:
                self.tabela_simbolos[nome_var] = tipo
                print(f"Variável '{nome_var}' do tipo '{tipo}' adicionada à tabela de símbolos.")

    def visitar_Atribuicao(self, no_atribuicao):
        nome_var = no_atribuicao.var.nome
        if nome_var not in self.tabela_simbolos:
            raise Exception(f"Erro Semântico: Variável '{nome_var}' não foi declarada.")
        
        self.visitar(no_atribuicao.expressao)
        print(f"Checando atribuição para a variável '{nome_var}'.")

    def visitar_Variavel(self, no_variavel):
        nome_var = no_variavel.nome
        if nome_var not in self.tabela_simbolos:
            raise Exception(f"Erro Semântico: Variável '{nome_var}' não foi declarada.")
        print(f"Variável '{nome_var}' encontrada na tabela de símbolos.")

    def visitar_Numero(self, no_numero):
        pass

    def visitar_OperacaoBinaria(self, no_op):
        self.visitar(no_op.esq)
        self.visitar(no_op.dir)
        print(f"Checando operação binária com o operador '{no_op.op}'.")

# --------------------------------------------------------------------
# ETAPA 4: CONSTRUIR E EXECUTAR TUDO
# --------------------------------------------------------------------

# Constrói o parser
parser = yacc.yacc()

# Lê o código fonte do arquivo de teste
try:
    with open('exemplo.pas', 'r') as file:
        codigo = file.read()

    # Inicia a Análise Sintática
    print("--- Iniciando Análise Sintática ---")
    arvore_sintatica = parser.parse(codigo)
    print("--- Análise Sintática Concluída ---")

    # Inicia a Análise Semântica, se a sintática foi bem-sucedida
    if arvore_sintatica:
        print("\n--- Iniciando Análise Semântica ---")
        try:
            analisador = AnalisadorSemantico()
            analisador.visitar(arvore_sintatica)
            print("--- Análise Semântica Concluída com Sucesso! ---")
            print("\nTabela de Símbolos Final:")
            print(analisador.tabela_simbolos)
        except Exception as e:
            print(f"\nERRO: {e}")

except FileNotFoundError:
    print("Arquivo 'exemplo.pas' não encontrado. Crie um com código para testar.")