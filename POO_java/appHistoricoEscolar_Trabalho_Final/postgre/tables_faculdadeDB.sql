
create table alunos(
    alunoID serial PRIMARY KEY,
	cpf varchar(11) not null,
	nome varchar(50) not null,
	email varchar(50) UNIQUE not null,
	fone varchar(14) not null,
	nascimento date not null
);
 
create table professores(
    profID serial primary key,
	nome varchar(50) not null,
	email varchar(50) UNIQUE not null,
	salario NUMERIC not null
);

create table cursos(
    cursoID serial primary key,
	nome varchar(50) not null,
	--descricao TEXT,
	cargaHr NUMERIC not null
);

create table cursosRequisitos(
    cursoID int,
	CONSTRAINT fk_curso FOREIGN KEY (cursoID) REFERENCES cursos (cursoID) ON DELETE CASCADE,
	cursoReqID int,
	CONSTRAINT fk_curso_req FOREIGN KEY (cursoReqID) REFERENCES cursos (cursoID) ON DELETE CASCADE,
	PRIMARY KEY (cursoID, cursoReqID),--testar
	CHECK (cursoID <> cursoReqID)
);

create table turmas(
    turmaID serial primary key,
	cursoID int,
	CONSTRAINT fk_curso FOREIGN KEY (cursoID) REFERENCES cursos (cursoID) ON DELETE CASCADE,
	profID int NULL,
	CONSTRAINT fk_prof FOREIGN KEY (profID) REFERENCES professores (profID) ON DELETE SET NULL
);

create table matriculas(
    matriculaID serial primary key,
	status char(40) not null,
	turmaID int,
	CONSTRAINT fk_turma FOREIGN KEY (turmaID) REFERENCES turmas (turmaID) ON DELETE CASCADE,
	alunoID int,
	CONSTRAINT fk_aluno FOREIGN KEY (alunoID) REFERENCES alunos (alunoID) ON DELETE CASCADE,
	UNIQUE (alunoID, turmaID)
);

--Refazer tabelas
/*
DROP TABLE matriculas;
DROP TABLE cursosRequisitos;
DROP TABLE turmas;
DROP TABLE alunos;
DROP TABLE professores;
DROP TABLE cursos;
*/




--===========================================================================================
-- Populando BD
--===========================================================================================
/*
insert into alunos (cpf,nome,email,fone,nascimento)
values
('cpf1', 'nome1', 'email1', 'fone1','2025-11-11'),
('cpf11', 'nome11', 'email11', 'fone11','2025-11-11'),
('cpf21', 'nome21', 'email21', 'fone21','2025-12-21');
select * from alunos;

insert into professores (nome,email,salario)
values
('nome2', 'email2', 15000.2),
('nome12', 'email12', 15000.12),
('nome22', 'email22', 15000.22);
select * from professores;

insert into cursos (nome,cargaHr)
values
('nome3', 60),
('nome4', 90),
('nome5', 30);
select * from cursos;

-- verificar idcursos atribuidos

insert into cursosRequisitos (cursoID,cursoReqID)
values
(2,1),
(3,1),
(3,2);
select * from cursosRequisitos;

insert into turmas (cursoID,profID)
values
(3,1),
(3,1),
(2,2);
select * from turmas;

insert into matriculas (status,turmaID,alunoID)
values
('matriculado/reprovado',1,1),
('matriculado/em andamento',3,1),
('matriculado/aprovado',2,2),
('matriculado/aprovado',3,2);
select * from matriculas;
*/

--===========
-- Read
--===========
select * from alunos;
select * from professores;
select * from cursos;
select * from cursosRequisitos;
select * from turmas;
select * from matriculas;

--===========
-- update
--===========
UPDATE alunos SET nome = 'teste' WHERE alunoID = 1;
select * from alunos;

--===========
-- Delete
--===========
DELETE FROM alunos WHERE alunoID = 1;

--===========
-- Limpar Tabelas
--===========
delete from alunos;
delete from professores;
delete from cursos;
delete from cursosRequisitos;
delete from turmas;
delete from matriculas;





--===========
-- CRUD alunos
--===========
--create:
insert into alunos (cpf,nome,email,fone,nascimento)
values
('cpf1', 'nome1', 'email1', 'fone1','2025-1-1');
--read:
select * from alunos;
--apdate:
UPDATE alunos SET cpf='newCpf',nome='newNome',email='newEmail',fone='newFone',nascimento='2025-1-2' WHERE alunoID = 1;
--delete:
DELETE FROM alunos WHERE alunoID = 7;

--===========
-- CRUD cursos
--===========
--create:
insert into cursos (nome,cargaHr)
values
('nome3', 60);
--read:
select * from cursos;
--apdate:
UPDATE cursos SET nome = 'testeNew', cargaHr = 45 WHERE cursoID = 1;
--delete:
DELETE FROM cursos WHERE cursoID = 23;

--===========
-- CRUD professores
--===========
--create:
insert into professores (nome,email,salario)
values
('nome2', 'email2', 15000.2);
--read:
select * from professores;
--apdate:
UPDATE professores SET nome = 'newNome', email='newEmail',salario=15000.3 WHERE profID = 2;
--delete:
DELETE FROM professores WHERE profID = 2;

--===========
-- CRUD cursosRequisitos
--===========
--create:
insert into cursosRequisitos (cursoID,cursoReqID)
values
(13,13);
--read:
select * from cursosRequisitos;
--apdate:
UPDATE cursosRequisitos SET cursoReqID = 3 WHERE cursoID = 13;
--delete:
DELETE FROM cursosRequisitos WHERE cursoID = 13;--AND cursoReqID = 3

--===========
-- CRUD turmas
--===========
--create:
insert into turmas (cursoID,profID)
values
(3,1);
--read:
select * from turmas;
--apdate:
UPDATE turmas SET cursoID=13,profID=22 WHERE turmaID = 25; --bloquear update campo "cursoID" no front-end
--delete:
DELETE FROM turmas WHERE turmaID = 25;

--===========
-- CRUD matriculas
--===========
--create:
insert into matriculas (status,turmaID,alunoID)
values
('matriculado/reprovado',5,1);
--read:
select * from matriculas;
--apdate:
UPDATE matriculas SET status='newStatus',turmaID=5,alunoID=11 WHERE matriculaID = 6; --bloquear update campo "alunoID" no front-end
--delete:
DELETE FROM matriculas WHERE matriculaID = 6;



--===========
-- Query relacionada
--===========
SELECT * FROM cursos
INNER JOIN cursosRequisitos 
    ON cursos.cursoID = cursosRequisitos.cursoID
--WHERE condition(s)

--===========
SELECT 
    c.nome AS curso,
    COALESCE(STRING_AGG(pr.nome, ', '), '-') AS prerequisitos
FROM 
    cursos c
LEFT JOIN cursosRequisitos cp ON cp.cursoID = c.cursoID
LEFT JOIN cursos pr ON pr.cursoID = cp.cursoReqID
GROUP BY c.nome
ORDER BY c.nome;

--===========
--verificação dos req. antes de add nova matricula
--===========
SELECT m.*
FROM matriculas m
INNER JOIN turmas t ON m.turmaID = t.turmaID
WHERE m.alunoID = 1
AND t.cursoID IN (
    SELECT cursoReqID
    FROM cursosRequisitos
    WHERE cursoID = (
        SELECT cursoID
        FROM turmas
        WHERE turmaID = 4
    )
);
