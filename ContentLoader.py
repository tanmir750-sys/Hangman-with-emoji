import json
class ContentLoader:
    def __init__(self, filename):
        with open(filename, "r") as file:
            self.data = json.load(file)
    def get_all_puzzles(self):
        return self.data
    def get_by_difficulty(self, difficulty):
        return [puzzle for puzzle in self.data if puzzle["difficulty"] == difficulty]
    puzzles = [
        {"emoji": "📚✏️🎓", "word": "STUDENT", "difficulty": "Easy"},
        {"emoji": "🎬🍿🎥", "word": "MOVIE", "difficulty": "Medium"},
        {"emoji": "🏏🏃🏆", "word": "CRICKET", "difficulty": "Hard"},
        {"emoji": "🎮🕹️🏆", "word": "GAMER", "difficulty": "Medium"},
        {"emoji": "🚀🌕⭐", "word": "ROCKET", "difficulty": "Medium"},
        {"emoji": "📱💬📞", "word": "MOBILE", "difficulty": "Medium"},
        {"emoji": "💻⌨️🖱️", "word": "COMPUTER", "difficulty": "Medium"},
        {"emoji": "🌧️☁️💧", "word": "WEATHER", "difficulty": "Medium"},
        {"emoji": "🔥🍳👨‍🍳", "word": "COOKING", "difficulty": "Hard"},
        {"emoji": "🎸🎵🎤", "word": "MUSICIAN", "difficulty": "Easy"},
        {"emoji": "📷🌄📸", "word": "PHOTOGRAPHY", "difficulty": "Hard"},
        {"emoji": "🏃💪🥇", "word": "ATHLETE", "difficulty": "Easy"},
        {"emoji": "👑🏰⚔️", "word": "KINGDOM", "difficulty": "Medium"},
        {"emoji": "🌍✈️🧳", "word": "TRAVELER", "difficulty": "Medium"},
        {"emoji": "🚗🛣️⛽", "word": "DRIVING", "difficulty": "Medium"},
        {"emoji": "🏥💉👨‍⚕️", "word": "DOCTOR", "difficulty": "Medium"},
        {"emoji": "⚖️📜🏛️", "word": "JUSTICE", "difficulty": "Medium"},
        {"emoji": "🌳🌱💧", "word": "NATURE", "difficulty": "Easy"},
        {"emoji": "🎨🖌️🖼️", "word": "ARTIST", "difficulty": "Medium"},
        {"emoji": "🔍🕵️📄", "word": "DETECTIVE", "difficulty": "Medium"},
        {"emoji": "📖🧠💡", "word": "KNOWLEDGE", "difficulty": "Medium"},
        {"emoji": "🏠🏗️🔨", "word": "BUILDING", "difficulty": "Medium"},
        {"emoji": "🍔🍟🥤", "word": "FASTFOOD", "difficulty": "Easy"},
        {"emoji": "📚🏫📝", "word": "HOMEWORK", "difficulty": "Easy"},
        {"emoji": "🚓🚨👮", "word": "POLICE", "difficulty": "Easy"},
        {"emoji": "🧪🔬⚗️", "word": "SCIENCE", "difficulty": "Hard"},
        {"emoji": "🎭🎬⭐", "word": "ACTOR", "difficulty": "Medium"},
        {"emoji": "📺🎤📰", "word": "REPORTER", "difficulty": "Medium"},
        {"emoji": "🌙⭐🌌", "word": "GALAXY", "difficulty": "Medium"},
        {"emoji": "⚡🔋🚗", "word": "ELECTRIC", "difficulty": "Hard"},
        {"emoji": "🗺️📍🌍", "word": "JOURNEY", "difficulty": "Medium"},
        {"emoji": "🏟️⚽🥅", "word": "FOOTBALL", "difficulty": "Medium"},
        {"emoji": "🍫🍬🍭", "word": "CANDY", "difficulty": "Easy"},
        {"emoji": "🛒🏬💳", "word": "SHOPPING", "difficulty": "Medium"},
        {"emoji": "🎹🎼🎵", "word": "PIANIST", "difficulty": "Medium"},
        {"emoji": "🐘🌿🌳", "word": "WILDLIFE", "difficulty": "Medium"},
        {"emoji": "✉️📬📨", "word": "MESSAGE", "difficulty": "Medium"},
        {"emoji": "🏆🥇🎖️", "word": "CHAMPION", "difficulty": "Medium"},
        {"emoji": "🎤🎶🎧", "word": "SINGER", "difficulty": "Hard"},
        {"emoji": "🧑‍💻💻☕", "word": "CODING", "difficulty": "Hard"},
        {"emoji": "📡🛰️🌍", "word": "NETWORK", "difficulty": "Hard"},
        {"emoji": "🕰️⏳⌛", "word": "TIMING", "difficulty": "Medium"},
        {"emoji": "🚲🏞️🌤️", "word": "CYCLING", "difficulty": "Hard"},
        {"emoji": "🍎🥗💪", "word": "HEALTHY", "difficulty": "Hard"},
        {"emoji": "🌋🔥🌍", "word": "VOLCANO", "difficulty": "Medium"},
        {"emoji": "🎓📖🏫", "word": "EDUCATION", "difficulty": "Medium"},
        {"emoji": "🔐💻🛡️", "word": "SECURITY", "difficulty": "Hard"},
        {"emoji": "🎂🎉🎁", "word": "BIRTHDAY", "difficulty": "Medium"},
        {"emoji": "🌊⛵🐟", "word": "OCEAN", "difficulty": "Medium"},
        {"emoji": "💰🏦📈", "word": "BANKING", "difficulty": "Hard"} ]
    with open("emoji_data.json", "w") as f:
        json.dump(puzzles, f, indent=2)
    print("emoji_data.json created successfully!")
