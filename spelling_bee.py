# a demo of the spelling bee game of new york times



# import the necessary packages to load the text file containing the words
import os
import random
import string
import sys


class SpellingBee:
    def __init__(self, bold_letter, letters):
        self.bold_letter = bold_letter
        self.letters = letters
        self.todays_letters = self.bold_letter + self.letters
   
        self.guessed_words = []
        self.score = 0
        
        # load the words from the text file as a list
        def load_words():
            with open('/Users/sena/side_projects/nyt_spelling_bee/words_alpha.txt') as f:
                words = f.read().splitlines()
            return words

        
                
        self.words = load_words()


        def is_valid(word):
            if len(word) >= 4:
                if self.bold_letter not in word:
                    print(f"Missing center letter: {self.bold_letter}")
                    return False
                if all(letter in self.todays_letters for letter in word):
                    return True


        

        #get the words that can be formed from the letters, including the bold letter 
        def get_possible_words():
            possible_words = []
            for word in self.words:
                if len(word)>=4 and all(letter in self.todays_letters for letter in word):
                    possible_words.append(word)
            
            #make a list of 4 letter possible words
            four_letter_possible_words = [word for word in possible_words if len(word) == 4]
            five_letter_possible_words = [word for word in possible_words if len(word) == 5]
            six_letter_possible_words = [word for word in possible_words if len(word) == 6]
            seven_letter_possible_words = [word for word in possible_words if len(word) == 7]
            return possible_words, four_letter_possible_words, five_letter_possible_words, six_letter_possible_words, seven_letter_possible_words
        
        self.four_letter_possible_words = get_possible_words()[1]
        self.five_letter_possible_words = get_possible_words()[2]
        self.six_letter_possible_words = get_possible_words()[3]
        self.seven_letter_possible_words = get_possible_words()[4]
        self.possible_words = get_possible_words()[0]
        print(f"Possible words: {len(self.possible_words)}")

        #get input from the user
        def get_input():
            print(f"Today's letters: {self.todays_letters}")
            print(f"C")
            user_input = input("Enter a word or command: ").strip().lower()

            # Check if the input is a command
            if user_input.startswith('/'):
                command = user_input[1:]  # Remove the leading '/'
                if command == "quit":
                    sys.exit("Thanks for playing!")
                elif command == "hint":
                    return "hint"  # Special keyword to trigger a hint
                else:
                    print(f"Unknown command: {command}")
                    return None
            else:
                return user_input

        
        def give_hint(): #print the number of four, five, six, and seven letter words
            print(f"Four letter words: {len(self.four_letter_possible_words)}")
            print(f"Five letter words: {len(self.five_letter_possible_words)}")
            print(f"Six letter words: {len(self.six_letter_possible_words)}")
            print(f"Seven letter words: {len(self.seven_letter_possible_words)}")
            print(f"Words that start with {self.bold_letter}: {len([word for word in self.possible_words if word[0] == self.bold_letter])}")
                    
        def play():
            while True:
                user_input = get_input()
                if user_input is None:
                    continue
                
                if user_input == "hint":
                    give_hint()
                    continue
                
                word = user_input

                if word in self.guessed_words:
                    print(f"You already guessed {word}")
                    continue
                
                if not is_valid(word):
                    print(f"{word} is not a valid word.")
                    continue
                
                if is_valid(word):
                    print(f"{word} is a valid word!")
                    self.guessed_words.append(word)
                    self.score += len(word)

                print(f"Score: {self.score}")
                print(f"Number of words left: {len(self.possible_words) - len(self.guessed_words)}")
                print('-----------------------------------')

                if len(self.guessed_words) == len(self.possible_words):
                    print("You guessed all the words!")
                    break

        play()