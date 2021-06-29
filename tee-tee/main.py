import sys
import math
from typing import List, Optional

from pydantic import BaseModel


class LogicalOperator(BaseModel):
    representation: str


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
        left = f"{self.left}" if isinstance(self.left, Variable) else f"({self.left})"
        right = (
            f"{self.right}" if isinstance(self.right, Variable) else f"({self.right})"
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


def find_equation(tt_output) -> LogicalOperator:
    """
    Given a truth tables resolution, determines
    the general function for the truth table.
    """
    num_variables = math.log(len(tt_output), 2)
    if not num_variables.is_integer():
        raise Exception("Truth table length is not a log of 2")

    num_variables = int(num_variables)
    variables = [chr(65 + i) for i in range(num_variables)]
    tt = generate_tt(num_variables)
    func: LogicalOperator = Or()
    for idx, result in enumerate(tt_output):
        row = tt[idx]
        if result:
            operand = And()
            for variable, variable_result in zip(variables, row):
                variable = Variable(representation=variable)
                if not variable_result:
                    variable = Not(operand=variable)
                operand += variable
            func += operand

    return func


def main():
    tt_output = [x == "1" for x in list(sys.argv[1])]
    print(find_equation(tt_output))


if __name__ == "__main__":
    main()
