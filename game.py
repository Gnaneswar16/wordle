from collections import Counter

# Game constants
MAX_GUESSES = 6
WORD_LENGTH = 5


class GuessResult:
    """Represents the result of evaluating a single Wordle guess."""

    def __init__(self, guess: str, statuses: list[str]) -> None:
        self.guess = guess
        self.statuses = statuses

    def __str__(self) -> str:
        """Display the guessed letters and their corresponding results."""

        symbols = {
            "correct": "✓",
            "present": "~",
            "absent": "✗",
        }

        letters = "  ".join(self.guess.upper())
        results = "  ".join(symbols[status] for status in self.statuses)

        return f"{letters}\n{results}"


def evaluate_guess(secret: str, guess: str) -> GuessResult:
    """
    Compare the secret word with the guessed word.

    Correct-position matches are identified first.
    Remaining letters are then checked for present matches.
    Duplicate letters are handled using letter counts.
    """

    if len(secret) != WORD_LENGTH or len(guess) != WORD_LENGTH:
        raise ValueError("Secret and guess must contain exactly 5 letters.")

    # Initially, assume every letter is absent.
    statuses = ["absent"] * WORD_LENGTH

    # Count the occurrences of each letter in the secret word.
    remaining_letters = Counter(secret)

    # PASS 1: Identify correct-position matches.
    for index in range(WORD_LENGTH):
        if guess[index] == secret[index]:
            statuses[index] = "correct"

            # Consume this occurrence of the letter.
            remaining_letters[guess[index]] -= 1

    # PASS 2: Identify present letters in incorrect positions.
    for index in range(WORD_LENGTH):
        if statuses[index] == "correct":
            continue

        letter = guess[index]

        if remaining_letters[letter] > 0:
            statuses[index] = "present"
            remaining_letters[letter] -= 1

    return GuessResult(guess, statuses)


class Game:
    """Manage a single round of Wordle."""

    def __init__(self, secret_word: str, word_list: list[str]) -> None:
        self.secret_word = secret_word.lower()
        self.word_list = [word.lower() for word in word_list]
        self.guesses: list[GuessResult] = []

        if len(self.secret_word) != WORD_LENGTH:
            raise ValueError("Secret word must contain exactly 5 letters.")

        if self.secret_word not in self.word_list:
            raise ValueError("Secret word must exist in the word list.")

    def make_guess(self, word: str) -> GuessResult:
        """Validate and evaluate a player's guess."""

        word = word.lower()

        # Check whether the game is already over.
        if self.is_over:
            raise RuntimeError("The game is already over.")

        # Check the length of the guess.
        if len(word) != WORD_LENGTH:
            raise ValueError("Guess must contain exactly 5 letters.")

        # Check whether the word exists in the word list.
        if word not in self.word_list:
            raise ValueError("Word is not in the word list.")

        # Evaluate the guess.
        result = evaluate_guess(self.secret_word, word)

        # Store the result.
        self.guesses.append(result)

        return result

    @property
    def is_won(self) -> bool:
        """Return True if the player has guessed the secret word."""
        return any(
            result.statuses == ["correct"] * WORD_LENGTH for result in self.guesses
        )

    @property
    def is_over(self) -> bool:
        """Return True if the player has won or exhausted all attempts."""
        return self.is_won or len(self.guesses) >= MAX_GUESSES

    def __str__(self) -> str:
        """Display the game board and remaining attempts."""

        board = ["\n".join(str(result) for result in self.guesses)]

        remaining = MAX_GUESSES - len(self.guesses)

        board.append(f"\nAttempts remaining: {remaining}/{MAX_GUESSES}")

        return "\n\n".join(board)
