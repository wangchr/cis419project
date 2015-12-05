from sklearn.feature_extraction.text import HashingVectorizer, TfidfVectorizer
from sklearn.ensemble import AdaBoostClassifier
from sklearn.cross_validation import train_test_split

import db

N_ESTIMATORS = 15

def load_pairs():
    return [line[:line.rfind(',')].replace(',', '+') for line in open('pairs.csv')][5:]


def load_data():
    real_recipes = db.all_recipes_pairs()
    fake_recipes = list(db.random_recipes(len(real_recipes)))
    tfidf_vectorizer = HashingVectorizer(tokenizer=lambda x: x.split(','))
    x = tfidf_vectorizer.fit_transform(real_recipes + fake_recipes)
    y = [1] * len(real_recipes) + [0] * len(fake_recipes)

    return x, y


def cook():
    x, y = load_data()
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=.3)
    classifier = AdaBoostClassifier(n_estimators=50)
    classifier.fit(x_train, y_train)
    print classifier.score(x_test, y_test)


if __name__ == '__main__':
    cook()
