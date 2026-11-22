import random
from pathlib import Path

from game import MAX_GUESSES, WORD_LENGTH, Game
from history import GameHistory


def load_words(filename: str = "words.txt") -> list[str]:
    """Load and validate five-letter words from a file."""

    file_path = Path(filename)

    if not file_path.exists():
        raise FileNotFoundError(f"Word list not found: {filename}")

    with file_path.open("r", encoding="utf-8") as file:
        words = [line.strip().lower() for line in file if line.strip()]

    if not words:
        raise ValueError("Word list cannot be empty.")

    for word in words:
        if len(word) != 5 or not word.isalpha():
            raise ValueError(f"Invalid word in word list: {word}")

    return words


def play_game() -> None:
    """Run one complete Wordle game."""

    words = load_words()

    secret_word = random.choice(words)

    game = Game(secret_word, words)

    history = GameHistory()

    print("\n================================")
    print("       WELCOME TO WORDLE")
    print("================================")
    print(f"\nYou have {MAX_GUESSES} attempts to guess a {WORD_LENGTH}-letter word.")
    print("✓ = Correct | ~ = Present | ✗ = Absent")

    print(game)
    while not game.is_over:
        guess = input("\nEnter your guess: ").strip()

        try:
            game.make_guess(guess)
        except (ValueError, RuntimeError) as error:
            print(f"\nInvalid guess: {error}")
            continue
        print(game)

    print("\n================================")
    print("          GAME OVER")
    print("================================")

    if game.is_won:
        print(f"\nYou got it in {len(game.guesses)}/{MAX_GUESSES}!")
    else:
        print(f"\nThe word was {secret_word.upper()}")

    history.record_game(won=game.is_won, attempts=len(game.guesses), word=secret_word)

    print("\n========== YOUR STATS ==========")
    print(f"Games played: {history.total_games}")
    print(f"Total wins: {history.total_wins}")
    print(f"Win percentage: {history.win_percentage:.2f}%")
    print(f"Current streak: {history.current_streak}")
    print(f"Best streak: {history.best_streak}")


if __name__ == "__main__":
    play_game()
