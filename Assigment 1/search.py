from problem import HeuristicFunction, Problem, S, A, Solution
from collections import deque
from helpers.utils import NotImplemented

#TODO: Import any modules you want to use
import heapq
import queue

# All search functions take a problem and a state
# If it is an informed search function, it will also receive a heuristic function
# S and A are used for generic typing where S represents the state type and A represents the action type

# All the search functions should return one of two possible type:
# 1. A list of actions which represent the path from the initial state to the final state
# 2. None if there is no solution

# Utils
#################################################################################################################################################
'''
Function  to print queue just used for debugging
'''
def print_queue(q:queue):
    copy_q=q.queue.copy()
    # print("***Queue")
    for item in copy_q:
        print(item)


'''
Function  to print Heap just used for debugging
'''
def print_heap(heap):
    # print("Heap")
    for item in list(heap):
        print(item)  

'''
Function  to remove value from a heap by using its value then heapify the result again so that a new heap is returned
'''
def remove_from_heap_by_property(heap, property_value):
    # Find the index of the element with the specified property value
    index_to_remove = next(
        (i for i, element in enumerate(heap) if element.node == property_value),
        None
    )
    if index_to_remove is not None:
        # Replace the element at index_to_remove with the last element
        heap[index_to_remove] = heap[-1]
        heap.pop()  # Remove the last element
        heapq.heapify(heap)  # Re-heapify the list after replacement
        # print(f"Removed the element with property value {property_value}.")
    # else:
        # print(f"Element with property value {property_value} not found in the heap.")

#################################################################################################################################################
'''
Class to Manage State as a Node in teh search tree
where it has 2 attributes the state its self [differs according to the problem]
and path from the initial state to this state
'''
class State:
    
    def __init__(self, node:str, path:[str]):
        self.node = node # Name of the state
        self.path = path # Path from the initial Stat to this state
        
    def __str__(self):
        return f"State:{self.node}, Path:{self.path}"
    
 

'''
Cost State is a State [inheritance]
With Extra attribute is the cost attribute to reach froth e initial state to this state
and also heuristic attribute which is the heuristic about teh coast from the current state to te goal :D
Here index is just to keep track of when it is pushed inside the Frontier bec in case of Tie of evaluation we just choose the FIFO
'''
class Cost_State(State):
    def __init__(self, node:str, path:[str],index,path_cost=0,heuristic=0):
        super().__init__(node,path) # State Constructor
        self.path_cost=path_cost
        self.heuristic=heuristic
        self.index=index
         
    def __str__(self):
        return super().__str__() +f" Path_Cost:{self.path_cost}, Index:{self.index}"
    
    # Operator > overloading for the heap 
    def __lt__(self, nxt): 
        if(self.path_cost+self.heuristic!=nxt.path_cost+nxt.heuristic): return self.path_cost+self.heuristic<nxt.path_cost+nxt.heuristic
        return self.index < nxt.index 
#################################################################################################################################################

    
    
def BreadthFirstSearch(problem: Problem[S, A], initial_state: S) -> Solution:
    #TODO: ADD YOUR CODE HERE
    # Create State object which has the initial state as its node and the path as an empty list because it is it self the initial state 
    current_state=State(initial_state,[])
    
    # if the initial state is the goal the return it
    if(problem.is_goal(current_state.node)): return current_state.path

    # Create Frontier to be Queue of States
    frontier=queue.Queue()
    frontier.put(current_state) # add the initial state to the Queue
    # Explored Set bec it is Graph Search Problem :D
    explored=set() #set of the explored nodes to solve the problem of repetition
    # Extra Data Memory to be used to search in the frontier in O(1) instead of searing in it in Queue O(n) so i add extra memory to be faster search
    frontier_set=set() #set of the explored nodes to solve the problem of repetition
    frontier_set.add(current_state.node)


    # Keep looping till frontier is empty bec if empty then there are no more states to explore --> No Sol :D
    while(not frontier.empty()):
        current_state=frontier.get() # Get shallowed node
        frontier_set.remove(current_state.node) # Set synced with Queue Frontier
        explored.add(current_state.node) # add node to the explored ones

        # Investigate  next successors
        for action in problem.get_actions(current_state.node):
            next_successor_state=problem.get_successor(current_state.node,action)

            # Skip previously explored points
            if next_successor_state in explored or next_successor_state in frontier_set :  # waiting for what in frontier
                continue

            # Check if this action is a goal then --> return path
            if(problem.is_goal(next_successor_state)): 
                return current_state.path+[action]
            # else Add to the frontier to explore its children later
            frontier.put(State(next_successor_state,current_state.path+[action]))
            frontier_set.add(next_successor_state)
    return None
    NotImplemented()
    
