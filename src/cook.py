from multi_gridsearch import multi_grid_search

# classifiers
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier

import numpy as np
#import matplotlib.pyplot as plt
#from matplotlib.colors import ListedColormap
from sklearn.preprocessing import StandardScaler
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cross_validation import train_test_split


import pdb
import sys

import db

plot = False
plot_size = 4

# LOAD DATA-----------------------------------------------------------------

# Load the recipe data
real_recipes = db.all_recipes_pairs()
fake_recipes = list(db.random_recipes(len(real_recipes)))
tfidf_vectorizer = TfidfVectorizer()
X = tfidf_vectorizer.fit_transform(real_recipes + fake_recipes)
Y = [1] * len(real_recipes) + [0] * len(fake_recipes)

# Generate a random training/testing split
Xtrain, Xtest, Ytrain, Ytest = train_test_split(X, Y, test_size=.4)

# DEFINE PARAMETERS----------------------------------------------------------

# Decision Tree
# depth_params = [x for x in range(1, 5)]
# criterion_params = ['gini', 'entropy']
# DTC_parameters =  {'max_depth': depth_params, 'criterion': criterion_params}

# Decision Tree
depth_params = [x for x in range(1, 5)]
criterion_params = ['gini', 'entropy']
features_params = [1, 2]
DTC_parameters =  {'max_depth': depth_params, 'max_features': features_params}

# Random Forests
C_params = [2**x for x in range(1,5)]
SVMRBF_parameters =  {'C': C_params}

# Random Forests
depth_params = [x for x in range(1, 5)]
criterion_params = ['gini', 'entropy']
estimator_params = [5 * x for x in range(1, 4)]
RF_parameters =  {'max_depth': depth_params, 'criterion': criterion_params, 'n_estimators': estimator_params}

# Adaboost
estimator_params = [5 * x for x in range(1, 4)]
AB_parameters =  {'n_estimators': estimator_params}



# DEFINE CLASSIFIERS----------------------------------------------------------

classifiers = {
	# 'Decision Tree': 		[DecisionTreeClassifier(), 	DTC_parameters, Xtrain, Ytrain],
    'SVM RBF': 				[SVC(), SVMRBF_parameters, Xtrain, Ytrain],
    'Random Forests': 		[RandomForestClassifier(), RF_parameters, Xtrain, Ytrain],
    'AdaBoost': 			[AdaBoostClassifier(), AB_parameters, Xtrain, Ytrain]
    }

# RUN MULTI GRID SEARCH
best_classifiers = multi_grid_search(classifiers)


# PLOT PERFORMANCE--------------------------------------------------------------------

if not plot:
	sys.exit()

# define figure
figure = plt.figure(figsize=((plot_size * 1.4 * len(classifiers), plot_size)))

#mesh step size
h = .02

# Plot Dataset
X = StandardScaler().fit_transform(Xtrain)
Y = Ytrain

x_min, x_max = X[:, 0].min() - .5, X[:, 0].max() + .5
y_min, y_max = X[:, 1].min() - .5, X[:, 1].max() + .5
xx, yy = np.meshgrid(np.arange(x_min, x_max, h),
                     np.arange(y_min, y_max, h))

cm = plt.cm.RdBu
cm_bright = ListedColormap(['#FF0000', '#0000FF'])
ax = plt.subplot(1, len(classifiers) + 1, 1)

# Plot data points
ax.scatter(X[:, 0], X[:, 1], c=Y, cmap=cm_bright)
ax.set_title('Data')
ax.set_xlim(xx.min(), xx.max())
ax.set_ylim(yy.min(), yy.max())
ax.set_xticks(())
ax.set_yticks(())

i = 2

# iterate over classifiers
for classifier in best_classifiers:
	# Scale the training data and the testing data
    Xtrain = StandardScaler().fit_transform(classifiers[classifier[1]][2])
    Ytrain = classifiers[classifier[1]][3]

    Xtest = StandardScaler().fit_transform(Xtest)
    Ytest = Ytest

    ax = plt.subplot(1, len(best_classifiers) + 1, i)

    model = classifier[0].fit(Xtrain, Ytrain)
    score = model.score(Xtest, Ytest)

    # Plot the decision boundary. For that, we will assign a color to each
    # point in the mesh [x_min, m_max]x[y_min, y_max].
    if hasattr(model, "decision_function"):
        Z = model.decision_function(np.c_[xx.ravel(), yy.ravel()])
    else:
        Z = model.predict_proba(np.c_[xx.ravel(), yy.ravel()])[:, 1]

    # Put the result into a color plot
    Z = Z.reshape(xx.shape)
    ax.contourf(xx, yy, Z, cmap=cm, alpha=.8)

    # Plot points
    ax.scatter(X[:, 0], X[:, 1], c=Y, cmap=cm_bright, alpha=0.6)

    ax.set_xlim(xx.min(), xx.max())
    ax.set_ylim(yy.min(), yy.max())
    ax.set_xticks(())
    ax.set_yticks(())
    ax.set_title(classifier[1])
    ax.text(xx.max() - .3, yy.min() + .3, ('%s %.2f' % ('Score:', score)),
            size=15, horizontalalignment='right')
    # pdb.set_trace()
    plt.xlabel(str(classifier[2]).replace(',', '\n'))

    i += 1

figure.subplots_adjust(left=.02, right=.98, bottom=0.25)
plt.show()


# Useful Links
# http://scikit-learn.org/stable/modules/grid_search.html
# http://scikit-learn.org/stable/modules/generated/sklearn.grid_search.GridSearchCV.html#sklearn.grid_search.GridSearchCV
# http://scikit-learn.org/stable/auto_examples/model_selection/randomized_search.html#example-model-selection-randomized-search-py
