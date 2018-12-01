#IMPORT MATPLOTLIB
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
#IMPORT TKINTER
import tkinter as tk
from tkinter import ttk
#import networkx
import networkx as nx
#----------------------------------------------------------------------------------------------
class MyApp():
    def __init__(self,root,Graph):
        self.root = root
        root.title("Graph")
        self.Graph = Graph
        #------------------------------------------------------------------
        #Create GRID
        label_sourcenode = tk.Label(self.root,text="Start Node :",width=20)
        self.entry_SOURCE = tk.Entry(self.root)
        #------------------------------------------------------------------
        label_TargetNode = tk.Label(self.root,text="End Node :",width=20)
        self.entry_target = tk.Entry(self.root)
        #------------------------------------------------------------------
        button_CalculateSR = tk.Button(self.root,text="Calc SR",command=self.calculateShortestPath)
        #------------------------------------------------------------------
        label_sourcenode.grid(row=0,column=0)
        self.entry_SOURCE.grid(row=0,column=1)
        label_TargetNode.grid(row=3,column=0)
        self.entry_target.grid(row=3,column=1)
        button_CalculateSR.grid(row=2,column=3)
        #------------------------------------------------------------------
        container = tk.Frame(self.root)
        container.grid(column=1,row=2)
        container.grid_rowconfigure(0,weight=1)
        container.grid_columnconfigure(0,weight=1)
        #----------------------------------------------------------------------------
        self.pos = nx.spring_layout(G)
        self.addgraph()

    def calculateShortestPath(self):
        source = int(self.entry_SOURCE.get())
        target = int(self.entry_target.get())
        path = dijkstra(self.Graph,source,target)
        self.addgraph(markpath=True,path=path)

    def addgraph(self,markpath=False,path=None):
        f = Figure(figsize=(5,5), dpi=100)
        a = f.add_subplot(111)

        if markpath == True:
            path_edges = list(zip(path,path[1:]))
            nx.draw(self.Graph,self.pos,with_labels=True,node_color='r',ax=a)
            # draw path in red
            nx.draw_networkx_nodes(self.Graph,self.pos,with_labels=True,nodelist=path,node_color='r',ax=a)
            nx.draw_networkx_edges(self.Graph,self.pos,with_labels=True,edgelist=path_edges,edge_color='r',width=10,ax=a)
        else:
            nx.draw(self.Graph,self.pos,with_labels=True,ax=a)
        canvas = FigureCanvasTkAgg(f, self.root)
        canvas.draw()
        canvas._tkcanvas.grid(row=4,column=1,columnspan=2, rowspan=2,sticky='wens', padx=5, pady=5)
        canvas.get_tk_widget().grid(row=5,column=1,columnspan=2, rowspan=2,sticky='wens', padx=5, pady=5)


inf = float('inf')
def neighbours(Graph):
    neighbours = {nodes: set() for nodes in set(Graph.nodes())}
    for nbr, datadict in G.adj.items():
        for i in datadict:
            neighbours[nbr].add((i,1/datadict[i]['weight']))
    return neighbours

def dijkstra(Graph, source, dest,bol=True):
    if source not in set(Graph.nodes()):return 'such node doesnt exist'
    distances = {vertex: inf for vertex in set(Graph.nodes())}
    previous_vertices = {vertex: None for vertex in set(Graph.nodes())}
    distances[source] = 0
    vertices = set(Graph.nodes()).copy()
    niga = neighbours(Graph)
    allcost = 0
    while vertices:
        current_vertex = min(vertices, key=lambda vertex: distances[vertex])
        vertices.remove(current_vertex)
        if distances[current_vertex] == inf:
            break

        for neighbour, cost in niga[current_vertex]:
            alternative_route = distances[current_vertex] + cost
            if alternative_route < distances[neighbour]:
                allcost += cost
                distances[neighbour] = alternative_route
                previous_vertices[neighbour] = current_vertex

    path, current_vertex = [], dest

    while previous_vertices[current_vertex] is not None:
        path.append(current_vertex)
        current_vertex = previous_vertices[current_vertex]

    if path:
        path.append(current_vertex)
    path.reverse()

    if len(path)==0 and bol ==True:
        try:
            pathb = dijkstra(Graph,dest,source,bol=False)
            pathb.reverse()
        except:
            pass
        return pathb
    return path

        
#=================================================================================================
G = nx.Graph()
edges=[(5,1,5),(5,3,2),(5,2,5),(5,7,1),(5,6,4),(2,1,6),(2,4,3),(6,3,1),(4,8,7),(3,10,3),(10,9,5),(7,11,5),(11,13,5),(13,10,4),(8,12,8)]
for start, end, weight in edges:
	# You can attach any attributes you want when adding the edge
	G.add_edge(start, end, weight=weight)
root = tk.Tk()  
myapp = MyApp(root,G)
root.mainloop()
print(dijkstra(G,5,2))
