# parser.py - Versão Final com Suporte a Blocos de Declaração

import ply.yacc as yacc
from lexer import lexer, tokens

# --------------------------------------------------------------------
# ETAPA 1: DEFINIÇÃO DAS CLASSES DA ÁRVORE DE SINTAXE ABSTRATA (AST)
# --------------------------------------------------------------------

class ASTNode:
    def __repr__(self):
        return f"{self.__class__.__name__}"

class DeclaracaoVar(ASTNode):
    def __init__(self, variaveis, tipo):
        self.variaveis = variaveis
        self.tipo = tipo

class Variavel(ASTNode):
    def __init__(self, nome):
        self.nome = nome

class Atribuicao(ASTNode):
    def __init__(self, var, expressao):
        self.var = var
        self.expressao = expressao

class Numero(ASTNode):
    def __init__(self, valor):
        self.valor = valor

class OperacaoBinaria(ASTNode):
    def __init__(self, esq, op, dir):
        self.esq = esq
        self.op = op
        self.dir = dir

class FunctionDecl(ASTNode):
    def __init__(self, nome, params, tipo_retorno, corpo):
        self.nome = nome
        self.params = params
        self.tipo_retorno = tipo_retorno
        self.corpo = corpo

class FunctionBody(ASTNode):
    def __init__(self, declaracoes_locais, comandos):
        self.declaracoes_locais = declaracoes_locais
        self.comandos = comandos

class FunctionCall(ASTNode):
    def __init__(self, nome, args):
        self.nome = nome
        self.args = args

class Param(ASTNode):
    def __init__(self, var_node, tipo_node):
        self.var_node = var_node
        self.tipo_node = tipo_node

class ReturnStmt(ASTNode):
    def __init__(self, expressao):
        self.expressao = expressao

class TypeDecl(ASTNode):
    def __init__(self, nome, definicao_tipo):
        self.nome = nome
        self.definicao_tipo = definicao_tipo

class ArrayType(ASTNode):
    def __init__(self, tamanho, tipo_base):
        self.tamanho = tamanho
        self.tipo_base = tipo_base

class ArrayAccess(ASTNode):
    def __init__(self, var, indice):
        self.var = var
        self.indice = indice

class RecordType(ASTNode):
    def __init__(self, campos):
        self.campos = campos

class RecordAccess(ASTNode):
    def __init__(self, var, campo):
        self.var = var
        self.campo = campo

# --------------------------------------------------------------------
# ETAPA 2: PARSER (ANÁLISE SINTÁTICA) - SEÇÃO CORRIGIDA
# --------------------------------------------------------------------

precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
)

def p_lista_comandos(p):
    '''lista_comandos : lista_comandos comando
                      | empty'''
    if len(p) == 3 and p[2]:
        p[0] = p[1] + p[2] if isinstance(p[2], list) else p[1] + [p[2]]
    else:
        p[0] = []

def p_comando(p):
    '''comando : declaracao_var_block
               | atribuicao
               | function_declaration
               | return_statement
               | type_declaration_block'''
    p[0] = p[1]

# --- NOVAS REGRAS CORRIGIDAS PARA BLOCOS 'type' e 'var' ---
def p_type_declaration_block(p):
    '''type_declaration_block : TYPE type_definition_list'''
    p[0] = p[2]

def p_type_definition_list(p):
    '''type_definition_list : type_definition_list single_type_definition
                           | single_type_definition'''
    if len(p) == 3: p[0] = p[1] + [p[2]]
    else: p[0] = [p[1]]

def p_single_type_definition(p):
    '''single_type_definition : ID EQUAL_TO type_definition SEMI'''
    p[0] = TypeDecl(nome=p[1], definicao_tipo=p[3])


def p_type_definition(p):
    '''type_definition : array_type_definition
                       | record_type_definition'''
    p[0] = p[1]

def p_declaracao_var_block(p):
    '''declaracao_var_block : VAR var_declaration_list'''
    p[0] = p[2]

# Esta regra agora é usada dentro dos blocos 'var' e de funções
def p_var_declaration_list(p):
    '''var_declaration_list : var_declaration_list declaracao_var
                           | declaracao_var'''
    if len(p) == 3: p[0] = p[1] + [p[2]]
    else: p[0] = [p[1]]

