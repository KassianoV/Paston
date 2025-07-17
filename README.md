# Compilador Simples para "Paston"

Este projeto é a implementação de um compilador simples para um subconjunto da linguagem Pascal, aqui chamado de "Paston". O compilador foi desenvolvido em Python, utilizando a biblioteca `PLY`, e abrange as principais fases da análise (léxica, sintática e semântica), além da fase de síntese com a geração de Código Intermediário de Três Endereços (TAC).

## 📜 Estrutura do Projeto

O repositório está organizado nos seguintes arquivos:

-   `lexer.py`: Contém o **analisador léxico**, responsável por converter o código-fonte em uma sequência de tokens.
-   `parser.py`: É o coração do compilador. Inclui:
    -   O **analisador sintático**, que constrói uma Árvore de Sintaxe Abstrata (AST).
    -   O **analisador semântico**, que verifica a consistência do código (tipos, declarações, etc.).
    -   O **gerador de código intermediário**, que traduz a AST para Código de Três Endereços (TAC).
-   `exemplo.pas`: Um arquivo de exemplo com código em "Paston" para testar o compilador.
-   `parsetab.py`: Um arquivo gerado automaticamente pela biblioteca `PLY`. Ele contém as tabelas de análise sintática LALR e não deve ser editado manualmente.

## 🚀 Tecnologias Utilizadas

-   **Linguagem:** Python 3
-   **Bibliotecas:**
    -   `PLY (Python Lex-Yacc)`: Uma biblioteca fundamental para a construção de analisadores léxicos e sintáticos em Python.

## ⚙️ Como Começar

Siga estes passos para configurar e executar o compilador em sua máquina local.

### Pré-requisitos

Certifique-se de que você tem o **Python 3** instalado. Em seguida, instale a única dependência do projeto, a `PLY`:

```bash
pip install ply '''

## Execução
Para compilar o código de exemplo, simplesmente execute o arquivo parser.py a partir do seu terminal:

Bash

python3 parser.py
O script irá ler o arquivo exemplo.pas por padrão, processá-lo através das fases do compilador e, se não houver erros, imprimirá o código intermediário gerado no final.

A saída esperada será:

--- Iniciando Análise Sintática ---
--- Análise Sintática Concluída ---

--- Iniciando Análise Semântica ---
--- Análise Semântica Concluída com Sucesso! ---

--- Iniciando Geração de Código Intermediário ---
--- Geração de Código Concluída! ---

Código Intermediário Gerado (TAC):
t0 := b * 2
t1 := a + t0
x := t1
🧠 Fases do Compilador
O processo de compilação é dividido em várias etapas-chave. A seguir, detalhamos como cada uma delas é implementada neste projeto.

1. Análise Léxica (lexer.py)
Objetivo: Ler o código-fonte como texto plano e dividi-lo em pequenos componentes chamados tokens. Cada token representa uma unidade léxica, como uma palavra-chave, um identificador, um número ou um operador.

Exemplo:
Dada a seguinte linha de código em exemplo.pas:

Delphi

x := a + b * 2;
O analisador léxico a converte na seguinte sequência de tokens:

Token

Valor

ID

'x'

ATRIB

':='

ID

'a'

PLUS

'+'

ID

'b'

TIMES

'*'

NUMERO

2

SEMI

';'


Exportar para as Planilhas
Implementação: Em lexer.py, os padrões de cada token são definidos usando expressões regulares. A biblioteca PLY utiliza essas definições para escanear o código e gerar os tokens.

2. Análise Sintática (parser.py)
Objetivo: Receber a sequência de tokens do analisador léxico e verificar se ela segue a estrutura gramatical da linguagem. Se a estrutura for válida, o analisador sintático constrói uma Árvore de Sintaxe Abstrata (AST), que é uma representação hierárquica do código.

Gramática: A estrutura da linguagem é definida por meio de regras de produção. Por exemplo:

Python

# Uma atribuição é um ID, seguido de ':=', uma expressão e um ';'
def p_atribuicao(p):
    '''
    atribuicao : ID ATRIB expressao SEMI
    '''
    p[0] = Atribuicao(var=Variavel(p[1]), expressao=p[3])
Árvore de Sintaxe Abstrata (AST): Para a expressão x := a + b * 2;, o parser gera a seguinte AST, respeitando a precedência de operadores (* antes de +):

      Atribuicao (:=)
      /           \
Variavel(x)    OperacaoBinaria (+)
                 /                 \
         Variavel(a)        OperacaoBinaria (*)
                             /                 \
                       Variavel(b)           Numero(2)
3. Análise Semântica (parser.py)
Objetivo: Analisar a AST para verificar o "significado" e a coerência do código. Esta fase detecta erros que a sintaxe por si só não consegue capturar.

Verificações Realizadas:

Declaração de Variáveis: A variável foi declarada antes de ser usada?

Declarações Múltiplas: Uma variável foi declarada mais de uma vez no mesmo escopo?

Checagem de Tipos: Os tipos de dados em uma operação ou atribuição são compatíveis?

Por exemplo, em x := a + b * 2, o analisador verifica se a e b são numéricos.

Também é verificado se o tipo do resultado da expressão é compatível com o tipo da variável x.

O compilador permite coerção de tipos (atribuir um integer a uma variável real, mas não o contrário).

Tabela de Símbolos: Para realizar essas verificações, o analisador semântico constrói uma tabela de símbolos, que armazena informações sobre cada identificador, como seu nome e tipo (integer, real, etc.).

Implementação: A classe AnalisadorSemantico utiliza o padrão de projeto Visitor para percorrer cada nó da AST e aplicar as regras semânticas correspondentes.

4. Geração de Código Intermediário (parser.py)
Objetivo: Traduzir a AST (já validada) para uma representação de baixo nível, que seja mais fácil de converter para código de máquina. Este projeto gera Código de Três Endereços (TAC).

Código de Três Endereços (TAC): É uma sequência de instruções simples, onde cada instrução tem no máximo três operandos (uma operação, um argumento e um destino).

Exemplo: A AST da expressão x := a + b * 2; é traduzida para o seguinte TAC:

t0 := b * 2
t1 := a + t0
x := t1
t0 e t1 são variáveis temporárias criadas pelo gerador de código.

Cada linha é uma instrução simples e clara, facilitando a otimização e a tradução futura para código de máquina.

Implementação: A classe GeradorCI também utiliza o padrão Visitor para percorrer a AST e emitir as instruções TAC correspondentes.