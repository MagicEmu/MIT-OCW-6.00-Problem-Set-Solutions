import random
import difflib

# -----------------------------------
# Helper code
# (you don't need to understand this helper code)
import string

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

# Actually load the dictionary of words and point to it with 
# the wordlist variable so that it can be accessed from anywhere
# in the program.
wordlist = load_words()

def ghost():
    print("Welcome to Ghost!")
    print("Player 1 goes first")
    turn = False
    curr = ""
    while len(curr) <= 3 or curr not in wordlist:
        print("Current word fragment: " + curr)
        if not turn and curr != "":
            print("Player 2's Turn.")
            turn = True
            letter = str(input("Player 2 says letter: "))
            curr += letter
        else:
            if curr != "":
                print("Player 1's Turn.")
            turn = False
            letter = str(input("Player 1 says letter: "))
            curr += letter
        curr.lower()
        if len(curr) > 3 and curr in wordlist:
            if turn == False:
                print("Player 1 loses because " + curr + " is a word!")
                print("Player 2 wins!")
                break
            else:
                print("Player 2 loses because " + curr + " is a word!")
                print("Player 1 wins!")
                break
        hasWords = False
        for word in wordlist:
            if word[:len(curr)] == curr:
                hasWords = True
                break
        if hasWords == False:
            if turn == False:
                print("Player 1 loses because no word begins with " + curr)
                print("Player 2 wins!")
                break
            else:
                print("Player 2 loses because no word begins with " + curr)
                print("Player 1 wins!")
                break

ghost()