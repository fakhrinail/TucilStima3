import math

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

    def __eq__(self, value):
        return self.name == value.name
    
    def __lt__(self, other):
        return self.f < other.f
    
    def __repr__(self):
        rep = self.name + ", position X: " + str(self.positionX) + ", position Y: " + str(self.positionY) + self.neighboringNodes
        return rep

    def calculateEuclidanDistance(self, other):
        return math.sqrt(pow(self.positionX-other.positionX, 2) + pow(self.positionY-other.positionY, 2))
    
    def calculateG(self, parent):
        return self.neighboringNodes[parent] + parent.getG()

    def setParent(self, parent):
        self.parent = parent

    def setH(self, other):
        self.h = self.calculateEuclidanDistance(other)
    
    def setG(self, valueG):
        self.g = valueG
    
    def setF(self, valueF):
        self.f = valueF

    def setNeighboringNodes(self, listOfNodes):
        self.neighboringNodes = listOfNodes
    
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

def aStar(startNode, endNode):
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
            while currentNode.getParent() != None:
                shortestDistance += currentNode.getG()
                result.append(currentNode)
                currentNode = currentNode.getParent()
            return (result, shortestDistance)
        
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
    file = open("../test/Alunalun.txt", "r")
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
            if j != i and adjMatrix[i][j] > 0:
                listOfNodes[i].addEdge(listOfNodes[j], adjMatrix[i][j])

    for node in listOfNodes:
        print(node)
    
    # aStar(listOfNodes[0], listOfNodes[1])

if __name__ == "__main__": main()