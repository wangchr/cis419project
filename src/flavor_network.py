import numpy as np


class FlavorNetwork:

    def __init__(self):
        '''
        Constructor
        '''

    def loadGraph(self):
        # Reads in ingredient pairs and weights from .csv file
        filepath = 'flavor_network_data/srep00196-s2.csv'
        file = open(filepath, 'r')
        data = np.genfromtxt(filepath, dtype = None, delimiter=',', skip_header=4)

        # Assign each unique ingredient an index
        index = 0
        for i in xrange(len(data)):
            ingred = data[i][1]
            if (!ingred_dict.has_key(ingred)):
                ingred_dict[ingred] = index;
                index += 1
            ingred = data[i][2]
            if (!ingred_dict.has_key(ingred)):
                ingred_dict[ingred] = index;
                index += 1

        # Create adjacency matrix of graph
        adj_mat = np.zeros([len(dict), len(dict)])
        for i in xrange(len(data)):
            ingred1 = data[i][1]
            ingred2 = data[i][2]
            adj_mat[ingred_dict[ingred1], ingred_dict[ingred2]] = data[i][3]

