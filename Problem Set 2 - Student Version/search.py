from typing import Tuple
from game import HeuristicFunction, Game, S, A
from helpers.utils import NotImplemented

#TODO: Import any modules you want to use
import math

# All search functions take a problem, a state, a heuristic function and the maximum search depth.
# If the maximum search depth is -1, then there should be no depth cutoff (The expansion should not stop before reaching a terminal state) 

# All the search functions should return the expected tree value and the best action to take based on the search results

# This is a simple search function that looks 1-step ahead and returns the action that lead to highest heuristic value.
# This algorithm is bad if the heuristic function is weak. That is why we use minimax search to look ahead for many steps.
def greedy(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1) -> Tuple[float, A]:
    agent = game.get_turn(state)
    
    terminal, values = game.is_terminal(state)
    if terminal: return values[agent], None

    actions_states = [(action, game.get_successor(state, action)) for action in game.get_actions(state)]
    value, _, action = max((heuristic(game, state, agent), -index, action) for index, (action , state) in enumerate(actions_states))
    return value, action



# Apply Minimax search and return the game tree value and the best action
# Hint: There may be more than one player, and in all the testcases, it is guaranteed that 
# game.get_turn(state) will return 0 (which means it is the turn of the player). All the other players
# (turn > 0) will be enemies. So for any state "s", if the game.get_turn(s) == 0, it should a max node,
# and if it is > 0, it should be a min node. Also remember that game.is_terminal(s), returns the values
# for all the agents. So to get the value for the player (which acts at the max nodes), you need to
# get values[0].
def minimax(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1) -> Tuple[float, A]:
    #TODO: Complete this function
    # print("minimax()")
    # print("game",game)
    # print("state",state)
    # print("heuristic",heuristic)
    # print("max_depth",max_depth)

    
    # Getting Agent Who's Turn is now ??
    agent=game.get_turn(state)

    # check terminal state
    terminal, values = game.is_terminal(state)


    if terminal:
        # print("Terminal State",values,state)
        return values[0], None # if it is terminal state then return value for this agent
    
    if(max_depth==0):
        # print("max_depth")
        # We have reached max Depth the use the heuristic at this point
        if(agent==0):
            value=heuristic(game, state, agent)
        else: value=-1*heuristic(game, state, agent)
        return value,None
    
    best_value=None
    # if(agent==0): best_value=-sys.maxsize - 1
    # else: best_value=sys.maxsize
    best_action=None

    # Investigate all the possible actions
    for action in game.get_actions(state):
        next_state=game.get_successor(state, action)
        value,_=minimax(game, next_state, heuristic, max_depth-1)
        if(agent==0):
            # My Turn then maximizing successors
            if(best_value is None or value>best_value):
                best_value=value
                best_action=action

        else:
            # My Turn then minimizing successors
            if(best_value is None or value<best_value):
                best_value=value
                best_action=action
                
    #Return the best choices according to the values till last terminal state 
    return best_value,best_action
    NotImplemented()

