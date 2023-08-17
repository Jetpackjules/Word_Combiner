import openai
import random

from nltk.corpus import words, brown
from nltk.probability import FreqDist

# Preprocess the word list and frequency distribution
word_list = set(words.words())
freq_dist = FreqDist(w.lower() for w in brown.words() if 2 <= len(w) <= 7)

common_words = [word for word in word_list if 2 <= len(word) <= 7 and word in freq_dist]
sorted_common_words = sorted(common_words, key=lambda x: freq_dist[x], reverse=True)[:5000]



# Initialize the OpenAI API with your key
openai.api_key = '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'

class WordAlchemyAI:
    def __init__(self):
        self.combinations = {}
        self.available_words = set()
        self.target_word = None
        self.best_path = []
        self.user_path = []

    def pre_generate_paths(self, depth=4):
        self.target_word = random.choice(sorted_common_words)
        current_word = self.target_word
        for _ in range(depth):
            word1 = self.get_word_from_api("return [1] single word similar to:", current_word)
            word2 = self.get_word_from_api("return [1] single word similar to:", current_word)
            self.combinations[(word1, word2)] = current_word
            current_word = word1
            self.best_path.append(current_word)

        for i in range(4):  # 1 to 4 inclusive
            self.available_words.add(self.best_path[-i])
        self.best_path.reverse()

    def get_word_from_api(self, prompt, related_word=None):
        if related_word:
            prompt += f" {related_word}"
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            max_tokens=30
        )
        return response.choices[0].text.strip()

    def play(self):
        print("Welcome to Word Alchemy with AI!")
        print(f"Your goal is to create the word: {self.target_word}")
        print(f"Starting with the words: {', '.join(self.available_words)}")
        while self.target_word not in self.available_words:
            print(f"Starting with the words: {', '.join(self.available_words)}")
            word1 = input("Choose the first word: ").strip().lower()
            word2 = input("Choose the second word: ").strip().lower()
            new = self.combinations
            print(self.combinations)
            if (word1, word2) in self.combinations:
                result = self.combinations[(word1, word2)]
                print(f"{word1} + {word2} = {result}")
                self.user_path.append(result)
                self.available_words.add(result)
            else:
                print("This combination does not exist. Try again.")
        print(f"\nCongratulations! You've created the word: {self.target_word}")
        if len(self.user_path) > len(self.best_path):
            print(f"You took {len(self.user_path)} steps. The best path was: {' -> '.join(self.best_path)}")

if __name__ == "__main__":
    game = WordAlchemyAI()
    game.pre_generate_paths()
    game.play()
