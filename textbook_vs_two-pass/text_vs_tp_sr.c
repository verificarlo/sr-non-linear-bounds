#include <assert.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define real float

// initialize arrays with random floating-points between 1024 and 1025
real *random_array(long n) {
  real *A = malloc(n * sizeof(real));
  for (int i = 0; i < n; i++) {
    A[i] = ( ((float)rand() / (float)RAND_MAX)) + 1024 ;
  }
  return A;
}

// compute the textbook and two-pass. This function will be instrumented with
// verificarlo mca-int backend.
__attribute__((noinline)) void text_vs_tp_sr(long n, real *U) {
  // textbook
  real text_res = 0.0;
  real sum = 0.0;
  real sum_square = 0.0;
  for (int i = 0; i < n; i++) {
    sum_square += U[i] * U[i];
    sum += U[i];
  }
  real s = sum * sum;
  text_res = sum_square - (s / n);
  
  // two-pass
  real tp_res = 0.0;
  real mean = sum / n;
  for (int i = 0; i < n; i++) {
    tp_res += (U[i] - mean) * (U[i] - mean);
  }
  printf("%.17f %.17f\n", text_res, tp_res);
}

int main(int argc, char *argv[]) {
  // seed RNG with fixed seed 0
  srand(0);
  assert(argc == 3);
  long n = strtol(argv[1], NULL, 10);
  long repetitions = strtol(argv[2], NULL, 10);
  real res;
  real *U = random_array(n);

  // errors are computed against a reference value
  // computed in quadruple precision (float128)
  __float128 sum_r = 0.0;
  __float128 sum_square_r = 0.0;
  __float128 norm = 0.0;
  for (int i = 0; i < n; i++) {
    __float128 u = U[i];
    sum_square_r += u * u;
    sum_r += u;
  }
  //textbook
  __float128 s_r = sum_r * sum_r;
  __float128 text_res = sum_square_r - (s_r / n);
  // two-pass
  __float128 tp_res = 0.0;
  __float128 mean = sum_r / n;
  for (int i = 0; i < n; i++) {
    __float128 u = U[i];
    tp_res += (u - mean) * (u - mean);
  }
  printf("%.17lf  %.17lf\n", (double)text_res, (double)tp_res);

  for (int r = 0; r < repetitions; r++) {
    text_vs_tp_sr(n, U);
  }

  free(U);
  return (0);
}