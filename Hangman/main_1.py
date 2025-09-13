import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import random
import os

# Word list
WORDS = ["python", "hangman", "tkinter", "programming", "developer", "function"]

class HangmanGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Hangman Game")
        self.root.state("zoomed")
        self.root.resizable(True, True)

        # Load background image
        self.bg_image = Image.open("background.jpg")
        self.bg_image = self.bg_image.resize((self.root.winfo_screenwidth(), self.root.winfo_screenheight()))
        self.bg_image = ImageTk.PhotoImage(self.bg_image)

        self.bg_label = tk.Label(self.root, image=self.bg_image)
        self.bg_label.place(relwidth=1, relheight=1)

        # Game state
        self.word = random.choice(WORDS)
        self.guessed = []
        self.wrong_guesses = 0
        self.hint_count = 0
        self.hint = None

        self.load_images()
        self.setup_gui()

    def load_images(self):
        self.images = []
        for i in range(7):
            img_path = os.path.join("images", f"stage{i}.png")
            img = Image.open(img_path).resize((250, 250))
            self.images.append(ImageTk.PhotoImage(img))

    def setup_gui(self):
        self.main_frame = tk.Frame(self.root, bg="#ccffcc", bd=10)
        self.main_frame.pack(expand=True)

        # Title
        self.title_label = tk.Label(self.main_frame, text="🎯 Hangman Game 🎯", font=("Arial", 45, "bold"), fg="#004d00", bg="#ccffcc")
        self.title_label.pack(pady=10)

        # Hangman image
        self.image_label = tk.Label(self.main_frame, image=self.images[0], bg="#ccffcc")
        self.image_label.pack(pady=20)

        # Word display
        self.word_label = tk.Label(self.main_frame, text=self.get_display_word(), font=("Courier", 40), fg="#003300", bg="#ccffcc")
        self.word_label.pack(pady=10)

        # Hint label
        self.hint_label = tk.Label(self.main_frame, text="Hint: No hint yet", font=("Arial", 20), fg="#cc6600", bg="#ccffcc")
        self.hint_label.pack(pady=5)

        # Entry box
        self.entry = tk.Entry(self.main_frame, font=("Arial", 28), width=5, justify="center", bg="#ffffff", fg="#000000", bd=5)
        self.entry.pack(pady=15)

        # Buttons
        button_frame = tk.Frame(self.main_frame, bg="#ccffcc")
        button_frame.pack(pady=10)

        self.guess_button = tk.Button(button_frame, text="Guess", command=self.make_guess,
                                      font=("Arial", 18, "bold"), bg="#4CAF50", fg="white", padx=20, pady=10)
        self.guess_button.grid(row=0, column=0, padx=10)

        self.reset_button = tk.Button(button_frame, text="Restart", command=self.reset_game,
                                      font=("Arial", 18, "bold"), bg="#FF5722", fg="white", padx=20, pady=10)
        self.reset_button.grid(row=0, column=1, padx=10)

        self.exit_button = tk.Button(button_frame, text="Exit", command=self.root.quit,
                                     font=("Arial", 18, "bold"), bg="gray", fg="white", padx=20, pady=10)
        self.exit_button.grid(row=0, column=2, padx=10)

    def get_display_word(self):
        return " ".join([letter if letter in self.guessed else "_" for letter in self.word])

    def get_hint(self):
        if self.hint_count >= 3:
            return "No more hints!"
        unguessed_letters = [l for l in self.word if l not in self.guessed]
        if unguessed_letters:
            self.hint_count += 1
            return random.choice(unguessed_letters)
        return "No more hints!"

    def make_guess(self):
        guess = self.entry.get().lower()
        self.entry.delete(0, tk.END)

        if not guess or len(guess) != 1 or not guess.isalpha():
            messagebox.showwarning("Invalid Input", "Please enter a single letter.")
            return

        if guess in self.guessed:
            messagebox.showinfo("Already Guessed", f"You already guessed '{guess}'")
            return

        self.guessed.append(guess)

        if guess in self.word:
            self.word_label.config(text=self.get_display_word())
            if all(letter in self.guessed for letter in self.word):
                messagebox.showinfo("🎉 Congratulations!", f"You won! The word was: {self.word}")
                # Optional: self.root.after(100, self.reset_game) to auto-restart on win
        else:
            self.wrong_guesses += 1
            self.image_label.config(image=self.images[self.wrong_guesses])
            self.hint = self.get_hint()
            self.hint_label.config(text=f"Hint: {self.hint}")

            if self.wrong_guesses == 6:
                messagebox.showinfo("💀 Game Over", f"You lost! The word was: {self.word}")
                self.root.after(100, self.reset_game)  # Delayed restart after losing

    def reset_game(self):
        self.word = random.choice(WORDS)
        self.guessed = []
        self.wrong_guesses = 0
        self.hint_count = 0
        self.hint = None

        self.image_label.config(image=self.images[0])
        self.word_label.config(text=self.get_display_word())
        self.hint_label.config(text="Hint: No hint yet")
        self.entry.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    game = HangmanGame(root)
    root.mainloop()
