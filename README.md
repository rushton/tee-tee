# tee-tee

tee-tee, phonetic acronym for "truth table", is a utility to aid with boolean logic.

# Usage

```shell
tt [truth_table_output] 
```

# Example

Imagine we want to find the boolean expression for the following truth table:

```
+---+---+--------+
| A | B | f(A,B) |
+---+---+--------+
| 1 | 1 |      1 |
| 1 | 0 |      0 |
| 0 | 1 |      0 |
| 0 | 0 |      0 |
+---+---+--------+
```

We have two variables `A` and `B` and the output of the unknown boolean function. Input the output of the truth table into tt to get the boolean expression which represents it:

```
#> tt 1000
A ^ B
```

We get the answer of `A ^ B` (A AND B) which properly represents the truth table.


# Symbols

tt uses logical symbols to represent boolean expressions, these are their meaning:  

`^` - AND
`v` - OR
`¬` - NOT
