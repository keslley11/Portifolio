
// Definição da estrutura min-heap

#define MAX_HEAP_SIZE 100

typedef struct MinHeap
{
    int *array;
    int size;
    int capacity;
} MinHeap;

MinHeap *createMinHeap(int capacity);
void swap(int *a, int *b);
void minHeapify(MinHeap *minHeap, int index);
void insert(MinHeap *minHeap, int value);
int extractMin(MinHeap *minHeap);
void printMinHeap(MinHeap *minHeap);
void destroyMinHeap(MinHeap *minHeap);