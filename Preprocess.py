import nltk
from nltk.tokenize import wordpunct_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.stem import SnowballStemmer


# nltk.download('PorterStemmer')
# nltk.download('stopwords')

def tokenize(text):
    return wordpunct_tokenize(text)


def detectLanguage(text):
    dutch = ['de', 'het', 'een', 'ik', 'wij', 'jij', 'hij', 'zij']
    for w in dutch:
        if w in text:
            print(w)
            return True
    return False


def stopWordRemoval(text, dutch):
    if dutch:
        stop_words = set(stopwords.words('dutch') + ['wij'])
    else:
        stop_words = set(stopwords.words('english'))
    # converts the words in word_tokens to lower case and then checks whether
    # they are present in stop_words or not
    return [w for w in text if not w.lower() in stop_words]


def stemming(text, dutch):
    if dutch:
        snowball = SnowballStemmer(language='dutch')
    else:
        snowball = SnowballStemmer(language='english')
    # return [PorterStemmer().stem(w) for w in text]
    return [snowball.stem(w) for w in text]


def preproccess(text):

    tokenized_Text = tokenize(text)
    dutch = detectLanguage(tokenized_Text)
    print(dutch)
    filtered_text = stopWordRemoval(tokenized_Text, dutch)
    stemmed_text = stemming(filtered_text, dutch)
    # print(stopwords.words('dutch'))
    print(tokenized_Text)
    print(filtered_text)
    print(stemmed_text)
