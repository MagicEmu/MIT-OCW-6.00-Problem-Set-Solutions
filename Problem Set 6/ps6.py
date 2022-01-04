import random
import string
from copy import copy
import time

VOWELS = 'aeiou'
CONSONANTS = 'bcdfghjklmnpqrstvwxyz'
HAND_SIZE = 7
points_dict = {}
rearrange_dict = {}

SCRABBLE_LETTER_VALUES = {
    'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4, 'i': 1, 'j': 8, 'k': 5, 'l': 1, 'm': 3, 'n': 1, 'o': 1, 'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10
}

# -----------------------------------
# Helper code
# (you don't need to understand this helper code)

WORDLIST_FILENAME = "words.txt"

def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.append(line.strip().lower())
    print("  ", len(wordlist), "words loaded.")
    return wordlist

def get_frequency_dict(sequence):
    """
    Returns a dictionary where the keys are elements of the sequence
    and the values are integer counts, for the number of times that
    an element is repeated in the sequence.

    sequence: string or list
    return: dictionary
    """
    # freqs: dictionary (element_type -> int)
    freq = {}
    for x in sequence:
        freq[x] = freq.get(x,0) + 1
    return freq


# (end of helper code)
# -----------------------------------

#
# Problem #1: Scoring a word
#
def get_word_score(word, n):
    """
    Returns the score for a word. Assumes the word is a
    valid word.

    The score for a word is the sum of the points for letters
    in the word, plus 50 points if all n letters are used on
    the first go.

    Letters are scored as in Scrabble; A is worth 1, B is
    worth 3, C is worth 3, D is worth 2, E is worth 1, and so on.

    word: string (lowercase letters)
    returns: int >= 0
    """
    score = 0
    for letter in word:
        score += SCRABBLE_LETTER_VALUES.get(letter, 0)
    if len(word) == n:
        score += 50
    return score

#
# Make sure you understand how this function works and what it does!
#
def display_hand(hand):
    """
    Displays the letters currently in the hand.

    For example:
       display_hand({'a':1, 'x':2, 'l':3, 'e':1})
    Should print out something like:
       a x x l l l e
    The order of the letters is unimportant.

    hand: dictionary (string -> int)
    """
    for letter in hand.keys():
        for j in range(hand[letter]):
            print(letter, end = ' ')               # print all on the same line
    print()                             # print an empty line

#
# Make sure you understand how this function works and what it does!
#
def deal_hand(n):
    """
    Returns a random hand containing n lowercase letters.
    At least n/3 the letters in the hand should be VOWELS.

    Hands are represented as dictionaries. The keys are
    letters and the values are the number of times the
    particular letter is repeated in that hand.

    n: int >= 0
    returns: dictionary (string -> int)
    """
    hand={}
    num_vowels = n//3
    
    for i in range(num_vowels):
        x = VOWELS[random.randrange(0,len(VOWELS))]
        hand[x] = hand.get(x, 0) + 1
        
    for i in range(num_vowels, n):    
        x = CONSONANTS[random.randrange(0,len(CONSONANTS))]
        hand[x] = hand.get(x, 0) + 1
        
    return hand

#
# Problem #2: Update a hand by removing letters
#
def update_hand(hand, word):
    """
    Assumes that 'hand' has all the letters in word.
    In other words, this assumes that however many times
    a letter appears in 'word', 'hand' has at least as
    many of that letter in it. 

    Updates the hand: uses up the letters in the given word
    and returns the new hand, without those letters in it.

    Has no side effects: does not mutate hand.

    word: string
    hand: dictionary (string -> int)    
    returns: dictionary (string -> int)
    """
    for letter in word:
        hand[letter] = hand[letter] - 1
        if hand[letter] == 0:
            hand.pop(letter)
    return hand

#
# Problem #3: Test word validity
#
def is_valid_word(word, hand, points_dict):
    """
    Returns True if word is in the word_list and is entirely
    composed of letters in the hand. Otherwise, returns False.
    Does not mutate hand or word_list.
    
    word: string
    hand: dictionary (string -> int)
    word_list: list of lowercase strings
    """
    amount = hand.copy()
    if word not in points_dict:
        return False
    for letter in word:
        if letter not in amount or amount[letter] == 0:
            return False
        else:
            amount[letter] -= 1
    return True

def get_time_limit(points_dict, k):
    """
    Return the time limit for the computer player as a function of the
    multiplier k.
    points_dict should be the same dictionary that is created by
    get_words_to_points.
    """
    start_time = time.time()
    # Do some computation. The only purpose of the computation is so we can
    # figure out how long your computer takes to perform a known task.
    for word in points_dict:
        get_frequency_dict(word)
        get_word_score(word, HAND_SIZE)
    end_time = time.time()
    return (end_time - start_time) * k

def get_words_to_points(word_list):
    for word in word_list:
        score = 0
        for letter in word:
            score += SCRABBLE_LETTER_VALUES[letter]
        points_dict[word] = score

def get_word_rearrangements(word_list):
    for word in word_list:
        char_list = []
        my_string = ''
        for char in word:
            char_list.append(char)
        char_list.sort()
        for each in range(len(char_list)):
            my_string += char_list[each]
        rearrange_dict[my_string] = word

def build_substrings(string):
    result = []
    if len(string) == 1:
        result.append(string)
    else:
        for substring in build_substrings(string[:-1]):
            result.append(substring)
            substring = substring + string[-1]
            result.append(substring)
        result.append(string[-1])
        result = list(set(result))
        result.sort()
    return result

