import nltk
#import SPACY_NER
from nltk.tokenize import wordpunct_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.stem import SnowballStemmer
from nltk.stem import WordNetLemmatizer
from nltk.tag import pos_tag

nltk.download('PorterStemmer')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')
import NER


def tokenize(text):
    return wordpunct_tokenize(text)


# detect the language of dutch and english with typical dutch words
def detectLanguage(text):
    """
    detect language of based on a list of language characterising words
    returns true for dutch
    return false for anything else (assumption that it is only english)
    """
    dutch = ['het', 'een', 'ik', 'wij', 'jij', 'hij', 'zij']
    for w in dutch:
        if w in text:
            print(w)
            return True
    return False


def stopWordRemoval(text, is_dutch_bool):
    """
    remove words that don't contain information (stopwords)
    returns list of information containing words
    """
    if is_dutch_bool:
        stop_words = set(stopwords.words('dutch') + ['wij'])
    else:
        stop_words = set(stopwords.words('english'))
    # converts the words in word_tokens to lower case and then checks whether
    # they are present in stop_words or not
    return [w for w in text if not w.lower() in stop_words]

#stemming is process of reducing a word to its stem. This is different for enlgish and dutch
def stemming(text, is_dutch_bool):
    """
    returns the tense of a verb into a single verb for each related verb's tense in text
    """
    if is_dutch_bool:
        snowball = SnowballStemmer(language='dutch')
    else:
        snowball = SnowballStemmer(language='english')
    # return [PorterStemmer().stem(w) for w in text]
    return [snowball.stem(w) for w in text]

#Lemmatization is stemming, but smarter. Only works in english.
def lemma(text, is_dutch_bool):
    """
    if dutch: uses stemming function that makes tenses of verb consistent
    lemmatizer if not in dutch (assumption that it is english)
    wordnetlemmatizer also works for irregular verbs
    """
    if is_dutch_bool:
        return stemming(text, is_dutch_bool)
    else:
        wordnet_lemmatizer = WordNetLemmatizer()
        return [wordnet_lemmatizer.lemmatize(word) for word in text]


def languageRecognizeProcess(website):
    for x in website:
        y = tokenize(x)
        if detectLanguage(y):
            return True
    return False


def preproccess(text, is_dutch_bool):
    # Step by step preprocessing
    # 1. tokenize
    tokenized_Text = tokenize(text)
    # 2. stopword removal
    sw_text = stopWordRemoval(tokenized_Text, is_dutch_bool)
    # 3.1 stemming (can be replaced with lemmetization)
    # However we chose lemmatization if the language is English as this is more accurate
    stemmed_text = lemma(sw_text, is_dutch_bool)

    combined_text = " ".join(stemmed_text)

    #tagged_text = EntityTagging.taggingSPACY(text, dutch)
    return stemmed_text