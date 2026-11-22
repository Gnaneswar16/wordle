import json
from pathlib import Path


class GameHistory:
    """Manage and persist the player's Wordle game history."""

    def __init__(self, filename: str = "history.json") -> None:
        self.filename = Path(filename)
        self.games: list[dict[str, bool | int | str]] = []

        self.load()

    def load(self) -> None:
        """Load previous game records from the JSON file."""

        if not self.filename.exists():
            self.save()
            return

        try:
            with self.filename.open("r", encoding="utf-8") as file:
                data = json.load(file)

            self.games = data.get("games", [])

        except json.JSONDecodeError:
            raise ValueError("History file contains invalid JSON.") from None

    def save(self) -> None:
        """Save all game records to the JSON file."""

        data = {"games": self.games}

        with self.filename.open("w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

    def record_game(self, won: bool, attempts: int, word: str) -> None:
        """Record a completed game and persist the history."""

        game_record = {"won": won, "attempts": attempts, "word": word}

        self.games.append(game_record)

        self.save()

    @property
    def total_games(self) -> int:
        """Return the total number of completed games."""

        return len(self.games)

    @property
    def total_wins(self) -> int:
        """Return the total number of games won."""

        return sum(game["won"] for game in self.games)

    @property
    def win_percentage(self) -> float:
        """Calculate the player's win percentage."""

        if self.total_games == 0:
            return 0.0

        return (self.total_wins / self.total_games) * 100

    @property
    def current_streak(self) -> int:
        """Calculate consecutive wins from the latest game backwards."""

        streak = 0

        for game in reversed(self.games):
            if game["won"]:
                streak += 1
            else:
                break

        return streak

    @property
    def best_streak(self) -> int:
        """Calculate the longest winning streak in the player's history."""

        best = 0
        current = 0

        for game in self.games:
            if game["won"]:
                current += 1
                best = max(best, current)
            else:
                current = 0

        return best
