from typing import Dict, List, Optional, Set, Tuple
from mdp import MarkovDecisionProcess
from environment import Environment
from mathutils import Point, Direction
from helpers.mt19937 import RandomGenerator
from helpers.utils import NotImplemented
import json
from dataclasses import dataclass
import math

"""
Environment Description:
    The snake is a 2D grid world where the snake can move in 4 directions.
    The snake always starts at the center of the level (floor(W/2), floor(H/2)) having a length of 1 and moving LEFT.
    The snake can wrap around the grid.
    The snake can eat apples which will grow the snake by 1.
    The snake can not eat itself.
    You win if the snake body covers all of the level (there is no cell that is not occupied by the snake).
    You lose if the snake bites itself (the snake head enters a cell occupied by its body).
    The action can not move the snake in the opposite direction of its current direction.
    The action can not move the snake in the same direction 
        i.e. (if moving right don't give an action saying move right).
    Eating an apple increases the reward by 1.
    Winning the game increases the reward by 100.
    Losing the game decreases the reward by 100.
"""


# IMPORTANT: This class will be used to store an observation of the snake environment
@dataclass(frozen=True)
class SnakeObservation:
    snake: Tuple[Point]     # The points occupied by the snake body 
                            # where the head is the first point and the tail is the last  
    direction: Direction    # The direction that the snake is moving towards
    apple: Optional[Point]  # The location of the apple. If the game was already won, apple will be None


