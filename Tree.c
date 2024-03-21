#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <math.h>
#include <float.h>
#include "Vector.h"

#define DIMENSION 256

// Structure to represent a vector node
typedef struct VectorNode {
    int id;
    Vector *vector;
    struct VectorNode *left, *right;
} VectorNode;

// Function to allocate memory for a new vector node
VectorNode* newNode(int id, int *vector) {
    VectorNode* node = (VectorNode*)malloc(sizeof(VectorNode));
    node->id = id;
    node->vector = vector;
    node->left = node->right = NULL;
    return node;
}

// Function to calculate distance between two vectors
double distance(int *a, int *b) {
    double dist = 0;
    for (int i = 0; i < DIMENSION; i++) {
        dist += pow(a[i] - b[i], 2);
    }
    return sqrt(dist);
}

// Function to compare vectors at a given dimension
int compare(VectorNode* a, VectorNode* b, int t) {
    return (a->vector[t] < b->vector[t]) ? -1 : 1;
}

// Function to insert a vector into the KD-tree
VectorNode* insert(VectorNode* root, int id, int *vector, int depth) {
    if (root == NULL) return newNode(id, vector);

    int currentDimension = depth % DIMENSION;

    // Compare the vector at the current dimension
    if (compare(root, newNode(id, vector), currentDimension) < 0)
        root->left = insert(root->left, id, vector, depth + 1);
    else
        root->right = insert(root->right, id, vector, depth + 1);

    return root;
}

// Function to search for nearest neighbor
void nearestNeighbor(VectorNode* root, int *query, VectorNode** nearest, double* minDist, int depth) {
    if (root == NULL) return;

    double dist = distance(root->vector, query);

    if (dist < *minDist) {
        *minDist = dist;
        *nearest = root;
    }

    int currentDimension = depth % DIMENSION;

    // Search the side of the splitting plane that contains the query point
    if (query[currentDimension] < root->vector[currentDimension])
        nearestNeighbor(root->left, query, nearest, minDist, depth + 1);
    else
        nearestNeighbor(root->right, query, nearest, minDist, depth + 1);

    // Search the other side of the splitting plane if needed
    if (pow(query[currentDimension] - root->vector[currentDimension], 2) < *minDist) {
        if (query[currentDimension] < root->vector[currentDimension])
            nearestNeighbor(root->right, query, nearest, minDist, depth + 1);
        else
            nearestNeighbor(root->left, query, nearest, minDist, depth + 1);
    }
}

int main() {    
    // Insert vectors into the KD-tree
    Vector vector1[DIMENSION] = {1, 2, 3, /*...*/, 255, 256};

    return 0;
}