def p_declaracao_var(p):
    '''declaracao_var : ID COLON tipo_specifier SEMI'''
    p[0] = DeclaracaoVar(variaveis=[Variavel(p[1])], tipo=p[3])


def p_array_type_definition(p):
    '''array_type_definition : ARRAY LBRACKET NUMERO RBRACKET OF tipo_specifier'''
    p[0] = ArrayType(tamanho=p[3], tipo_base=p[6])

def p_record_type_definition(p):
    '''record_type_definition : RECORD field_list END SEMI'''
    p[0] = RecordType(campos=p[2])

def p_field_list(p):
    '''field_list : field_list field_declaration
                  | empty'''
    if len(p) == 3: p[0] = p[1] + [p[2]]
    else: p[0] = []

def p_field_declaration(p):
    '''field_declaration : ID COLON tipo_specifier SEMI'''
    p[0] = Param(Variavel(p[1]), p[3])

def p_tipo_specifier(p):
    '''tipo_specifier : INTEGER
                      | REAL
                      | STRING
                      | ID'''
    p[0] = p[1]

def p_atribuicao(p):
    '''atribuicao : Variavel ATRIB expressao SEMI'''
    p[0] = Atribuicao(var=p[1], expressao=p[3])

def p_function_declaration(p):
    '''function_declaration : DEF ID LPAREN params_opt RPAREN tipo_retorno_opt function_body'''
    p[0] = FunctionDecl(nome=p[2], params=p[4], tipo_retorno=p[6], corpo=p[7])

def p_function_body(p):
    '''function_body : var_declarations_opt BEGIN lista_comandos END SEMI'''
    p[0] = FunctionBody(declaracoes_locais=p[1], comandos=p[3])

def p_var_declarations_opt(p):
    '''var_declarations_opt : VAR var_declaration_list
                           | empty'''
    p[0] = p[2] if len(p) > 2 else []

def p_return_statement(p):
    '''return_statement : RETURN expressao SEMI'''
    p[0] = ReturnStmt(p[2])

def p_params_opt(p):
    '''params_opt : params
                  | empty'''
    p[0] = p[1] if p[1] else []

def p_params(p):
    '''params : params COMMA param
              | param'''
    if len(p) == 4: p[0] = p[1] + [p[3]]
    else: p[0] = [p[1]]

def p_param(p):
    '''param : ID COLON tipo_specifier'''
    p[0] = Param(Variavel(p[1]), p[3])

def p_tipo_retorno_opt(p):
    '''tipo_retorno_opt : COLON COLON tipo_specifier
                       | empty'''
    if len(p) == 4: p[0] = p[3]
    else: p[0] = 'void'

def p_expressao(p):
    '''expressao : expressao PLUS expressao
                 | expressao MINUS expressao
                 | expressao TIMES expressao
                 | expressao DIVIDE expressao'''
    p[0] = OperacaoBinaria(esq=p[1], op=p[2], dir=p[3])

def p_expressao_termo(p):
    '''expressao : termo'''
    p[0] = p[1]

def p_termo(p):
    '''termo : LPAREN expressao RPAREN
             | NUMERO
             | function_call
             | Variavel'''
    if len(p) == 4: p[0] = p[2]
    elif isinstance(p[1], (int, float)): p[0] = Numero(p[1])
    else: p[0] = p[1]

def p_Variavel(p):
    '''Variavel : ID
                | array_access
                | record_access'''
    p[0] = p[1] if isinstance(p[1], ASTNode) else Variavel(p[1])

def p_record_access(p):
    '''record_access : Variavel DOT ID'''
    p[0] = RecordAccess(var=p[1], campo=Variavel(p[3]))

def p_array_access(p):
    '''array_access : ID LBRACKET expressao RBRACKET'''
    p[0] = ArrayAccess(var=Variavel(p[1]), indice=p[3])

def p_function_call(p):
    '''function_call : ID LPAREN args_opt RPAREN'''
    p[0] = FunctionCall(nome=p[1], args=p[3])

def p_args_opt(p):
    '''args_opt : args
                | empty'''
    p[0] = p[1] if p[1] else []

def p_args(p):
    '''args : args COMMA expressao
            | expressao'''
    if len(p) == 4: p[0] = p[1] + [p[3]]
    else: p[0] = [p[1]]

def p_empty(p):
    'empty :'
    pass

