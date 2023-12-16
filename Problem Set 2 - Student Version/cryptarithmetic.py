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

        #  unary_equal_condition is a lambda function that takes one parameter f. It returns another lambda function that takes a parameter v and checks if v is equal to f.
        unary_equal_condition = lambda f: (lambda v: v == f)

        # print("from_text()")
        # print(text)
        # print( problem.LHS )
        # print( problem.RHS )


        # Getting Variables
        operand_1=problem.LHS[0]
        operand_2=problem.LHS[1]
        sum=problem.RHS
        problem.variables=list(set(operand_1) | set(operand_2) | set(sum))

        # Getting Domains
        problem.domains = {}
        # print("Entering Loop(1)[Adding  Variables]...................")
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
        # print("Entering Loop(2) [all diff]...................")
        for index,variable in enumerate(problem.variables):
            problem.constraints.extend(BinaryConstraint((variable, other), not_equal_condition) for other in problem.variables [index+1:])


        ###########################################Carries#################################
        # Adding Carries Variable
        problem.variables.extend([f"C{i}" for i in range(max(len(LHS0),len(LHS1))+1)])


        # print("Entering Loop(3) [Adding Carries Var]...................")
        for i in range(max(len(LHS0),len(LHS1))+1):
            problem.domains[f"C{i}"]=set([0,1])

        # C0 is set to 0 :D No Carry in
        problem.constraints.append(UnaryConstraint('C0', unary_equal_condition(0)))


        ###################################Addition Constraints#################

        # Summation constraint
        # operand_1[-1]+operand_2[-1]
        # Lambda Expression that takes 2 Variables and check if the second one is the first right digit in the first parameter
        first_digit_condition_3= lambda abc, a: abc[0] == str(a)
        second_digit_condition_3= lambda abc, b: abc[1] == str(b)
        third_digit_condition_3= lambda abc, c: abc[2] == str(c)

        first_digit_condition = lambda ab, a: ab[0] == str(a)
        
        first_2_digit_condition = lambda abc, ab: abc[0:2] == str(ab)

        second_digit_condition = lambda ab, b: ab[-1] == str(b)

        digits_3_sum_condition = lambda abc, sum: (int(abc[2])+int(abc[1])+int(abc[0])) % 10 == sum
        digits_3_carry_condition = lambda abc, carry: ((int(abc[2])+int(abc[1])+int(abc[0]))-(int(abc[2])+int(abc[1])+int(abc[0])) % 10)//10 == carry

        # A+B+C0=C+C1

        # A,B->AB  [2 binary]  **************************** NO NEED FOR THIS :D it gives me time limit just define 1 variable ABC0 with 3 Binary constrains ****************
        # AB,C0->ABC0 [2 binary]
        
        # sum(ABC0) mod 10 = C  (sum)[1 binary]
        # sum(ABC0)- [sum(ABC0) mod 10] = C1  (carry)[1 binary]

        # 12 % 10 = 2  -> sum
        # 12 % 10  = 2  12-2 =10 /10=1  C
        # 14 % 10  = 4  14-4 =10 /10=1 C

        # 8 % 10 =8 ==>sum
        # 8 % 10  = 8  8-8 =0 /10=0  C

        # TODO Handle not equal size
        # print("Entering Loop(4) [Constraints 1 ].........")
        for i in range(1,min(len(LHS0),len(LHS1))+1):
            # New Variable to be added in the Domain
            LSH_var=LHS0[-1*i]+LHS1[-1*i]

            # problem.variables.append(LSH_var) # AB
            problem.variables.append(LSH_var+f"C{i-1}") # ABC0


            # # Domains for new Variables
            # if(LSH_var[0]!=LSH_var[1]):
            #     problem.domains[LSH_var]=set([f"{a}{b}" for a in range(10) for b in range(10) if a!=b]) #AB
            # else:
            #     problem.domains[LSH_var]=set([f"{a}{b}" for a in range(10) for b in range(10) if a==b]) #AB
            
            problem.domains[LSH_var+f"C{i-1}"]=set([f"{a}{b}{c}" for a in range(10) for b in range(10) for c in range(2)]) # ABC0


            # Add Constraints
            # problem.constraints.append(BinaryConstraint((LSH_var, LHS0[-1*i]), first_digit_condition)) #AB
            # problem.constraints.append(BinaryConstraint((LSH_var, LHS1[-1*i]), second_digit_condition)) #AB
    

            problem.constraints.append(BinaryConstraint((LSH_var+f"C{i-1}", LHS0[-1*i]), first_digit_condition_3)) # ABC0
            problem.constraints.append(BinaryConstraint((LSH_var+f"C{i-1}", LHS1[-1*i]), second_digit_condition_3)) # ABC0
            problem.constraints.append(BinaryConstraint((LSH_var+f"C{i-1}", f"C{i-1}"), third_digit_condition_3)) # ABC0


            problem.constraints.append(BinaryConstraint((LSH_var+f"C{i-1}", RHS[-1*i]), digits_3_sum_condition)) # A+B+C0 %10=C
            problem.constraints.append(BinaryConstraint((LSH_var+f"C{i-1}", f"C{i}"), digits_3_carry_condition)) # A+B+C0 -(A+B+C0)%10=C1



        digits_2_sum_condition = lambda ab, sum: (int(ab[1])+int(ab[0])) % 10 == sum
        digits_2_carry_condition = lambda ab, carry: ((int(ab[1])+int(ab[0]))-(int(ab[1])+int(ab[0])) % 10)//10 == carry

        # # Case Not equal size
        if(len(LHS0)!=len(LHS1)):
            LHS_big= LHS0 if  len(LHS0)>len(LHS1) else LHS1
            #  A
            # BC
            # DE
            # B, C1 -->BC1 [2 binary]  
            # sum(BC1) mod 10 = D  (sum)[1 binary]
            # sum(BC1)- [sum(BC1) mod 10] = C2  (carry)[1 binary]

            start_index = min(len(LHS0), len(LHS1))
            end_index = max(len(LHS0), len(LHS1))
            # print("Entering Loop(5) [Constraints 2 ].........")
            # print("start_index",start_index,"end_index",end_index)
            for i in range(start_index,end_index):
                # Add new Variable
                # print(LHS1[-i-1]+f"C{i}")
                problem.variables.append(LHS_big[-i-1]+f"C{i}") # BC1

                # Domains for new Variables
                problem.domains[LHS_big[-i-1]+f"C{i}"]=set([f"{a}{b}" for a in range(10) for b in range(2)]) # BC1
           

                # Add Constraints
                problem.constraints.append(BinaryConstraint((LHS_big[-i-1]+f"C{i}", LHS_big[-i-1]), first_digit_condition)) # BC1
                problem.constraints.append(BinaryConstraint((LHS_big[-i-1]+f"C{i}",f"C{i}"), second_digit_condition)) # BC1

                problem.constraints.append(BinaryConstraint((LHS_big[-i-1]+f"C{i}", RHS[-i-1]), digits_2_sum_condition)) # sum(BC1) mod 10 = D sum
                problem.constraints.append(BinaryConstraint((LHS_big[-i-1]+f"C{i}", f"C{i+1}"), digits_2_carry_condition)) #  sum(BC1)- [sum(BC1) mod 10] = C2  (carry)[1 binary]
        
        # A+B=CD
        if(len(RHS)>max(len(LHS0),len(LHS1))):
            max_len_LHS=max(len(LHS0),len(LHS1))
            # Unary both = 1
            problem.constraints.append(UnaryConstraint(RHS[0], unary_equal_condition(1)))
            problem.constraints.append(UnaryConstraint(f"C{max_len_LHS}", unary_equal_condition(1)))

            # Or it can be 1 binary that they are equal
            # equal_condition = lambda a, b: a == b
            # problem.constraints.append(BinaryConstraint((RHS[0],f"C{max_len_LHS}"), equal_condition)) #  C=C1
   




        # problem.variables = []
        # problem.domains = {}
        # problem.constraints = []

        # print(problem.variables)
        # print(problem.domains)]
        # print("end....")
        return problem

    # Read a cryptarithmetic puzzle from a file
    @staticmethod
    def from_file(path: str) -> "CryptArithmeticProblem":
        with open(path, 'r') as f:
            return CryptArithmeticProblem.from_text(f.read())