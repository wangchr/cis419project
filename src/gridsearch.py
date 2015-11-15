from sklearn.grid_search import GridSearchCV

import numpy as np
from sklearn import metrics

import os
from time import gmtime, strftime
import sys
import pdb

# pdb.set_trace()

#Outputs a formatted score sheet
def print_scores(name, scores, parameters):
	
	# Open new file. Create new directory if it does not exist
	script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
	filename = '_'.join((name, '-'.join(parameters.keys()), strftime("%Y-%m-%d %H-%M-%S") + '.txt'))
	folder_path = os.path.join(script_dir, "test_results")
	if not os.path.exists(folder_path):
	    os.makedirs(folder_path)
	
	file_path = os.path.join(folder_path, filename)
	file = open(file_path, 'w')

	# Write results to file
	file.write('Testing order:\n')
	for x in range(len(scores)):
		file.write(str(scores[x]))
		file.write('\n')

	file.write('\n')

	file.write('========================================================\n')

	scores = sorted(scores, key=lambda x: x[1]) # sort by mean score
	file.write('Mean score order:\n')
	for x in range(len(scores)):
		file.write(str(scores[x]))
		file.write('\n')

	print('\n========================================================\n')
	
	print('Finished Grid Search of ' + name)
	print('Best Parameters Found:')
	best_parameters, score, _ = max(scores, key=lambda x: x[1])
	for param_name in sorted(parameters.keys()):
	    print("%s: %r" % (param_name, best_parameters[param_name]))

	file.close()


# Grid Search
# name 			- name assigned to output file. 
# parameters 	- dict or list of dictionaries of desired parameters to vary
# model 		- the model to gridsearch over
# cv 			- integer, cv generator, or iterable that yields training/testing splits
# 					default value is 3 (when input to grid search)
# Xtrain		- Training Data
# Ytrain		- Labels of training data
def grid_search(name, model, parameters, Xtrain, Ytrain, cv=None):
	GS = GridSearchCV(model, parameters, error_score=0, cv=cv)
	GS.fit(Xtrain, Ytrain)
	scores = GS.grid_scores_
	print_scores(name, scores, parameters)
	return GS