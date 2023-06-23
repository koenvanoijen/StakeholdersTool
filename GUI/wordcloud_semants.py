import gensim
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from datetime import date
import os




# Path to dataset
word2vec_path = "GoogleNews-vectors-negative300.bin"

# Load 200,000 most common words
word2vec_model = gensim.models.KeyedVectors.load_word2vec_format(word2vec_path, binary=True, limit=200000)

def clean_word(word):
    """
        :param word: word to clean
        :return: cleaned word
    """
    return word.replace("_", " ")

def make_list_of_word(word):
    """
        :param word: word or list of words
        :return: list of words
    """
    return [clean_word(word) for word in word] if isinstance(word, list) else [clean_word(word)]


def most_similar_100(positive_words: list, negative_words=None):
    """
        :param positive_words: list of positive words
        :param negative_words: list of negative words
        :return: list of tuples (word, probability)


    """
    if negative_words is None:
        return word2vec_model.most_similar(positive=make_list_of_word(positive_words), topn=100)
    else:
        return word2vec_model.most_similar(positive=make_list_of_word(positive_words),
                                           negative=make_list_of_word(negative_words), topn=100)


def list_to_frequency_dict(frequency_list):
    """
        :param frequency_list: list of tuples (word, probability)
        :return: dictionary of words and their probabilities
    """
    return {element: probability for element, probability in frequency_list}


def create_wordcloud(frequencies_dict, path_to_save):
    """
        :param frequencies_dict: dictionary of words and their probabilities
        :saves a wordcloud.png file
    """
    word_cloud = WordCloud(width=1600, height=800, background_color='white').generate_from_frequencies(frequencies_dict)

    plt.figure(figsize=(20, 10))

    plt.imshow(word_cloud, interpolation='bilinear')
    plt.axis("off")
    plt.tight_layout(pad=0)
    plt.savefig(path_to_save, bbox_inches='tight')

# here I want



def get_file_path_today(path_to_save):
    """
        :param path_to_save: path to save wordcloud.png
        :return: path to save wordcloud.png with today's date and a number that doesn't exist yet
            num = 1000 if there are already 1000 files with today's date
    """
    output = path_to_save.format(today=date.today(), num="{num}")
    i=1
    while os.path.exists(output.format(num=i)) and i<1000:
        i += 1
    output = output.format(num=i)
    return output

def generate_word_cloud(positive_words, path_to_save, negative_words=None):
    """
    a function that executes the whole cell, so that it gives only a set of negative and positive words and a path to save the wordcloud

        :param positive_words: list of positive words
        :param negative_words: list of negative words
        :param path_to_save: path to save wordcloud.png
    """
    print(positive_words)
    print(negative_words)
    print(path_to_save)
    positive_words = make_list_of_word(positive_words)
    negative_words = make_list_of_word(negative_words)

    frequency_list = most_similar_100(positive_words, negative_words)
    frequencies_dict = list_to_frequency_dict(frequency_list)

    output_path = get_file_path_today(path_to_save)
    create_wordcloud(frequencies_dict, output_path)
    return output_path, sorted(frequency_list, reverse=True, key=lambda x: x[1])

print(make_list_of_word(["hello_hi", "world"]))

def generate_word_cloud_from_freq(frequency_list, path_to_save):
    """
    a function that executes the whole cell, so that it gives only a set of negative and positive words and a path to save the wordcloud

        :param positive_words: list of positive words
        :param negative_words: list of negative words
        :param path_to_save: path to save wordcloud.png
    """

    frequencies_dict = list_to_frequency_dict(frequency_list)

    output_path = get_file_path_today(path_to_save)
    create_wordcloud(frequencies_dict, output_path)
    return output_path, sorted(frequency_list, reverse=True, key=lambda x: x[1])
