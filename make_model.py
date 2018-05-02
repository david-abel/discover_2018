# Python imports.
from collections import defaultdict
import dill

def clean_data(file_name):
    '''
    Args:
        file_name (str)

    Summary:
        Removes undesired symbols from the corpus and rewrites to "haiku_pre_processed.txt".
    '''

    remove_chars = ["\"", "'", "-", "_", "*", "$", "[", "]", ">", "<", "=", "(", ")", ":", ";" "\n"]

    new_file_text = ""

    for line in open(file_name).readlines():
        line = line.replace("\t", " ")
        words_in_line = line.split(" ")
        for word in words_in_line:
            word = word.lower()
            for char in remove_chars:
                word = word.replace(char,"")
            new_file_text += word + " "

    out_file = open("data/processed.txt","w")
    out_file.write(new_file_text)

def read_in_data(file_name="data/processed.txt"):
	'''
	Args:
		file_name (str)

	Returns:
		(list): In order words of poems (with newlines still in there).
	'''
	# Get data.
	text = open(file_name).read().lower()
	words = text.split(" ")

	return words

def make_n_gram_model(words, n):
	'''
	Args:
		words (list)
		n (int): Must be < 3

	Returns:
		(dict)
	'''
	word_count_dict = {}

	prev_words = []
	for word in words:

		# Get last n words.
		inner_dict = word_count_dict
		for i in range(n - 1, 0, -1):

			inner_dict = inner_dict[prev_words[-i]]

		# Add a count.
		inner_dict[word] += 1
		prev_words.append(word)
	
	return word_count_dict

def make_fivegram_model(words):
	'''
	Args:
		words (list)

	Returns:
		(dict)
	'''
	word_count_dict = defaultdict(lambda: defaultdict(lambda:  defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: 1)))))
	
	prev_word_a = ""
	prev_word_b = ""
	prev_word_c = ""
	prev_word_d = ""

	for word in words:

		word = word.replace(" ", "")

		if "\n" in word:
			word = word.replace("\n", "")
			word_count_dict[prev_word_a][prev_word_b][prev_word_c][word]["\n"] += 1

		word_count_dict[prev_word_a][prev_word_b][prev_word_c][prev_word_d][word] += 1
		prev_word_a = prev_word_b
		prev_word_b = prev_word_c
		prev_word_c = prev_word_d
		prev_word_b = word
	
	return word_count_dict

def make_fourgram_model(words):
	'''
	Args:
		words (list)

	Returns:
		(dict):
			Key: word
			Val: dict
				Key: word
				Val: dict
					Key: word
					Val: float
	'''
	word_count_dict = defaultdict(lambda:  defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: 1))))
	
	prev_word_a = ""
	prev_word_b = ""
	prev_word_c = ""

	for word in words:

		word = word.replace(" ", "")

		if "\n" in word:
			word = word.replace("\n", "")
			word_count_dict[prev_word_a][prev_word_b][word]["\n"] += 1

		word_count_dict[prev_word_a][prev_word_b][prev_word_c][word] += 1
		prev_word_a = prev_word_b
		prev_word_b = prev_word_c
		prev_word_c = word
	
	return word_count_dict

def make_trigram_model(words):
	'''
	Args:
		words (list)

	Returns:
		(dict):
			Key: word
			Val: dict
				Key: word
				Val: dict
					Key: word
					Val: float
	'''
	word_count_dict = defaultdict(lambda:  defaultdict(lambda: defaultdict(lambda: 1)))
	
	prev_word_a = ""
	prev_word_b = ""

	for word in words:

		word = word.replace(" ", "")

		if "\n" in word:
			word = word.replace("\n", "")
			word_count_dict[prev_word_a][word]["\n"] += 1

		word_count_dict[prev_word_a][prev_word_b][word] += 1
		prev_word_a = prev_word_b
		prev_word_b = word
	
	return word_count_dict

def make_bigram_model(words):
	'''
	Args:
		words (list)

	Returns:
		(dict):
			Key: word
			Val: dict
				Key: word
				Val: probability (float)
	'''
	word_count_dict = defaultdict(lambda:  defaultdict(lambda: 1))
	
	prev_word = ""
	for word in words:

		word = word.replace(" ", "")

		if "\n" in word:
			word = word.replace("\n", "")
			word_count_dict[word]["\n"] += 1

		word_count_dict[prev_word][word] += 1
		prev_word = word
	
	return word_count_dict

def make_unigram_model(words):
	'''
	Args:
		words (list)

	Returns:
		(dict):
			Key: word
			Val: count
	'''
	word_count_dict = defaultdict(lambda: 1)
	
	for word in words:
		word = word.replace(" ", "")

		if "\n" in word:
			word = word.replace("\n", "")
			word_count_dict["\n"] += 1

		word_count_dict[word] += 1
	
	return word_count_dict


def save_count_dict(markov_model, model_name):
	'''
	Args:
		markov_model (dict)
		model_name (str)
	'''
	with open('models/' + model_name + '.pkl', 'wb') as f:
		dill.dump(markov_model, f)

def load_count_dict(model_name):
	'''
	Args:
		model_name (str)

	Returns:
		(dict)
	'''
	return dill.load(open('models/' + model_name + '.pkl','r'))

def make_and_save_markov_model_from_file(file_name, model_name):
	'''
	Args:
		file_name (str)
		model_name (str)

	Summary:
		Cleans @file_name, makes a word count dict, saves to @model_name.pickle
	'''
	clean_data(file_name)
	words = read_in_data()

	# Make model.
	if model_name == "unigram":
		word_count_dict = make_unigram_model(words)
	elif model_name == "bigram":
		word_count_dict = make_bigram_model(words)
	elif model_name == "trigram":
		word_count_dict = make_trigram_model(words)
	elif model_name == "fourgram":
		word_count_dict = make_fourgram_model(words)
	elif model_name == "fivegram":
		word_count_dict = make_fivegram_model(words)

	# Save.
	save_count_dict(word_count_dict, model_name)

def main():
	make_and_save_markov_model_from_file(file_name="data/haiku_all.txt", model_name="unigram")
	make_and_save_markov_model_from_file(file_name="data/haiku_all.txt", model_name="bigram")
	make_and_save_markov_model_from_file(file_name="data/haiku_all.txt", model_name="trigram")
	make_and_save_markov_model_from_file(file_name="data/haiku_all.txt", model_name="fourgram")
	make_and_save_markov_model_from_file(file_name="data/haiku_all.txt", model_name="fivegram")
	# markov_model = load_count_dict(model_name="fourgram")

if __name__ == "__main__":
	main()
