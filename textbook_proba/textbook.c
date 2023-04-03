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
    A[i] = ( ((float)rand() / (float)RAND_MAX));
  }
  return A;
}

// compute the condition numbers of the textbook. 
int main(int argc, char *argv[]) {
  // seed RNG with fixed seed 0
  srand(0);
  assert(argc == 2);
  long n = strtol(argv[1], NULL, 10);
  real res;
  real *U = random_array(n);

  // the condition numbers are computed in quadruple precision (float128)
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
  printf("%.17lf %.17lf\n", (double)cond_1, (double)cond_2);

  free(U);
  return (0);
}
