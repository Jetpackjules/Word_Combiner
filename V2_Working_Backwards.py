import nltk
nltk.download('wordnet')
from nltk.corpus import wordnet as wn

def get_synonyms(word, depth=3):
    """Recursively fetch synonyms up to a given depth."""
    synonyms = set()

    if depth == 0:
        return synonyms

    for syn in wn.synsets(word):
        for lemma in syn.lemmas():
            synonyms.add(lemma.name())
            # Recursively fetch synonyms of the current lemma
            synonyms.update(get_synonyms(lemma.name(), depth-1))
    
    return synonyms

def find_common_word(word1, word2, depth=3):
    synonyms1 = get_synonyms(word1, depth)
    synonyms2 = get_synonyms(word2, depth)
    
    # Find the intersection of the two sets of synonyms
    common_synonyms = synonyms1.intersection(synonyms2)
    
    # If there are common synonyms, return the first one
    if common_synonyms:
        return list(common_synonyms)[0]
    else:
        return None

word1 = input("Enter the first word: ")
word2 = input("Enter the second word: ")

result = find_common_word(word1, word2, depth=10)

if result:
    print(f"The word that shares the most common synonyms with '{word1}' and '{word2}' is: {result}")
else:
    print(f"No common synonyms found for '{word1}' and '{word2}'.")

