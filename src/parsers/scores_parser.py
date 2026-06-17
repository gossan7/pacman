import json
from pathlib import Path


class ScoreParser:
    """
    Loads the persistent highscore table from a JSON file.

    Invalid entries are skipped, the result is sorted by descending score
    and capped at the top ten. A missing file is created and treated as an
    empty table rather than an error.
    """

    def parse(self, filename: str) -> list[tuple[str, int]]:
        """
        Read and sanitise the highscore file.

        Args:
            filename: Path to the JSON scores file.

        Returns:
            Up to ten (name, score) tuples sorted by descending score; an
            empty list if the file is missing, empty or invalid.
        """
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                raw = f.read()
        except FileNotFoundError:
            print(f"Info: Scores file '{filename}' not found. Creating it.")
            try:
                Path(filename).touch()
            except OSError as e:
                print(f"Warning: could not create '{filename}': {e}")
            return []
        except Exception as e:
            print(f"Warning: could not read '{filename}': {e}")
            return []

        if not raw.strip():
            return []

        try:
            content = json.loads(raw)
        except (ValueError, RecursionError) as e:
            print(f"Warning: '{filename}' is not valid JSON: {e}. "
                  f"Ignoring scores.")
            return []

        if not isinstance(content, list):
            print(f"Warning: '{filename}' must be a JSON list. "
                  f"Ignoring scores.")
            return []

        res: list[tuple[str, int]] = []
        for item in content:
            entry = self._parse_entry(item)
            if entry is not None:
                res.append(entry)

        res.sort(key=lambda x: x[1], reverse=True)
        return res[:10]

    def _valid_name(self, name: str) -> bool:
        """
        Check that a highscore name is acceptable.

        Args:
            name: The candidate player name.

        Returns:
            True if the name is 1-10 non-blank alphanumeric (or space)
            characters.
        """
        if not 1 <= len(name) <= 10:
            return False
        if not name.strip():
            return False
        return all(c.isalnum() or c == ' ' for c in name)

    def _parse_entry(self, item: object) -> tuple[str, int] | None:
        """
        Validate and convert a single raw scores entry.

        Args:
            item: A decoded JSON element, expected to be a dict with
                ``name`` and ``score`` fields.

        Returns:
            A (name, score) tuple if the entry is valid, otherwise None.
        """
        if not isinstance(item, dict):
            return None
        name = item.get("name")
        score = item.get("score")
        if not isinstance(name, str) or not self._valid_name(name):
            return None
        if not isinstance(score, int) or isinstance(score, bool):
            return None
        if score < 0:
            return None
        return (name, score)
