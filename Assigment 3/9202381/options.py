# This file contains the options that you should modify to solve Question 2

def question2_1():
    #TODO: Choose options that would lead to the desired results 
    return {
        "noise": 0, #non noisy action 
        "discount_factor": 0.5,
        "living_reward":-1
        # Trials for noise 0.01(fine)  0.1 Failed 0 fine
        # Trials for discount 1   --> Failed
        # Trials for  living_reward --> he kept making moving collecting rewards not reaching goal (infinite loop)
        # living_reward--> 0 so he still keeps looping 

    }

def question2_2():
    #TODO: Choose options that would lead to the desired results
    return {
        "noise": 0.2,  # make action noisy  VIP
        "discount_factor": 0.5,
        "living_reward": -1
    }

def question2_3():
    #TODO: Choose options that would lead to the desired results
    return {
        "noise": 0,  # the action must not be noisy
        "discount_factor": 1,  # discount factor =1 so that he reaches 10 not 1 :D
        "living_reward": -1
    }

def question2_4():
    #TODO: Choose options that would lead to the desired results
        #same as above for the case of discount factor but must make noisy
        return {
        "noise": 0.2,
        "discount_factor": 1,
        "living_reward": -0.1  # after thinking and trying a lot the key is in the living reward
    }

def question2_5():
    #TODO: Choose options that would lead to the desired results
    # Make reward of living zero more than reward of any terminal state
    return {
        "noise": 0.5, # increase noise to solve problem of being going to a wall more than falling in terminal
        "discount_factor": 1,
        "living_reward": 15
    }

def question2_6():
    #TODO: Choose options that would lead to the desired results
    return {
        "noise": 0.1,
        "discount_factor": 1,
        "living_reward": -50  # reward of living very bad death is better for him
    }