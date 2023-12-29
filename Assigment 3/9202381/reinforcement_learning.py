from typing import Callable, DefaultDict, Dict, Generic, List, Optional, Union
from agents import Agent
from environment import Environment, S, A
from helpers.mt19937 import RandomGenerator
from helpers.utils import NotImplemented

import json
from collections import defaultdict

import sys


# The base class for all Reinforcement Learning Agents required for this problem set


class RLAgent(Agent[S, A]):
    rng: RandomGenerator  # A random number generator used for exploration
    actions: List[A]  # A list of all actions that the environment accepts
    discount_factor: float  # The discount factor "gamma"
    epsilon: float  # The exploration probability for epsilon-greedy
    learning_rate: float  # The learning rate "alpha"

    def __init__(self,
                 actions: List[A],
                 discount_factor: float = 0.99,
                 epsilon: float = 0.5,
                 learning_rate: float = 0.01,
                 seed: Optional[int] = None) -> None:
        super().__init__()
        # initialize the random generator with a seed for reproducability
        self.rng = RandomGenerator(seed)
        self.actions = actions
        self.discount_factor = discount_factor
        self.epsilon = epsilon
        self.learning_rate = learning_rate

    # A virtual function that returns the Q-value for a specific state and action
    # This should be overriden by the derived RL agents
    def compute_q(self, env: Environment[S, A], state: S, action: A) -> float:
        return 0

    # Returns true if we should explore (rather than exploit)
    def should_explore(self) -> bool:
        return self.rng.float() < self.epsilon

    def act(self, env: Environment[S, A], observation: S, training: bool = False) -> A:
        actions = env.actions()
    
        if training and self.should_explore():
            # TODO: Return a random action whose index is "self.rng.int(0, len(actions)-1)"
            return actions[self.rng.int(0, len(actions)-1)]
            NotImplemented()
        else:
            # TODO: return the action with the maximum q-value as calculated by "compute_q" above
            # if more than one action has the maximum q-value, return the one that appears first in the "actions" list

            # Initially by -inf
            max_q_value = float('-inf')
            max_action=None

            # Loop over the actions
            for action in actions:
                # This is > to solve the case that we have 2 max we take the first one that appears 
                if self.compute_q(env,observation,action)>max_q_value:
                    max_q_value=self.compute_q(env,observation,action)
                    max_action=action
            return max_action
            NotImplemented()

#############################
#######     SARSA      ######
#############################

# This is a class for a generic SARSA agent


class SARSALearningAgent(RLAgent[S, A]):
    Q: DefaultDict[S, DefaultDict[A, float]]  # The table of the Q values
    # The first key is the string representation of the state
    # The second key is the string representation of the action
    # The value is the Q-value of the given state and action

    def __init__(self,
                 actions: List[A],
                 discount_factor: float = 0.99,
                 epsilon: float = 0.5,
                 learning_rate: float = 0.01,
                 seed: Optional[int] = None) -> None:
        super().__init__(actions, discount_factor, epsilon, learning_rate, seed)
        self.Q = defaultdict(lambda: defaultdict(
            lambda: 0))  # The default Q value is 0

    def compute_q(self, env: Environment[S, A], state: S, action: A) -> float:
        # Return the Q-value of the given state and action
        return self.Q[state][action]
        # NOTE: we cast the state and the action to a string before querying the dictionaries

    # Update the value of Q(state, action) using this transition via the SARSA update rule
    def update(self, env: Environment[S, A], state: S, action: A, reward: float, next_state: S, next_action: Optional[A]):
        # TODO: Complete this function to update Q-table using the SARSA update rule
        # If next_action is None, then next_state is a terminal state in which case, we consider the Q-value of next_state to be 0


        # Q_value for the current state and action
        q_current=self.compute_q(env,state,action)

        # Q_value for the next state and action
        q_next=self.compute_q(env,next_state,next_action)

        # Applying Equation
        # Q(s,a) ← Q(s,a) + α(r + γQ(s' , a') − Q(s,a))
        self.Q[state][action]=q_current + self.learning_rate * ( reward + self.discount_factor*q_next - q_current)
        # NotImplemented()

    # Save the Q-table to a json file
    def save(self, env: Environment[S, A], file_path: str):
        with open(file_path, 'w') as f:
            Q = {
                env.format_state(state): {
                    env.format_action(action): value for action, value in state_q.items()
                } for state, state_q in self.Q.items()
            }
            json.dump(Q, f, indent=2, sort_keys=True)

    # load the Q-table from a json file
    def load(self, env: Environment[S, A], file_path: str):
        with open(file_path, 'r') as f:
            Q = json.load(f)
            self.Q = {
                env.parse_state(state): {
                    env.parse_action(action): value for action, value in state_q.items()
                } for state, state_q in Q.items()
            }