class SnakeEnv(Environment[SnakeObservation, Direction]):

    rng: RandomGenerator  # A random generator which will be used to sample apple locations

    snake: List[Point]
    direction: Direction
    apple: Optional[Point]

    def __init__(self, width: int, height: int) -> None:
        super().__init__()
        assert width > 1 or height > 1, "The world must be larger than 1x1"
        self.rng = RandomGenerator()
        self.width = width
        self.height = height
        self.snake = []
        self.direction = Direction.LEFT
        self.apple = None

    def generate_random_apple(self) -> Point:
        """
        Generates and returns a random apple position which is not on a cell occupied 
        by the snake's body.
        """
        snake_positions = set(self.snake)
        possible_points = [Point(x, y) 
            for x in range(self.width) 
            for y in range(self.height) 
            if Point(x, y) not in snake_positions
        ]
        return self.rng.choice(possible_points)

    def reset(self, seed: Optional[int] = None) -> Point:
        """
        Resets the Snake environment to its initial state and returns the starting state.
        Args:
            seed (Optional[int]): An optional integer seed for the random
            number generator used to generate the game's initial state.

        Returns:
            The starting state of the game, represented as a Point object.
        """
        if seed is not None:
            self.rng.seed(seed) # Initialize the random generator using the seed
        # TODO add your code here
        # IMPORTANT NOTE: Define the snake before calling generate_random_apple
        print("reset()")
        
        
        # Snake is initially of length 1 and at the centre
        self.snake=[Point(x=math.floor(self.width/2),y=math.floor(self.height/2))]


        # Start the snake is in the Left direction
        self.direction = Direction.LEFT

        # Generating the first apple
        self.apple=self.generate_random_apple()

    
        return SnakeObservation(tuple(self.snake), self.direction, self.apple)

    def actions(self) -> List[Direction]:
        """
        Returns a list of the possible actions that can be taken from the current state of the Snake game.
        Returns:
            A list of Directions, representing the possible actions that can be taken from the current state.

        """
        # TODO add your code here
        # a snake can wrap around the grid
        # NOTE: The action order does not matter
        print("actions()")
        # Actions to be taken based on conditions mentioned above

        # Initially 
        actions={Direction.RIGHT,Direction.UP,Direction.LEFT,Direction.DOWN,Direction.NONE}

        # The action can not move the snake in the same direction (if moving right don't give an action saying move right).
        actions.remove(self.direction)

        # The action can not move the snake in the opposite direction of its current direction.
        opposite_direction=self.direction.rotate(2)
        actions.remove(opposite_direction)       

        
        # The snake can not eat itself.
        # Check if the successor of the action occupied by the snake

        # Getting head of the snake --> the last index in the snake list
        snake_head=self.snake[0]

        actions_copy=actions.copy()
        for action in actions_copy:
            # Action of the vector
            vector=Direction._Vectors[action]

            # Getting next points
            new_point=snake_head + vector

            # The snake can wrap around the grid.
            # Module next point to be in grid
            new_point = Point((new_point.x) % self.width, (new_point.y) % self.height)

            # if(new_point.x==self.width):
            #     new_point=new_point.__sub__(Point(self.width,0))
            # elif(new_point.x==-1):
            #     new_point=new_point.__add__(Point(self.width,0))


            # if(new_point.y==self.height):
            #     new_point=new_point.__sub__(Point(0,self.height))
            # elif(new_point.y==-1):
            #     new_point=new_point.__add__(Point(0,self.height))
            
            

            if action is Direction.NONE:
            # then next point is in the same direction
                new_point=snake_head + Direction._Vectors[self.direction]


            # if snake is in this cell then he will eat himself
            if(new_point in self.snake):
                actions.remove(action)

        return actions
        # NotImplemented()

    def step(self, action: Direction) -> \
            Tuple[SnakeObservation, float, bool, Dict]:
        """
        Updates the state of the Snake game by applying the given action.

        Args:
            action (Direction): The action to apply to the current state.

        Returns:
            A tuple containing four elements:
            - next_state (SnakeObservation): The state of the game after taking the given action.
            - reward (float): The reward obtained by taking the given action.
            - done (bool): A boolean indicating whether the episode is over.
            - info (Dict): A dictionary containing any extra information. You can keep it empty.
        """
        # TODO Complete the following function

        # # Getting Head
        # print("snake_head",snake_head)
        reward=0

        # Action of the vector
        action_vector=Direction._Vectors[action]

        if action is Direction.NONE:
        # then next point is in the same direction
            action_vector= Direction._Vectors[self.direction]

        # Update the direction to be the same as the action
        if action!=Direction.NONE:
            self.direction=action


        # Make Him move [Head only]
        snake_head=self.snake[0]+action_vector
        # The snake can wrap around the grid.
        # Module next point to be in grid
        snake_head = Point((snake_head.x) % self.width, (snake_head.y) % self.height)


        

    
        # Case(1) Lose
        # if snake is in this cell then he will eat himself
        if(snake_head in self.snake):
            reward-=100
            done= True
            observation = SnakeObservation(tuple(self.snake), self.direction, self.apple)
            return observation, reward, done, {}
        

        # Case(3)
        # Add new head to the snake
        self.snake.insert(0,snake_head)


        # Non terminating action
        done = False

        #Case(2) If eating apple
        if snake_head==self.apple:
            # inc reward
            reward+=1          

            # Generate new apple for the next
            if not len(self.snake) == self.width * self.height:
                self.apple=self.generate_random_apple()

        else:
            # no apple 
            reward=0

            # Remove old tail
            self.snake.pop()        
        


        # Case(2) Win
        # if the len of the snack list is = to area of the map :D
        if(len(self.snake)==self.width*self.height):        
            reward+=100
            done= True
      
                 

        observation = SnakeObservation(tuple(self.snake), self.direction, self.apple)

        
        return observation, reward, done, {}

    ###########################
    #### Utility Functions ####
    ###########################

    def render(self) -> None:
        # render the snake as * (where the head is an arrow < ^ > v) and the apple as $ and empty space as .
        for y in range(self.height):
            for x in range(self.width):
                p = Point(x, y)
                if p == self.snake[0]:
                    char = ">^<v"[self.direction]
                    print(char, end='')
                elif p in self.snake:
                    print('*', end='')
                elif p == self.apple:
                    print('$', end='')
                else:
                    print('.', end='')
            print()
        print()

    # Converts a string to an observation
    def parse_state(self, string: str) -> SnakeObservation:
        snake, direction, apple = eval(str)
        return SnakeObservation(
            tuple(Point(x, y) for x, y in snake), 
            self.parse_action(direction), 
            Point(*apple)
        )
    
    # Converts an observation to a string
    def format_state(self, state: SnakeObservation) -> str:
        snake = tuple(tuple(p) for p in state.snake)
        direction = self.format_action(state.direction)
        apple = tuple(state.apple)
        return str((snake, direction, apple))
    
    # Converts a string to an action
    def parse_action(self, string: str) -> Direction:
        return {
            'R': Direction.RIGHT,
            'U': Direction.UP,
            'L': Direction.LEFT,
            'D': Direction.DOWN,
            '.': Direction.NONE,
        }[string.upper()]
    
    # Converts an action to a string
    def format_action(self, action: Direction) -> str:
        return {
            Direction.RIGHT: 'R',
            Direction.UP:    'U',
            Direction.LEFT:  'L',
            Direction.DOWN:  'D',
            Direction.NONE:  '.',
        }[action]