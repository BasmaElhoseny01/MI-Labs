from typing import Tuple, List
import utils
from helpers.test_tools import read_text_file, read_word_list
import sys
'''
    The DecipherResult is the type defintion for a tuple containing:
    - The deciphered text (string).
    - The shift of the cipher (non-negative integer).
        Assume that the shift is always to the right (in the direction from 'a' to 'b' to 'c' and so on).
        So if you return 1, that means that the text was ciphered by shifting it 1 to the right, and that you deciphered the text by shifting it 1 to the left.
    - The number of words in the deciphered text that are not in the dictionary (non-negative integer).
'''
DechiperResult = Tuple[str, int, int]


def caesar_dechiper(ciphered: str, dictionary: List[str]) -> DechiperResult:
    '''
        This function takes the ciphered text (string)  and the dictionary (a list of strings where each string is a word).
        It should return a DechiperResult (see above for more info) with the deciphered text, the cipher shift, and the number of deciphered words that are not in the dictionary. 
    '''
    # utils.NotImplemented()
    freq_array = {}
    max_count = 0
    max_char = ''
    a_candidate = -1
    for index, char in enumerate(ciphered):
        if ((index == 0 or ciphered[index-1] == " ") and (index == len(ciphered)-1 or ciphered[index+1] == " ")):
            a_candidate = char
            break

        if char == ' ':
            continue
        freq_array[char] = freq_array.get(char, 0)+1
        if (freq_array[char] > max_count):
            max_count = freq_array[char]
            max_char = char

    if (a_candidate != -1):
        # Only 1 possible shift which is mapping thus alone letter to a :D
        possible_shifts = [(ord(a_candidate) - ord(ch)) %
                           26 for ch in ['a']]
    else:
        possible_shifts = [(ord(max_char) - ord(ch)) %
                           26 for ch in ['e', 't', 'a', 'o']]

    dechiper = ""
    min_non_intersect_count = sys.maxsize
    shift = 0
    # for i in range(26): # Brute Force
    for i in possible_shifts: # 4 or 1 possible shifts  
        result = ''.join([chr(((ord(char) - ord('a') - i) % 26) + ord('a'))
                         if ('a' <= char <= 'z') else (char) for char in ciphered])
        count_non_intersect = 0
        non_intersecting_words = [
            word for word in result.split() if word not in dictionary]
        count_non_intersect = len(non_intersecting_words)

        if (count_non_intersect < min_non_intersect_count):
            min_non_intersect_count = count_non_intersect
            dechiper = result
            shift = i
    return (dechiper, shift, min_non_intersect_count)
