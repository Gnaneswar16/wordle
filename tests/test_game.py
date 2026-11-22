import pytest

from game import Game, evaluate_guess
from history import GameHistory
from wordle import load_words


def test_fully_correct_guess():
    """Test when every letter is in the correct position."""

    result = evaluate_guess("APPLE", "APPLE")

    assert result.statuses == ["correct"] * 5


def test_mixed_guess():
    """Test a guess containing correct, present and absent letters."""

    result = evaluate_guess("CRANE", "TRACE")

    assert result.statuses == ["absent", "correct", "correct", "present", "correct"]


def test_duplicate_letters():
    """Test that duplicate letters are evaluated correctly."""

    result = evaluate_guess("SPINE", "SPEED")

    assert result.statuses == ["correct", "correct", "present", "absent", "absent"]


def test_invalid_word_raises_exception():
    """Test that a word outside the word list is rejected."""

    game = Game("apple", ["apple", "spine", "speed"])

    with pytest.raises(ValueError):
        game.make_guess("grape")


def test_game_is_won():
    """Test that a correct guess wins the game."""

    game = Game("apple", ["apple", "spine", "speed"])

    game.make_guess("apple")

    assert game.is_won is True


def test_game_is_over_after_six_failed_guesses():
    """Test that six incorrect guesses end the game."""

    words = ["apple", "spine", "speed", "crane", "trace", "chess", "brain"]

    game = Game("apple", words)

    guesses = ["spine", "speed", "crane", "trace", "chess", "brain"]

    for guess in guesses:
        game.make_guess(guess)

    assert game.is_won is False
    assert game.is_over is True
    assert len(game.guesses) == 6


def test_record_game(tmp_path):
    history_file = tmp_path / "history.json"

    history = GameHistory(str(history_file))

    history.record_game(won=True, attempts=3, word="apple")

    assert history.total_games == 1
    assert history.total_wins == 1


def test_history_persistence(tmp_path):
    history_file = tmp_path / "history.json"

    history = GameHistory(str(history_file))

    history.record_game(won=True, attempts=3, word="apple")

    # Create a new object using the same file.
    loaded_history = GameHistory(str(history_file))

    assert loaded_history.total_games == 1
    assert loaded_history.total_wins == 1


def test_win_percentage(tmp_path):
    history_file = tmp_path / "history.json"
    history = GameHistory(str(history_file))

    history.record_game(True, 3, "apple")
    history.record_game(False, 6, "brain")
    history.record_game(True, 4, "crane")
    history.record_game(True, 2, "spine")

    assert history.total_games == 4
    assert history.total_wins == 3
    assert history.win_percentage == 75.0


def test_current_streak(tmp_path):
    history_file = tmp_path / "history.json"
    history = GameHistory(str(history_file))

    history.record_game(True, 3, "apple")
    history.record_game(True, 2, "spine")
    history.record_game(False, 6, "brain")
    history.record_game(True, 4, "crane")
    history.record_game(True, 2, "trace")
    history.record_game(True, 3, "speed")

    assert history.current_streak == 3


def test_best_streak(tmp_path):
    history_file = tmp_path / "history.json"
    history = GameHistory(str(history_file))

    history.record_game(True, 3, "apple")
    history.record_game(True, 2, "spine")
    history.record_game(False, 6, "brain")
    history.record_game(True, 4, "crane")
    history.record_game(True, 2, "trace")
    history.record_game(True, 3, "speed")
    history.record_game(True, 2, "grape")
    history.record_game(False, 6, "chess")
    history.record_game(True, 3, "river")

    assert history.best_streak == 4
    assert history.current_streak == 1


def test_load_valid_words(tmp_path):
    words_file = tmp_path / "words.txt"

    words_file.write_text("apple\nbrain\ncrane\n", encoding="utf-8")

    words = load_words(str(words_file))

    assert words == ["apple", "brain", "crane"]


def test_load_invalid_words(tmp_path):
    words_file = tmp_path / "words.txt"

    words_file.write_text("apple\nbanana\n", encoding="utf-8")

    with pytest.raises(ValueError, match="Invalid word"):
        load_words(str(words_file))


def test_load_missing_file(tmp_path):
    words_file = tmp_path / "missing.txt"

    with pytest.raises(FileNotFoundError, match="Word list not found"):
        load_words(str(words_file))


def test_load_empty_file(tmp_path):
    words_file = tmp_path / "words.txt"

    words_file.write_text("", encoding="utf-8")

    with pytest.raises(ValueError, match="Word list cannot be empty"):
        load_words(str(words_file))