def p_error(p):
    if p: print(f"Erro de sintaxe no token '{p.value}' (tipo: {p.type}) na linha {p.lineno}")
    else: print("Erro de sintaxe: Fim inesperado do arquivo!")

# --------------------------------------------------------------------
# ETAPA 3: ANÁLISE SEMÂNTICA
# --------------------------------------------------------------------

class AnalisadorSemantico:
    def __init__(self):
        self.pilha_escopos = [{}]
        self.funcao_atual = None

    def visitar(self, no):
        if no is None: return
        # Lida com listas de nós (como lista_comandos, que pode ser uma lista de listas)
        if isinstance(no, list):
            for item in no:
                self.visitar(item)
            return

        nome_metodo = f'visitar_{type(no).__name__}'
        visitante = getattr(self, nome_metodo, self.erro_generico)
        return visitante(no)

    def erro_generico(self, no):
        raise Exception(f'Nenhum método visitar_{type(no).__name__} encontrado')

    def abrir_escopo(self): self.pilha_escopos.append({})
    def fechar_escopo(self): self.pilha_escopos.pop()

    def declarar_simbolo(self, nome, info):
        escopo_atual = self.pilha_escopos[-1]
        if nome in escopo_atual: raise Exception(f"Erro Semântico: Símbolo '{nome}' já foi declarado neste escopo.")
        escopo_atual[nome] = info

    def buscar_simbolo(self, nome):
        for escopo in reversed(self.pilha_escopos):
            if nome in escopo: return escopo[nome]
        return None

    def visitar_TypeDecl(self, no):
        nome_tipo = no.nome
        self.visitar(no.definicao_tipo)
        info_tipo = {'tipo_estrutura': 'type', 'definicao': no.definicao_tipo}
        self.declarar_simbolo(nome_tipo, info_tipo)

    def visitar_ArrayType(self, no):
        tipo_base = no.tipo_base
        if tipo_base not in ['integer', 'real', 'string'] and not self.buscar_simbolo(tipo_base):
            raise Exception(f"Erro Semântico: Tipo base '{tipo_base}' do array não foi definido.")

    def visitar_RecordType(self, no):
        for campo in no.campos:
            tipo_campo = campo.tipo_node
            if tipo_campo not in ['integer', 'real', 'string'] and not self.buscar_simbolo(tipo_campo):
                raise Exception(f"Erro Semântico: Tipo '{tipo_campo}' usado no campo '{campo.var_node.nome}' não foi definido.")

    def visitar_ArrayAccess(self, no):
        nome_var = no.var.nome
        info_var = self.buscar_simbolo(nome_var)
        if not info_var or info_var['tipo_estrutura'] != 'var':
            raise Exception(f"Erro Semântico: '{nome_var}' não é uma variável declarada.")
        info_tipo_var = self.buscar_simbolo(info_var['tipo'])
        if not info_tipo_var or not isinstance(info_tipo_var.get('definicao'), ArrayType):
            raise Exception(f"Erro de Tipo: A variável '{nome_var}' não é do tipo vetor (array).")
        tipo_indice = self.visitar(no.indice)
        if tipo_indice != 'integer': raise Exception(f"Erro de Tipo: O índice de um vetor deve ser um 'integer', mas recebeu '{tipo_indice}'.")
        definicao_array = info_tipo_var['definicao']
        if isinstance(no.indice, Numero):
            if not (1 <= no.indice.valor <= definicao_array.tamanho):
                raise Exception(f"Erro Semântico: Índice '{no.indice.valor}' fora dos limites do vetor '{nome_var}' (1 a {definicao_array.tamanho}).")
        return definicao_array.tipo_base

    def visitar_RecordAccess(self, no):
        tipo_var_esquerda = self.visitar(no.var)
        info_tipo = self.buscar_simbolo(tipo_var_esquerda)
        if not info_tipo or not isinstance(info_tipo.get('definicao'), RecordType):
            raise Exception(f"Erro de Tipo: Tentativa de acessar campo em uma variável que não é do tipo '{tipo_var_esquerda}' (record).")
        definicao_record = info_tipo['definicao']
        nome_campo_acessado = no.campo.nome
        for campo_declarado in definicao_record.campos:
            if campo_declarado.var_node.nome == nome_campo_acessado:
                return campo_declarado.tipo_node
        raise Exception(f"Erro Semântico: O campo '{nome_campo_acessado}' não existe no tipo '{tipo_var_esquerda}'.")

    def visitar_DeclaracaoVar(self, no):
        tipo_nome = no.tipo
        info_tipo = self.buscar_simbolo(tipo_nome)
        if tipo_nome not in ['integer', 'real', 'string'] and (not info_tipo or info_tipo.get('tipo_estrutura') != 'type'):
            raise Exception(f"Erro Semântico: Tipo '{tipo_nome}' não foi definido.")
        self.declarar_simbolo(no.variaveis[0].nome, {'tipo_estrutura': 'var', 'tipo': tipo_nome})

    def visitar_FunctionDecl(self, no):
        nome_func = no.nome
        info_func = {'tipo_estrutura': 'function', 'tipo_retorno': no.tipo_retorno, 'parametros': []}
        self.declarar_simbolo(nome_func, info_func)
        self.funcao_atual = info_func
        self.abrir_escopo()
        if no.params:
            for param in no.params:
                nome_param = param.var_node.nome
                tipo_param = param.tipo_node
                info_param = {'tipo_estrutura': 'var', 'tipo': tipo_param}
                self.declarar_simbolo(nome_param, info_param)
                info_func['parametros'].append(info_param)
        self.visitar(no.corpo)
        self.fechar_escopo()
        self.funcao_atual = None

    def visitar_FunctionBody(self, no):
        if no.declaracoes_locais: self.visitar(no.declaracoes_locais)
        if no.comandos: self.visitar(no.comandos)

    def visitar_ReturnStmt(self, no):
        if self.funcao_atual is None: raise Exception("Erro Semântico: Instrução 'return' encontrada fora de uma função.")
        tipo_retornado = self.visitar(no.expressao)
        tipo_esperado = self.funcao_atual['tipo_retorno']
        if tipo_retornado != tipo_esperado: raise Exception(f"Erro de Tipo: A função espera um retorno do tipo '{tipo_esperado}', mas recebeu '{tipo_retornado}'.")

    def visitar_FunctionCall(self, no):
        nome_func = no.nome
        info_func = self.buscar_simbolo(nome_func)
        if not info_func or info_func['tipo_estrutura'] != 'function': raise Exception(f"Erro Semântico: Função '{nome_func}' não foi declarada.")
        params_esperados = info_func['parametros']
        args_passados = no.args
        if len(params_esperados) != len(args_passados): raise Exception(f"Erro Semântico: Função '{nome_func}' espera {len(params_esperados)} argumentos, mas recebeu {len(args_passados)}.")
        for i, arg_node in enumerate(args_passados):
            tipo_esperado = params_esperados[i]['tipo']
            tipo_passado = self.visitar(arg_node)
            if tipo_esperado != tipo_passado: raise Exception(f"Erro de Tipo: Argumento {i+1} da função '{nome_func}' deveria ser do tipo '{tipo_esperado}', mas é do tipo '{tipo_passado}'.")
        return info_func['tipo_retorno']

    def visitar_Atribuicao(self, no):
        tipo_expressao = self.visitar(no.expressao)
        tipo_lhs = self.visitar(no.var)
        if tipo_lhs != tipo_expressao:
            raise Exception(f"Erro de Tipo: Não é possível atribuir tipo '{tipo_expressao}' a um local do tipo '{tipo_lhs}'.")

    def visitar_Variavel(self, no):
        nome_var = no.nome
        info_var = self.buscar_simbolo(nome_var)
        if not info_var: raise Exception(f"Erro Semântico: Símbolo '{nome_var}' não foi declarado.")
        if info_var['tipo_estrutura'] == 'var': return info_var['tipo']
        elif info_var['tipo_estrutura'] == 'type': return no.nome
        else: raise Exception(f"Erro Semântico: '{nome_var}' não é uma variável ou tipo utilizável neste contexto.")
    
    def visitar_Numero(self, no):
        if isinstance(no.valor, int): return 'integer'
        elif isinstance(no.valor, float): return 'real'

    def visitar_OperacaoBinaria(self, no):
        tipo_esq = self.visitar(no.esq)
        tipo_dir = self.visitar(no.dir)
        validos = ['integer', 'real']
        if tipo_esq not in validos or tipo_dir not in validos: raise Exception(f"Erro de Tipo: Operação '{no.op}' não suportada entre '{tipo_esq}' e '{tipo_dir}'.")
        if tipo_esq == 'real' or tipo_dir == 'real': return 'real'
        else: return 'integer'

