from sokoban import SokobanProblem, SokobanState
from mathutils import Direction, Point, manhattan_distance
from helpers.utils import NotImplemented

import sys


# This heuristic returns the distance between the player and the nearest crate as an estimate for the path cost
# While it is consistent, it does a bad job at estimating the actual cost thus the search will explore a lot of nodes before finding a goal
def weak_heuristic(problem: SokobanProblem, state: SokobanState):
    return min(manhattan_distance(state.player, crate) for crate in state.crates) - 1

#TODO: Import any modules and write any functions you want to use


def strong_heuristic(problem: SokobanProblem, state: SokobanState) -> float:
    # return
    #TODO: ADD YOUR CODE HERE
    #IMPORTANT: DO NOT USE "problem.get_actions" HERE.
    # Calling it here will mess up the tracking of the expanded nodes count
    # which is the number of get_actions calls during the search
    #NOTE: you can use problem.cache() to get a dictionary in which you can store information that will persist between calls of this function
    # This could be useful if you want to store the results heavy computations that can be cached and used across multiple calls of this function


    '''
    Original no of nodes expanded when using heuristic of  0 so that i use it as a benchmark for more improvements <3
    Test Case #     # of nodes expanded
    test case 1     6,477
    test case 2     97,523
    test case 3     441,629


    Results of Handling the dead lock Case(1)
    Test Case #     # of nodes expanded
    test case 1     3,171
    test case 2     46,914
    test case 3     229,733


    
    Results of Handling the dead lock Case(3)
    Test Case #     # of nodes expanded
    test case 1     1,401
    test case 2     14,935
    test case 3     57,792


    Results of Handling the dead lock Case(2)+ Adding case of being trapped by a similar crate
    Test Case #     # of nodes expanded
    test case 1     1,350
    test case 2     10,9086
    test case 3     55,581



        
    Results of Heuristic
    Test Case #     # of nodes expanded
    test case 1     1,192
    test case 2     7,518
    test case 3     54,670


    WOOOOOOOOOOOOOOOOOOOOOOOOOOW :D
    '''
    
    # Get Dimension of the layout to be used later
    width=state.layout.width
    height=state.layout.height

    # player_x=state.player.x
    # player_y=state.player.y

    # Saving the Goals and walkable and crates positions to be used later
    goals=state.layout.goals
    walkable=state.layout.walkable
    crates= state.crates


    if(len(goals)!= len(crates)):
        return sys.float_info.max
    

    # Creating a dictionary to be used as a check if there are some goals at the sides of the layout (sides= lines beside walls in 4 directions  col 0 and col -1 row 0 and row -1)
    goals_on_corners={
        'left':False,
        'right':False,
        'up':False,
        'down':False,
    }
    # Checking goals in all directions
    for goal in goals:
        # The aim of the dictionary is just flag not counting so if if found goals in 4 directions then no need to complete the loop :D
        if(goals_on_corners['left'] and goals_on_corners['right'] and goals_on_corners['up'] and goals_on_corners['down']): break
        if(goal.x==1 ): goals_on_corners['left']=True
        elif (goal.x==width-2): goals_on_corners['right']=True
        elif (goal.y==1): goals_on_corners['up']=True
        elif (goal.y==height-2): goals_on_corners['down']=True

   # Caching
    # cache=problem.cache() 
    # cache['goals_on_corners']=None

    # ############################################################Step (1) Check Deadlocked states ##########################################################################
    # Loop Over the Crates to Check DeadLocks
    for crate in crates:
        # To reach a dead lock of course the crate that is thought to causing a dead lock must not be places on a goal :D
        if(Point(crate.x,crate.y) not in goals): # This point isn't a goal



            # Case(3): Crate on Edge and no goal on that edge
            #Left
            '''
            ########
            #      #
            #    @ #
            #     .#
            #$     #
            #      #
            ########

            Then it is at the left most and i can't get it to the right @ all :(
            '''
            if(crate.x==1 and not goals_on_corners['left']):
                # print("Empty Left Side")
                return sys.float_info.max
            
            #Up
            '''same as test case above but with the upper wall'''
            if(crate.y==1 and not goals_on_corners['up']):
                # print("Empty Up Side")
                return sys.float_info.max
            
            # Right
            '''same as test case above but with the right wall'''
            if(crate.x==width-2 and not goals_on_corners['right']):
                # print("Empty Right Side")
                return sys.float_info.max
            
            # Down
            '''same as test case above but with the Down wall'''
            if(crate.y==height-2 and not goals_on_corners['down']):
                # print("Empty Down Side")
                return sys.float_info.max
            


            # #######
            # #     #
            # #     #
            # #  @  #
            # #  #  #
            # #.$$. #
            # #######
            # if()
            



            # Case(1): Crate is in a corner
            '''
            ########
            #      #
            #    @ #
            #     .#
            #      #
            #$     #
            ########

            Then crate can't be moved an y more --> it is also not on a goal due to the first check we have added above to check for the crate causing deadlock if it isn't on a goal
            '''
            if(Point(crate.x-1,crate.y) not in walkable and Point(crate.x,crate.y-1) not in walkable and Point(crate.x-1,crate.y-1) not in walkable):
                # print("Corner(1)")
                return sys.float_info.max
            
            '''same as test case above but corner 2'''
            if(Point(crate.x+1,crate.y) not in walkable and Point(crate.x,crate.y-1) not in walkable and Point(crate.x+1,crate.y-1) not in walkable):
                # print("Corner(2)")
                return sys.float_info.max
            
            '''same as test case above but corner 3'''            
            if(Point(crate.x+1,crate.y) not in walkable and Point(crate.x,crate.y+1) not in walkable and Point(crate.x+1,crate.y+1) not in walkable):
                # print("Corner(3)")
                return sys.float_info.max
            
            '''same as test case above but corner 4'''
            if(Point(crate.x-1,crate.y) not in walkable and Point(crate.x,crate.y+1) not in walkable and Point(crate.x-1,crate.y+1) not in walkable):
                # print("Corner(4)")
                return sys.float_info.max
            



            # Case(2): Trapped between 3 and this point isn't a goal :D
            '''
             #
            #$
             #
            
            or 
             #
            $$
             #
            
            I can't move 2 together
            '''            
            if((Point(crate.x-1,crate.y) not in walkable or Point(crate.x-1,crate.y) in crates )and (Point(crate.x,crate.y-1) not in walkable  or Point(crate.x,crate.y-1) in crates) and (Point(crate.x,crate.y+1) not in walkable  or Point(crate.x,crate.y+1) in crates )):
                # print("Trap(1)")
                return sys.float_info.max
            
            if((Point(crate.x+1,crate.y) not in walkable or Point(crate.x+1,crate.y)  in crates) and (Point(crate.x,crate.y-1) not in walkable or Point(crate.x,crate.y-1) in crates) and (Point(crate.x,crate.y+1) not in walkable or Point(crate.x,crate.y+1) in crates)):
                # print("Trap(2)")
                return sys.float_info.max

            if((Point(crate.x-1,crate.y) not in walkable or Point(crate.x-1,crate.y) in crates) and (Point(crate.x+1,crate.y) not in walkable or Point(crate.x+1,crate.y) in crates) and (Point(crate.x,crate.y+1) not in walkable or Point(crate.x,crate.y+1) in crates)):
                # print("Trap(3)")
                return sys.float_info.max
            
            if((Point(crate.x-1,crate.y) not in walkable or Point(crate.x-1,crate.y) in crates) and (Point(crate.x+1,crate.y) not in walkable or Point(crate.x+1,crate.y) in crates) and (Point(crate.x,crate.y-1) not in walkable or Point(crate.x,crate.y-1) in crates)):
                # print("Trap(4)")
                return sys.float_info.max
            

    ############################################################Step (2) Check Deadlocked states ##########################################################################
    heuristic = 0
    # The heuristic will be the sum of min distances between each crate and its nearest Goal :D  ==> The smaller the heuristic the nearer i am to the goal State <3
    '''
    #######
    #     #
    #     #
    #     #
    # $.  #
    #  $ .#
    #######
    In this case the cost is 3    but my heuristic is  just 2  because both crates will be assigned to the goal nearest them which is logic for the heuristic to be less than the actual
    cost 
    Another way i have thought about is assigning one crate to a goal and other to another goal(not the same goal used by the one) but by this i have got overestimation bec in some cases 
    heuristic is more thant the actual cost meaning theta the heuristic function isn't admissable
    because it depends on the order of the crates being assigned to the goal for ex 
    #######
    #     #
    # $   #
    # @$. #
    #. #$ #
    #.$ . #
    #######

    By luck $ at (4,4) is assigned to goal (4,3) because it is nearest to it than (4,6) that's fine but when it is order of $ at (3,3) the nearest non assign goal is at (4,6) bec
    the one near it is taken by the $ came first ==> so in that case h =8 although cost is 6 overestimation 
    So to get intuition simply accept multiple assignment of crates to teh same goal [THAT IS HUBRISTIC :D]
    '''
    for crate in crates:
        min_distance = min(manhattan_distance(goal,crate) for goal in goals)  # Get manhattan_distance between caret and the nearest goal
        heuristic += min_distance
    return heuristic


    NotImplemented()

    #     __slots__ = ("width", "height", "walkable", "goals")
    # width: int
    # height: int
    # walkable: FrozenSet[Point]
    # goals: FrozenSet[Point]