def pick_best_word(hand, points_dict):
    for word in sorted(points_dict, key=points_dict.get, reverse=True):
        if is_valid_word(word, hand, points_dict):
            return word
    return '.'

def pick_best_word_faster(hand, rearrange_dict):
    hand_string = ''
    for each in hand:
        if hand[each] > 0:
            hand_string += each * hand[each]
    best_word = ''
    best_word_score = 0
    subsets = build_substrings(hand_string)
    subset_value = 0
    for subset in subsets:
        sorted_subset = sorted(subset)
        if sorted_subset in rearrange_dict:
            subset_value = get_word_score(sorted_subset, HAND_SIZE)
            if subset_value > best_word_score:
                best_word = rearrange_dict[sorted_subset]
                best_word_score = subset_value
    if best_word_score > 0:
        return best_word
    else:
        return '.'

#
# Problem #4: Playing a hand
#
def play_hand(hand, word_list):
    """
    Allows the user to play the given hand, as follows:

    * The hand is displayed.
    
    * The user may input a word.

    * An invalid word is rejected, and a message is displayed asking
      the user to choose another word.

    * When a valid word is entered, it uses up letters from the hand.

    * After every valid word: the score for that word and the total
      score so far are displayed, the remaining letters in the hand 
      are displayed, and the user is asked to input another word.

    * The sum of the word scores is displayed when the hand finishes.

    * The hand finishes when there are no more unused letters.
      The user can also finish playing the hand by inputing a single
      period (the string '.') instead of a word.

    * The final score is displayed.

      hand: dictionary (string -> int)
      word_list: list of lowercase strings
    """
    score = 0
    limit = int(input("Enter time limit, in seconds, for players: "))
    curr = limit
    while hand:
        display_hand(hand)
        start = time.time()
        word = str(input("Enter word, or a . to indicate that you are finished: "))
        if word == ".":
            break
        stop = False
        while not is_valid_word(word, hand, points_dict):
            word = str(input("Enter word, or a . to indicate that you are finished: "))
            if word == ".":
                stop = True
                break
        if stop == True:
            break
        end = time.time()
        took = round(end-start, 2)
        curr -= took
        if curr < 0:
            print("Total time exceeds", limit, "seconds.")
            break
        if took == 0.00:
            took = 0.01
        update_hand(hand, word)
        temp = round(get_word_score(word, HAND_SIZE)/took, 2)
        print("It took", took, "seconds to provide an answer")
        print("You have", curr, "seconds remaining.")
        print(word, "earned", temp, "points. Total:", score, "points")
        score += temp
    print("You scored", score, "points.")


def computer_play_hand(hand, word_list):
    """
    Allows the user to play the given hand, as follows:

    * The hand is displayed.

    * The user may input a word.

    * An invalid word is rejected, and a message is displayed asking
      the user to choose another word.

    * When a valid word is entered, it uses up letters from the hand.

    * After every valid word: the score for that word and the total
      score so far are displayed, the remaining letters in the hand
      are displayed, and the user is asked to input another word.

    * The sum of the word scores is displayed when the hand finishes.

    * The hand finishes when there are no more unused letters.
      The user can also finish playing the hand by inputing a single
      period (the string '.') instead of a word.

    * The final score is displayed.

      hand: dictionary (string -> int)
      word_list: list of lowercase strings
    """
    score = 0
    get_words_to_points(word_list)
    limit = get_time_limit(points_dict, 1)
    curr = limit
    while hand:
        display_hand(hand)
        start = time.time()
        word = pick_best_word(hand, points_dict)
        if word == ".":
            break
        stop = False
        while not is_valid_word(word, hand, points_dict):
            word = pick_best_word(hand, points_dict)
            if word == ".":
                stop = True
                break
        if stop == True:
            break
        end = time.time()
        took = round(end - start, 2)
        curr -= took
        if curr < 0:
            print("Total time exceeds", limit, "seconds.")
            break
        curr = round(curr, 2)
        if took == 0.00:
            took = 0.01
        update_hand(hand, word)
        temp = round(get_word_score(word, HAND_SIZE)/took, 2)
        print("It took", took, "seconds to provide an answer")
        print("Computer has", curr, "seconds remaining.")
        print(word, "earned", temp, "points. Total:", score, "points")
        score += temp
    print("Computer scored", score, "points.")

#
# Problem #5: Playing a game
# Make sure you understand how this code works!
# 
def play_game(word_list):
    """
    Allow the user to play an arbitrary number of hands.

    * Asks the user to input 'n' or 'r' or 'e'.

    * If the user inputs 'n', let the user play a new (random) hand.
      When done playing the hand, ask the 'n' or 'e' question again.

    * If the user inputs 'r', let the user play the last hand again.

    * If the user inputs 'e', exit the game.

    * If the user inputs anything else, ask them again.
    """
    hand = deal_hand(HAND_SIZE) # random init
    while True:
        cmd = input('Enter n to deal a new hand, r to replay the last hand, c to let computer play, or e to end game: ')
        if cmd == 'n':
            hand = deal_hand(HAND_SIZE)
            play_hand(copy(hand), word_list)
            print
        elif cmd == 'r':
            play_hand(copy(hand), word_list)
            print
        elif cmd == 'e':
            break
        elif cmd == 'c':
            computer_play_hand(copy(hand), word_list)
            print
        else:
            print("Invalid command.")

#
# Build data structures used for entire session and play game
#
if __name__ == '__main__':
    word_list = load_words()
    play_game(word_list)

## Problem 5 ##
     # your response here.
     # as many lines as you want.
# pick_best_word is linear
# pick_best_word_faster is