#############################
#####   Q-Learning     ######
#############################

# This is a class for a generic Q-learning agent


class QLearningAgent(RLAgent[S, A]):
    Q: DefaultDict[str, DefaultDict[str, float]]  # The table of the Q values
    # The first key is the string representation of the state
    # The second key is the string representation of the action
    # The value is the Q-value of the given state and action

    def __init__(self,
                 actions: List[A],
                 discount_factor: float = 0.99,
                 epsilon: float = 0.5,
                 learning_rate: float = 0.01,
                 seed: Optional[int] = None) -> None:
        super().__init__(actions, discount_factor, epsilon, learning_rate, seed)
        self.Q = defaultdict(lambda: defaultdict(
            lambda: 0))  # The default Q value is 0

    def compute_q(self, env: Environment[S, A], state: S, action: A) -> float:
        # Return the Q-value of the given state and action
        return self.Q[state][action]
        # NOTE: we cast the state and the action to a string before querying the dictionaries

    # Given a state, compute and return the utility of the state using the function "compute_q"
    def compute_utility(self, env: Environment[S, A], state: S) -> float:
        # TODO: Complete this function.

        # Getting actions
        actions=env.actions()
        # U(s)=max a Q(s,a)
        return max([self.compute_q(env,state,action) for action in actions])
        NotImplemented()

    # Update the value of Q(state, action) using this transition via the Q-Learning update rule
    def update(self, env: Environment[S, A], state: S, action: A, reward: float, next_state: S, done: bool):
        # TODO: Complete this function to update Q-table using the Q-Learning update rule
        # If done is True, then next_state is a terminal state in which case, we consider the Q-value of next_state to be 0

        # Q_value for the current state and action
        q_current=self.compute_q(env,state,action)


        # Q(s,a) ← Q(s,a) + α(r + γ max a' Q(s' , a') − Q(s,a))
        self.Q[state][action]=q_current +  self.learning_rate * (reward + self.discount_factor * self.compute_utility(env,next_state) - q_current)
        # NotImplemented()
        

    # Save the Q-table to a json file
    def save(self, env: Environment[S, A], file_path: str):
        with open(file_path, 'w') as f:
            Q = {
                env.format_state(state): {
                    env.format_action(action): value for action, value in state_q.items()
                } for state, state_q in self.Q.items()
            }
            json.dump(Q, f, indent=2, sort_keys=True)

    # load the Q-table from a json file
    def load(self, env: Environment[S, A], file_path: str):
        with open(file_path, 'r') as f:
            Q = json.load(f)
            self.Q = {
                env.parse_state(state): {
                    env.parse_action(action): value for action, value in state_q.items()
                } for state, state_q in Q.items()
            }

#########################################
#####   Approximate Q-Learning     ######
#########################################
# The type definition for a set of features representing a state
# The key is the feature name and the value is the feature value
Features = Dict[str, float]

# This class takes a state and returns the a set of features


class FeatureExtractor(Generic[S, A]):

    # Returns a list of feature names.
    # This will be used by the Approximate Q-Learning agent to initialize its weights dictionary.
    @property
    def feature_names(self) -> List[str]:
        return []

    # Given an enviroment and an observation (a state), return a set of features that represent the given state
    def extract_features(self, env: Environment[S, A], state: S) -> Features:
        return {}

