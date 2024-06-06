# tee-tee

tee-tee, phonetic acronym for "truth table", is a utility to aid with boolean logic.

# Usage

### Generate boolean expression for truth table output
```shell
tt boolean-expression [truth-table-output]
```

### Generate truth table for variables
```shell
tt truth-table <num-variables>
```

### Generate truth table for variables in csv format
```shell
tt truth-table --csv-format <num-variables>
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
#> tt truth-table 1000
A ^ B
```

We get the answer of `A ^ B` (A AND B) which properly represents the truth table.


# Symbols

tt uses logical symbols to represent boolean expressions, these are their meaning:  

`^` - AND  
`v` - OR  
`¬` - NOT  
