import re

def parse_natural_language_query(query: str):
    parsed = {}
    q = query.lower()

    if "palindromic" in q:
        parsed["is_palindrome"] = True

    if "single word" in q:
        parsed["word_count"] = 1

    match = re.search(r"longer than (\d+)", q)
    if match:
        parsed["min_length"] = int(match.group(1)) + 1

    match = re.search(r"shorter than (\d+)", q)
    if match:
        parsed["max_length"] = int(match.group(1)) - 1

    match = re.search(r"containing the letter (\w)", q)
    if match:
        parsed["contains_character"] = match.group(1)

    return parsed

query = "all single word palindromic strings"
print("Hello: " , parse_natural_language_query(query))
