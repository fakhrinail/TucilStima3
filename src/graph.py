import math
import networkx as nx
import matplotlib.pyplot as plt

class Node:
    def __init__(self, name, x, y):
        self.name = name
        self.positionX = x
        self.positionY = y
        self.parent = None
        self.g = 0 # traversal distance from starting node
        self.h = 0 # euclidan distance from end node
        self.f = 0 # g + h
        self.neighboringNodes = {}
    
    def __hash__(self):
        return hash(self.name)

    def __eq__(self, value):
        return self.name == value.name
    
    def __lt__(self, other):
        return self.f < other.f
    
    def __repr__(self):
        rep = self.name + ", position X: " + str(self.positionX) + ", position Y: " + str(self.positionY)
        return rep

    def calculateEuclidanDistance(self, other):
        return math.sqrt(pow(self.positionX-other.positionX, 2) + pow(self.positionY-other.positionY, 2))
    
    def calculateG(self, parent):
        return self.neighboringNodes[parent] + parent.getG()

    def setParent(self, parent):
        self.parent = parent

    def setH(self, valueH):
        self.h = valueH
    
    def setG(self, valueG):
        self.g = valueG
    
    def setF(self, valueF):
        self.f = valueF

    def setNeighboringNodes(self, neighboringNodes):
        self.neighboringNodes = neighboringNodes
    
    # TODO : nanti ganti balik buat weighted adj matrix
    # def addEdge(self, edgeNode, edgeValue):
    #     edgeValue = self.calculateEuclidanDistance(edgeNode)
    #     self.neighboringNodes[edgeNode] = edgeValue
    
    def addEdge(self, edgeNode, edgeValue):
            self.neighboringNodes[edgeNode] = edgeValue

    def getName(self):
        return self.name
    
    def getX(self):
        return self.positionX
    
    def getY(self):
        return self.positionY
    
    def getParent(self):
        return self.parent
    
    def getG(self):
        return self.g
    
    def getH(self):
        return self.h

    def getF(self):
        return self.f
    
    def getNeighboringNodes(self):
        return self.neighboringNodes
    
def drawGraph(G):
    pos = nx.get_node_attributes(G, 'pos')
    #labels
    labels = nx.get_edge_attributes(G, 'weight')
    # nodes
    nx.draw_networkx_nodes(G, pos, node_size=10)

    #biar ada weight
    nx.draw_networkx_edge_labels(G,pos, edge_labels=labels)
    nx.draw(G,pos,node_color='blue',with_labels=True)
    plt.show()
    #End of Visualisasi Graph awal
    
def drawResult(G,start,finish):
    resultGraph = nx.astar_path(G, start, finish )
    #position
    pos = nx.get_node_attributes(G, 'pos')
    #labels
    labels = nx.get_edge_attributes(G, 'weight')
    # nodes
    nx.draw_networkx_nodes(G, pos, node_size=700)

    #biar ada weight
    nx.draw_networkx_edge_labels(G,pos, edge_labels=labels)


    # Set all edge color attribute to black
    for e in G.edges():
        G[e[0]][e[1]]['color'] = 'black'
    # Set color of edges of the shortest path to green
    for i in range(len(resultGraph)-1):
        G[resultGraph[i]][resultGraph[i+1]]['color'] = 'blue'
    # Store in a list to use for drawing
    edge_color_list = [ G[e[0]][e[1]]['color'] for e in G.edges() ]
    node_colors = ["red" if n in resultGraph else "blue" for n in G.nodes()]
    nx.draw(G,pos,node_color=node_colors,edge_color = edge_color_list, with_labels = True)
    plt.show()
    
def aStar(startNode, endNode):
    print(startNode)
    print(endNode)
    openQueue = [] # priority queue for to-be-evaluated-nodes
    finishedList = [] #  list for already evaluated nodes
    result = [] # result path
    shortestDistance = 0
    
    openQueue.append(startNode)
    while len(openQueue) != 0:
        openQueue.sort()
        currentNode = openQueue.pop(0)
        finishedList.append(currentNode)

        if currentNode == endNode:
            # TODO : benerin nilai g
            shortestDistance = currentNode.getG()
            while currentNode != startNode:
                print(currentNode, currentNode.getG())
                result.append(currentNode)
                currentNode = currentNode.getParent()
            result.append(startNode)
            print(startNode, startNode.getG())
            result.reverse()
            return (result, shortestDistance)
        
        # TODO : add exception buat nangani gaada sisi berhubungan
        listOfNeighboringNodes = currentNode.getNeighboringNodes().keys()
        for node in listOfNeighboringNodes:
            # hitung f,g,h
            newG = currentNode.getG() + node.calculateG(currentNode)
            newH = node.calculateEuclidanDistance(endNode)
            newF = newH + newG
            if node not in openQueue or newF < node.getF():
                node.setG(newG)
                node.setH(newH)
                node.setF(newF)
                node.setParent(currentNode)
                if node not in openQueue:
                    openQueue.append(node)

def main():
    file = open("../test/ITB.txt", "r")
    lines = file.readlines()
    rawNodes = []
    adjMatrix = []
    listOfNodes = []

    countNodes = int(lines[0])
    for i in range(1, len(lines)):
        if i <= countNodes:
            rawNodes.append(lines[i].split())
        else:
            adjMatrix.append(lines[i].split())
    
    for i in range(countNodes):
        nodeName = rawNodes[i][0]
        nodePositionX = float(rawNodes[i][1])
        nodePositionY = float(rawNodes[i][2])
        listOfNodes.append(Node(nodeName, nodePositionX, nodePositionY))
    
    for i in range(len(adjMatrix)):
        for j in range(len(adjMatrix)):
            if j != i and float(adjMatrix[i][j]) > 0:
                listOfNodes[i].addEdge(listOfNodes[j], float(adjMatrix[i][j]))

    for node in listOfNodes:
        print(node)
        print(node.getNeighboringNodes())

    print("Welcome to our map!")
    
    #Visualisasi Graph
    G=nx.Graph()
    for i in range(countNodes):
        G.add_node(rawNodes[i][0],pos=(float(rawNodes[i][1]),float(rawNodes[i][2])) )
    
    for i in range(len(adjMatrix)):
        for j in range(len(adjMatrix)):
            if j != i and float(adjMatrix[i][j]) > 0:
                G.add_edge(rawNodes[i][0],rawNodes[j][0],weight=float(adjMatrix[i][j]))
    drawGraph(G)
    
    print("Please input your starting node here: ")
    for (index, node) in enumerate(listOfNodes):
        print(index+1, node)
    startInput = int(input())
    print("Please input your end node here: ")
    for (index, node) in enumerate(listOfNodes):
        print(index+1, node)
    endInput = int(input())
    result = aStar(listOfNodes[startInput-1], listOfNodes[endInput-1])
    print("path", result[0])
    print("distance", result[1])
    
    #Visualize path
    drawResult(G, listOfNodes[startInput-1].name, listOfNodes[endInput-1].name)
    
    

if __name__ == "__main__": main()
