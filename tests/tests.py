import unittest
from RGPageRank.DictTransformer import DictTransformer
from RGPageRank.DirectoryTransformer import DirectoryTransformer
from RGPageRank.PageRank import PageRank
from os import path

abs_path = path.dirname(path.abspath(__file__)) + path.sep


class DictTransformerTest(unittest.TestCase):

    def test_dict(self):
        dict_transformer = DictTransformer({'John': 'Mike', 'Mike': 'John Carl', 'Carl': 'Mike'})

        self.assertEquals(['John', 'Mike', 'Carl'], dict_transformer.nodes())
        self.assertEquals({'John': 0, 'Mike': 1, 'Carl': 2}, dict(dict_transformer.nodes_with_number()))
        self.assertEquals(
            {'John': ['Mike'], 'Mike': ['John', 'Carl'], 'Carl': ['Mike']},
            dict_transformer.prepare_nodes()
        )
        self.assertEquals({'John': 'Mike', 'Mike': 'John Carl', 'Carl': 'Mike'}, dict_transformer.get_data())
        self.assertEquals(
            {'John': {'Mike': {'weight': 1}}, 'Mike': {'John': {'weight': 1}, 'Carl': {'weight': 1}},
             'Carl': {'Mike': {'weight': 1}}},
            dict_transformer.make_graph().adj
        )


class DirectoryTransformerTest(unittest.TestCase):

    def test_not_recursive(self):
        dir_transformer = DirectoryTransformer(abs_path + 'testdata')

        self.assertEquals(['Carl', 'Jimmy', 'John'], dir_transformer.nodes())
        self.assertEquals({'Carl': 0, 'Jimmy': 1, 'John': 2}, dict(dir_transformer.nodes_with_number()))
        self.assertEquals(
            {'Carl': ['Jimmy', 'Carl'], 'Jimmy': ['Carl', 'John'], 'John': ['Jimmy']},
            dir_transformer.prepare_nodes()
        )
        self.assertEquals(
            {'Carl': {'Jimmy': {'weight': 1}}, 'Jimmy': {'Carl': {'weight': 1}, 'John': {'weight': 1}},
             'John': {'Jimmy': {'weight': 1}}},
            dir_transformer.make_graph().adj
        )

        ntr_dir_transformer = DirectoryTransformer(abs_path + 'testdata', truncate_extension=False)

        self.assertEquals(['Carl.txt', 'Jimmy.txt', 'John.txt'], ntr_dir_transformer.nodes())
        self.assertEquals({'Carl.txt': 0, 'Jimmy.txt': 1, 'John.txt': 2}, dict(ntr_dir_transformer.nodes_with_number()))
        self.assertEquals(
            {'Carl.txt': [], 'Jimmy.txt': [], 'John.txt': []},
            ntr_dir_transformer.prepare_nodes()
        )
        self.assertEquals(
            {'Carl.txt': {}, 'Jimmy.txt': {}, 'John.txt': {}},
            ntr_dir_transformer.make_graph().adj
        )

    def test_recursive(self):
        dir_transformer = DirectoryTransformer(abs_path + 'testdata', recursive=True)

        self.assertEquals(['Carl', 'Jimmy', 'John', 'Bob', 'Denis'], dir_transformer.nodes())
        self.assertEquals(
            {'Carl': 0, 'Jimmy': 1, 'John': 2, 'Bob': 3, 'Denis': 4},
            dict(dir_transformer.nodes_with_number())
        )
        self.assertEquals(
            {'Carl': ['Jimmy', 'Carl'], 'Jimmy': ['Carl', 'John'], 'John': ['Jimmy', 'Carl'], 'Bob': ['Jimmy'],
             'Denis': ['Carl', 'Bob']},
            dir_transformer.prepare_nodes()
        )
        self.assertEquals(
            {'Carl': {'Jimmy': {'weight': 1}}, 'Jimmy': {'Carl': {'weight': 1}, 'John': {'weight': 1}},
            'John': {'Jimmy': {'weight': 1}, 'Carl': {'weight': 1}}, 'Bob': {'Jimmy': {'weight': 1}},
            'Denis': {'Carl': {'weight': 1}, 'Bob': {'weight': 1}}},
            dir_transformer.make_graph().adj
        )

        ntr_dir_transformer = DirectoryTransformer(abs_path + 'testdata', truncate_extension=False, recursive=True)

        self.assertEquals(['Carl.txt', 'Jimmy.txt', 'John.txt', 'Bob.txt', 'Denis.txt'], ntr_dir_transformer.nodes())
        self.assertEquals(
            {'Carl.txt': 0, 'Jimmy.txt': 1, 'John.txt': 2, 'Bob.txt': 3, 'Denis.txt': 4},
            dict(ntr_dir_transformer.nodes_with_number())
        )
        self.assertEquals(
            {'Carl.txt': [], 'Jimmy.txt': [], 'John.txt': [], 'Bob.txt': [], 'Denis.txt': []},
            ntr_dir_transformer.prepare_nodes()
        )
        self.assertEquals(
            {'Carl.txt': {}, 'Jimmy.txt': {}, 'John.txt': {}, 'Bob.txt': {}, 'Denis.txt': {}},
            ntr_dir_transformer.make_graph().adj
        )


class PageRankTest(unittest.TestCase):

    def test_page_rank(self):
        page_rank = PageRank({'John': 'Mike Carl', 'Mike': 'John Carl', 'Carl': 'Mike'})

        ranks = page_rank.page_rank()

        self.assertEquals(0.223, round(ranks['John'], 3))
        self.assertEquals(0.444, round(ranks['Mike'], 3))
        self.assertEquals(0.334, round(ranks['Carl'], 3))

        dir_page_rank = PageRank(abs_path + 'testdata', recursive=True)

        dir_ranks = dir_page_rank.page_rank()

        self.assertEquals(0.333, round(dir_ranks['Carl'], 3))
        self.assertEquals(0.444, round(dir_ranks['Jimmy'], 3))
        self.assertEquals(0.222, round(dir_ranks['John'], 3))
        self.assertEquals(0.001, round(dir_ranks['Bob'], 3))
        self.assertEquals(0.001, round(dir_ranks['Denis'], 3))


if __name__ == '__main__':
   unittest.main()
