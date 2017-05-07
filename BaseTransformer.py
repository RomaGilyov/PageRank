from abc import ABCMeta, abstractmethod
from re import findall
import networkx as nx


class BaseTransformer(metaclass=ABCMeta):
    """
    :var data
    :type dict|OrderedDict
    """
    __data = {}

    """
    :var graph
    :type DiGraph
    """
    __graph = False

    def __init__(self, data):
        self.__data = self.prepare(data)

    @abstractmethod
    def prepare(self, data):
        pass

    def get_data(self):
        return self.__data

    def count(self):
        return len(self.__data)

    def enumerate(self):
        return ((node, number) for number, node in enumerate(list(self.__data.keys())))

    def nodes(self):
        return list(self.__data.keys())

    def prepare_nodes(self):

        """
        grasp links (keys) from given resources (values)

        :return: dict
        """

        links = {}

        pattern = ''
        for node in self.__data.keys():
            pattern += str(node) + '|'

        pattern = pattern.rstrip('|')

        for node, content in self.__data.items():
            links[node] = findall(pattern, content)

        return links

    def make_graph(self):

        """
        build directed graph with the prepared data

        :return: DiGraph
        """

        if isinstance(self.__graph, nx.DiGraph):
            return self.__graph

        edges = []
        for key, values in self.prepare_nodes().items():
            edges_weights = {}
            for v in values:
                if v == key:
                    continue

                edges_weights[v] = edges_weights[v] + 1 if v in edges_weights else 1

            for successor, weight in edges_weights.items():
                edges.append([key, successor, {'weight': weight}])

        self.__graph = nx.DiGraph()
        self.__graph.add_nodes_from(list(self.__data.keys()))
        self.__graph.add_edges_from(edges)

        return self.__graph