def DepthFirstSearch(problem: Problem[S, A], initial_state: S) -> Solution:
    #TODO: ADD YOUR CODE HERE
    # Create State object which has the initial state as its node and the path as an empty list because it is it self the initial state 
    current_state=State(initial_state,[])

    # if the initial state is the goal the return it
    if(problem.is_goal(current_state.node)): return current_state.path

    # Create Frontier to be Stack of States
    frontier = deque()
    frontier.append(current_state) # add the initial state to the Queue
    explored=set() #set of the explored nodes to solve the problem of repetition
    frontier_set=set() #set of the explored nodes to solve the problem of repetition
    frontier_set.add(current_state.node)


    # Keep looping till frontier is empty bec if empty then there are no more states to explore --> No Sol :D
    while(len(frontier)!= 0):
        current_state=frontier.pop() # Get Top of Stack
        frontier_set.remove(current_state.node) # Syn Set with the Frontier
        explored.add(current_state.node) # add node to the explored ones


        
        # Check if this action is a goal then --> return path
        if(problem.is_goal(current_state.node)): 
            return current_state.path

        
        # Investigate  next successors
        for action in problem.get_actions(current_state.node):
            next_successor_state=problem.get_successor(current_state.node,action)

            # Skip previously explored points
            if next_successor_state in explored or next_successor_state in frontier_set : 
                continue

            # else Add to the frontier to explore its children later
            frontier.append(State(next_successor_state,current_state.path+[action]))
            frontier_set.add(next_successor_state)
    return None
    NotImplemented()
    



# "Heap" doesn't mean "sorted" (if it did, you couldn't build it for arbitrary values in O(n) time). 
# It means it satisfies the heap invariant, for a min-heap like Python's, this just means that the smallest value is at the top (if there's a tie, an arbitrary value wins)
def UniformCostSearch(problem: Problem[S, A], initial_state: S) -> Solution:
    #TODO: ADD YOUR CODE HERE
    index=0
    # Create Cost_State object which has the initial state as its node and the path as an empty list because it is it self the initial state 
    # Here I have used Cost_State because i need the cost it is uniform cost Algorithm
    current_state=Cost_State(initial_state,[],index,0)  #Cost is set to 0 and index =0 bec first node enter frontier

    # Create Frontier to be Priority Queue of States
    frontier=[current_state]
    heapq.heapify(frontier)  # Convert to heap
    explored=set()  # Keep track of explored sets
    frontier_hash={current_state.node:0} # node cost

    # Keep looping till frontier is empty bec if empty then there are no more states to explore --> No Sol :D
    while(len(frontier)>0):
        min_cost_state=heapq.heappop(frontier)# choose lowest-cost node form the frontier
        del frontier_hash[min_cost_state.node] # Syncing

        # Check if goal here we check if goal after popped from the frontier bec when insetting it may be not the best(optimal) goal
        if(problem.is_goal(min_cost_state.node)):
            return min_cost_state.path #no need to add [action] bec it is here checked when out of the frontier
        
        # Add the node to the explored ones
        explored.add(min_cost_state.node)

       
        # Investigate  next successors
        for action in problem.get_actions(min_cost_state.node):
            next_successor_state=problem.get_successor(min_cost_state.node,action)

             # Skip previously explored points
            if next_successor_state in explored : continue

            # If This state is in the frontier with higher path cost
            elif next_successor_state in frontier_hash:
                # Check if its cost is less than its current cost 
                # remove it
                new_can_cost=min_cost_state.path_cost+problem.get_cost(min_cost_state.node,action)

                if(new_can_cost<frontier_hash[next_successor_state]):
                    # Remove old one from the frontier
                    remove_from_heap_by_property(frontier, next_successor_state)
                    del frontier_hash[next_successor_state]

                    # Add new one :D
                    # Cost = Cost of the parent (from initial state) + cost from the current state to this next successor
                    heapq.heappush(frontier, Cost_State(next_successor_state,min_cost_state.path+[action],index,new_can_cost))
                    frontier_hash[next_successor_state]=new_can_cost
                    # inc index
                    index=index+1
                
                # else no effect continue :D this state is achieved by a more costly path :( so i have ignored it

            else: # Not in explored or in the frontier
                # Add to the frontier
                new_cost=min_cost_state.path_cost+problem.get_cost(min_cost_state.node,action)
                heapq.heappush(frontier, Cost_State(next_successor_state,min_cost_state.path+[action],index,new_cost))
                frontier_hash[next_successor_state]=new_cost
                index=index+1

        
    return None # No sol was found

