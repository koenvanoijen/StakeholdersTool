import nltk
from nltk.tokenize import wordpunct_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.stem import SnowballStemmer
from nltk.stem import WordNetLemmatizer
from nltk.tag import pos_tag



# nltk.download('PorterStemmer')
# nltk.download('stopwords')
#nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')

def tokenize(text):
    return wordpunct_tokenize(text)


# detect the language of dutch and english with typical dutch words
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

def lemma(text, dutch):
    if dutch:
        return stemming(text, dutch)
    else:
        wordnet_lemmatizer = WordNetLemmatizer()
        return [wordnet_lemmatizer.lemmatize(word) for word in text]

def tagged(text, dutch):
    if not dutch:
        return nltk.pos_tag(text)
    else:
        return text

def preproccess(text):
    # Step by step preprocessing
    # 1. tokenize
    tokenized_Text = tokenize(text)
    # 2. detect the language
    dutch = detectLanguage(tokenized_Text)
    # 3. stopword removal
    sw_text = stopWordRemoval(tokenized_Text, dutch)
    # 4.1 stemming (can be replaced with lemmetization)
    # However we chose lemmatization if the language is English
    if dutch:
        stemmed_text = stemming(sw_text, dutch)
    else:
        # 4.2 Lemmatization (can be replaced with stemming
        stemmed_text = lemma(sw_text, dutch)

    #part of speech tagging
    tagged_text = tagged(stemmed_text, dutch)


    print(dutch)
    print(tokenized_Text)
    print(sw_text)
    print(stemmed_text)
    print(tagged_text)