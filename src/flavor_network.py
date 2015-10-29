import numpy as np


class FlavorNetwork:

    def __init__(self):
        '''
        Constructor
        '''

    def createAdjMatrix(self):
        # Reads in ingredient pairs and weights from .csv file
        filepath = 'flavor_network_data/srep00196-s2.csv'
        file = open(filepath, 'r')
        data = np.genfromtxt(filepath, dtype = None, delimiter=',', skip_header=4)
self.
        # Assign each unique ingredient an index
        index = 0
        self.ingred_dict = {}
        for i in xrange(len(data)):
            ingred = data[i][0]
            if (not self.ingred_dict.has_key(ingred)):
                self.ingred_dict[ingred] = index;
                index += 1
            ingred = data[i][1]
            if (not self.ingred_dict.has_key(ingred)):
                self.ingred_dict[ingred] = index;
                index += 1

        # Create adjacency matrix representation of graph
        n_ingred = len(self.ingred_dict)
        self.adj_mat = np.zeros([n_ingred,n_ingred])
        for i in xrange(len(data)):
            ingred1 = data[i][0]
            ingred2 = data[i][1]
            self.adj_mat[self.ingred_dict[ingred1], self.ingred_dict[ingred2]] = data[i][2]
