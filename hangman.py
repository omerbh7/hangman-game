import requests
import string

API_URL = "https://random-word-api.herokuapp.com/word"


def get_random_word():
    try:
        response = requests.get(API_URL)
        response.raise_for_status()
        data = response.json()
        if isinstance(data, list) and data:
            return data[0].lower()
        else:
            print("API did not return a valid word. Using fallback word.")
            return "python"
    except Exception as e:
        print(f"Error fetching word from API: {e}\nUsing fallback word.")
        return "python"

def display_word(word, guessed_letters):
    return " ".join([letter if letter in guessed_letters else "_" for letter in word])

def hangman():
    word = get_random_word()
    guessed_letters = set()
    wrong_guesses = set()
    max_attempts = 6

    print("Welcome to Hangman!")
    print(f"The word has {len(word)} letters.")

    while True:
        print("\nWord:", display_word(word, guessed_letters))
        print(f"Wrong guesses ({len(wrong_guesses)}/{max_attempts}):", " ".join(sorted(wrong_guesses)))
        guess = input("Guess a letter: ").lower()

        if len(guess) != 1 or guess not in string.ascii_lowercase:
            print("Please enter a single letter (a-z).")
            continue
        if guess in guessed_letters or guess in wrong_guesses:
            print("You already guessed that letter.")
            continue

        if guess in word:
            guessed_letters.add(guess)
            if all(letter in guessed_letters for letter in word):
                print("\nCongratulations! You guessed the word:", word)
                break
        else:
            wrong_guesses.add(guess)
            if len(wrong_guesses) >= max_attempts:
                print(f"\nGame over! The word was: {word}")
                break

if __name__ == "__main__":
    hangman()
