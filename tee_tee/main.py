import sys
import math
from typing import List, Optional
import string

from pydantic import BaseModel
from quine_mccluskey.qm import QuineMcCluskey
import typer
from rich.console import Console
from rich.table import Table


app = typer.Typer()
console = Console()


class LogicalOperator(BaseModel):
    representation: str

    def __add__(self, operand: "LogicalOperator"):
        return self


class BinaryOperator(LogicalOperator):
    left: Optional[LogicalOperator]
    right: Optional[LogicalOperator]

    def __add__(self, operand: LogicalOperator):
        if not self.left:
            return self.__class__(left=operand)
        if not self.right:
            return self.__class__(left=self.left, right=operand)
        return self.__class__(left=self, right=operand)

    def __str__(self):
        if not self.left and not self.right:
            return ""
        if not self.left:
            return str(self.right)
        if not self.right:
            return str(self.left)
        else:
            left = (
                f"{self.left}" if isinstance(self.left, Variable) else f"({self.left})"
            )
            right = (
                f"{self.right}"
                if isinstance(self.right, Variable)
                else f"({self.right})"
            )
            return f"{left} {self.representation} {right}"


class And(BinaryOperator):
    representation: str = "^"


class Or(BinaryOperator):
    representation: str = "v"


class Not(LogicalOperator):
    representation: str = "¬"
    operand: LogicalOperator

    def __str__(self):
        if isinstance(self.operand, Variable):
            return f"{self.representation}{self.operand}"
        else:
            return f"{self.representation}({self.operand})"


class Variable(LogicalOperator):
    representation: str

    def __str__(self):
        return self.representation


def find_equation(tt_output: List[str]) -> LogicalOperator:
    """
    Given a truth tables resolution, determines
    the general function for the truth table.
    """
    num_variables = max(1.0, math.log(len(tt_output), 2))
    if not num_variables.is_integer():
        raise Exception("Truth table length is not a log of 2")

    num_variables = int(num_variables)
    variables = [chr(65 + i) for i in range(num_variables)]
    tt = generate_tt(num_variables)
    func: LogicalOperator = Or()
    qm = QuineMcCluskey()
    ones = [idx for idx, o in enumerate(tt_output) if o == "1"]
    dont_cares = [idx for idx, o in enumerate(tt_output) if o == "-"]

    prime_implicants = qm.simplify(ones, dc=dont_cares, num_bits=num_variables)
    if not prime_implicants:
        raise Exception("Boolean expression not possible for this truth table")

    for prime_implicant in prime_implicants:
        node = And()
        for idx, variable in enumerate(prime_implicant):
            if variable == "0":
                node += Not(operand=Variable(representation=variables[idx]))
            if variable == "1":
                node += Variable(representation=variables[idx])
        func += node

    return func


def generate_tt(num_variables: int) -> List[List[bool]]:
    """
    Generates a truth table for all boolean combinations
    of the possible variables.
    """
    tt = []
    # the binary representation of each number in the
    # range 0..(2^num_variables) gives us all
    # possibilities for the truth table
    # using this because it is compact and simple
    for i in range(int(math.pow(2, num_variables))):
        tt.append([x == "0" for x in list(f"{{0:0{num_variables}b}}".format(i))])
    return tt


@app.command()
def truth_table(num_variables: int, csv_format: bool = False):
    variables = [string.ascii_uppercase[i] for i in range(num_variables)]
    tt = generate_tt(num_variables)
    if not csv_format:
        table = Table(*variables)
        for row in tt:
            table.add_row(*[str(1 if cell else 0) for cell in row])
        console.print(table)
    else:
        print(",".join(variables))
        for row in tt:
            print(",".join([str(1 if cell else 0) for cell in row]))


@app.command()
def boolean_expression(truth_table: str):
    try:
        typer.echo(find_equation(list(reversed(truth_table))))
    except Exception as e:
        typer.echo(f"ERROR: {e}")
        typer.Exit(1)


if __name__ == "__main__":
    app()
