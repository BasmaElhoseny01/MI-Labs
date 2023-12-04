from typing import Any, Dict, List, Optional
from CSP import Assignment, BinaryConstraint, Problem, UnaryConstraint
from helpers.utils import NotImplemented
import sys
import heapq
import copy
from queue import PriorityQueue

# This function applies 1-Consistency to the problem.
# In other words, it modifies the domains to only include values that satisfy their variables' unary constraints.
# Then all unary constraints are removed from the problem (they are no longer needed).
# The function returns False if any domain becomes empty. Otherwise, it returns True.
def one_consistency(problem: Problem) -> bool:
    remaining_constraints = []
    solvable = True
    for constraint in problem.constraints:
        if not isinstance(constraint, UnaryConstraint):
            remaining_constraints.append(constraint)
            continue
        variable = constraint.variable
        new_domain = {value for value in problem.domains[variable] if constraint.condition(value)}
        if not new_domain:
            solvable = False
        problem.domains[variable] = new_domain
    problem.constraints = remaining_constraints
    return solvable

# This function returns the variable that should be picked based on the MRV heuristic.
# NOTE: We don't use the domains inside the problem, we use the ones given by the "domains" argument 
#       since they contain the current domains of unassigned variables only.
# NOTE: If multiple variables have the same priority given the MRV heuristic, 
#       we order them in the same order in which they appear in "problem.variables".
def minimum_remaining_values(problem: Problem, domains: Dict[str, set]) -> str:
    _, _, variable = min((len(domains[variable]), index, variable) for index, variable in enumerate(problem.variables) if variable in domains)
    return variable

# This function should implement forward checking
# The function is given the problem, the variable that has been assigned and its assigned value and the domains of the unassigned values
# The function should return False if it is impossible to solve the problem after the given assignment, and True otherwise.
# In general, the function should do the following:
#   - For each binary constraints that involve the assigned variable:
#       - Get the other involved variable.
#       - If the other variable has no domain (in other words, it is already assigned), skip this constraint.
#       - Update the other variable's domain to only include the values that satisfy the binary constraint with the assigned variable.
#   - If any variable's domain becomes empty, return False. Otherwise, return True.
# IMPORTANT: Don't use the domains inside the problem, use and modify the ones given by the "domains" argument 
#            since they contain the current domains of unassigned variables only.
def forward_checking(problem: Problem, assigned_variable: str, assigned_value: Any, domains: Dict[str, set]) -> bool:
    #TODO: Write this function
    # print("forward_checking()")

    # The Constraints here of course aren't unary they are binary :D
    # Loop over all constraints
    for constraint in problem.constraints:
        # The Variables of the binary constraint
        constraint_variables=constraint.variables

        # If this constraint doesn't have the assigned_variable then nothing to be done bec we are implementing forward checking
        if assigned_variable not in constraint_variables: continue

        # So Here we have a Binary Constraint that involves the assigned_variable
        # Getting the other variable 
        index_of_variable = constraint_variables.index(assigned_variable)
        other_variable=constraint_variables[1 - index_of_variable]

        # Check if the other variable is in the Domain dictionary else it is assigned before
        if other_variable not in domains.keys(): continue  #assigned before

        # Update other variable's domain
        other_variable_domain=domains[other_variable]
        other_variable_domain.discard(assigned_value)

        # Check if empty Set(this variable has no domain)
        if( not other_variable_domain):
            return False
        

        
    # All unassigned variables will still have domain after this value assigned to the variable
    return True
    NotImplemented()


from functools import cmp_to_key

def custom_comparison(x, y):
    # Compare by priority first
    priority_diff = x[0] - y[0]
    if priority_diff != 0:
        return priority_diff
    
    # If priorities are equal, compare by value
    return x[1] - y[1]


