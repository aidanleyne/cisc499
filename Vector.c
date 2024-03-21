#include <stdio.h>
#include <string.h>
#include <stdbool.h>

#define ARRAY_SIZE 256

typedef struct {
    int array[ARRAY_SIZE];
    char name[128];
} Vector;

// Function to populate the array based on a string of comma-separated values
void populate(Vector *obj, const char *values) {
    char *token;
    int i = 0;

    // Tokenize the input string based on comma as delimiter
    token = strtok(values, ",");
    while (token != NULL && i < ARRAY_SIZE) {
        // Convert token to integer and store in array
        obj->array[i++] = strtokl(token);
        token = strtok(NULL, ",");
    }
}

// Function to check if two objects are equal
bool isEqual(Vector *vec1, Vector *vec2) {
    for (int i = 0; i < ARRAY_SIZE; i++) {
        if (vec1->array[i] != vec2->array[i]) {
            return false;
        }
    }
    return true;
}

// Function to check if a value at a position is equal to the value at that position in the object
bool compare(Vector *vec, int value, int position) {
    // bounds checking
    if (position < 0 || position >= ARRAY_SIZE) {
        printf("Position out of bounds.\n");
        return false;
    }

    return vec->array[position] == value;
}

// Function to print the vector's contents along with it's name
void printVector(Vector *vec) {
    printf("%s : ", vec->name);
    for (int i = 0; i < ARRAY_SIZE-1; i++) {
        printf("%d, ", vec->array[i]);
    }
    printf("%d\n", vec->array[ARRAY_SIZE-1]);
}

int main() {
    Vector obj1, obj2;
    const char *values = "1,2,3,4,5";

    populate(&obj1, values);
    populate(&obj2, values);

    if (isEqual(&obj1, &obj2)) {
        printf("Objects are equal\n");
    } else {
        printf("Objects are not equal\n");
    }

    // Check if value at position 2 in obj1 is equal to 3
    if (compare(&obj1, 3, 2)) {
        printf("Value at position 2 in obj1 is equal to 3\n");
    } else {
        printf("Value at position 2 in obj1 is not equal to 3\n");
    }

    return 0;
}
