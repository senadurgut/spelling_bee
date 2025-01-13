import tkinter as tk
from tkinter import messagebox
import time
import random

class SpellingBee:
    def __init__(self, bold_letter, letters):
        self.bold_letter = bold_letter
        self.letters = letters
        self.todays_letters = self.bold_letter + self.letters

        self.guessed_words = []
        self.score = 0
        self.start_time = time.time()  # Start the chronometer when the game starts

        self.words = self.load_words()

        self.possible_words, self.four_letter_possible_words, self.five_letter_possible_words, self.six_letter_possible_words, self.seven_letter_possible_words = self.get_possible_words()

        self.setup_gui()

    def load_words(self):
        with open('/Users/sena/side_projects/nyt_spelling_bee/words_alpha.txt') as f:
            words = f.read().splitlines()
        return words

    def is_valid(self, word):
        if len(word) >= 4:
            if self.bold_letter not in word:
                return False
            if all(letter in self.todays_letters for letter in word):
                return True
        return False

    def get_possible_words(self):
        possible_words = []
        for word in self.words:
            if len(word) >= 4 and all(letter in self.todays_letters for letter in word):
                possible_words.append(word)

        four_letter_possible_words = [word for word in possible_words if len(word) == 4]
        five_letter_possible_words = [word for word in possible_words if len(word) == 5]
        six_letter_possible_words = [word for word in possible_words if len(word) == 6]
        seven_letter_possible_words = [word for word in possible_words if len(word) == 7]
        return possible_words, four_letter_possible_words, five_letter_possible_words, six_letter_possible_words, seven_letter_possible_words

    def setup_gui(self):
        self.root = tk.Tk()
        self.root.title("Spelling Bee Game")

        # Adjust the canvas size to better fit the hexagons
        self.canvas = tk.Canvas(self.root, width=500, height=500)
        self.canvas.pack()

        # Adjusted coordinates for hexagons (center hexagon is at (250, 250))
        hexagons = [
            (250, 250),  # Center hexagon
            (190, 150), (310, 150),  # Top row
            (140, 250), (360, 250),  # Middle row
            (190, 350), (310, 350)   # Bottom row
        ]

        # Ensure that there are exactly 7 letters to match the 7 hexagons
        if len(self.todays_letters) != 7:
            raise ValueError("There must be exactly 7 letters (1 bold letter and 6 others).")

        # Draw hexagons and place letters
        self.hex_labels = []
        letters = list(self.todays_letters)  # Should be exactly 7 letters
        for i, (x, y) in enumerate(hexagons):
            fill_color = "yellow" if i == 0 else "white"  # Make the center hexagon yellow
            self.hex_labels.append(self.draw_hexagon(x, y, 50, letters[i], fill_color))

        # Entry box for user input
        self.entry = tk.Entry(self.root)
        self.entry.pack(pady=10)

        # Bind the Enter key to the check_word function
        self.entry.bind('<Return>', self.check_word)

        # Buttons for interaction
        self.submit_button = tk.Button(self.root, text="Submit", command=self.check_word)
        self.submit_button.pack(pady=10)

        self.shuffle_button = tk.Button(self.root, text="Shuffle Letters", command=self.shuffle_letters)
        self.shuffle_button.pack(pady=10)

        self.hint_button = tk.Button(self.root, text="Hint", command=self.give_hint)
        self.hint_button.pack(pady=10)

        self.show_words_button = tk.Button(self.root, text="Show All Possible Words", command=self.show_possible_words)
        self.show_words_button.pack(pady=10)
        
        self.quit_button = tk.Button(self.root, text="Quit", command=self.root.quit)
        self.quit_button.pack(pady=10)

        # Display result
        self.result_label = tk.Label(self.root, text="")
        self.result_label.pack(pady=10)
        
        self.show_total_words_button = tk.Button(self.root, text="Show Total Possible Words", command=self.show_total_possible_words)
        self.show_total_words_button.pack(pady=10)

        # Display score
        self.score_label = tk.Label(self.root, text=f"Score: {self.score}")
        self.score_label.pack(pady=10)

        # Display guessed words
        self.guessed_words_label = tk.Label(self.root, text="Guessed words: None")
        self.guessed_words_label.pack(pady=10)

        # Display chronometer
        self.chronometer_label = tk.Label(self.root, text="Time elapsed: 00:00")
        self.chronometer_label.pack(pady=10)

        # Start the chronometer
        self.update_chronometer()

        self.root.mainloop()

    def draw_hexagon(self, x, y, size, letter, fill_color):
        # Calculate vertices of the hexagon
        points = [
            x + size * 0.5, y,
            x + size, y + size * 0.866,
            x + size * 0.5, y + size * 1.732,
            x - size * 0.5, y + size * 1.732,
            x - size, y + size * 0.866,
            x - size * 0.5, y
        ]
        # Draw the hexagon
        self.canvas.create_polygon(points, outline="black", fill=fill_color, width=2)
        # Draw the letter in black
        label_id = self.canvas.create_text(x, y + size * 0.866, text=letter, font=("Helvetica", 24, "bold"), fill="black")
        return label_id

    def shuffle_letters(self):
        # Extract the letters excluding the bold letter
        letters_list = list(self.todays_letters[1:])
        random.shuffle(letters_list)
        
        # Reinsert the bold letter at the start
        self.todays_letters = self.bold_letter + ''.join(letters_list)
        
        self.update_hexagons()


    def update_hexagons(self):
        # Update the letters in the hexagons
        letters = list(self.todays_letters)
        for i, label_id in enumerate(self.hex_labels):
            self.canvas.itemconfig(label_id, text=letters[i])

    def check_word(self, event=None):
        word = self.entry.get().strip().lower()
        self.entry.delete(0, tk.END)

        if word in self.guessed_words:
            self.result_label.config(text=f"You already guessed {word}")
            return
        if len(word) < 4:
            self.result_label.config(text=f"{word} is too short.")
            return

        if not self.is_valid(word):
            self.result_label.config(text=f"{word} is not a valid word.")
            return
        


        if self.is_valid(word):
            self.result_label.config(text=f"{word} is a valid word!")
            self.guessed_words.append(word)
            self.score += len(word)
            self.score_label.config(text=f"Score: {self.score}")
            self.update_guessed_words_label()

        if len(self.guessed_words) == len(self.possible_words):
            messagebox.showinfo("Congratulations", "You guessed all the words!")
            self.root.quit()

    def update_guessed_words_label(self):
        # Sort the guessed words alphabetically
        sorted_guessed_words = sorted(self.guessed_words)
        guessed_words_text = ", ".join(sorted_guessed_words)
        self.guessed_words_label.config(text=f"Guessed words: {guessed_words_text}")

    def show_possible_words(self):
        # Display all possible words in a message box
        possible_words_text = ", ".join(self.possible_words)
        messagebox.showinfo("All Possible Words", f"Possible words: {possible_words_text}")

    def update_chronometer(self):
        elapsed_time = int(time.time() - self.start_time)
        minutes = elapsed_time // 60
        seconds = elapsed_time % 60
        self.chronometer_label.config(text=f"Time elapsed: {minutes:02}:{seconds:02}")
        self.root.after(1000, self.update_chronometer)  # Update every second

    def give_hint(self):
        hint_text = (
            f"Four letter words: {len(self.four_letter_possible_words)}\n"
            f"Five letter words: {len(self.five_letter_possible_words)}\n"
            f"Six letter words: {len(self.six_letter_possible_words)}\n"
            f"Seven letter words: {len(self.seven_letter_possible_words)}\n"
            f"Words that start with {self.bold_letter}: {len([word for word in self.possible_words if word[0] == self.bold_letter])}"
        )
        messagebox.showinfo("Hint", hint_text)
        
    def show_total_possible_words(self):
        total_words = len(self.possible_words)
        messagebox.showinfo("Total Possible Words", f"Total possible words: {total_words}")


if __name__ == "__main__":
    game = SpellingBee(bold_letter="o", letters="kigutn")
