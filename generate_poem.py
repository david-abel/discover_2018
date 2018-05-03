# Python imports.
import numpy as np
import random
from collections import defaultdict

# Other imports
from make_model import load_count_dict

OBJ_WORD_BIAS = 3000

def _post_process(poem_words):
    '''
    Args:
        poem_words (list)

    Returns:
        (str)
    '''

    if len(poem_words) == 0:
        return ""

    while poem_words[0] == " ":
        poem_words = poem_words[1:]

    # Convert to string
    poem = ""
    for word in poem_words[:-1]:
        poem += word + " "

    poem += poem_words[-1]
    poem = poem.replace("    ", " ")
    poem = poem.replace("   ", " ")
    poem = poem.replace("  ", " ")
    poem = poem.replace("\t", "")

    return poem

def merge_counts_from_n_markov_models(poem_words, markov_models, bias_toward_n=1):
    '''
    Args:
        poem_words (list)
        markov_models (list)
        bias_toward_n (int): Adds more probability mass to higher n-grams.

    Returns:
        (dict): Merges the counts
    '''
    merged_model = defaultdict(int)

    # For each markov model, grab it's probabilities.
    for markov_model in markov_models:
        layers = 1 # the "n" in ngram

        temp_for_counting_layers = markov_model
        while len(temp_for_counting_layers.values()) != 0 and isinstance(temp_for_counting_layers.values()[0], dict):
            layers += 1
            temp_for_counting_layers = temp_for_counting_layers.values()[0]

        for i in range(1, layers):
            markov_model = markov_model[poem_words[-layers + i]]

        for word in markov_model.keys():
            merged_model[word] += markov_model[word] * layers

    return merged_model


def generate_poem_line_from_markov_model(markov_models, objects_in_scene=[]):
    '''
    Args:
        markov_models (list)
        objects_in_scene (list)

    Returns:
        (str)
    '''
    poem_words = [""] * 6
    obj_biases = defaultdict(lambda: OBJ_WORD_BIAS)
    max_poem_length = 12 # in words.
    n_gram_bias = random.randint(1, 6)

    # Make poem
    i = 0
    while len(poem_words) < max_poem_length:

        # Build object model.
        obj_word_model = defaultdict(int)
        for obj in objects_in_scene:
            obj_relevant_words = obj.get_words()
            for word in obj_relevant_words:
                obj_word_model[word] += obj_biases[obj.name]

        # Merge Markov models with object counts.
        merged_word_counts = merge_counts_from_n_markov_models(poem_words, markov_models + [obj_word_model], n_gram_bias)

        # Sample.
        tot_count = sum(merged_word_counts.values())
        multinomial = [float(count) / tot_count for count in merged_word_counts.values()]
        try:
            sampled_word_list = np.random.multinomial(1, multinomial).tolist()
        except ValueError:
            next_word = ""
            continue
        indices = [i for i, x in enumerate(sampled_word_list) if x > 0]
        if len(indices) == 0:
            next_word = ""
            continue
        next_word = merged_word_counts.keys()[indices[0]]
        poem_words.append(next_word)

        # Adjust biases.
        for obj in objects_in_scene:
            if next_word in obj.get_words():
                obj_biases[obj.name] = max(obj_biases[obj.name] / 2, 1)

        if len(poem_words) > 7 and random.random() > i / float(max_poem_length):
            break

        i +=1

    poem = _post_process(poem_words)

    return poem


def main():
    markov_model = load_count_dict(model_name="fourgram")

    print(generate_poem_from_markov_model(markov_model))


if __name__ == "__main__":
    main()
