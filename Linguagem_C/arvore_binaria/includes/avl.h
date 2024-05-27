

// Definição da estrutura do nó da árvore AVL
typedef struct AVLNode
{
    int key;
    struct AVLNode *left;
    struct AVLNode *right;
    int height;
} AVLNode;

AVLNode *createNode(int key);
int height(AVLNode *node);
int balanceFactor(AVLNode *node);
void updateHeight(AVLNode *node);
AVLNode *rotateRight(AVLNode *y);
AVLNode *rotateLeft(AVLNode *x);
AVLNode *insertNode(AVLNode *root, int key);
AVLNode *searchNode(AVLNode *root, int key);
AVLNode *minValueNode(AVLNode *node);
AVLNode *deleteNode(AVLNode *root, int key);
void inOrderTraversal(AVLNode *root);
void deleteTree(AVLNode *root);