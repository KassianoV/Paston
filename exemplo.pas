# Teste completo com record e array

type 
    aluno == record
        matricula: integer;
        media: real;
    end;

type
    turma == array [20] of aluno;

var 
    minha_turma: turma;
    aluno_temp: aluno;

# Atribuindo valores a um registro
aluno_temp.matricula := 123;
aluno_temp.media := 8.5;

# Colocando o registro dentro do array
minha_turma[1] := aluno_temp;

# Acessando um campo de um elemento do array
minha_turma[2].matricula := 456;