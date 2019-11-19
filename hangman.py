import random
import string

letters = string.ascii_lowercase

def setupGame():

    print("Please set up the following parameters for the game...\n")

    guess_count_control = True
    while guess_count_control:
        no_of_guesses = input("How many guesses should there be? please provide an integer...")
        try:
            no_of_guesses = int(no_of_guesses)
            guess_count_control = False
        except ValueError:
            print("\nPlease provide an integer!")

    return no_of_guesses


def pickWord(words = "words.txt"):
    
    global word_list
    print("\nLoading word list from file...")
    my_file = open(words, "r")

    #split the words in the text file by whitespace
    for words in my_file:
        word_list = words.split(" ")

    print("%s words loaded." %len(word_list))
    print("\nWelcome to the game Hangman!")

    #shuffle the list before picking a word
    random.shuffle(word_list)
    secret_word = word_list[0]
    print("I am thinking of a word that is %s letters long." %len(secret_word))

    return secret_word


def removeGuessfrAlphabet(guess, letters_guessed):
    
    global letters
    letters = letters.replace(guess,"")
    print("\n",guess,"\n")

    if guess != "":
        letters_guessed.append(guess)

    return letters_guessed


def deduceGuess(no_of_guesses):

    no_of_guesses -= 1
    return no_of_guesses


def getGuessedWord(letters_guessed,secret_word):
    
    word_to_display = []

    for letter in secret_word:
        if letter not in letters_guessed:
            word_to_display.append("_")
        else:
            word_to_display.append(letter)

    return " ".join(word_to_display)


def guessSecretWord(secret_word):

    isGameWon = False
    guess_secret_word = input("Please type your guess...")
    if guess_secret_word != secret_word:
        print("\nWrong! The secret word is ... %s" %secret_word)
    else:
        print("\nCongratulations! You win! The secret word is indeed %s" %secret_word)
        isGameWon = True

    return isGameWon


def getSameLengthWords(secret_word):
    
    same_length_words = []
    for word in word_list:
        if len(word) == len(secret_word):
            same_length_words.append(word)
            
    return same_length_words
    

def getHint(secret_word, word_to_display, letters_guessed):

    same_length_words = getSameLengthWords(secret_word)

    word_to_display_dict = {}

    #print(len(same_length_words), "*"*10)
    word_to_display = word_to_display.replace(" ", "")
    for i, letter in enumerate(word_to_display):
        if letter != "_" and letter != " ":
            word_to_display_dict[i] = letter 
    
    matching_letters = list(word_to_display_dict.values())
    letters_not_in = list(set(letters_guessed) - set(matching_letters))

    matching_words = []
    possible_words_dict = {}

    #print(word_to_display_dict, "*"*10)
    for word in same_length_words:
        for i, letter in enumerate(word):
            possible_words_dict[i] = letter

        check_list = [letter in word for letter in letters_not_in]
        if all(item in possible_words_dict.items() for item in word_to_display_dict.items()) and sum(check_list) == 0:
            matching_words.append(word)

    print("\nPotential matches are:")
    for word in matching_words:
        print(word)


def getGuess(no_of_guesses, no_of_hint, letters_guessed, secret_word, no_of_warnings):
    
    isGameWon = None
    guess_type_control = True
    while guess_type_control and isGameWon == None:
        guess = input("Please make a guess... The guess should be a single letter...\
         \nYou can make a guess anytime by typing \"guess\"...\
         \nTo ask for a hint, please type \"hint\"...")
        word_to_display = getGuessedWord(letters_guessed, secret_word)

        #If the user wants to make a guess
        if guess.lower() == "guess":
            isGameWon = guessSecretWord(secret_word)

        elif guess.lower() == "hint" and no_of_hint != 0:
            getHint(secret_word, word_to_display, letters_guessed)
            no_of_hint -= 1
        elif guess.lower() == "hint" and no_of_hint == 0:
            print("\n****************************\
                   \nYou are out of hints, sorry!...\
                   \n****************************\n")

        #If the guess is a valid guess
        elif guess.lower() in letters:
            guess_type_control = False

            if guess != "":
                no_of_guesses = deduceGuess(no_of_guesses)
            letters_guessed = removeGuessfrAlphabet(guess, letters_guessed)
            word_to_display = getGuessedWord(letters_guessed, secret_word)

            if guess == "":
                pass
            elif guess in secret_word:
                print("Good guess: %s" %word_to_display)
            else:
                print("Oops! That letter is not in my word: %s" %word_to_display)

        elif guess.lower() in letters_guessed and no_of_warnings > 1:
            no_of_warnings -= 1
            print("\nOops! That is not a valid letter. You have guessed -{0}- before. You now have {1} warnings: {2}".\
            format(guess, no_of_warnings,word_to_display))

        else:
            if no_of_warnings > 1:
                no_of_warnings -= 1
                print("\nOops! That is not a valid letter. Invalid input! You now have {0} warnings: {1}".\
                format(no_of_warnings ,word_to_display))
            else:
                no_of_guesses = deduceGuess(no_of_guesses)
                print("You have used all of your warnings and therefore lost a guess. Remaining guesses %s" %no_of_guesses)
                no_of_warnings = 3
                if no_of_guesses == 0:
                    print("You ran out of guesses!...")
                    isGameWon = guessSecretWord(secret_word)

    return no_of_guesses, no_of_hint, letters_guessed, no_of_warnings, isGameWon


def initGame():
    
    no_of_warnings = 3
    letters_guessed = []
    no_of_guesses = setupGame()
    secret_word = pickWord()
    isGameWon = None
    no_of_hint = 1

    while no_of_guesses > 0 and no_of_warnings > 0 and isGameWon is None:
        print("\nRemaining letters are: ---%s---" %letters)
        print("Your guesses: %s" %letters_guessed)
        print("You have %s guesses left\n" %no_of_guesses)
        if no_of_hint == 1:
            print("Don't forget you can ask for a hint by typing \"hint\"!...")
        no_of_guesses, no_of_hint, letters_guessed, no_of_warnings, isGameWon = \
        getGuess(no_of_guesses, no_of_hint, letters_guessed, secret_word, no_of_warnings)

        if no_of_guesses == 0 and isGameWon is None:
            guessSecretWord(secret_word)

