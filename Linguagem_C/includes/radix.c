#include <stdio.h>
#include <stdlib.h>
#include "radix.h"

/*
Busca Radix (arvores digitais de busca):

    chaves representadas em base 2, por bit: se for 0 desce pra esquerda, se for 1 desce pra direita. Uma arvore com altura baixa, mas com muitos nos
*/

unsigned bit(unsigned chave, int k)
{
    return chave >> (bits_na_chave - 1 - k) & 1;
}

No *criar_arvore()
{
    return NULL;
}

void destruir_arvore(No **p)
{
    if (*p == NULL)
        return;
    destruir_arvore(&((*p)->esq));
    destruir_arvore(&((*p)->dir));
    free(*p);
    *p = NULL;
}

No *buscar_rec(No *p, unsigned x, int nivel)
{ // precisamos saber o n´ıvel
    if (p == NULL)
        return NULL;
    if (x == p->chave)
        return p; // encontrou o valor!
    if (bit(x, nivel) == 0)
        return buscar_rec(p->esq, x, nivel + 1);
    else
        return buscar_rec(p->dir, x, nivel + 1);
}

No *buscar(No *p, unsigned x)
{
    return buscar_rec(p, x, 0);
}

No *inserir_rec(No *p, unsigned chave, int nivel)
{
    if (p == NULL)
    {
        No *novo = (No *)malloc(sizeof(No));
        novo->esq = novo->dir = NULL;
        novo->chave = chave;
        return novo;
    }
    if (chave == p->chave)
        return p; // nao insere valores repetidos
    if (bit(chave, nivel) == 0)
        p->esq = inserir_rec(p->esq, chave, nivel + 1);
    else
        p->dir = inserir_rec(p->dir, chave, nivel + 1);
    return p;
}

No *inserir(No *p, unsigned chave)
{
    return inserir_rec(p, chave, 0);
}

void printnode(int x, int h)
{
    int i;
    for (i = 0; i < h; i++)
        printf("-");
    printf("%2d\n", x);
}

void print(No *p, int h)
{
    if (p == NULL)
        return;
    print(p->dir, h + 1);
    printnode(p->chave, h);
    print(p->esq, h + 1);
}

void imprimir(No *p, int level)
{
    printf("Arvore:\n");
    print(p, 0);
}

// Remoção:

/*
Para remover:
    • uma folha, basta apaga-la
    • um no com um filho, basta fazer o pai apontar para o neto
    • um no com dois filhos
        – copie um descendente qualquer por cima do n´o (compartilha k bits)
        – apague o descendente

*/

// Função recursiva para encontrar o nó mais à direita em uma subárvore
No *encontrar_maior(No *p)
{
    while (p->dir != NULL)
    {
        p = p->dir;
    }
    return p;
}
// Função recursiva para remover um nó da árvore
No *remover_rec(No *p, unsigned chave, int nivel)
{
    if (p == NULL)
        return NULL;

    if (chave == p->chave)
    {
        if (p->esq == NULL && p->dir == NULL)
        {
            // Caso 1: nó é uma folha
            free(p);
            return NULL;
        }
        else if (p->esq == NULL || p->dir == NULL)
        {
            // Caso 2: nó tem um filho
            No *temp = (p->esq != NULL) ? p->esq : p->dir;
            free(p);
            return temp;
        }
        else
        {
            // Caso 3: nó tem dois filhos
            No *maior = encontrar_maior(p->esq);
            p->chave = maior->chave;
            p->esq = remover_rec(p->esq, maior->chave, nivel + 1);
        }
    }
    else if (bit(chave, nivel) == 0)
    {
        p->esq = remover_rec(p->esq, chave, nivel + 1);
    }
    else
    {
        p->dir = remover_rec(p->dir, chave, nivel + 1);
    }
    return p;
}

// Função para remover um nó da árvore
No *remover(No *p, unsigned chave)
{
    return remover_rec(p, chave, 0);
}