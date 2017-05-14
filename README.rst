# PageRank
Google page rank

## Installation ##

```python
pip install rgpagerank
```

## Usage ##

```python

from rgpagerank import *

'''
You may pass either directory name or dictionary with data as a first (data) parameter to the new object:
'''

dir_pg = PageRank('directory_name', recursive=True, truncate_extension=True)

'''
Where
    directory_name - can be either absolute path to a directory or relative path, in the second case
    the script will use path of the script where the script file contains
    recursive - read nested directories or not
    truncate_extension - truncate extensions of the files

Each file name inside the directory is a node name and content are the corresponding data:
    dir:
        test.txt
        test1.txt
        nested_dir:
            test2.txt
            test.txt

So it will be: {'test': 'test data', 'test1': 'test1 data', 'test2': 'test2 data'}

If there are files with the same name the content of the files will be merged, so the dict above will contain
data from `dir/test.txt` and `dir/nested_dir/test.txt` for the `test` key
'''

dict_pg = PageRank({'test': 'Hello test1 and test2 I'm test', 'test1': 'Hi test good to see you', 'test2': 'Sup test'})

'''
To get page rank for the data use either `page_rank()` or `sorted_page_rank()`
'''

print(dict_pg.page_rank())
print(dict_pg.sorted_page_rank(reverse=True))

'''
There are also two helper classes: DictTransformer and DirectoryTransformer which is actually transform a given data
to a directed graph you may use it to get the graph and do something with it or draw the graph
'''

#dir_transformer = DirectoryTransformer('directory_name', recursive=True, truncate_extension=True)
dict_transformer = DirectoryTransformer(
    {'Jimmy': 'Hello John and Carl, Carl', 'Carl': 'Hi John', 'John': 'Sup Jimmy and Carl'}
)

#print(dir_transformer.make_graph())
#dir_transformer.draw_graph()

print(dict_transformer.make_graph())
dict_transformer.draw_graph()
```