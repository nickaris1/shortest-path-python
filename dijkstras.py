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
#=====================================================================================================================
#=====================================================================================================================
#=====================================================================================================================
class MyApp():
    def __init__(self,root,Graph):
        self.root = root
        root.title("Graph")
        self.Graph = Graph
        #------------------------------------------------------------------
        
        self.mf = tk.Frame(self.root)
        self.mf.pack(side='top',fill='x',expand=1)


        self.fg = tk.Frame(self.root)
        self.fg.pack(side='bottom',fill='both',expand=1)
        self.mf1 = tk.Frame(self.mf)
        self.mf1.pack(side='left',fill='x',expand=1)
        self.f1 = tk.Frame(self.mf1)
        self.f1.pack(side = 'left', fill='x')
        self.f2 = tk.Frame(self.mf1)
        self.f2.pack(side = 'right', fill='x')
        self.f3 = tk.Frame(self.mf)
        self.f3.pack(side = 'right', fill='x',expand=1)



        label_sourcenode = tk.Label(self.f1,text="Start Node :",width=20)
        self.entry_SOURCE = tk.Entry(self.f2)
        #------------------------------------------------------------------
        label_TargetNode = tk.Label(self.f1,text="End Node :",width=20)
        self.entry_target = tk.Entry(self.f2)
        #------------------------------------------------------------------
        button_CalculateSR = tk.Button(self.f3,text="Calc SR",command=self.calculateShortestPath)
        button_clear = tk.Button(self.f3,text='Clear',command=self.addgraph)
        #------------------------------------------------------------------
        label_sourcenode.pack(expand=1,side='top')
        self.entry_SOURCE.pack(expand=1,side='top')
        label_TargetNode.pack(expand=1,side='bottom')
        self.entry_target.pack(expand=1,side='bottom')
        button_CalculateSR.pack(expand=1,side='top')
        button_clear.pack(expand=1,side='bottom')
        #------------------------------------------------------------------
        self.root.bind('<Return>',self.calculateShortestPathBind)
        self.pos = nx.spring_layout(G)
        self.addgraph()
    def calculateShortestPathBind(self,*args): self.calculateShortestPath()
    
    def calculateShortestPath(self):
        source = int(self.entry_SOURCE.get())
        target = int(self.entry_target.get())
        path = dijkstra(self.Graph,source,target)
        self.addgraph(markpath=True,path=path)

    def addgraph(self,markpath=False,path=None):
        try:
            for w in self.fg.winfo_children():
                    w.destroy()
        except:
            pass

        self.f = Figure(figsize=(5,5), dpi=100)
        self.a = self.f.add_subplot(111)
        if markpath == True:
            path_edges = list(zip(path,path[1:]))
            nx.draw(self.Graph,self.pos,with_labels=True,node_color='r',ax=self.a)
            # draw path in red
            nx.draw_networkx_nodes(self.Graph,self.pos,with_labels=True,nodelist=path,node_color='r',ax=self.a)
            nx.draw_networkx_edges(self.Graph,self.pos,with_labels=True,edgelist=path_edges,edge_color='r',width=10,ax=self.a)
        else:
            nx.draw(self.Graph,self.pos,with_labels=True,ax=self.a)
        
        self.canvas = FigureCanvasTkAgg(self.f, self.fg)
        self.fg.canvas= self.canvas
        self.fg.ax = self.a

        self.canvas.draw()
        self.canvas._tkcanvas.pack(expand=1,fill=tk.BOTH)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

#=====================================================================================================================
#=====================================================================================================================
#=====================================================================================================================
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
#=====================================================================================================================
if __name__ == '__main__':
    inf = float('inf')
    G = nx.Graph()
    edges=[(5,1,5),(5,3,2),(5,2,5),(5,7,1),(5,6,4),(2,1,6),(2,4,3),(6,3,1),(4,8,7),(3,10,3),(10,9,5),(7,11,5),(11,13,5),(13,10,4),(8,12,8)]
    for start, end, weight in edges:
        # You can attach any attributes you want when adding the edge
        G.add_edge(start, end, weight=weight)
    root = tk.Tk()  
    myapp = MyApp(root,G)
    root.mainloop()
