

// Definição da estrutura do nó da árvore
typedef struct Node
{
    int key;
    struct Node *left;
    struct Node *right;
} Node;

Node *createNode(int key);
Node *insertNode(Node *root, int key);
Node *searchNode(Node *root, int key);
Node *minValueNode(Node *node);
Node *deleteNode(Node *root, int key);
void inOrderTraversal(Node *root);
void deleteTree(Node *root);