# Teste completo com as estruturas de type, record e array.

type
    # Definição de um novo tipo 'aluno' como um registro.
    # Note que não há ponto e vírgula depois de 'end'.
    aluno == record
        matricula: integer;
        media: real;
    end;

    # Definição de um novo tipo 'turma' como um vetor do tipo 'aluno'.
    turma == array [30] of aluno;

var
    # Declaração de variáveis usando os novos tipos definidos.
    sala_a: turma;
    melhor_aluno: aluno;
    uma_matricula: integer;

# --- Início dos Comandos ---

begin

    # Acessa e atribui valores aos campos de uma variável do tipo record.
    melhor_aluno.matricula := 101;
    melhor_aluno.media := 9.8;

    # Atribui uma variável do tipo record a um elemento do array.
    # A checagem de tipo deve verificar se 'melhor_aluno' e 'sala_a[1]' são ambos do tipo 'aluno'.
    sala_a[1] := melhor_aluno;

    # Acessa um campo de um registro que está dentro de um array.
    uma_matricula := sala_a[1].matricula;

    # Atribuição direta a um campo de um elemento do array.
    sala_a[2].media := 7.5;

end;