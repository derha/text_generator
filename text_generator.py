from nltk.tokenize import WhitespaceTokenizer
from collections import Counter, defaultdict
from random import choice, choices

# FILE_NAME should contain a path to corpus file
# One generated line may contain more than one sentence.

FILE_NAME = "dostoevsky.txt"
LINE_NUM = 5
MIN_LINE_LENGTH = 10


def get_tokens(file_name):
    with open(file_name, "r", encoding="utf-8") as f:
        text = f.read()
        tokenizer = WhitespaceTokenizer()
        return tokenizer.tokenize(text)


def tokens_to_trigrams(tokens):
    return [(tokens[i], tokens[i + 1], tokens[i + 2]) for i in range(len(tokens) - 2)]


def generate_markov_model(trigrams):
    head_tails = defaultdict(list)

    for trigram in trigrams:
        head_tails[(trigram[0], trigram[1])].append(trigram[2])

    for head in head_tails:
        head_tails[head] = Counter(head_tails[head])

    return head_tails


def choose_first_token(head_tails):
    possible_tokens = [head for head in head_tails.keys() if head[0][0].isupper() and head[0][-1] not in ".!?"]
    return choice(possible_tokens)


def is_last_word(word):
    return word[-1] in ".!?"


def generate_line(head_tails):
    first_token = choose_first_token(head_tails)
    tokens = [first_token[0], first_token[1]]

    while True:
        population = list(head_tails[(tokens[-2], tokens[-1])].keys())
        weights = list(head_tails[(tokens[-2], tokens[-1])].values())
        next_word = choices(population, weights)[0]

        tokens.append(next_word)

        if len(tokens) >= MIN_LINE_LENGTH and is_last_word(next_word):
            break

    return " ".join(tokens)


def main():
    tokens = get_tokens(FILE_NAME)
    trigrams = tokens_to_trigrams(tokens)
    head_tails_dict = generate_markov_model(trigrams)

    for _ in range(LINE_NUM):
        print(generate_line(head_tails_dict))


if __name__ == "__main__":
    main()
