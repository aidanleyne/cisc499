// Vector.h

#ifndef Vector_H
#define Vector_H

#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#define ARRAY_SIZE 256

typedef struct {
    int array[ARRAY_SIZE];
} Vector;

void populate(Vector *vec, const char *values);
int isEqual(Vector *vec1, Vector *vec2);
int compare(Vector *vec, int value, int position);
void printVector(Vector *vec);

#endif // Vector_H
