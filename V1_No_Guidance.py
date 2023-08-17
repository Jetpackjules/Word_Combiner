import openai
import random

# Download the required datasets
# import nltk
# nltk.download('words')
# nltk.download('brown')
from nltk.corpus import words, brown
from nltk.probability import FreqDist

# Preprocess the word list and frequency distribution
word_list = set(words.words())
freq_dist = FreqDist(w.lower() for w in brown.words() if 2 <= len(w) <= 7)

common_words = [word for word in word_list if 2 <= len(word) <= 7 and word in freq_dist]
sorted_common_words = sorted(common_words, key=lambda x: freq_dist[x], reverse=True)[:5000]

def get_simple_word():
    return random.choice(sorted_common_words)

# Initialize the OpenAI API with your key
openai.api_key = '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'

class WordAlchemyAI:
    def __init__(self):
        self.combinations = {}
        self.available_words = set()
        self.target_word = get_simple_word()  # Change this to the word you want players to reach

    def add_starting_words(self, num_words=6):
        starting_words = random.sample(sorted_common_words, num_words)
        for word in starting_words:
            self.available_words.add(word)

    def combine_words(self, word1, word2):
        # Check if combination already exists
        if (word1, word2) in self.combinations:
            result = self.combinations[(word1, word2)]
        elif (word2, word1) in self.combinations:
            result = self.combinations[(word2, word1)]
        else:
            # Ask OpenAI for a likely combination
            response = openai.Completion.create(
                engine="davinci",
                prompt=f"Combine words to create NEW COMMON 1-word results (must be at least vaguely connected by logic, like kneel + sudden = guillotine or decapitation):\nBird + fire = phoenix \nfire + mud = brick \ntax + cow = farmer \nthief + jail = inmate \n{word1} + {word2} =",
                max_tokens=3
            )
            result2 = response.choices[0].text.strip()
            result = result2.split()[0]
            # Store the combination
            self.combinations[(word1, word2)] = result

        print(f"{word1} + {word2} = {result}")
        self.available_words.add(result)
        return result

    def play(self):
        print("Welcome to Word Alchemy with AI!")
        print(f"Your goal is to create the word: {self.target_word}")
        while self.target_word not in self.available_words:
            print("\nAvailable words:", ", ".join(self.available_words))
            word1 = input("Choose the first word: ").strip().lower()
            word2 = input("Choose the second word: ").strip().lower()
            if word1 in self.available_words and word2 in self.available_words:
                self.combine_words(word1, word2)
            else:
                print("One or both of the words are not available. Try again.")
        print(f"\nCongratulations! You've created the word: {self.target_word}")

if __name__ == "__main__":
    game = WordAlchemyAI()
    game.add_starting_words()
    game.play()
