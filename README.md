# sr-non-linear-bounds

Scripts to reproduce the numerical experiments of the paper ["Bounds on Non-linear Errors for Variance Computation with Stochastic Rounding"](https://hal.science/hal-04056057).

Before running the scripts, ensure that you have installed [Verificarlo v0.8.0](https://github.com/verificarlo/verificarlo/releases/tag/v0.8.0), Python 3, and matplotlib on your computer.


## Textbook algorithm

To reproduce textbook algorithm experiments use the following commands:


```bash
# To generate figure 3 with 1 - lambda = 0.9 (left)

sr-non-linear-bounds$ cd textbook

# The generated plot is a pdf file named textbook-n.pdf
sr-non-linear-bounds/textbook$ verificarlo-c -O2 --function=textbook_sr ./textbook.c -o textbook -lm
sr-non-linear-bounds/textbook$ ./run-and-plot_over_n.py

# To generate figure 3 with n= 10^6 (right)

sr-non-linear-bounds$ cd textbook_proba

# The generated plot is a pdf file named textbook-p.pdf
sr-non-linear-bounds/textbook$ gcc ./textbook.c -o textbook -lm
sr-non-linear-bounds/textbook$ ./run-and-plot_over_n.py
```

## textbook against two-pass

To reproduce the experiments of textbook algorithm against two-pass algorithm use the following commands:

```bash
sr-non-linear-bounds$ cd textbook_vs_two-pass

# To generate figure 4 (left)
# The generated plot is a pdf file named text-vs-tp.pdf
sr-non-linear-bounds/textbook_vs_two-pass$ verificarlo-c -O2 --function=text_vs_tp_sr ./text_vs_tp_sr.c -o text_vs_tp_sr -lm
sr-non-linear-bounds/textbook_vs_two-pass$ text-tp.py

# To generate figure 4 (right)
# First, modify the random_array function in the text_vs_tp_sr.c file to generate random values between 1024 and 1025.
# The generated plot is a pdf file named text-vs-tp.pdf
sr-non-linear-bounds/textbook_vs_two-pass$ verificarlo-c -O2 --function=text_vs_tp_sr ./text_vs_tp_sr.c -o text_vs_tp_sr -lm
sr-non-linear-bounds/textbook_vs_two-pass$ text-tp.py
