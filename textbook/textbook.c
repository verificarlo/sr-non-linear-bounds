#include <assert.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define real float

// initialize arrays with positive floating-points between 0 and 1
real *random_array(long n) {
  real *A = malloc(n * sizeof(real));
  for (int i = 0; i < n; i++) {
    A[i] =  ( ((float)rand() / (float)RAND_MAX));
  }
  return A;
}

// compute the textbook. This function will be instrumented with
// verificarlo mca-int backend.
__attribute__((noinline)) void textbook_sr(long n, real *U) {
  real res = 0.0;
  real sum = 0.0;
  real sum_square = 0.0;
  for (int i = 0; i < n; i++) {
    sum_square += U[i] * U[i];
    sum += U[i];
  }
  real s = sum * sum;
  res = sum_square - (s / n);
  printf("%.17f\n", res);
}

int main(int argc, char *argv[]) {
  // seed RNG with fixed seed 0
  srand(0);
  assert(argc == 3);
  long n = strtol(argv[1], NULL, 10);
  long repetitions = strtol(argv[2], NULL, 10);
  real res;
  real *U = random_array(n);

  // errors and condition numbers are computed against a reference value
  // computed in quadruple precision (float128)
  __float128 sum_r = 0.0;
  __float128 sum_square_r = 0.0;
  __float128 norm = 0.0;
  for (int i = 0; i < n; i++) {
    __float128 u = U[i];
    sum_square_r += u * u;
    sum_r += u;
    norm += fabsl(u);
  }
  __float128 s_r = sum_r * sum_r;
  __float128 res_r = sum_square_r - (s_r / n);
  __float128 cond_1 = norm / sqrt(res_r * n);
  __float128 cond_2 = sqrt(sum_square_r) / sqrt(res_r);
  printf("%.17lf %.17lf %.17lf\n", (double)cond_1, (double)cond_2, (double)res_r);

  for (int r = 0; r < repetitions; r++) {
    textbook_sr(n, U);
  }

  free(U);
  return (0);
}
