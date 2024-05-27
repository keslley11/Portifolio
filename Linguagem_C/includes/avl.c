#include "avl.h"

/*
Árvore binária de busca Balanceada (AVL):

    a diferença de altura entre as subárvores esquerda e direita de qualquer nó é no máximo 1

*/

#include <stdio.h>
#include <stdlib.h>

// Função para criar um novo nó
AVLNode *createNode(int key)
{
    AVLNode *newNode = (AVLNode *)malloc(sizeof(AVLNode));
    newNode->key = key;
    newNode->left = NULL;
    newNode->right = NULL;
    newNode->height = 1; // Novo nó é adicionado como folha, então sua altura é 1
    return newNode;
}

// Função para obter a altura de um nó
int height(AVLNode *node)
{
    if (node == NULL)
        return 0;
    else
        return node->height;
}

// Função para calcular o fator de balanceamento de um nó
int balanceFactor(AVLNode *node)
{
    if (node == NULL)
        return 0;
    else
        return height(node->left) - height(node->right);
}

// Função para atualizar a altura de um nó
void updateHeight(AVLNode *node)
{
    int leftHeight = height(node->left);
    int rightHeight = height(node->right);
    node->height = (leftHeight > rightHeight ? leftHeight : rightHeight) + 1;
}

// Função para fazer uma rotação simples à direita
AVLNode *rotateRight(AVLNode *y)
{
    AVLNode *x = y->left;
    AVLNode *T2 = x->right;

    // Realiza a rotação
    x->right = y;
    y->left = T2;

    // Atualiza as alturas dos nós afetados
    updateHeight(y);
    updateHeight(x);

    // Retorna o novo nó raiz
    return x;
}

// Função para fazer uma rotação simples à esquerda
AVLNode *rotateLeft(AVLNode *x)
{
    AVLNode *y = x->right;
    AVLNode *T2 = y->left;

    // Realiza a rotação
    y->left = x;
    x->right = T2;

    // Atualiza as alturas dos nós afetados
    updateHeight(x);
    updateHeight(y);

    // Retorna o novo nó raiz
    return y;
}

// Função para inserir um novo nó em uma árvore AVL
AVLNode *insertNode(AVLNode *root, int key)
{
    // Passo 1: inserção padrão de um novo nó BST
    if (root == NULL)
        return createNode(key);

    if (key < root->key)
        root->left = insertNode(root->left, key);
    else if (key > root->key)
        root->right = insertNode(root->right, key);
    else // Chaves iguais não são permitidas na BST
        return root;

    // Passo 2: atualizar a altura do nó atual
    updateHeight(root);

    // Passo 3: obter o fator de balanceamento deste nó
    int balance = balanceFactor(root);

    // Se o nó se tornar desbalanceado, são necessárias rotações para restaurar o balanceamento
    // Casos de rotação: esquerda-esquerda, esquerda-direita, direita-direita, direita-esquerda
    if (balance > 1 && key < root->left->key)
        return rotateRight(root);

    if (balance < -1 && key > root->right->key)
        return rotateLeft(root);

    if (balance > 1 && key > root->left->key)
    {
        root->left = rotateLeft(root->left);
        return rotateRight(root);
    }

    if (balance < -1 && key < root->right->key)
    {
        root->right = rotateRight(root->right);
        return rotateLeft(root);
    }

    // Retorna o ponteiro para o nó raiz (sem mudança se o nó já existir)
    return root;
}

// Função para encontrar um nó na árvore AVL
AVLNode *searchNode(AVLNode *root, int key)
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

// Função para encontrar o nó com o valor mínimo (menor chave) na árvore AVL
AVLNode *minValueNode(AVLNode *node)
{
    AVLNode *current = node;

    // Percorre a árvore pela esquerda até encontrar o nó com o valor mínimo
    while (current && current->left != NULL)
        current = current->left;

    return current;
}

// Função para remover um nó da árvore AVL
AVLNode *deleteNode(AVLNode *root, int key)
{
    // Caso base: se a árvore estiver vazia, retorna
    if (root == NULL)
        return root;

    // Passo 1: inserir a remoção padrão de um nó BST
    if (key < root->key)
        root->left = deleteNode(root->left, key);
    else if (key > root->key)
        root->right = deleteNode(root->right, key);
    else
    {
        // Nó com apenas um filho ou sem filhos
        if (root->left == NULL)
        {
            AVLNode *temp = root->right;
            free(root);
            return temp;
        }
        else if (root->right == NULL)
        {
            AVLNode *temp = root->left;
            free(root);
            return temp;
        }

        // Nó com dois filhos: obtém o sucessor (nó mais à esquerda da subárvore direita)
        AVLNode *temp = minValueNode(root->right);

        // Copia o valor do sucessor para este nó
        root->key = temp->key;

        // Remove o sucessor
        root->right = deleteNode(root->right, temp->key);
    }

    // Se a árvore tinha apenas um nó, retorne
    if (root == NULL)
        return root;

    // Passo 2: atualizar a altura do nó atual
    updateHeight(root);

    // Passo 3: obter o fator de balanceamento deste nó
    int balance = balanceFactor(root);

    // Se o nó se tornar desbalanceado, são necessárias rotações para restaurar o balanceamento
    // Casos de rotação: esquerda-esquerda, esquerda-direita, direita-direita, direita-esquerda
    if (balance > 1 && balanceFactor(root->left) >= 0)
        return rotateRight(root);

    if (balance > 1 && balanceFactor(root->left) < 0)
    {
        root->left = rotateLeft(root->left);
        return rotateRight(root);
    }

    if (balance < -1 && balanceFactor(root->right) <= 0)
        return rotateLeft(root);

    if (balance < -1 && balanceFactor(root->right) > 0)
    {
        root->right = rotateRight(root->right);
        return rotateLeft(root);
    }

    // Retorna o ponteiro para o nó raiz (sem mudança se o nó já existir)
    return root;
}

// Função para percorrer a árvore em ordem (esquerda, raiz, direita)
void inOrderTraversal(AVLNode *root)
{
    if (root != NULL)
    {
        inOrderTraversal(root->left);
        printf("%d ", root->key);
        inOrderTraversal(root->right);
    }
}

void deleteTree(AVLNode *root)
{
    if (root == NULL)
        return;

    // Primeiro, desalocamos os nós filhos (esquerda e direita)
    deleteTree(root->left);
    deleteTree(root->right);

    // Em seguida, liberamos o nó atual
    free(root);
}
