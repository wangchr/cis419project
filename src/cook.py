import numpy as np

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.cross_validation import train_test_split
from sklearn.decomposition import TruncatedSVD
from sklearn.metrics import classification_report

import db

def load_pairs():
    return ','.join((i1+'+'+i2)*int(q) for line in open('pairs.csv') for i1, i2, q in [line.strip().split(',')])


def load_data():
    real_recipes = db.all_recipes_pairs()
    fake_recipes = list(db.random_recipes(len(real_recipes)))
    vectorizer = CountVectorizer(tokenizer=lambda x: x.split(','))
    x = vectorizer.fit_transform(real_recipes + fake_recipes)
    y = (1,) * len(real_recipes) + (0,) * len(fake_recipes)

    # Load the recipe data
    network_pairs = [load_pairs()]
    pairs_vector = vectorizer.transform(network_pairs)

    return x, y, pairs_vector


def weighted(x, weights):
    return x.multiply(weights.toarray() + 1)


def truncated(train, test):
    n_components = 200
    svd = TruncatedSVD(n_components, random_state=42)
    train_svd = svd.fit_transform(train)
    test_svd = svd.transform(test)
    return train_svd, test_svd

def cook():
    x, y, weights = load_data()
    n_components = 200
    svd = TruncatedSVD(n_components, random_state=42)
    x_unweighted = svd.fit_transform(x)
    x_weighted = svd.fit_transform(weighted(x, weights))

    for i in range(9):
        frac = 1 - (i * 0.01 + 0.01)
        print frac

        x_train, x_test, y_train, y_test = train_test_split(x_unweighted, y, test_size=frac)
        classifier = AdaBoostClassifier(n_estimators=100)
        classifier.fit(x_train, y_train)
        print "Unweighted: ", classifier.score(x_test, y_test)

        x_train, x_test, y_train, y_test = train_test_split(x_weighted, y, test_size=frac)
        classifier = AdaBoostClassifier(n_estimators=100)
        classifier.fit(x_train, y_train)
        print "Weighted: ", classifier.score(x_test, y_test)

        print '--------------------------'


    '''
    print classification_report(y_test, classifier.predict(x_test), digits=8)

    classifier = DecisionTreeClassifier(max_depth=4)
    classifier.fit(x_train, y_train)
    print "DTC: ", classifier.score(x_test, y_test)
    print classification_report(y_test, classifier.predict(x_test), digits=8)

    classifier = RandomForestClassifier()
    classifier.fit(x_train, y_train)
    print "DForest: ", classifier.score(x_test, y_test)
    print classification_report(y_test, classifier.predict(x_test), digits=8)

    classifier = SVC()
    classifier.fit(x_train, y_train)
    print "SVC: ", classifier.score(x_test, y_test)
    print classification_report(y_test, classifier.predict(x_test), digits=8)
    '''

if __name__ == '__main__':
    cook()
