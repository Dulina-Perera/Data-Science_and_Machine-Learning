#include <stdio.h>
#include <stdlib.h>
#include <time.h>

float train[][2] = {
    {0, 0},
    {1, 2},
    {2, 4},
    {3, 6},
    {4, 8},
};
#define train_len (sizeof(train) / sizeof(train[0]))

float rand_float(void) {
    return (float) rand() / (float) RAND_MAX;
}

float mse(float w) {
    float err = 0.0f;
    for (size_t i = 0; i < train_len; ++i) {
        float y = train[i][0] * w;
        float d = y - train[i][1];
        err += d*d;
    }
    err /= train_len;
    return err;
}

int main() {
    // srand(time(0));
    srand(69);
    float w = rand_float() * 10.0f;
    printf("Mean Squared Error: %f\n", mse(w));
    
    return 0;
}
