
# 📘 Compilador Simples para "Paston"

Este projeto é a implementação de um compilador simples para um subconjunto da linguagem Pascal, aqui chamado de **"Paston"**.  
O compilador foi desenvolvido em **Python**, utilizando a biblioteca `PLY`, e abrange as principais fases de compilação: análise **léxica**, **sintática**, **semântica** e **geração de código intermediário** (Código de Três Endereços - TAC).

---

## 📁 Estrutura do Projeto

- `lexer.py` — **Analisador Léxico**: converte o código-fonte em uma sequência de tokens.
- `parser.py` — **Analisador Sintático**, **Analisador Semântico** e **Gerador de Código Intermediário**.
- `exemplo.pas` — Arquivo de teste com código em "Paston".
- `parsetab.py` — Gerado automaticamente pela biblioteca `PLY`. Não edite manualmente.

---

## 🚀 Tecnologias Utilizadas

- **Linguagem:** Python 3
- **Bibliotecas:**
  - [`PLY`](https://www.dabeaz.com/ply/): Implementação de Lex e Yacc para Python.

---

## ⚙️ Como Executar

### 1. Pré-requisitos

Certifique-se de ter o Python 3 instalado.  
Instale a dependência principal:

```bash
pip install ply
```

### 2. Execução

Para compilar o código de exemplo, execute:

```bash
python3 parser.py
```

O script lerá o arquivo `exemplo.pas`, executará todas as fases do compilador e imprimirá o Código Intermediário (TAC), caso não haja erros.

### ✅ Saída Esperada

```text
--- Iniciando Análise Sintática ---
--- Análise Sintática Concluída ---

--- Iniciando Análise Semântica ---
--- Análise Semântica Concluída com Sucesso! ---

--- Iniciando Geração de Código Intermediário ---
--- Geração de Código Concluída! ---

Código Intermediário Gerado (TAC):

t0 := 123
aluno_temp.matricula := t0

t1 := 8.5
aluno_temp.media := t1

minha_turma[1] := aluno_temp

t2 := 456
minha_turma[2].matricula := t2
```

---

## 🧠 Fases do Compilador

### 1. 🔍 Análise Léxica (`lexer.py`)

Responsável por identificar **tokens** no código-fonte, como palavras-chave, operadores e identificadores.

#### Exemplo:

Código-fonte:

```pascal
x := a + b * 2;
```

Tokens gerados:

| Token | Valor |
|-------|-------|
| ID    | `x`   |
| ATRIB | `:=`  |
| ID    | `a`   |
| PLUS  | `+`   |
| ID    | `b`   |
| TIMES | `*`   |
| NUM   | `2`   |
| SEMI  | `;`   |

---

### 2. 🏗️ Análise Sintática (`parser.py`)

Verifica se a sequência de tokens segue as regras da gramática. Constrói uma **Árvore de Sintaxe Abstrata (AST)**.

#### Exemplo de regra:

```python
def p_atribuicao(p):
    '''
    atribuicao : ID ATRIB expressao SEMI
    '''
    p[0] = Atribuicao(var=Variavel(p[1]), expressao=p[3])
```

#### AST gerada para `x := a + b * 2;`:

```
        Atribuição (:=)
        /             \
  Variável(x)      Operação(+)
                   /           \
            Variável(a)     Operação(*)
                             /         \
                       Variável(b)   Número(2)
```

---

### 3. 🧾 Análise Semântica (`parser.py`)

Valida o **significado** do código:

- Verifica se as variáveis foram declaradas.
- Detecta declarações múltiplas.
- Faz **checagem de tipos** e permite **coerção segura** (integer → real).

Uma **tabela de símbolos** é construída para rastrear tipos e identificadores.  
O padrão **Visitor** é usado para percorrer a AST e aplicar as regras semânticas.

---

### 4. ⚙️ Geração de Código Intermediário (TAC) (`parser.py`)

Gera um **Código de Três Endereços (TAC)** simples, útil para etapas posteriores de compilação (como otimizações e geração de código de máquina).

#### Exemplo de TAC para `x := a + b * 2;`:

```text
t0 := b * 2
t1 := a + t0
x := t1
```

Cada linha representa uma operação simples, com no máximo três elementos: destino, operação, operando.

---

## 🧑‍💻 Contribuindo

Contribuições são bem-vindas! Sinta-se livre para abrir issues ou pull requests para correções, melhorias ou novas funcionalidades.

---

## 📄 Licença

Este projeto é distribuído sob a licença MIT. Consulte o arquivo `LICENSE` para mais detalhes.
