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

    for i in range(5):
        listOfTests.append(Test("test" + str(i), i, i, i))
    
    listOfTests.append(Test("test", 1, 0, 10))
    listOfTests.sort()
    print(listOfTests)
    # if test in listOfTests:
    #     print("bisa")
    # else:
    #     print("gagal")

if __name__ == "__main__": main()