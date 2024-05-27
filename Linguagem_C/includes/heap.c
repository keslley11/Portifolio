#include <stdio.h>
#include <stdlib.h>
#include "heap.h"

/*
Árvore Binária de Heap (fila de prioridade - acesso rapido ao maior , ou menor):

    Existem dois tipos principais de heaps: heap máximo, onde
    cada nó pai tem um valor maior ou igual ao valor de seus filhos,
    e heap mínimo, onde cada nó pai tem um valor menor ou igual ao valor de seus filhos.
    (heap mínimo neste caso)
*/

MinHeap *createMinHeap(int capacity)
{
    MinHeap *minHeap = (MinHeap *)malloc(sizeof(MinHeap));
    minHeap->capacity = capacity;
    minHeap->size = 0;
    minHeap->array = (int *)malloc(capacity * sizeof(int));
    return minHeap;
}

void swap(int *a, int *b)
{
    int temp = *a;
    *a = *b;
    *b = temp;
}

void minHeapify(MinHeap *minHeap, int index)
{
    int smallest = index;
    int left = 2 * index + 1;
    int right = 2 * index + 2;

    if (left < minHeap->size && minHeap->array[left] < minHeap->array[smallest])
        smallest = left;

    if (right < minHeap->size && minHeap->array[right] < minHeap->array[smallest])
        smallest = right;

    if (smallest != index)
    {
        swap(&minHeap->array[index], &minHeap->array[smallest]);
        minHeapify(minHeap, smallest);
    }
}

void insert(MinHeap *minHeap, int value)
{
    if (minHeap->size == minHeap->capacity)
    {
        printf("Heap esta cheia. Nao e possivel inserir mais elementos.\n");
        return;
    }

    int index = minHeap->size++;
    minHeap->array[index] = value;

    while (index != 0 && minHeap->array[(index - 1) / 2] > minHeap->array[index])
    {
        swap(&minHeap->array[index], &minHeap->array[(index - 1) / 2]);
        index = (index - 1) / 2;
    }
}

int extractMin(MinHeap *minHeap)
{
    if (minHeap->size <= 0)
        return -1;

    if (minHeap->size == 1)
    {
        minHeap->size--;
        return minHeap->array[0];
    }

    int root = minHeap->array[0];
    minHeap->array[0] = minHeap->array[minHeap->size - 1];
    minHeap->size--;
    minHeapify(minHeap, 0);

    return root;
}

void printMinHeap(MinHeap *minHeap)
{
    printf("Min Heap: ");
    for (int i = 0; i < minHeap->size; ++i)
        printf("%d ", minHeap->array[i]);
    printf("\n");
}

void destroyMinHeap(MinHeap *minHeap)
{
    free(minHeap->array);
    free(minHeap);
}