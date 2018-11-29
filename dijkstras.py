import networkx as nx

import matplotlib.pyplot as plt

#from collections import deque

inf = float('inf')

def neighbours(Graph):

        neighbours = {nodes: set() for nodes in set(Graph.nodes())}

        for edge in list(Graph.edges):

            

            #__1__neighbours[edge[0]].add((edge[1], Graph.get_edge_data(edge[0],edge[1])['weight']))

            neighbours[edge[0]].add((edge[1], 1/Graph.get_edge_data(edge[0],edge[1])['weight']))

        return neighbours

        #--------------------

        #{1: {(4, 5), (2, 1)}, 2: {(3, 2)}, 3: {(4, 1)}, 4: {(5, 5000)}, 5: set()}

        #-------------------------

def dijkstra(Graph, source, dest):

        if source not in set(Graph.nodes()):return 'such node doesnt exist'

        

        

        distances = {vertex: inf for vertex in set(Graph.nodes())}

        previous_vertices = {

            vertex: None for vertex in set(Graph.nodes())

        }

        distances[source] = 0

        vertices = set(Graph.nodes()).copy()

        niga = neighbours(Graph)

        while vertices:

            current_vertex = min(vertices, key=lambda vertex: distances[vertex])

            vertices.remove(current_vertex)

            if distances[current_vertex] == inf:

                break

            

            for neighbour, cost in niga[current_vertex]:

                alternative_route = distances[current_vertex] + cost

                if alternative_route < distances[neighbour]:

                    distances[neighbour] = alternative_route

                    previous_vertices[neighbour] = current_vertex

        #path, current_vertex = deque(), dest

        path, current_vertex = [], dest

        while previous_vertices[current_vertex] is not None:

                path.append(current_vertex)

            #path.appendleft(current_vertex)

        

                current_vertex = previous_vertices[current_vertex]

        if path:

            #path.appendleft(current_vertex)

                path.append(current_vertex)

        path.reverse()

        return path

        

#=================================================================================================

G = nx.Graph()

edges=[(5,7,6),(5,4,2),(5,10,5),(10,6,6),(10,1,7),(6,9,1),(7,4,5),(1,3,4),(7,2,8),(3,8,9.5),(2,8,10),(4,8,3),(2,9,5)]

for start, end, weight in edges:

	# You can attach any attributes you want when adding the edge	G.add_edge(start, end, weight=weight)

nx.draw(G,with_labels=True)

plt.show()

print(dijkstra(G,5,2))