# This function should return the domain of the given variable order based on the "least restraining value" heuristic.
# IMPORTANT: This function should not modify any of the given arguments.
# Generally, this function is very similar to the forward checking function, but it differs as follows:
#   - You are not given a value for the given variable, since you should do the process for every value in the variable's
#     domain to see how much it will restrain the neighbors domain
#   - Here, you do not modify the given domains. But you can create and modify a copy.
# IMPORTANT: If multiple values have the same priority given the "least restraining value" heuristic, 
#            order them in ascending order (from the lowest to the highest value).
# IMPORTANT: Don't use the domains inside the problem, use and modify the ones given by the "domains" argument 
#            since they contain the current domains of unassigned variables only.
def least_restraining_values(problem: Problem, variable_to_assign: str, domains: Dict[str, set]) -> List[Any]:
    #TODO: Write this function
    # This is value ordering heuristic :D
    print("least_restraining_values()")
    print("variable_to_assign",variable_to_assign)
    # print(domains)
    # print(domains['(2, 3)'])
    # print(domains['(3, 2)'])
    # return None

    # We need to check on all the values[Domain values] of the variable_to_assign
    variable_to_assign_values=domains[variable_to_assign]

    least_restraining_values_list=[]
    # Min Priority Queue
    # priority_queue = PriorityQueue()
    

    # Loop over all the values in the variable_to_assign domain
    for variable_to_assign_value in variable_to_assign_values:
        # if(variable_to_assign_value not in [2]):continue
        print("variable_to_assign_value",variable_to_assign_value)

        # Create a copy [Deep] of the domains Dictionary
        domains_copy=copy.deepcopy(domains)

        # The question is which heuristic to use ==> we need to choose the value that makes the min among remaining values of all other unassigned variables the min
        # min_remaining_values_count=sys.maxsize
        remaining_values={}


        
        # Loop over Constraints
        for constraint in problem.constraints:
            # The Variables of the binary constraint
            constraint_variables=constraint.variables
    
            # If this constraint doesn't have the assigned_variable then nothing to be done bec we are implementing forward checking
            if variable_to_assign not in constraint_variables: continue
 
            
            # So Here we have a Binary Constraint that involves the assigned_variable
            # Getting the other variable 
            index_of_variable = constraint_variables.index(variable_to_assign)
            other_variable=constraint_variables[1 - index_of_variable]

            # Check if the other variable is in the Domain dictionary else it is assigned before
            if other_variable not in domains_copy.keys(): continue  #assigned before

            # Then Fine we have an unassigned variable and a value of the variable_to_assign we need to check if this value restraints the constrains or not
            # Just Assume we will take this value what is the remaining values for the unassigned variable
            other_variable_domain=domains_copy[other_variable]

            if(variable_to_assign_value not in other_variable_domain ):
                remaining_values[other_variable]=len(other_variable_domain)
                print("*********")
                continue
            

            # print("other_variable_domain",other_variable_domain)
            other_variable_domain.discard(variable_to_assign_value)
            remaining_values[other_variable]=len(other_variable_domain)
            # print("other_variable_domain",other_variable_domain)
      

            # Count the Remaining values for the unassigned_variable if this value(for variable_to_assign) is chosen
            # other_variable_remaining_values_count=len(other_variable_domain)
            # print("other_variable_remaining_values_count",other_variable_remaining_values_count)
            # print("-----------")

            # Update min_remaining_values_count with other_variable_remaining_values_count
            # Taking min ie if the remaining values of this variable is less than the previous one then take this as the min
            # print("other_variable",other_variable)
            # if(other_variable_remaining_values_count<min_remaining_values_count):
                # min_remaining_values_count=other_variable_remaining_values_count
                # print(other_variable)
                # print(other_variable_domain)
            # min_remaining_values_count=min(other_variable_remaining_values_count,min_remaining_values_count)

        # Add the heuristic value as priority of the list
        # print("min_remaining_values_count",min_remaining_values_count)
        # least_restraining_values_list.append((-1*min_remaining_values_count,variable_to_assign_value))

        # Calculate LCV heuristic = summation of the remaining domains for all the variables
        # NB: I have discarded the domains that don't interact with the variable to be assigned bec we just will have the same no added to 
        # all values all we need here is just to know who is bigger not the exact no
        sum_remaining_values=sum(remaining_values.values())

        # Add the heuristic value as priority of the list
        least_restraining_values_list.append((-1*sum_remaining_values,variable_to_assign_value))

    # Sort by the summation of the total remaining values
    least_restraining_values_list=sorted(least_restraining_values_list, key=cmp_to_key(custom_comparison))

    # Extract values by discarding the priority
    least_restraining_values_list = [value for priority, value in least_restraining_values_list]

    print(least_restraining_values_list)

    return least_restraining_values_list
    least_restraining_values_list=sorted(least_restraining_values_list, key=cmp_to_key(custom_comparison))

    # Extract values by discarding the priority
    least_restraining_values_list = [value for priority, value in least_restraining_values_list]
    print(least_restraining_values_list)
    return least_restraining_values_list



            # return None
  
        

        # # For each other unassigned variable
        # for unassigned_variable in domains.keys():
        #     # if this is the variable we are trying to find its value -> continue
        #     if(unassigned_variable==variable_to_assign): continue

        #     # Remove variable_to_assign_value from the unassigned_variable domain
        #     unassigned_variable_domain=domains[unassigned_variable]
        #     unassigned_variable_domain.discard(variable_to_assign_value)

        #     # Count the Remaining values for the unassigned_variable if this value(for variable_to_assign) is chosen
        #     unassigned_variable_remaining_values_count=len(unassigned_variable_domain)

        #     # Update min_remaining_values_count with unassigned_variable_remaining_values_count
        #     # Taking min ie if the remaining values of this variable is less than the previous one then take this as the min
        #     min_remaining_values_count=min(unassigned_variable_remaining_values_count,unassigned_variable_remaining_values_count)

        # Add this value to the priority queue with priority of min_remaining_values_count
        # heapq.heappush(least_restraining_values_list,-1*min_remaining_values_count)


    # Return Heap (orderd list)
    # Convert the heap to an ordered list (from smallest to largest)
    # least_restraining_values_list = heapq.nlargest(len(least_restraining_values_list), least_restraining_values_list)
    # return least_restraining_values_list

    NotImplemented()

# This function should solve CSP problems using backtracking search with forward checking.
# The variable ordering should be decided by the MRV heuristic.
# The value ordering should be decided by the "least restraining value" heurisitc.
# Unary constraints should be handled using 1-Consistency before starting the backtracking search.
# This function should return the first solution it finds (a complete assignment that satisfies the problem constraints).
# If no solution was found, it should return None.
# IMPORTANT: To get the correct result for the explored nodes, you should check if the assignment is complete only once using "problem.is_complete"
#            for every assignment including the initial empty assignment, EXCEPT for the assignments pruned by the forward checking.
#            Also, if 1-Consistency deems the whole problem unsolvable, you shouldn't call "problem.is_complete" at all.
def solve(problem: Problem) -> Optional[Assignment]:
    #TODO: Write this function
    NotImplemented()
    