#include <stdio.h>
#include <string.h>
#include <stdbool.h>

#define ARRAY_SIZE 256

typedef struct {
    int array[ARRAY_SIZE];
} CustomObject;

// Function to populate the array based on a string of comma-separated values
void populateArray(CustomObject *obj, const char *values) {
    char *token;
    int i = 0;

    // Tokenize the input string based on comma as delimiter
    token = strtok(values, ",");
    while (token != NULL && i < ARRAY_SIZE) {
        // Convert token to integer and store in array
        obj->array[i++] = atoi(token);
        token = strtok(NULL, ",");
    }
}

// Function to check if two objects are equal
bool isEqual(CustomObject *obj1, CustomObject *obj2) {
    for (int i = 0; i < ARRAY_SIZE; i++) {
        if (obj1->array[i] != obj2->array[i]) {
            return false;
        }
    }
    return true;
}

// Function to check if a value at a position is equal to the value at that position in the object
bool isEqualToValueAtPosition(CustomObject *obj, int value, int position) {
    return obj->array[position] == value;
}

int main() {
    // Example usage
    CustomObject obj1, obj2;
    const char *values = "1,2,3,4,5";

    populateArray(&obj1, values);
    populateArray(&obj2, values);

    if (isEqual(&obj1, &obj2)) {
        printf("Objects are equal\n");
    } else {
        printf("Objects are not equal\n");
    }

    // Check if value at position 2 in obj1 is equal to 3
    if (isEqualToValueAtPosition(&obj1, 3, 2)) {
        printf("Value at position 2 in obj1 is equal to 3\n");
    } else {
        printf("Value at position 2 in obj1 is not equal to 3\n");
    }

    return 0;
}
