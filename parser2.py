# parser.py (versão 2)

import ply.yacc as yacc
from lexer import tokens

# --- Classes da Árvore de Sintaxe Abstrata (AST) ---

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

# NOVAS CLASSES PARA EXPRESSÕES
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

# --- Definição da Precedência dos Operadores ---
precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
)

# --- Regras da Gramática e Construção da AST ---

# Regra inicial (vamos usar 'lista_comandos' como ponto de partida)
def p_lista_comandos(p):
    '''
    lista_comandos : lista_comandos comando
                   | comando
    '''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]  # Adiciona o novo comando à lista de comandos
    else:
        p[0] = [p[1]]  # Inicia uma nova lista de comandos

def p_comando(p):
    '''
    comando : declaracao_var
            | atribuicao
    '''
    # Um comando agora pode ser uma declaração OU uma atribuição
    p[0] = p[1]

def p_declaracao_var(p):
    '''
    declaracao_var : VAR ID COLON tipo SEMI
    '''
    # Agora, em vez de imprimir, criamos um objeto DeclaracaoVar
    p[0] = DeclaracaoVar(variaveis=[Variavel(p[2])], tipo=p[4])

def p_tipo(p):
    '''
    tipo : INTEGER
         | REAL
         | STRING
    '''
    p[0] = p[1]

# NOVA REGRA PARA ATRIBUIÇÃO
def p_atribuicao(p):
    '''
    atribuicao : ID ATRIB expressao SEMI
    '''
    # Criamos um objeto Atribuicao
    p[0] = Atribuicao(var=Variavel(p[1]), expressao=p[3])


# NOVAS REGRAS PARA EXPRESSÕES MATEMÁTICAS
def p_expressao_binaria(p):
    '''
    expressao : expressao PLUS expressao
              | expressao MINUS expressao
              | expressao TIMES expressao
              | expressao DIVIDE expressao
    '''
    # Criamos um objeto OperacaoBinaria
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
    # Criamos um objeto Numero
    p[0] = Numero(p[1])

def p_expressao_id(p):
    '''
    expressao : ID
    '''
    # Criamos um objeto Variavel
    p[0] = Variavel(p[1])


# --- Tratamento de Erros de Sintaxe ---
def p_error(p):
    if p:
        print(f"Erro de sintaxe no token '{p.value}' (tipo: {p.type}) na linha {p.lineno}")
    else:
        print("Erro de sintaxe: Fim inesperado do arquivo!")


# --- Construir e Executar o Parser ---
parser = yacc.yacc()

with open('exemplo.pas', 'r') as file:
    codigo = file.read()

print("--- Iniciando Análise Sintática ---")
arvore_sintatica = parser.parse(codigo)
print("--- Análise Sintática Concluída ---")

print("\nÁrvore de Sintaxe Abstrata (AST) Gerada:")
print(arvore_sintatica)