#include <stdio.h>
#include <stdlib.h>
// #include "includes/bst.h"
//  #include "includes/avl.h"
//  #include "includes/heap.h"
#include "includes/radix.h"
// #include "includes/splay.h"

/*
Para compilar:

gcc -Wall -Werror -c INCLUDE_X.c    (cd includes)
gcc -Wall -Werror -c main.c         (cd ../)
gcc main.o includes/INCLUDE_X.o -lm -o main

(Para executar: ./main)


ou usando Makefile

    all: main

    main_9: main.o INCLUDE_X.o
        gcc main.o INCLUDE_X.o -lm -o main

    main.o: main.c INCLUDE_X.h
        gcc -Wall -Werror -c main.c

    INCLUDE_X.o: INCLUDE_X.c INCLUDE_X.h
        gcc -Wall -Werror -c INCLUDE_X.c

*/

// Função principal
int main()
{

    /*================================================================================================
    BST
    ==================================================================================================*/
    /*
    Node *root = NULL;
    root = insertNode(root, 50);
    insertNode(root, 30);
    insertNode(root, 20);
    insertNode(root, 40);
    insertNode(root, 70);
    insertNode(root, 60);
    insertNode(root, 80);

    printf("Arvore BST apos insercao: ");
    inOrderTraversal(root);
    printf("\n");

    // Procurando um nó
    int searchKey = 40;
    Node *searchResult = searchNode(root, searchKey);
    if (searchResult != NULL)
        printf("O elemento %d foi encontrado na arvore.\n", searchKey);
    else
        printf("O elemento %d nao foi encontrado na arvore.\n", searchKey);

    // Removendo um nó
    int deleteKey = 20;
    root = deleteNode(root, deleteKey);
    printf("Arvore BST apos remocao do elemento %d: ", deleteKey);
    inOrderTraversal(root);
    printf("\n");

    deleteTree(root);
    //*/

    /*================================================================================================
    AVL
    ==================================================================================================*/
    /*
    AVLNode *root = NULL;
    root = insertNode(root, 9);
    root = insertNode(root, 5);
    root = insertNode(root, 10);
    root = insertNode(root, 0);
    root = insertNode(root, 6);
    root = insertNode(root, 11);
    root = insertNode(root, -1);
    root = insertNode(root, 1);
    root = insertNode(root, 2);

    printf("Arvore AVL apos insercao: ");
    inOrderTraversal(root);
    printf("\n");

    // Procurando um nó
    int searchKey = 10;
    AVLNode *searchResult = searchNode(root, searchKey);
    if (searchResult != NULL)
        printf("O elemento %d foi encontrado na arvore AVL.\n", searchKey);
    else
        printf("O elemento %d nao foi encontrado na arvore AVL.\n", searchKey);

    // Removendo um nó
    int deleteKey = 10;
    root = deleteNode(root, deleteKey);
    printf("Arvore AVL apos remocao do elemento %d: ", deleteKey);
    inOrderTraversal(root);
    printf("\n");

    deleteTree(root);
    //*/

    /*================================================================================================
    Heap
    ==================================================================================================*/
    /*
    MinHeap *minHeap = createMinHeap(MAX_HEAP_SIZE);

    insert(minHeap, 10);
    insert(minHeap, 20);
    insert(minHeap, 15);
    insert(minHeap, 40);
    insert(minHeap, 50);
    insert(minHeap, 100);

    printf("Apos insercao:\n");
    printMinHeap(minHeap);

    printf("Extraindo o menor elemento: %d\n", extractMin(minHeap));
    printf("Min Heap apos extracao:\n");
    printMinHeap(minHeap);

    destroyMinHeap(minHeap);
    //*/

    /*================================================================================================
    Radix
    ==================================================================================================*/
    ///*
    int i;
    No *T = criar_arvore();
    for (i = 0; i < 16; i++)
    {
        if (i == 2)
            continue;
        T = inserir(T, i);
    }
    T = inserir(T, 2); // nao insere repetidos
    imprimir(T, 0);

    // remover
    T = remover(T, 2);
    imprimir(T, 0);

    destruir_arvore(&T);
    //*/
    /*================================================================================================
        Splay      (não está compilando, mas roda no editor online)
    ==================================================================================================*/
    /*
    SplayNode *root = NULL;

    // Adiciona alguns nós à Árvore Binária de Busca Splay
    root = insertNode(root, 100);
    root = insertNode(root, 50);
    root = insertNode(root, 200);
    root = insertNode(root, 40);
    root = insertNode(root, 30);

    printf("Arvore Binaria de Busca Splay apos insercao: ");
    inOrderTraversal(root);
    printf("\t(rootKey:%d)\n", root->key);

    // Procurando um nó
    int searchKey = 45;
    SplayNode *searchResult = searchNode(root, searchKey);
    if (searchResult != NULL && searchResult->key == searchKey)
    {
        printf("O elemento %d foi encontrado na Arvore Binaria de Busca Splay.\n", searchKey);
    }
    else
        printf("O elemento %d nao foi encontrado na Arvore Binaria de Busca Splay.\n", searchKey);
    root = searchResult;

    printf("Arvore Binaria de Busca Splay apos busca: ");
    inOrderTraversal(root);
    printf("\t(rootKey:%d)\n", root->key);

    destroyTree(root);
    //*/
    return 0;
}