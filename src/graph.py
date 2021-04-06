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
        if self.f == other.f:
            return self.g < other.g

        return self.f < other.f
    
    def __repr__(self):
        return self.name
        # return self.name + ", f" + str(self.f) + ", g" + str(self.g) + ", h" + str(self.h)

    def calculateEuclidanDistance(self, other):
        return math.sqrt(pow(self.positionX-other.positionX, 2) + pow(self.positionY-other.positionY, 2))
    
    def calculateG(self, parent):
        return self.neighboringNodes[parent] + parent.getG()
    
    def resetValues(self):
        self.parent = None
        self.g = 0 
        self.h = 0 
        self.f = 0 

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
    nx.draw_networkx_nodes(G, pos, node_size=5)

    #biar ada weight
    nx.draw_networkx_edge_labels(G,pos, edge_labels=labels)
    nx.draw(G,pos,node_color='blue',with_labels=True)
    plt.show()
    #End of Visualisasi Graph awal
    
def drawResult(G,resultGraph):
    
    #position
    pos = nx.get_node_attributes(G, 'pos')
    #labels
    labels = nx.get_edge_attributes(G, 'weight')
    # nodes
    nx.draw_networkx_nodes(G, pos, node_size=5)

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

def resetNodesValue(listOfNodes):
    for node in listOfNodes:
        node.resetValues()

def initNodesAndEdges(rawNodes, adjMatrix, countNodes):
    listOfNodes =  []

    # init nodes
    for i in range(countNodes):
        nodeName = rawNodes[i][0]
        nodePositionX = float(rawNodes[i][1])
        nodePositionY = float(rawNodes[i][2])
        listOfNodes.append(Node(nodeName, nodePositionX, nodePositionY))
    
    # add edges to nodes
    for i in range(len(adjMatrix)):
        for j in range(len(adjMatrix)):
            if j != i and float(adjMatrix[i][j]) > 0:
                listOfNodes[i].addEdge(listOfNodes[j], float(adjMatrix[i][j]))
    
    return listOfNodes

def aStar(startNode, endNode):
    print("start", startNode)
    print("end", endNode)
    openQueue = [] # priority queue for to-be-evaluated-nodes
    finishedList = [] #  list for already evaluated nodes
    result = [] # result path
    shortestDistance = 0
    
    openQueue.append(startNode)
    while len(openQueue) != 0:
        openQueue.sort()
        print(openQueue)
        currentNode = openQueue.pop(0)
        finishedList.append(currentNode)

        if currentNode == endNode:
            shortestDistance = currentNode.getG()
            print(currentNode)
            print(currentNode.getParent())
            while currentNode != startNode:
                print(currentNode, currentNode.getG())
                result.append(currentNode)
                currentNode = currentNode.getParent()
            
            result.append(startNode)
            result.reverse()

            return (result, shortestDistance)
        
        # TODO : add exception buat nangani gaada sisi berhubungan
        listOfNeighboringNodes = currentNode.getNeighboringNodes().keys()
        for neighboringNode in listOfNeighboringNodes:
            if neighboringNode in finishedList:
                continue
            
            # hitung f,g,h
            newG = neighboringNode.calculateG(currentNode)
            newH = neighboringNode.calculateEuclidanDistance(endNode)
            newF = newH + newG
            if newG < neighboringNode.getG() or neighboringNode not in openQueue:
                neighboringNode.setG(newG)
                neighboringNode.setH(newH)
                neighboringNode.setF(newF)
                neighboringNode.setParent(currentNode)
                if neighboringNode not in openQueue:
                    openQueue.append(neighboringNode)

def main():
    print("Input your file name: ")
    fileName = input()
    file = open("../test/" + fileName + ".txt", "r")
    lines = file.readlines()
    rawNodes = []
    adjMatrix = []

    # read input file
    countNodes = int(lines[0])
    for i in range(1, len(lines)):
        if i <= countNodes:
            rawNodes.append(lines[i].split())
        else:
            adjMatrix.append(lines[i].split())

    listOfNodes = initNodesAndEdges(rawNodes, adjMatrix, countNodes)
    # for node in listOfNodes:
    #     print(node)
    #     print(node.getNeighboringNodes())

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
    
    menuInput = "continue"
    while menuInput != "exit":
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
        resultGraph=[]
        for node in result[0]:
            resultGraph.append(node.name)
        
        #Visualize path
        drawResult(G, resultGraph)

        print("Type exit if you want to exit")
        print("Type anything else if you want to continue")
        menuInput = input()
        resetNodesValue(listOfNodes)
    
    exit()

if __name__ == "__main__": main()
