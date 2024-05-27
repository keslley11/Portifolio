#include <stdio.h>
#include <stdlib.h>
#include "bst.h"

/*
Árvore Binária de Busca (BST):

    cada nó tem no máximo dois filhos, o filho da esquerda contém um valor menor que o nó pai e o filho da direita contém um valor maior

*/

// Função para criar um novo nó
Node *createNode(int key)
{
    Node *newNode = (Node *)malloc(sizeof(Node));
    newNode->key = key;
    newNode->left = NULL;
    newNode->right = NULL;
    return newNode;
}

// Função para adicionar um novo nó à BST
Node *insertNode(Node *root, int key)
{
    // Se a árvore estiver vazia, retorna um novo nó
    if (root == NULL)
        return createNode(key);

    // Caso contrário, percorre a árvore
    if (key < root->key)
        root->left = insertNode(root->left, key);
    else if (key > root->key)
        root->right = insertNode(root->right, key);

    // Retorna o ponteiro para o nó raiz (sem mudança se o nó já existir)
    return root;
}

// Função para encontrar um nó na BST
Node *searchNode(Node *root, int key)
{
    // Se a árvore estiver vazia ou o elemento for encontrado, retorna o nó
    if (root == NULL || root->key == key)
        return root;

    // Se a chave for menor que a chave do nó, procura na subárvore esquerda
    if (key < root->key)
        return searchNode(root->left, key);
    // Se a chave for maior que a chave do nó, procura na subárvore direita
    else
        return searchNode(root->right, key);
}

// Função para encontrar o nó com o valor mínimo (menor chave) na BST
Node *minValueNode(Node *node)
{
    Node *current = node;

    // Percorre a árvore pela esquerda até encontrar o nó com o valor mínimo
    while (current && current->left != NULL)
        current = current->left;

    return current;
}

// Função para remover um nó da BST
Node *deleteNode(Node *root, int key)
{
    // Caso base: se a árvore estiver vazia, retorna
    if (root == NULL)
        return root;

    // Se a chave for menor que a chave do nó atual, procura na subárvore esquerda
    if (key < root->key)
        root->left = deleteNode(root->left, key);
    // Se a chave for maior que a chave do nó atual, procura na subárvore direita
    else if (key > root->key)
        root->right = deleteNode(root->right, key);
    // Se a chave for igual à chave do nó atual, este é o nó a ser removido
    else
    {
        // Nó com apenas um filho ou sem filhos
        if (root->left == NULL)
        {
            Node *temp = root->right;
            free(root);
            return temp;
        }
        else if (root->right == NULL)
        {
            Node *temp = root->left;
            free(root);
            return temp;
        }

        // Nó com dois filhos: obtém o sucessor (nó mais à esquerda da subárvore direita)
        Node *temp = minValueNode(root->right);

        // Copia o valor do sucessor para este nó
        root->key = temp->key;

        // Remove o sucessor
        root->right = deleteNode(root->right, temp->key);
    }
    return root;
}

// Função para percorrer a árvore em ordem (esquerda, raiz, direita)
void inOrderTraversal(Node *root)
{
    if (root != NULL)
    {
        inOrderTraversal(root->left);
        printf("%d ", root->key);
        inOrderTraversal(root->right);
    }
}

void deleteTree(Node *root)
{
    if (root == NULL)
        return;

    // Primeiro, desalocamos os nós filhos (esquerda e direita)
    deleteTree(root->left);
    deleteTree(root->right);

    // Em seguida, liberamos o nó atual
    free(root);
}