# --------------------------------------------------------------------
# ETAPA 4: GERAÇÃO DE CÓDIGO INTERMEDIÁRIO (CI)
# --------------------------------------------------------------------
class InstrucaoTAC:
    def __init__(self, op, arg1, arg2, dest): self.op = op; self.arg1 = arg1; self.arg2 = arg2; self.dest = dest
    def __repr__(self):
        if self.op in ['+', '-', '*', '/']: return f"{self.dest} := {self.arg1} {self.op} {self.arg2}"
        elif self.op == ':=': return f"{self.dest} := {self.arg1}"
        elif self.op == 'return': return f"return {self.arg1}"
        elif self.op == 'param': return f"param {self.arg1}"
        elif self.op == 'call': return f"{self.dest} := call {self.arg1}, {self.arg2}"
        else: return f"{self.op} {self.arg1} {self.arg2} {self.dest}"

class GeradorCI:
    def __init__(self): self.codigo = []; self.contador_temp = 0
    def novo_temp(self): nome_temp = f"t{self.contador_temp}"; self.contador_temp += 1; return nome_temp
    def visitar(self, no):
        if no is None: return
        if isinstance(no, list):
            for item in no: self.visitar(item)
            return
        nome_metodo = f'visitar_{type(no).__name__}'; visitante = getattr(self, nome_metodo, self.erro_generico); return visitante(no)
    def erro_generico(self, no): pass
    def visitar_Atribuicao(self, no):
        loc_expr = self.visitar(no.expressao)
        dest = self.visitar(no.var)
        instr = InstrucaoTAC(':=', loc_expr, None, dest); self.codigo.append(instr)
    def visitar_OperacaoBinaria(self, no): loc_esq = self.visitar(no.esq); loc_dir = self.visitar(no.dir); temp_dest = self.novo_temp(); instr = InstrucaoTAC(no.op, loc_esq, loc_dir, temp_dest); self.codigo.append(instr); return temp_dest
    def visitar_Numero(self, no): return no.valor
    def visitar_Variavel(self, no): return no.nome
    def visitar_ArrayAccess(self, no): indice_loc = self.visitar(no.indice); return f"{no.var.nome}[{indice_loc}]"
    def visitar_RecordAccess(self, no): base_loc = self.visitar(no.var); return f"{base_loc}.{no.campo.nome}"
    def visitar_FunctionCall(self, no):
        args_locs = [self.visitar(arg) for arg in no.args];
        for loc in reversed(args_locs): self.codigo.append(InstrucaoTAC('param', loc, None, None))
        temp_retorno = self.novo_temp(); self.codigo.append(InstrucaoTAC('call', no.nome, len(args_locs), temp_retorno)); return temp_retorno
    def visitar_ReturnStmt(self, no): loc_expr = self.visitar(no.expressao); self.codigo.append(InstrucaoTAC('return', loc_expr, None, None))

# --------------------------------------------------------------------
# ETAPA FINAL: EXECUTAR TODAS AS FASES DO COMPILADOR
# --------------------------------------------------------------------
parser = yacc.yacc()
try:
    with open('exemplo.pas', 'r') as file:
        codigo = file.read()
    
    print("--- Iniciando Análise Sintática ---")
    arvore_sintatica = parser.parse(codigo, lexer=lexer)
    print("--- Análise Sintática Concluída ---\n")

    if arvore_sintatica:
        print("--- Iniciando Análise Semântica ---")
        try:
            analisador = AnalisadorSemantico()
            analisador.visitar(arvore_sintatica)
            print("--- Análise Semântica Concluída com Sucesso! ---\n")
            
            print("--- Iniciando Geração de Código Intermediário ---")
            gerador = GeradorCI()
            gerador.visitar(arvore_sintatica)
            codigo_intermediario = gerador.codigo
            print("--- Geração de Código Concluída! ---")
            
            print("\nCódigo Intermediário Gerado (TAC):")
            for instr in codigo_intermediario:
                print(instr)

        except Exception as e:
            print(f"\nERRO: {e}")
except FileNotFoundError:
    print("Arquivo 'exemplo.pas' não encontrado. Crie um com código para testar.")