def AStarSearch(problem: Problem[S, A], initial_state: S, heuristic: HeuristicFunction) -> Solution:
    #TODO: ADD YOUR CODE HERE
    index=0
    current_state=Cost_State(initial_state,[],index,0,0)  #Cost is set to 0 and index =0 bec first node enter frontier

    # Create Frontier to be Priority Queue of States
    frontier=[current_state]
    heapq.heapify(frontier) 
    explored=set()
    frontier_hash={current_state.node:0} # <node,cost>

    while(len(frontier)>0):
        min_cost_state=heapq.heappop(frontier)#choose lowest-cost node form the frontier
        # frontier_set.remove(min_cost_state.node)
        del frontier_hash[min_cost_state.node]

        # Check if goal here we check if goal after popped from the frontier bec when insetting it may be not the best(optimal) goal
        if(problem.is_goal(min_cost_state.node)):
            return min_cost_state.path #no need to add [action] bec it is here checked when out of the frontier
        

        # Add the node to the explored ones
        explored.add(min_cost_state.node)

    
        # Investigate  next successors
        for action in problem.get_actions(min_cost_state.node):
            # print("action",action)
            next_successor_state=problem.get_successor(min_cost_state.node,action)

             # Skip previously explored points
            if next_successor_state in explored : continue

            # If This state is in the frontier with higher path cost
            elif next_successor_state in frontier_hash:
                # Check if its cost is less than its current cost 
                # remove it
                # new_can_cost=min_cost_state.path_cost+problem.get_cost(min_cost_state.node,action)
                new_can_cost=min_cost_state.path_cost+problem.get_cost(min_cost_state.node,action)
                new_heuristic=heuristic(problem,next_successor_state)

                # if its cost+ heuristic is less that the one iin the frontier 
                # We need to replace with the one in the frontier
                if(new_can_cost+new_heuristic<frontier_hash[next_successor_state]):
                    # Remove old one from the frontier
                    remove_from_heap_by_property(frontier, next_successor_state)
                    del frontier_hash[next_successor_state]
                    # Add new one :D
                    # Note that here we accumulate cost only not the heuristic
                    heapq.heappush(frontier, Cost_State(next_successor_state,min_cost_state.path+[action],index,new_can_cost,new_heuristic))
                    frontier_hash[next_successor_state]=new_can_cost+new_heuristic
                    # inc index
                    index=index+1


                
            #     # else no effect continue :D this state is achieved by a more costly path :( so i have ignored it

            else: # Not in explored or in the frontier
                # Add to the frontier
                new_cost=min_cost_state.path_cost+problem.get_cost(min_cost_state.node,action)
                new_heuristic=heuristic(problem,next_successor_state)
                heapq.heappush(frontier, Cost_State(next_successor_state,min_cost_state.path+[action],index,new_cost,new_heuristic))
                frontier_hash[next_successor_state]=new_cost+new_heuristic
                index=index+1

    return None


def BestFirstSearch(problem: Problem[S, A], initial_state: S, heuristic: HeuristicFunction) -> Solution:
    #TODO: ADD YOUR CODE HERE
    index=0
    # Create Cost_State object which has the initial state as its node and the path as an empty list because it is it self the initial state 
    # Here I have used Cost_State because i need the cost it is BestFirstSearch cost Algorithm
    current_state=Cost_State(initial_state,[],index,0)  #Cost is set to 0 and index =0 bec first node enter frontier

    # Create Frontier to be Priority Queue of States
    frontier=[current_state]
    heapq.heapify(frontier) 
    explored=set()
    frontier_hash={current_state.node:0} # <node,cost>

    while(len(frontier)>0):
        min_cost_state=heapq.heappop(frontier)#choose lowest-cost node form the frontier
        # frontier_set.remove(min_cost_state.node)
        del frontier_hash[min_cost_state.node]

        # Check if goal here we check if goal after popped from the frontier bec when insetting it may be not the best(optimal) goal
        if(problem.is_goal(min_cost_state.node)):
            return min_cost_state.path #no need to add [action] bec it is here checked when out of the frontier
        

        # Add the node to the explored ones
        explored.add(min_cost_state.node)

    
       
        # Investigate  next successors
        for action in problem.get_actions(min_cost_state.node):
            # print("action",action)
            next_successor_state=problem.get_successor(min_cost_state.node,action)

             # Skip previously explored points
            if next_successor_state in explored : continue

            # If This state is in the frontier with higher path cost
            elif next_successor_state in frontier_hash:
                # Check if its cost is less than its current cost 
                # Priority is the Heuristics
                new_can_cost=heuristic(problem,next_successor_state)

                if(new_can_cost<frontier_hash[next_successor_state]):
                    # Remove old one from the frontier
                    remove_from_heap_by_property(frontier, next_successor_state)
                    del frontier_hash[next_successor_state]
                    # Add new one :D
                    heapq.heappush(frontier, Cost_State(next_successor_state,min_cost_state.path+[action],index,new_can_cost))
                    frontier_hash[next_successor_state]=new_can_cost
                    # inc index
                    index=index+1


                
                # else no effect continue :D this state is achieved by a more costly path :( so i have ignored it

            else: # Not in explored or in the frontier
                # Add to the frontier
                # Cost is the Heuristics to the goal from that state
                new_cost=heuristic(problem,next_successor_state)
                heapq.heappush(frontier, Cost_State(next_successor_state,min_cost_state.path+[action],index,new_cost))
                frontier_hash[next_successor_state]=new_cost
                index=index+1

       
        
    return None # No sol was found
    NotImplemented()