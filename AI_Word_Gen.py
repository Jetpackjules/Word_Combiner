import openai
import random
from nltk.corpus import words, brown

# Preprocess the word list
word_list = set(words.words())

# Get nouns from the Brown corpus
nouns = set(word.lower() for word, pos in brown.tagged_words() if pos in ['NN', 'NNS'])

# Intersect with the word list and filter based on length
common_nouns = [word for word in nouns if 2 <= len(word) <= 7 and word in word_list]

def get_simple_word():
    return random.choice(common_nouns)



# Initialize the OpenAI API with your key
openai.api_key = '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'



combinations = {}
available_words = set()
target_word = get_simple_word()  # Change this to the word you want players to reach

def add_starting_words(num_words=4):
    starting_words = random.sample(common_nouns, num_words)
    for word in starting_words:
        available_words.add(word)
    return starting_words

def combine_words(word1, word2):
    # Check if combination already exists
    if (word1, word2) in combinations:
        result = combinations[(word1, word2)]
    elif (word2, word1) in combinations:
        result = combinations[(word2, word1)]
    else:
        # Ask OpenAI for a likely combination
        response = openai.Completion.create(
            engine="davinci",
            # An alternate route would be to find the word with the most common factor "synonyms" to the other word...
            prompt=f"Combine words to create NEW, REAL, 1-word NOUN results (Think of what would happen if the two things would be combined physically, the outcome OR the closest word that is similar to these two words):\nBird + fire = phoenix \nfire + mud = brick \ntax + cow = farmer \nthief + jail = inmate \n{word1} + {word2} =",
            max_tokens=3
        )
        result2 = response.choices[0].text.strip()
        result = result2.split()[0]
        # Store the combination
        combinations[(word1, word2)] = result

    print(f"{word1} + {word2} = {result}")
    available_words.add(result)
    return result

def play():
    print("Welcome to Word Alchemy with AI!")
    print(f"Your goal is to create the word: {target_word}")
    while target_word not in available_words:
        print("\nAvailable words:", ", ".join(available_words))
        word1 = input("Choose the first word: ").strip().lower()
        word2 = input("Choose the second word: ").strip().lower()
        if word1 in available_words and word2 in available_words:
            combine_words(word1, word2)
        else:
            print("One or both of the words are not available. Try again.")
    print(f"\nCongratulations! You've created the word: {target_word}")

# starters = add_starting_words()
# play()
