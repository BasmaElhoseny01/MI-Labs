from typing import Any, Dict, Set, Tuple, List
from problem import Problem
from mathutils import Direction, Point
from helpers.utils import NotImplemented



#TODO: (Optional) Instead of Any, you can define a type for the parking state
# ParkingState = Any
ParkingState =  List[Point] # List of Points where  ParkingState[0] ==> point of car A

# An action of the parking problem is a tuple containing an index 'i' and a direction 'd' where car 'i' should move in the direction 'd'.
ParkingAction = Tuple[int, Direction]

# This is the implementation of the parking problem
class ParkingProblem(Problem[ParkingState, ParkingAction]):
    passages: Set[Point]    # A set of points which indicate where a car can be (in other words, every position except walls).
    cars: Tuple[Point]      # A tuple of points where state[i]/cars[i] is the position of car 'i'. 
    slots: Dict[Point, int] # A dictionary which indicate the index of the parking slot (if it is 'i' then it is the slot of car 'i') for every position.
                            # if a position does not contain a parking slot, it will not be in this dictionary.
    width: int              # The width of the parking slot.
    height: int             # The height of the parking slot.

    # This function should return the initial state
    def get_initial_state(self) -> ParkingState:
        #TODO: ADD YOUR CODE HERE

        # The State is the cars position
        return [car_pos for car_ind,car_pos in enumerate(self.cars)]# Converting tuple of positions to list
        # NotImplemented()
    
    # This function should return True if the given state is a goal. Otherwise, it should return False.
    def is_goal(self, state: ParkingState) -> bool:
        #TODO: ADD YOUR CODE HERE

        # To Reach Goal the current State = slot :D
        for slot,car in self.slots.items():
            if(state[car]!=slot):
                return False
        return True
    
    
    # This function returns a list of all the possible actions that can be applied to the given state
    def get_actions(self, state: ParkingState) -> List[ParkingAction]:
        #TODO: ADD YOUR CODE HERE
        actions=[]
        for car,position in enumerate(state):
            # Defining Directions for easy use UP,Down ,...
            directions=[Direction.RIGHT,Direction.LEFT,Direction.UP,Direction.DOWN]
            for direction in directions:
                new_position=position.__add__(direction.to_vector())
               
                # Check if new point is inside the parking area
                in_boundary=new_position.x<self.width and new_position.x>=0 and new_position.y<self.height and new_position.y>=0
               
                # Check if the slot at this direction don't contain a wall i.e is in {passages}
                # Check if the slot at this direction don't contain another car now i.e 8 is in {cars}
                if(in_boundary and new_position in self.passages and new_position not in state): 
                    # search here(self.passages) is in O(1) bec set used hashing but searching in state is in O(n)  
                    actions.append((car,direction))
            # # RIGHT
            # right_position=position.__add__(Direction.RIGHT.to_vector())
            # # Check if the slot at the right don;t contain a wall i.e is in {passages}
            # if(right_position.x<self.width and right_position in self.passages  and right_position not in self.cars): # search here is in O(1) bec set used hashing
            #     actions.append((car,Direction.RIGHT))
    
        # print(actions)

        return actions
        # NotImplemented()
    
    # This function returns a new state which is the result of applying the given action to the given state
    def get_successor(self, state: ParkingState, action: ParkingAction) -> ParkingState:
        #TODO: ADD YOUR CODE HERE
        # print("get_successor()")
        # Get car and the direction to move in
        car,direction=action
        
        # Update Current State by moving the car to d
        state[car]=state[car].__add__(direction.to_vector())
        
        return state
    
    # This function returns the cost of applying the given action to the given state
    def get_cost(self, state: ParkingState, action: ParkingAction) -> float:
        #TODO: ADD YOUR CODE HERE

        car,direction=action
        #Cost of moving a car is a function in ots order[employees hierarchy]
        move_car_cost=-1*car+26 


        # penalty if the direction there is the slot of another car
        penalty=0
        new_position:Point =state[car].__add__(direction.to_vector())
        slot_owner=self.slots.get(new_position)
        # print("slot_owner:",slot_owner)
        # print("car:",car)
        # print("slot_owner!=car",slot_owner!=car)

        # Check if this slot is for another car than that in the action
        if(slot_owner is not None and slot_owner!=car):
            # Apply Penalty
            # print("Penalty")
            penalty=100

        # print("Test",action)
        # print("move_car_cost+penalty",move_car_cost+penalty)

        return move_car_cost+penalty  #the cost i sthe summation of moving a car and a penalty if it applies
        # NotImplemented()
    
    
     # Read a parking problem from text containing a grid of tiles
    @staticmethod
    def from_text(text: str) -> 'ParkingProblem':
        passages =  set()
        cars, slots = {}, {}
        lines = [line for line in (line.strip() for line in text.splitlines()) if line]
        width, height = max(len(line) for line in lines), len(lines)
        for y, line in enumerate(lines):
            for x, char in enumerate(line):
                if char != "#":
                    passages.add(Point(x, y))
                    if char == '.':
                        pass
                    elif char in "ABCDEFGHIJ":
                        cars[ord(char) - ord('A')] = Point(x, y)
                    elif char in "0123456789":
                        slots[int(char)] = Point(x, y)
        problem = ParkingProblem()
        problem.passages = passages
        problem.cars = tuple(cars[i] for i in range(len(cars)))
        problem.slots = {position:index for index, position in slots.items()}
        problem.width = width
        problem.height = height
        return problem

    # Read a parking problem from file containing a grid of tiles
    @staticmethod
    def from_file(path: str) -> 'ParkingProblem':
        with open(path, 'r') as f:
            return ParkingProblem.from_text(f.read())
