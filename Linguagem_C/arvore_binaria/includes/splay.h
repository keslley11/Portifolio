// Definição da estrutura do nó da Árvore Binária de Busca Splay
typedef struct SplayNode
{
    int key;
    struct SplayNode *left;
    struct SplayNode *right;
} SplayNode;

SplayNode *createNode(int key);
SplayNode *rightRotate(SplayNode *x);
SplayNode *leftRotate(SplayNode *x);
SplayNode *splay(SplayNode *root, int key);
SplayNode *insertNode(SplayNode *root, int key);
SplayNode *searchNode(SplayNode *root, int key);
void inOrderTraversal(SplayNode *root);
SplayNode *deleteNode(SplayNode *root, int key);
void destroyTree(SplayNode *root);