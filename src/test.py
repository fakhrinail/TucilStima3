class Test:
    def __init__(self, name, x, y, value):
        self.name = name
        self.positionX = x
        self.positionY = y
        self.value = value
        
    def __eq__(self, other):
        return self.name == other.name
    
    def __lt__(self, other):
        return self.value < other.value
    
    def __repr__(self):
        return str(self.value)

def main():
    test = Test("test", 0, 0, 5)
    listOfTests = []
    listOfTuples =[]

    for i in range(5):
        listOfTests.append(Test("test" + str(i), i, i, i))
        tupleTest = ("test"+ str(i), i)
        listOfTuples.append(tupleTest)
    
    listOfTests.append(Test("test", 1, 0, 10))
    listOfTests.sort()
    print(listOfTests)
    # if test in listOfTests:
    #     print("bisa")
    # else:
    #     print("gagal")

    testTuple = ("test1", 1)
    test = "test1"
    if test in listOfTuples:
        print("tuple")

if __name__ == "__main__": main()