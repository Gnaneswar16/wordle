# Wordle CLI Game

A Python-based command-line implementation of the popular Wordle word-guessing game.

## Features

- Guess a hidden five-letter word.
- Maximum of six attempts per game.
- Provides feedback for correct letters and their positions.
- Handles duplicate letters during guess evaluation.
- Maintains game history using JSON.
- Includes automated tests using pytest.

## Tech Stack

- Python
- JSON
- pytest
- Ruff

## Project Structure

```text
wordle/
├── game.py
├── history.py
├── wordle.py
├── words.txt
├── tests/
│   └── test_game.py
├── .gitignore
└── README.md
```

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/Gnaneswar16/wordle.git
cd wordle
```

### 2. Create a virtual environment

```bash
python3 -m venv .venv
```

### 3. Activate the virtual environment

macOS/Linux:

```bash
source .venv/bin/activate
```

### 4. Run the game

```bash
python wordle.py
```

## Running Tests

Run the automated test suite using:

```bash
python -m pytest -v
```

## Code Quality

Check code formatting and linting with:

```bash
ruff check .
```

## How to Play

1. Start the application.
2. Enter a five-letter word as your guess.
3. Receive feedback for each letter.
4. Use the feedback to improve your next guess.
5. Guess the hidden word within six attempts to win!

## Author

Gananeswar16
