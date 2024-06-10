import requests
from requests.exceptions import ConnectionError
from collections import defaultdict
import time

MAX_RETRIES = 3
DELAY_BETWEEN_RETRIES = 1  # in seconds

def fetch_words_from_api():
    api_url = "https://api.wordsapi.com/v1/words"
    params = {"random": "true", "limit": 50}
    retries = 0

    while retries < MAX_RETRIES:
        try:
            response = requests.get(api_url, params=params)
            response.raise_for_status()  # Raise HTTPError for bad requests
            words_data = response.json()
            words = [word_info["word"] for word_info in words_data]
            return words
        except ConnectionError as e:
            print(f"Error: {e}")
            print(f"Retrying in {DELAY_BETWEEN_RETRIES} seconds...")
            time.sleep(DELAY_BETWEEN_RETRIES)
            retries += 1
        except requests.HTTPError as e:
            print(f"HTTP Error: {e}")
            break
        except Exception as e:
            print(f"Error: {e}")
            break

    print("Failed to fetch words from the API after multiple retries.")
    return []

def anagram_solver(words):
    anagrams = defaultdict(list)
    for word in words:
        sorted_word = ''.join(sorted(word))
        anagrams[sorted_word].append(word)
    grouped_anagrams = [anagram_group for anagram_group in anagrams.values() if len(anagram_group) > 1]
    return grouped_anagrams

word_list = fetch_words_from_api()

if word_list:
    result = anagram_solver(word_list)
    print("Groups of Anagrams:")
    print(result)
else:
    print("No words fetched from the API.")
