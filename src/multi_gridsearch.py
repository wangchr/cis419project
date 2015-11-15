from gridsearch import grid_search

import os
from time import gmtime, strftime
import sys
import pdb
import operator

#Outputs a formatted score sheet
def print_scores(name, names, scores):
	
	# Open new file. Create new directory if it does not exist
	script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
	filename = '_'.join((name, '-'.join(names), strftime("%Y-%m-%d %H-%M-%S") + '.txt'))
	folder_path = os.path.join(script_dir, "test_results")
	if not os.path.exists(folder_path):
	    os.makedirs(folder_path)
	
	file_path = os.path.join(folder_path, filename)
	file = open(file_path, 'w')

	# Write results to file
	for x in range(len(scores)):
		file.write('%-24s: %s' % (names[x], str(scores[x])))
		file.write('\n')
		
	print('\n========================================================')
	print('--------------------------------------------------------')
	print('========================================================\n')

	print('Finished Multi Grid Search')
	print('Best Classifier Found:')
	print '%s: %s' % (names[0], scores[0])

	file.close()

# classifiers - dictionary of the form key=name, value = [classifier, parameters, Xdata, Ydata]
best_classifiers = []
def multi_grid_search(classifiers):
	for key, value in classifiers.iteritems():
		classifier = grid_search(key, value[0], value[1], value[2], value[3])
		# store best best results of each classifier
		best_classifiers.append([classifier.best_estimator_, key, max(classifier.grid_scores_, key=lambda x: x[1])])

	sorted_classifiers = sorted(best_classifiers, key=lambda x: x[2][1], reverse=True)
	names = [row[1] for row in sorted_classifiers]
	scores = [row[2] for row in sorted_classifiers]

	print_scores('multi_grid_search', names, scores)

	return best_classifiers
