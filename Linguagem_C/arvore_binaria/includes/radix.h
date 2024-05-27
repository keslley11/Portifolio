#ifndef ADB_H
#define ADB_H

// Dados
typedef struct No
{
    unsigned chave;
    struct No *esq, *dir;
} No;

#define bits_na_chave 4 // 32

// Funcoes
No *criar_arvore();
void destruir_arvore(No **p);

No *inserir(No *p, unsigned chave);
No *buscar(No *p, unsigned x);

void imprimir(No *p, int level);

No *remover(No *p, unsigned chave);

#endif
