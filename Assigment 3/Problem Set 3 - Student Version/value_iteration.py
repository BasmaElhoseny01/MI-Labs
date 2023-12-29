from typing import Dict, Optional
from agents import Agent
from environment import Environment
from mdp import MarkovDecisionProcess, S, A
import json
from helpers.utils import NotImplemented

# This is a class for a generic Value Iteration agent
class ValueIterationAgent(Agent[S, A]):
    mdp: MarkovDecisionProcess[S, A] # The MDP used by this agent for training 
    utilities: Dict[S, float] # The computed utilities
                                # The key is the string representation of the state and the value is the utility
    discount_factor: float # The discount factor (gamma)

    def __init__(self, mdp: MarkovDecisionProcess[S, A], discount_factor: float = 0.99) -> None:
        super().__init__()
        self.mdp = mdp
        self.utilities = {state:0 for state in self.mdp.get_states()} # We initialize all the utilities to be 0
        self.discount_factor = discount_factor
    
    # Given a state, compute its utility using the bellman equation
    # if the state is terminal, return 0
    def compute_bellman(self, state: S) -> float:
        #TODO: Complete this function
        # print("compute_bellman()")
        # Terminal State
        if self.mdp.is_terminal(state): return 0


        # Equation
        # U(s) = max a sum s' P(s'|s,a)[R(s,a,s') + γU(s')]
        # So we need to get the actions
        actions=self.mdp.get_actions(state)

        max_val = float('-inf')


        for action in actions:
            # Transition model given action a and sate s
            # Dictionary key--> next state and value --> p
            p_next_states=self.mdp.get_successor(state, action)

            summation=sum([p_next_state*(self.mdp.get_reward(state,action,next_state)
                                         + self.discount_factor * self.utilities[next_state])
                                           for next_state,p_next_state in p_next_states.items()])
            if summation>max_val:
                max_val=summation

         
        return max_val
    
    # Applies a single utility update
    # then returns True if the utilities has converged (the maximum utility change is less or equal the tolerance)
    # and False otherwise
    def update(self, tolerance: float = 0) -> bool:
        #TODO: Complete this function

        # Compute updates for all teh current state
        updates ={state:self.compute_bellman(state) for state in self.mdp.get_states()}

        # Check in the max_change in the updates
        max_change=float('-inf')
        for state in self.mdp.get_states():
            change=abs(updates[state]-self.utilities[state])
            if change > max_change:
                max_change = change 
        

        # Update the utils <3
        self.utilities = updates

        # if max_change is less than tolerance then end of algorithm :D
        return max_change<=tolerance

    # This function applies value iteration starting from the current utilities stored in the agent and stores the new utilities in the agent
    # NOTE: this function does incremental update and does not clear the utilities to 0 before running
    # In other words, calling train(M) followed by train(N) is equivalent to just calling train(N+M)
    def train(self, iterations: Optional[int] = None, tolerance: float = 0) -> int:
        #TODO: Complete this function to apply value iteration for the given number of iteration
        i = 0

        while i<iterations:
            i+=1
            # update
            if self.update(tolerance):
                # if converged 
                break
        # Return no of iterations of running the algo
        return i
    
    # Given an environment and a state, return the best action as guided by the learned utilities and the MDP
    # If the state is terminal, return None
    def act(self, env: Environment[S, A], state: S) -> A:
        #TODO: Complete this function

        # terminal state
        if(self.mdp.is_terminal(state)): return None

        # Note i have tried to use self.compute_bellman but i couldn't bec it computes the max and we 
        # want here the argmax :D as we said in the tutorial
        return max(
            self.mdp.get_actions(state),
            key=lambda a: sum(
                self.mdp.get_successor(state, a)[next_state]
                * (
                    self.mdp.get_reward(state, a, next_state)
                    + self.discount_factor * self.utilities[next_state]
                )
                for next_state in self.mdp.get_successor(state, a)
            ),
        )

    
    # Save the utilities to a json file
    def save(self, env: Environment[S, A], file_path: str):
        with open(file_path, 'w') as f:
            utilities = {self.mdp.format_state(state): value for state, value in self.utilities.items()}
            json.dump(utilities, f, indent=2, sort_keys=True)
    
    # loads the utilities from a json file
    def load(self, env: Environment[S, A], file_path: str):
        with open(file_path, 'r') as f:
            utilities = json.load(f)
            self.utilities = {self.mdp.parse_state(state): value for state, value in utilities.items()}
