#include <stdio.h>
#include <stdlib.h>
#include "splay.h"

/*
Árvore Binária de Busca Splay:

árvore binária de busca auto-ajustável, onde após cada operação de busca,
inserção ou remoção, o nó acessado é movido para a raiz da árvore.
Isso ajuda a otimizar operações subsequentes
*/

// Função para criar um novo nó
SplayNode *createNode(int key)
{
    SplayNode *newNode = (SplayNode *)malloc(sizeof(SplayNode));
    newNode->key = key;
    newNode->left = NULL;
    newNode->right = NULL;
    return newNode;
}

// Função para fazer a rotação à direita
SplayNode *rightRotate(SplayNode *x)
{
    SplayNode *y = x->left;
    x->left = y->right;
    y->right = x;
    return y;
}

// Função para fazer a rotação à esquerda
SplayNode *leftRotate(SplayNode *x)
{
    SplayNode *y = x->right;
    x->right = y->left;
    y->left = x;
    return y;
}

// Função Splay para trazer o nó com a chave especificada para a raiz
SplayNode *splay(SplayNode *root, int key)
{
    // Se a árvore estiver vazia ou a chave estiver na raiz, retorne a raiz
    if (root == NULL || root->key == key)
        return root;

    // A chave é menor que a chave da raiz
    if (key < root->key)
    {
        // A chave não está na árvore, retorna a raiz
        if (root->left == NULL)
            return NULL;

        // Zig-zig (esquerda-esquerda)
        if (key < root->left->key)
        {
            // Splay na subárvore esquerda da subárvore esquerda
            root->left->left = splay(root->left->left, key);
            // Rotação à direita na raiz
            root = rightRotate(root);
        }
        // Zig-zag (esquerda-direita)
        else if (key > root->left->key)
        {
            // Splay na subárvore direita da subárvore esquerda
            root->left->right = splay(root->left->right, key);
            // Se a subárvore direita da subárvore esquerda não for nula, faça uma rotação à esquerda na subárvore esquerda
            if (root->left->right != NULL)
                root->left = leftRotate(root->left);
        }

        // Se a subárvore esquerda não for nula, faça uma rotação à direita na raiz
        return (root->left == NULL) ? root : rightRotate(root);
    }
    // A chave é maior que a chave da raiz
    else
    {
        // A chave não está na árvore, retorna a raiz
        if (root->right == NULL)
            return NULL;

        // Zig-zag (direita-esquerda)
        if (key < root->right->key)
        {
            // Splay na subárvore esquerda da subárvore direita
            root->right->left = splay(root->right->left, key);
            // Se a subárvore esquerda da subárvore direita não for nula, faça uma rotação à direita na subárvore direita
            if (root->right->left != NULL)
                root->right = rightRotate(root->right);
        }
        // Zig-zig (direita-direita)
        else if (key > root->right->key)
        {
            // Splay na subárvore direita da subárvore direita
            root->right->right = splay(root->right->right, key);
            // Rotação à esquerda na raiz
            root = leftRotate(root);
        }

        // Se a subárvore direita não for nula, faça uma rotação à esquerda na raiz
        return (root->right == NULL) ? root : leftRotate(root);
    }
}

// Função para adicionar um novo nó à Árvore Binária de Busca Splay
SplayNode *insertNode(SplayNode *root, int key)
{
    // Se a árvore estiver vazia, retorna um novo nó
    if (root == NULL)
        return createNode(key);

    // Splay para trazer a chave para a raiz, se existir
    root = splay(root, key);

    // Se a chave já existe, não faça nada
    if (root->key == key)
        return root;

    // Aloca um novo nó
    SplayNode *newNode = createNode(key);

    // Se a chave for menor que a raiz, adiciona à esquerda
    if (key < root->key)
    {
        newNode->right = root;
        newNode->left = root->left;
        root->left = NULL;
    }
    // Se a chave for maior que a raiz, adiciona à direita
    else
    {
        newNode->left = root;
        newNode->right = root->right;
        root->right = NULL;
    }

    return newNode;
}

// Função para procurar um nó na Árvore Binária de Busca Splay
SplayNode *searchNode(SplayNode *root, int key)
{
    // Executa o splay na árvore para trazer o nó com a chave especificada para a raiz
    root = splay(root, key);

    /*
        // Se a raiz agora contém a chave especificada, retorna a raiz
        if (root != NULL && root->key == key)
            return root;
        else
            return NULL; // Se a chave não estiver na árvore, retorna NULL
    */
    return root;
}

// Função para percorrer a árvore em ordem (esquerda, raiz, direita)
void inOrderTraversal(SplayNode *root)
{
    if (root != NULL)
    {
        inOrderTraversal(root->left);
        printf("%d ", root->key);
        inOrderTraversal(root->right);
    }
}

// Função para remover um nó da Árvore Binária de Busca Splay
SplayNode *deleteNode(SplayNode *root, int key)
{
    if (root == NULL)
        return NULL;

    root = splay(root, key);

    if (key != root->key)
        return root;

    SplayNode *temp;
    if (root->left == NULL)
    {
        temp = root;
        root = root->right;
    }
    else
    {
        temp = root;
        root = splay(root->left, key);
        root->right = temp->right;
    }

    free(temp);
    return root;
}

// Função para desalocar toda a árvore Splay
void destroyTree(SplayNode *root)
{
    if (root == NULL)
        return;
    destroyTree(root->left);
    destroyTree(root->right);
    free(root);
}