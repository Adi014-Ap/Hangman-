import random
import string

class AIGuesser:
    def __init__(self, word_list):
        self.word_list = word_list
        self.possible_words = list(word_list)
        self.guessed_letters = set()
        self.incorrect_guesses = 0
        self.current_pattern = []

    def reset(self):
        self.possible_words = list(self.word_list)
        self.guessed_letters = set()
        self.incorrect_guesses = 0
        self.current_pattern = []

    def make_guess(self, display_word):
        # Update current pattern based on display_word
        self.current_pattern = [letter if letter != '_' else None for letter in display_word.replace(' ', '')]

        # Filter possible words based on current pattern and guessed letters
        self.possible_words = [word for word in self.possible_words if self._matches_pattern(word)]

        # If no possible words left, or AI has made too many incorrect guesses, fallback to random valid letter
        if not self.possible_words or self.incorrect_guesses >= 6:
            available_letters = list(set(string.ascii_lowercase) - self.guessed_letters)
            if available_letters:
                guess = random.choice(available_letters)
                self.guessed_letters.add(guess)
                return guess
            return None # No more letters to guess

        # Count letter frequency in remaining possible words
        letter_frequency = {}
        for word in self.possible_words:
            for letter in word:
                if letter not in self.guessed_letters:
                    letter_frequency[letter] = letter_frequency.get(letter, 0) + 1

        # If no new letters to guess among possible words (e.g. all letters already guessed)
        if not letter_frequency:
            available_letters = list(set(string.ascii_lowercase) - self.guessed_letters)
            if available_letters:
                guess = random.choice(available_letters)
                self.guessed_letters.add(guess)
                return guess
            return None

        # Choose the most frequent letter that hasn't been guessed
        best_guess = max(letter_frequency, key=letter_frequency.get)
        self.guessed_letters.add(best_guess)
        return best_guess

    def _matches_pattern(self, word):
        if len(word) != len(self.current_pattern):
            return False
        for i, letter_pattern in enumerate(self.current_pattern):
            if letter_pattern is not None and letter_pattern != word[i]:
                return False
            if word[i] in self.guessed_letters and letter_pattern is None: # Guessed incorrect letter, but word contains it
                return False
        # Ensure the word does not contain any incorrectly guessed letters that are not in the pattern
        for guessed_letter in self.guessed_letters:
            if guessed_letter not in self.word_list[0] and guessed_letter in word:
                return False
        return True

    def inform_of_guess_result(self, guess, is_correct, display_word):
        if not is_correct:
            self.incorrect_guesses += 1
        # Re-filter words based on the outcome of the guess
        if is_correct:
            self.possible_words = [word for word in self.possible_words if guess in word and self._matches_pattern(word)]
        else:
            self.possible_words = [word for word in self.possible_words if guess not in word and self._matches_pattern(word)]
        self.current_pattern = [letter if letter != '_' else None for letter in display_word.replace(' ', '')]

