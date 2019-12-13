# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.4'
#       jupytext_version: 1.2.4
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

import numpy as np
import networkx as nx
from matplotlib import pyplot as plt
# %matplotlib inline
from itertools import *
from collections import *

# +
dzip = lambda *args: dict(zip(*args))

class IITriangles:
    
    def __init__(self, seed, n):
        self.seed = seed
        self.n = n
        self.puzzle = self.generate_puzzle(seed, n)


# -

# # Creating the Puzzle
#
# First we generate a puzzle from the seed and number of cubes. We format the puzzle as a dictionary where the key is the cube id and the value is a tuple containing the colors. We use excel-column label format for the cube names to 
# differenciate them from the colors.
#
# | cube | color 1 | color 2 | color 3 |
# |:---: | :------ | :------ | :------ |
# |**A** | 1       | 2       | 3       |
# |**B** | 3       | 2       | 1       |
# |**C** | 1       | 3       | 3       |
#
# The puzzle above would be encoded as the dictionary below
#
# ```python
# {
#     'A': (1, 2, 3),
#     'B': (3, 2, 1),
#     'C': (1, 3, 3)
# }
# ```

# +
def generate_puzzle(self, seed, n):
        group = lambda l, n: (tuple(l[j:j+n]) for j in range(0, len(l), n))
        generate_colors = lambda i: int(1+(np.floor(i*seed)%n))
        colors = group(list(map(generate_colors, range(1, 3*n+1))), 3)
        cubes = map(self.name_node, range(1, n+1))
        return dzip(cubes, colors)

def name_node(self, n):
        name = ''
        while True:
            n -= 1;
            name = chr(ord('A') + n%26) + name;
            n = n // 26
            if n < 0:
                break
        return name[1:]

IITriangles.generate_puzzle = generate_puzzle
IITriangles.name_node = name_node


# -

# # Color Counts
#
# example text

# +
@property
def color_counts(self):
    return Counter(chain(*self.puzzle.values()))

IITriangles.color_counts = color_counts


# -

# # Finding Obstacles
#
# example text

# +
def find_obstacle(self):
    
    strategy = {
        2: self.size2_strategy,
        3: self.size3_strategy,
        4: self.size4_strategy,
        None: self.other_strategy
    }
    
    if all(lambda i: i != 3, self.color_counts):
        for obstacle_size in (2, 3, 4):
            obstacle = strategy[obstacle_size]()
            break
    else:
        obstacle = strategy[None]()
    
    return obstacle

IITriangles.find_obstacle = find_obstacle


# -

# # Single Cube DiGraphs
#
# example text

# +
def single_cube_digraph(self, cube):
    dG = nx.DiGraph()
    dG.add_nodes_from(zip(self.puzzle[cube], [{'color': color} for color in self.puzzle[cube]]))
    dG.add_edges_from([
        (self.puzzle[cube][0], self.puzzle[cube][1]),
        (self.puzzle[cube][1], self.puzzle[cube][2]),
        (self.puzzle[cube][2], self.puzzle[cube][0])
    ])
    return dG

IITriangles.single_cube_digraph = single_cube_digraph


# -

# # Size 2 Obstacles
#
# example text

# +
def size2_strategy(self):
            
    color_combinations = defaultdict(list)
    for cube, colors in self.puzzle.items():
        color_combinations[frozenset(colors)].append(cube)
    
    more_than_one = lambda cubes: len(cubes) > 1
    for colors, cubes in {k:v for k,v in color_combinations.items() if more_than_one(v)}.items():
        
        CubeRecord = namedtuple('CubeRecord', ['label', 'graph'])
        prev_cube = CubeRecord(cubes[0], self.single_cube_digraph(cubes[0]))
        
        for cube in cubes[1:]:
            dG = self.single_cube_digraph(cube)
            
            matcher = nx.isomorphism.DiGraphMatcher(dG.reverse(), prev_cube.graph,
                            node_match=nx.isomorphism.categorical_node_match('color', None))
            
            if matcher.is_isomorphic():
                return (cube, prev_cube.label)                
            prev_cube = CubeRecord(cube, dG)
    else: 
        return None
    
IITriangles.size2_strategy = size2_strategy


# -

# # Size 3 Obstacles
#
# example text

# +
def size3_strategy(self):
            
    color_combinations = defaultdict(set)
    for cube, colors in self.puzzle.items():
        color_pairs = (frozenset(pair) for pair in combinations(colors, 2))
        for pair in color_pairs:
            color_combinations[pair].add(cube)
            
    three_or_more = lambda cubes: len(cubes) >= 3
    for colors, obstacle_candidate_iter in {
        k: combinations(cubes, 3) for k,cubes in color_combinations.items() if three_or_more(cubes)
    }.items():
        
        for obstacle_candidate in obstacle_candidate_iter:
             
            cube_edges = [self.single_cube_digraph(i).edges for i in obstacle_candidate]

            edge_fwd = tuple(colors)
            edge_rev = tuple(reversed(edge_fwd))
            
            contains_fwd = [edge_fwd in edges for edges in cube_edges]
            contains_rev = [edge_rev in edges for edges in cube_edges]
            
            if (sum(contains_fwd) >= 2 and sum(contains_rev) >= 1) \
                or (sum(contains_fwd) >= 1 and sum(contains_rev) >= 2):
                return obstacle_candidate
    else:
        return None      
    
IITriangles.size3_strategy = size3_strategy
# -

# # Size 4 Obstacles
#
# example text



# # Larger than 4 Obstacles
#
# example text


