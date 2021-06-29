import sys
import math
from typing import List


def generate_tt(num_variables: int) -> List[List[bool]]:
    """
    Generates a truth table for all boolean combinations
    of the possible variables.
    """
    tt = []
    # the binary representation of 2^num_variables
    # gives us all possibilities for the truth table
    # using this because it is compact and simple
    for i in range(int(math.pow(2, num_variables))):
        tt.append([x == "0" for x in list(f"{{0:0{num_variables}b}}".format(i))])
    return tt


def find_equation(tt_output) -> str:
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
    func = ""
    for idx, result in enumerate(tt_output):
        row = tt[idx]
        if result:
            func += "("
            for variable, variable_result in zip(variables, row):
                if not variable_result:
                    func += "NOT "
                func += variable + " ^ "
            func = func.rstrip("^ ")
            func += ") v "
    func = func.rstrip("v ")

    return func


def main():
    tt_output = [x == "1" for x in list(sys.argv[1])]
    print(find_equation(tt_output))


if __name__ == "__main__":
    main()
