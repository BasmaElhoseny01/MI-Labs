from typing import Tuple
import re
from CSP import Assignment, Problem, UnaryConstraint, BinaryConstraint

#TODO (Optional): Import any builtin library or define any helper function you want to use

# This is a class to define for cryptarithmetic puzzles as CSPs
class CryptArithmeticProblem(Problem):
    LHS: Tuple[str, str]
    RHS: str

    # Convert an assignment into a string (so that is can be printed).
    def format_assignment(self, assignment: Assignment) -> str:
        LHS0, LHS1 = self.LHS
        RHS = self.RHS
        letters = set(LHS0 + LHS1 + RHS)
        formula = f"{LHS0} + {LHS1} = {RHS}"
        postfix = []
        valid_values = list(range(10))
        for letter in letters:
            value = assignment.get(letter)
            if value is None: continue
            if value not in valid_values:
                postfix.append(f"{letter}={value}")
            else:
                formula = formula.replace(letter, str(value))
        if postfix:
            formula = formula + " (" + ", ".join(postfix) +  ")" 
        return formula

    @staticmethod
    def from_text(text: str) -> 'CryptArithmeticProblem':
        # Given a text in the format "LHS0 + LHS1 = RHS", the following regex
        # matches and extracts LHS0, LHS1 & RHS
        # For example, it would parse "SEND + MORE = MONEY" and extract the
        # terms such that LHS0 = "SEND", LHS1 = "MORE" and RHS = "MONEY"
        pattern = r"\s*([a-zA-Z]+)\s*\+\s*([a-zA-Z]+)\s*=\s*([a-zA-Z]+)\s*"
        match = re.match(pattern, text)
        if not match: raise Exception("Failed to parse:" + text)
        LHS0, LHS1, RHS = [match.group(i+1).upper() for i in range(3)]

        problem = CryptArithmeticProblem()
        problem.LHS = (LHS0, LHS1)
        problem.RHS = RHS

        #TODO Edit and complete the rest of this function
        # problem.variables:    should contain a list of variables where each variable is string (the variable name)
        # problem.domains:      should be dictionary that maps each variable (str) to its domain (set of values)
        #                       For the letters, the domain can only contain integers in the range [0,9].
        # problem.constaints:   should contain a list of constraint (either unary or binary constraints).


        # not_equal_condition is a lambda function that takes two parameters a and b and checks if they are not equal. 
        not_equal_condition = lambda a, b: a != b

        # unary_not_equal_condition is a lambda function that takes one parameter f. It returns another lambda function that takes a parameter v and checks if v is not equal to f.
        unary_not_equal_condition = lambda f: (lambda v: v != f)

        print("from_text()")
        print(text)
        print( problem.LHS )
        print( problem.RHS )


        # Getting Variables
        operand_1=problem.LHS[0]
        operand_2=problem.LHS[1]
        sum=problem.RHS
        problem.variables=list(set(operand_1) | set(operand_2) | set(sum))

        # Getting Domains
        problem.domains = {}
        for letter in problem.variables:
            problem.domains[letter]=set(range(0,10))

        # Constraints
        problem.constraints=[]

        # Unary Constraints
        # First Digit can't be set to Zero
        problem.constraints.append(UnaryConstraint(operand_1[0], unary_not_equal_condition(0)))
        problem.constraints.append(UnaryConstraint(operand_2[0], unary_not_equal_condition(0)))
        problem.constraints.append(UnaryConstraint(sum[0], unary_not_equal_condition(0)))

        # Different All diff Not Equal
        for index,variable in enumerate(problem.variables):
            problem.constraints.extend(BinaryConstraint((variable, other), not_equal_condition) for other in problem.variables [index+1:])

        # Summation constraint
        # operand_1[-1]+operand_2[-1]
        # Lambda Expression that takes 2 Variables and check if the second one is the first right digit in the first parameter
        first_digit_condition = lambda ab, a: ab[0] == str(a)
        second_digit_condition = lambda ab, b: ab[1:] == str(b)
        digit_sum_condition = lambda ab, cd: int(ab[1])+int(ab[0]) == int(cd[1])+int(cd[0])


        # O+O=T+C1

        # G,T->GT  [2 binary]
        # U,C2->UC2 [2 binary]
        # sum(GT)=sum(UC2)  1 binary
        # TODO Handel no equal size
        for i in range(1,min(len(LHS0),len(LHS1))+1):
            # New Variable to be added in the Domain
            LSH_var=LHS0[-1*i]+LHS1[-1*i]
            RSH_var=RHS[-1*i]+f"C{i}"
            problem.variables.append(LSH_var) #GT
            
            problem.variables.append(f"C{i}")
            problem.variables.append(RSH_var) #UC2

            # Domains for new Variables
            problem.domains[LSH_var]=set([f"{a}{b}" for a in range(10) for b in range(10)])
            problem.domains[f"C{i}"]=set([0,1])
            problem.domains[RSH_var]=set([f"{a}{b}" for a in range(10) for b in range(2)])


            # Add Constraints
            problem.constraints.append(BinaryConstraint((LSH_var, LHS0[-1*i]), first_digit_condition))
            problem.constraints.append(BinaryConstraint((LSH_var, LHS1[-1*i]), second_digit_condition))
            
            problem.constraints.append(BinaryConstraint((RSH_var, RHS[-1*i]), first_digit_condition))
            problem.constraints.append(BinaryConstraint((RSH_var, f"C{i}"), second_digit_condition))

            problem.constraints.append(BinaryConstraint((LSH_var, RSH_var), digit_sum_condition))

        print(problem.variables)
        print(problem.domains)

        



        # problem.variables = []
        # problem.domains = {}
        # problem.constraints = []
        return problem

    # Read a cryptarithmetic puzzle from a file
    @staticmethod
    def from_file(path: str) -> "CryptArithmeticProblem":
        with open(path, 'r') as f:
            return CryptArithmeticProblem.from_text(f.read())