# This is a class for a generic Q-learning agent


class ApproximateQLearningAgent(RLAgent[S, A]):
    weights: Dict[A, Features]    # The weights dictionary for this agent.
    # The first key is action and the second key is the feature name
    # The value is the weight
    # The feature extractor used to extract the features corresponding to a state
    feature_extractor: FeatureExtractor[S, A]

    def __init__(self,
                 feature_extractor: FeatureExtractor[S, A],
                 actions: List[A],
                 discount_factor: float = 0.99,
                 epsilon: float = 0.5,
                 learning_rate: float = 0.01,
                 seed: Optional[int] = None) -> None:
        super().__init__(actions, discount_factor, epsilon, learning_rate, seed)
        feature_names = feature_extractor.feature_names
        self.weights = {action: {feature: 0 for feature in feature_names}
                        for action in actions}  # we initialize the weights to 0
        self.feature_extractor = feature_extractor

    # Given the features of state and an action, compute and return the Q value
    def __compute_q_from_features(self, features: Dict[str, float], action: A) -> float:
        # TODO: Complete this function
        # NOTE: Remember to cast the action to string before quering self.weights

        # Weights of the given action
        actions_weights=self.weights[action]


        Q_s_a=0

        # Q(s,a) =w1*f1(s,a)+w2*f2(s,a)+......
        for feature,value in features.items():
            # print(key,value)
            # print("index,feature",index,feature)
            Q_s_a+=actions_weights[feature]*value

        return Q_s_a
        # NotImplemented()

    # Given the features of a state, compute and return the utility of the state using the function "__compute_q_from_features"
    def __compute_utility_from_features(self, features: Dict[str, float]) -> float:
        # TODO: Complete this function
        # Actions
        actions=self.actions

        max_q=  float('-inf')

        # Eq: max a Q(s,a)
        # The max q for the features fo all the action :D
        for action in actions:
            # Loop over actions and getting the max Q from all actions given the features passed
            q_value=self.__compute_q_from_features(features, action)
            if q_value > max_q:
                max_q=q_value

        # return max q_value <3
        return  max_q
        NotImplemented()

    def compute_q(self, env: Environment[S, A], state: S, action: A) -> float:
        features = self.feature_extractor.extract_features(env, state)
        return self.__compute_q_from_features(features, action)

    # Update the value of Q(state, action) using this transition via the Q-Learning update rule
    def update(self, env: Environment[S, A], state: S, action: A, reward: float, next_state: S, done: bool):
        # TODO: Complete this function to update weights using the Q-Learning update rule
        # If done is True, then next_state is a terminal state in which case, we consider the Q-value of next_state to be 0

        # Getting features of the current state
        features = self.feature_extractor.extract_features(env, state)


        # Next State features
        features_next = self.feature_extractor.extract_features(env, next_state)
        

        # q_value of the next state in case next state is terminal ie done=1 --> q_value is 0
        # else the next_q is the utility of next state given its features
        q_next_max=0 if done else self.__compute_utility_from_features(features_next)

        # q_value for the current state and action
        q= self.compute_q(env, state, action)
        for feature in features:
            # Q-Learning update rule: wia ← wia + α * (r + γ * maxQ(s', a') - Q(s, a)) * wi
            self.weights[action][feature]= self.weights[action][feature] + self.learning_rate * ( reward + self.discount_factor*q_next_max - q )*features[feature]

        
        # NotImplemented()

    # Save the weights to a json file
    def save(self, env: Environment[S, A], file_path: str):
        with open(file_path, 'w') as f:
            weights = {env.format_action(
                action): w for action, w in self.weights.items()}
            json.dump(weights, f, indent=2, sort_keys=True)

    # load the weights from a json file
    def load(self, env: Environment[S, A], file_path: str):
        with open(file_path, 'r') as f:
            weights = json.load(f)
            self.weights = {env.parse_action(
                action): w for action, w in weights.items()}
