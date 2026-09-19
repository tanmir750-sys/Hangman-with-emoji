import json
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SCORES_FILE = os.path.join(BASE_DIR, "scores.json")
def load_scores(path=SCORES_FILE):
    if not os.path.exists(path):
        return []
    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read().strip()
        if not content:
            return []
        data = json.loads(content)
        if not isinstance(data, list):
            raise ValueError("scores.json should contain a list")
        valid_scores = []
        for entry in data:
            if not isinstance(entry, dict):
                continue
            if "name" not in entry or "score" not in entry:
                continue
            try:
                valid_scores.append({
                    "name": str(entry["name"])[:20],
                    "score": int(entry["score"]),
                    "level": str(entry.get("level", "Easy")),
                })
            except (ValueError, TypeError):
                continue

        return valid_scores

    except (json.JSONDecodeError, ValueError, OSError):
        _quarantine_corrupted_file(path)
        return []
def _quarantine_corrupted_file(path):
    try:
        if os.path.exists(path):
            backup_path = path + ".corrupted"
            os.replace(path, backup_path)
            print(f"Warning: {os.path.basename(path)} was corrupted. "
                  f"Backed up as {os.path.basename(backup_path)} and starting fresh.")
    except OSError as e:
        print(f"Warning: could not back up corrupted save file ({e}).")


def save_score(name, score, level, path=SCORES_FILE):

    scores = load_scores(path)
    scores.append({
        "name": (name or "Player").strip()[:20] or "Player",
        "score": int(score),
        "level": level,
    })

    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(scores, f, indent=2)
    except OSError as e:
        print(f"Warning: could not save score to disk ({e}).")


def get_top_scores(n=10, path=SCORES_FILE):
    scores = load_scores(path)
    return sorted(scores, key=lambda s: s["score"], reverse=True)[:n]
if __name__ == "__main__":
    print("Current top scores:")
    for i, entry in enumerate(get_top_scores(), start=1):
        print(f"{i}. {entry['name']} - {entry['score']} pts ({entry['level']})")