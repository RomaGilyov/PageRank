from collections import OrderedDict
from BaseTransformer import BaseTransformer
from DirectoryTransformer import DirectoryTransformer
from DictTransformer import DictTransformer
from numpy import zeros
from numpy import matrix
from numpy.random import random
from numpy import sum, ones, dot


class PageRank(object):

    __graph = False

    __NX = 0

    __epsilon = 0.01

    def __init__(self, graph, recursive=False, truncate_extension=True):

        if isinstance(graph, BaseTransformer):
            self.__graph = graph
        elif isinstance(graph, str):
            self.__graph = DirectoryTransformer(graph, recursive, truncate_extension)
        elif isinstance(graph, dict) or isinstance(graph, OrderedDict):
            self.__graph = DictTransformer(graph)
        else:
            raise TypeError(
                'PageRank class must receive '
                'DictTransformer or DirectoryTransformer or directory path or dict or OrderedDict.'
            )

        self.__NX = self.__graph.count()

    def set_epsilon(self, value):
        if value is float:
            self.__epsilon = value
            return self

        raise TypeError('Epsilon must be float.')

    def get_epsilon(self):
        return self.__epsilon

    def transition_matrix(self):
        transition_matrix = matrix(zeros((self.__NX, self.__NX)))

        nodes_numbers = dict(self.__graph.nodes_with_number())

        for predecessor, successors in self.__graph.make_graph().adj.items():
            for s, edge_data in successors.items():
                transition_matrix[nodes_numbers[predecessor], nodes_numbers[s]] = edge_data['weight']

        return transition_matrix

    def markov_chain(self):
        """
        1. Add uniform probability matrix E to transition matrix T (L = T + eE)
        2. Sum all values in each L's row and divide each value in the L's row by the sum
           after that we getting stochastic matrix G (Markov chain)

        :return: matrix
        """

        T = self.transition_matrix()
        E = ones(T.shape)/self.__NX
        L = T + E * self.__epsilon
        G = matrix(zeros(L.shape))

        for i in range(self.__NX):
            G[i, :] = L[i, :] / sum(L[i, :])

        return G

    def calculate_ranks(self):
        PI = random(self.__NX)
        PI /= sum(PI)

        G = self.markov_chain()

        for __ in range(100):
            PI = dot(PI, G)

        return PI.tolist()[0]

    def page_rank(self):

        ranks = self.calculate_ranks()

        nodes = self.__graph.nodes()

        page_rank = {}

        for i in range(self.__NX):
            page_rank[nodes[i]] = ranks[i]

        return page_rank
