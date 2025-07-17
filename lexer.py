import ply.lex as lex
import sys

# Dicionário de palavras reservadas da gramática Paston
# Modificado para refletir as palavras-chave da gramática fornecida.
reserved = {
    'begin': 'BEGIN',
    'const': 'CONST',
    'type': 'TYPE',
    'var': 'VAR',
    'def': 'DEF',          # 'def' é usado para definir rotinas/funções. 
    'end': 'END',
    'if': 'IF',
    'then': 'THEN',
    'else': 'ELSE',
    'while': 'WHILE',
    'do': 'DO',
    'return': 'RETURN',   # 'return' é usado para retornar valores de rotinas. 
    'write': 'WRITE',
    'read': 'READ',
    'integer': 'INTEGER',
    'real': 'REAL',
    'string': 'STRING',   # 'string' é um tipo de dado na gramática Paston. 
    'array': 'ARRAY',
    'of': 'OF',
    'record': 'RECORD'
}

# Lista de tokens. Inclui os literais e os nomes das palavras reservadas.
tokens = [
    'NUMERO', 'ID', 'CONST_VALOR',
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE',
    'LPAREN', 'RPAREN', 'LBRACKET', 'RBRACKET',
    'SEMI', 'COLON', 'DOT', 'COMMA',
    'ATRIB',          # Para o operador de atribuição ':='. 
    'EQUAL_TO',       # Para o operador de comparação '=='. 
    'NOT_EQUAL_TO',   # O operador '!' na gramática  é comumente representado como '!='.
    'GREATER_THAN_OR_EQUAL', # Para '>='. 
    'LESS_THAN_OR_EQUAL',    # Para '<='. 
    'GREATER_THAN',   # Para '>'. 
    'LESS_THAN',      # Para '<'. 
    'EQUAL'           # A gramática também define um '=' simples como operador lógico. 
] + list(reserved.values())

# Expressões regulares para operadores e pontuação simples
t_PLUS      = r'\+'
t_MINUS     = r'-'
t_TIMES     = r'\*'
t_DIVIDE    = r'/'
t_LPAREN    = r'\('
t_RPAREN    = r'\)'
t_LBRACKET  = r'\['
t_RBRACKET  = r'\]'
t_SEMI      = r';'
t_COLON     = r':'
t_DOT       = r'\.'
t_COMMA     = r','
t_EQUAL     = r'=' # Corresponde ao [OP_LOGICO] (=). 

# Operadores de múltiplos caracteres. A ordem é importante para o PLY fazer o match mais longo primeiro.
t_ATRIB     = r':=' # Corresponde ao '(:=)'. 
t_EQUAL_TO        = r'==' # Corresponde ao '(==)'. 
t_NOT_EQUAL_TO    = r'!=' # Corresponde ao [OP_LOGICO] (!). 
t_GREATER_THAN_OR_EQUAL = r'>=' # Corresponde ao [OP_LOGICO] (>=). 
t_LESS_THAN_OR_EQUAL    = r'<=' # Corresponde ao [OP_LOGICO] (<=). 
t_GREATER_THAN    = r'>'  # Corresponde ao [OP_LOGICO] (>). 
t_LESS_THAN       = r'<'  # Corresponde ao [OP_LOGICO] (<). 

# A definição de NÚMERO casa com a da gramática: "sequência numérica com no máximo um ponto". [cite: 29]
def t_NUMERO(t):
    r'\d+(\.\d+)?'
    t.value = float(t.value) if '.' in t.value else int(t.value)
    return t

# A definição de ID casa com a da gramática: "sequência alfanumérica iniciada por char". [cite: 27]
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value.lower(), 'ID')    # Verifica se é uma palavra reservada
    return t

# A definição de CONST_VALOR casa com a da gramática: "iniciada por aspas e terminada em aspas". 
def t_CONST_VALOR(t):
    r'\"([^\\\"]|\\.)*\"'
    t.value = t.value[1:-1] # Remove as aspas
    return t

# Ignora espaços e tabulações
t_ignore = ' \t'

# A gramática não especifica comentários, mas manteremos o suporte a eles.
def t_COMMENT(t):
    r'\#.*'
    pass # Nenhum token é retornado

# Regra para contagem de linhas
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Tratamento de erros
def t_error(t):
    print(f"Caractere inválido: '{t.value[0]}' na linha {t.lineno}")
    t.lexer.skip(1)

# Constrói o analisador léxico
lexer = lex.lex()

# --- Função de teste (não alterada) ---
def testa_lexico_com_arquivo(arquivo):
    try:
        with open(arquivo, 'r') as file:
            data = file.read()
        lexer.input(data)
        while True:
            tok = lexer.token()
            if not tok:
                break
            print(tok)
    except FileNotFoundError:
        print(f"Arquivo {arquivo} não encontrado")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python3 lexer.py <arquivo>")
        sys.exit(1)

    arquivo = sys.argv[1]
    testa_lexico_com_arquivo(arquivo)
    print("\nAnálise léxica concluída com sucesso.")