def alphabeta_search(game: Game[S, A], state: S,alpha,beta, heuristic: HeuristicFunction, max_depth: int = -1,order_values=False) -> Tuple[float, A]:
    # check terminal state
    terminal, values = game.is_terminal(state)

    if terminal:
        # print("Terminal State",values,state)
        return values[0], None # if it is terminal state then return value for this agent
    
    # Check whose turn
    agent=game.get_turn(state)

    if(max_depth==0):
        # We have reached max Depth the use the heuristic at this point by it is min Node 
        if agent==0:
            value=heuristic(game, state, agent)
        else:
            value=-1* heuristic(game,state,agent)
        # Then take the -ve of heuristic
        return value,None
    
    # We need to explore possible action from teh current state
    actions_nextStates=[(action, game.get_successor(state,action)) for action in game.get_actions(state)]
    # The step above i have get teh list to make action and the corresponding state tuple just to not repeat the code for the value ordering function <3 
    
    
    # For Value ordering for the exploration of the children
    if order_values:
        print("order_values")
        # Get teh states from the next actions
        action_states=[ game.get_successor(state,action) for action in game.get_actions(state)] #[next_state]

        # Then sort the 
        print(action_states)



        # Then we need to sort this list based on the heuristic of the next states :D
        return None


    if agent==0:
        # My Turn
        # It is max Node Set value to be -ve infinity
        value= -1* math.inf
        best_action=None

        #  Explore Children
        for action in game.get_actions(state):

            #TODO check how to optimize ths

            # The Next State from this action :D
            next_state=game.get_successor(state, action)

            # Call Min Value for the next node bec --> it will enemy (Min Node)
            next_min_node_value,_=alphabeta_search(game,next_state,alpha,beta,heuristic,max_depth-1)
                
            # Take the max of current value and the value of the just explored min_Node
            # value=max(value,next_min_node_value)
            if value<next_min_node_value:
                value=next_min_node_value
                best_action=action

            # Check if pruning is required [We are in max node then check with beta]
            if(value>=beta): return value ,best_action #No need to continue all what will get next will be useless for us <3

            # Passed pruning check --> the we need to update alpha
            alpha=max(alpha,value)
        # After all children nodes are explored (No pruning in this case)
        # Pass the node value to the its parent
        return value,best_action

    else:
        # Enemy
        # It is min Node Set value to be +ve infinity
        value= math.inf
        best_action=None

        #  Explore Children
        for action in game.get_actions(state):
            alpha_copy=alpha
            beta_copy=beta

            # The Next State from this action :D
            next_state=game.get_successor(state, action)

            # Call Min Value for the next node bec --> it will enemy (Min Node)
            next_max_node_value,_=alphabeta_search(game,next_state,alpha_copy,beta_copy,heuristic,max_depth-1)

            # Take the max of current value and the value of the just explored min_Node
            # value=min(value,next_max_node_value)
            if value>next_max_node_value:
                value=next_max_node_value
                best_action=action



            # Check if pruning is required [We are in min node then check with alpha]
            if(value<=alpha): return value,best_action #No need to continue all what will get next will be useless for us <3

            # Passed pruning check --> the we need to update beta
            beta=min(beta,value)
        # After all children nodes are explored (No pruning in this case)
        # Pass the node value to the its parent
        return value,best_action




def alphabeta(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1) -> Tuple[float, A]:
    #TODO: Complete this function
    # print("alphabeta()")
    # print("game",game)
    # print("state",state)
    # print("heuristic",heuristic)
    # print("max_depth",max_depth)

    # Initially
    # 1. Set alpha to be min_value
    alpha= -1*math.inf
    # 2.Set beta to be max_value
    beta= math.inf
    # My Turn so i will start --> Max Node
    value,action=alphabeta_search(game,state,alpha,beta,heuristic,max_depth)


    return value,action
    NotImplemented()

# Apply Alpha Beta pruning with move ordering and return the tree value and the best action
# Hint: There may be more than one player, and in all the testcases, it is guaranteed that 
# game.get_turn(state) will return 0 (which means it is the turn of the player). All the other players
# (turn > 0) will be enemies. So for any state "s", if the game.get_turn(s) == 0, it should a max node,
# and if it is > 0, it should be a min node. Also remember that game.is_terminal(s), returns the values
# for all the agents. So to get the value for the player (which acts at the max nodes), you need to
# get values[0].
def alphabeta_with_move_ordering(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1) -> Tuple[float, A]:
    #TODO: Complete this function
    print("alphabeta_with_move_ordering()")

    # This function is the same as above all we need to do is to sort the children being explored

    # Initially
    # 1. Set alpha to be min_value
    alpha= -1*math.inf
    # 2.Set beta to be max_value
    beta= math.inf
    # My Turn so i will start --> Max Node
    value,action=alphabeta_search(game,state,alpha,beta,heuristic,max_depth,order_values=True)

    return value,action

    NotImplemented()

# Apply Expectimax search and return the tree value and the best action
# Hint: Read the hint for minimax, but note that the monsters (turn > 0) do not act as min nodes anymore,
# they now act as chance nodes (they act randomly).
def expectimax(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1) -> Tuple[float, A]:
    #TODO: Complete this function
    NotImplemented()