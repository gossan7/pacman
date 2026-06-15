import json
from pathlib import Path


class ScoreParser:

    def parse(self, filename: str) -> list[tuple[str, int]]:
        res = []

        try:
            with open(filename, 'r', encoding='utf-8') as f:
                content = json.load(f)
        except FileNotFoundError:
            print(f"Info: Scores file '{filename}' not found. Creating it.")
            Path(filename).touch()
            return []
        except Exception as e:
            raise Exception(f"Could not open {filename}: {e}")

        if not isinstance(content, list):
            raise ValueError("Scores must be a JSON list")

        for item in content:
            if not isinstance(item, dict):
                raise ValueError("Each score must be a JSON object")

            if "name" not in item or "score" not in item:
                raise ValueError("Each score must have 'name' and 'score'")

            name = item["name"]
            score = item["score"]

            if not isinstance(name, str):
                raise ValueError(
                    f"Name must be string, got {type(name).__name__}")
            if not name.strip():
                raise ValueError("Name must not be empty")
            if not isinstance(score, int):
                raise ValueError(
                    f"Score must be int, got {type(score).__name__}")

            res.append((name, score))

        return sorted(res, key=lambda x: x[1], reverse=True)
