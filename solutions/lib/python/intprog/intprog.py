"""
codemonkey@jleadbetter.com
License: AGPLv3
"""

class IPBase(object):
    """
    Stores a representation of an integer programming (IP) problem.
    
    An IP problem uses the following setup:
    
        Minimize (or Maximize): 1*x0 + 1*x1 + 1*x2
        such that: 1*x0 + 0*x2 + 3*x3 >= 12
                   0*x0 + 1*x2 + 0*x3 <= 6
                   2*x0 + 2*x2 + 0*x3 <= 10

    Let's also assume that we only want positive numbers.

    We can represent this problem in the following way:

        min = True
        equation = [1, 1, 1]
        constraints = [[1, 0, 3, GTE, 12],
                       [0, 1, 0, LTE, 6],
                       [2, 2, 0, LTE, 10]]
        ip = IP(min, equation, constraints, pos_only=True)

    NOTE: this class does not provide any solvers for an IP problem. The 
    solvers will be implemented in each of the project solutions.
    """

    GTE = 1    # greater than or equals
    EQ = 0     # equals
    LTE = -1   # less than or equals

    def __init__(self, min=True, equation=None, contraints=None, pos_only=True):
        """
        See documentation on the class for an example of using the init.

        :param min: Whether this is a minimization or a maximization problem
        :param equation: list of integers representing the coefficients in the
                equation to maximize
        :param constraints: list of lists. Each sub-list should be integers
            representing the coeffiecients for each constraint equation. Use
            one of the IP constants (EQ, GTE, LTE) to specify the
            type of equation. Lists must be of equal length.
        :param pos_only: Constrain solutions to positive integers only
        """
        self.min = min
        self.equation = equation or []
        self.constraints = constraints or []
        self.solution = []

    def check_constraint(self, solution, constraint_row):
        """
        Verifies that the proposed solution fits the constraint.

        :param solution: list of integers representing a possible solution
        :param constraint_row: integer index of which row in self.constraints
                should be checked against the solution
        :return: tuple (boolean, numeric) representing whether it passed the
                constraint and what the current value of the constraint is.

        :throws: IndexError - if constraint_row does not exist or 
                len(solution) <= len(constraint_row) - 2
        """
        equation, operator, result = self.parse_constraint(constraint_row)
        total = self.sum_of_products(solution, equation)
        return eval(total, result, operator), total

    def check_solution(self, solution):
        """
        Verifies that the proposed solution fits all constraints.

        :param solution: list of integers representing a possible solution
        :return: A tuple (boolean, numeric, list) - boolean indicating if the
                solution fits within the constraints, numeric value of the
                current solution, and a list of the results of check_constraint
                on each row
        """
        curr_value = self.sum_of_products(solution, self.equation)
        row_vals = [self.check_constraint(solution, row) for row in self.constraints]
        passed = bool(filter(lambda x: x[0], row_values))
        return passed, curr_value, row_vals

    @property
    def eval(self, left_side, right_side, comparison_operator=None):
        """
        Evaluates a comparison expression -- e.g. 3 >= 2

        :param left_side: value for the left-hand side of the comparison
        :param right_side: value for the right-hand side of the comparison
        :param comparison_operator: LTE, GTE, or EQ. Defaults to EQ.
        :return: boolean - true if the expression is true; false otherwise
        """
        if comparison_operator == self.GTE:
            return left_side >= right_side
        elif comparison_operator == self.LTE:
            return left_side <= right_side
        return left_side == right_side

    def parse_constraint(self, constraint_row):
        """
        Break a row in self.constraints into equation, operator, and result

        :param constraint_row: integer for the row in self.constraints
        :return: tuple (list, int, int) -- the list representing the equation,
                an int (EQ, GTE, LTE) for the comparison operator, and the
                right-hand value of the constraint equation

        :throws: IndexError - if constraint_row does not exist
        """
        row = self.constraints[constraint_row]
        return row[:-2], row[-2], row[-1]

    @property
    def sum_of_products(self, list1, list2):
        """
        Finds the sum of the products of two lists.

        :param list1: list of numeric values
        :param list2: list of numeric values
        :return: numeric

        :throws: IndexError if list1 and list2 are not the same length
        """
        if len(list1) != len(list2):
            # We're going to use zip later, which silently truncates the
            # longer array. Let's fail now, before we get bad results.
            raise IndexError("Solution and constraints must be of equal length")

        # multiply the solution and constraint, and then add to get a sum
        return sum(map(lambda x: x[0]*x[1], zip(list1, list2)))