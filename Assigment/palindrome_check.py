import utils


def palindrome_check(string: str) -> bool:
    '''
    This function takes string and returns where a string is a palindrome or not
    A palindrome is a string that does not change if read from left to right or from right to left
    Assume that empty strings are palindromes
    '''
    # TODO: ADD YOUR CODE HERE
    # utils.NotImplemented()
    for i in range(len(string)):
        if (string[i] != string[-1*(i+1)]):
            return False
    return True
