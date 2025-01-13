from flask import Flask, render_template, request, jsonify
import time
import random

app = Flask(__name__)

# Load words from the file
def load_words():
    with open('words_alpha.txt') as f:
        words = f.read().splitlines()
    return words

WORDS = load_words()

# Global game state
class SpellingBeeGame:
    def __init__(self, bold_letter, letters):
        self.bold_letter = bold_letter
        self.letters = letters
        self.todays_letters = self.bold_letter + self.letters
        self.reset_game()

    def reset_game(self):
        self.guessed_words = []
        self.score = 0
        self.start_time = time.time()
        self.possible_words = self.get_possible_words()

    def is_valid(self, word):
        if len(word) >= 4 and self.bold_letter in word:
            return all(letter in self.todays_letters for letter in word)
        return False

    def get_possible_words(self):
        possible_words = []
        for word in WORDS:
            if len(word) >= 4 and all(letter in self.todays_letters for letter in word):
                possible_words.append(word)
        return possible_words

    def check_word(self, word):
        if word in self.guessed_words:
            return {"result": "already_guessed", "score": self.score, "guessed_words": self.guessed_words}

        if not self.is_valid(word):
            return {"result": "invalid", "score": self.score, "guessed_words": self.guessed_words}

        self.guessed_words.append(word)
        self.score += len(word)

        if len(self.guessed_words) == len(self.possible_words):
            return {"result": "game_won", "score": self.score, "guessed_words": self.guessed_words}

        return {"result": "valid", "score": self.score, "guessed_words": self.guessed_words}

# Initialize game state
game = SpellingBeeGame(bold_letter="e", letters="xmplds")

@app.route('/')
def index():
    game.reset_game()  # Reset the game state when the page is loaded
    return render_template('index.html', game=game)

@app.route('/submit_word', methods=['POST'])
def submit_word():
    word = request.json.get('word', '').strip().lower()
    result = game.check_word(word)
    return jsonify(result)

@app.route('/shuffle', methods=['POST'])
def shuffle_letters():
    letters_list = list(game.todays_letters)
    random.shuffle(letters_list)
    game.todays_letters = ''.join(letters_list)
    return jsonify({"letters": game.todays_letters})

@app.route('/hint', methods=['GET'])
def hint():
    return jsonify({
        "four_letter_count": len([w for w in game.possible_words if len(w) == 4]),
        "five_letter_count": len([w for w in game.possible_words if len(w) == 5]),
        "six_letter_count": len([w for w in game.possible_words if len(w) == 6]),
        "seven_letter_count": len([w for w in game.possible_words if len(w) == 7]),
        "start_with_bold": len([w for w in game.possible_words if w.startswith(game.bold_letter)]),
    })

@app.route('/show_all_words', methods=['GET'])
def show_all_words():
    return jsonify({"words": game.possible_words})

if __name__ == "__main__":
    app.run(debug=True)
