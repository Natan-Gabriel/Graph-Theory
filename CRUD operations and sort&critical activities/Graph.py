import math
import queue
from random import random, randint


class Graph:
    def __init__(self, n):
        """Creates a graph with n vertices (numbered from 0 to n-1)
        and no edges"""
        self._n = n
        self._vector=[[math.inf for x in range(n)] for y in range(n)]
        for i in range(self._n):
            self._vector[i][i]=0

        self._eb = {}  # earliest begin
        self._ee = {}  # earliest end
        # self._eb[0]=0
        # self._ee[0]=0
        self._lb = {}  # latest begin
        self._le = {}
        # self._lb[0]=0
        # self._le[0]=0

        for i in range(0, self._n):
            self._eb[i] = 0
            self._lb[i] = math.inf
            self._ee[i] = 0
            self._le[i] = math.inf

        self._lb[0] = 0
        self._le[0] = 0

        self._vertices = n
        self._edges = 0
        self._dictOut = {}
        self._dictIn = {}
        for i in range(self._n):
            self._dictOut[i] = []
            self._dictIn[i] = []
        self._costs = {}
        self._eb[0] = 0
        self._eb[self._n - 1] = 0
        self.cc = 0
        # self.readFromFile()
        # print(self._dictOut)
        # print(self._dictIn)

    def readFromFile(self):

        # result=[]
        try:
            f = open("file.txt", 'r')
            line = f.readline().strip()
            line = line.split(" ")
            self._vertices = int(line[0])
            self._edges = int(line[1])
            line = f.readline().strip()
            while len(line) > 0:
                line = line.split(' ')

                self._dictOut[int(line[0])].append(int(line[1]))
                self._dictIn[int(line[1])].append(int(line[0]))
                self._costs[int(line[1])] = int(line[2])
                # self._costs[(int(line[1]),int(line[0]))]=int(line[2])

                # self._vector[int(line[0])][int(line[1])]=int(line[2])
                # print(int(line[0]))
                # print(int(line[1]))
                line = f.readline().strip()
            f.close()
        except IOError as e:
            print(e)

    def parseX(self):
        """Returns an iterable containing all the vertices"""
        return self._dictOut.keys()

    '''
    def parseNout(self,x):
        """Returns an iterable containing the outbound neighbours of x"""
        return self._dictOut[x]
    '''

    def parseNin(self, x):
        """Returns an iterable containing the inbound neighbours of x"""
        return self._dictIn[x]

    def isEdge(self, x, y):
        """Returns True if there is an edge from x to y, False otherwise"""
        # print(self._dictOut[x])
        if (0 <= x and 0 <= y and x < self._vertices and y < self._vertices):
            return y in self._dictIn[x]
        else:
            return -1

    # except ValueError("value error")

    def addEdge(self, x, y, z):
        """Adds an edge from x to y.
        Precondition: there is no edge from x to y"""

        if self.isEdge(x, y) == -1:
            print("Imposible to add this edge")

        elif self.isEdge(x, y) == False:
            self._dictIn[x].append(y)
            self._dictIn[y].append(x)
            self._costs[(x, y)] = z
            self._costs[(y, x)] = z
        elif self.isEdge(x, y) == False:
            print("Already existing")

    def isVertex(self, vertex):
        return vertex in self._dictIn.keys()

    def deleteEdge(self, x, y):
        if self.isEdge(x, y) == -1:
            print("Imposible to add this edge")
        elif self.isEdge(x, y):
            self._dictIn[x].remove(y)
            self._dictIn[y].remove(x)
            del self._costs[(x, y)]
        else:
            print("There is no edge between x and y")

    def addVertex(self, vertex):
        if not self.isVertex(vertex):
            self._dictIn[vertex] = []
            self._vertices += 1
        else:
            print("Already existing")

    def deleteVertex(self, vertex):
        if self.isVertex(vertex):
            # print("Yes")
            '''
            for i in self._dictOut[vertex]:
                self.deleteEdge(vertex,i)
                '''
            for i in self._dictIn[vertex]:
                self.deleteEdge(i, vertex)
                self.deleteEdge(vertex, i)
            # del self._dictOut[vertex]
            del self._dictIn[vertex]
            self._vertices -= 1

        else:
            print("Inexisting vertex!")

    def getNumberOfVertices(self):
        return self._vertices

    def getInDegree(self, vertex):
        return len(self._dictIn[vertex])

    def getOutDegree(self, vertex):
        return len(self._dictOut[vertex])

    def getVertices(self):
        return self._dictIn.keys()

    def getInboundVertices(self, vertex):
        if self.isVertex(vertex):
            return self._dictIn[vertex]
        else:
            return False

    def getOutboundVertices(self, vertex):
        if self.isVertex(vertex):
            return self._dictOut[vertex]
        else:
            return False

    def seeCost(self, x):
        return self._costs[x]

    def modifyCost(self, x, y, z):
        if (self.isEdge(x, y) == False):
            return False
        self._costs[(x, y)] = z

    def makeCopy(self):
        # new_self_vertices=self._vertices
        dictOutCopy = {}
        dictInCopy = {}
        costsCopy = {}
        for i in range(self._n):
            dictOutCopy[i] = deepcopy(self._dictOut[i])
            dictInCopy[i] = deepcopy(self._dictIn[i])
        for i in range(self._n):
            for j in range(self._n):
                costsCopy[(i, j)] = deepcopy(self._costs[(i, j)])
        return [dictOutCopy, dictInCopy, costsCopy]

    def createRandom(self, vertices, edges):
        if (vertices * vertices < edges):
            return 1
        a = Graph(vertices)
        for i in range(0, edges):
            v1 = randint(0, vertices - 1)
            v2 = randint(0, vertices - 1)
            cost = randint(-1000, 1000)
            while a.isEdge(v1, v2):
                v1 = randint(0, vertices - 1)
                v2 = randint(0, vertices - 1)
            a.addEdge(v1, v2, cost)
        return a

    def BFS(self, list, s):
        a = 0

        visited = [False] * (self._n)
        queue = []
        edges = []
        queue.append(s)
        visited[s] = True

        while queue:
            s = queue.pop(0)
            print(s, " ")
            list.append(s)
            a += 1
            for i in self._dictIn[s]:
                if visited[i] == False:
                    edges.append([s, i])
                    queue.append(i)
                    visited[i] = True
                elif visited[i] == True and [i, s] not in edges:
                    edges.append([s, i])
        print("")
        # if (a!=1000):
        #    print (a)
        # print (a)
        return [list, edges]

    def printMatrix(self):
        for i in range(self._n):
            print(self._vector[i][0], self._vector[i][1], self._vector[i][2], self._vector[i][3], self._vector[i][4])

    def costOfPath(self, path):
        sum = 0
        if len(path) == 2:
            return self._vector[path[0]][path[1]]
        for i in range(len(path) - 1):
            sum += self._vector[path[i]][path[i + 1]]
        return sum

    def printAllPathsUtil(self, u, d, visited, path, minCost):

        # Mark the current node as visited and store in path
        visited[u] = True
        path.append(u)

        # If current vertex is same as destination, then print
        # current path[]
        if u == d and minCost == self.costOfPath(path):
            print(path)
        else:
            # If current vertex is not destination
            # Recur for all the vertices adjacent to this vertex
            for i in range(self._n):
                if self._vector[u][i] != math.inf and visited[i] == False:
                    self.printAllPathsUtil(i, d, visited, path, minCost)

                    # Remove current vertex from path[] and mark it as unvisited
        path.pop()
        visited[u] = False

    # Prints all paths from 's' to 'd'
    def printAllPaths(self, s, d, minCost):
        # minCost=self.cost(s,d,200)
        # Mark all the vertices as not visited
        visited = [False] * (self._n)

        # Create an array to store paths
        path = []

        # Call the recursive helper function to print all paths
        self.printAllPathsUtil(s, d, visited, path, minCost)

    def countPathsUtil(self, u, d, visited, pathCount):
        visited[u] = True

        if (u == d):
            pathCount[0] += 1
        else:
            for index in range(self._n):
                if (self._vector[u][index] != math.inf and not visited[index]):
                    # pathCount[1]+=
                    self.countPathsUtil(index, d, visited, pathCount)
        visited[u] = False

    def allPaths(self, s, d):
        a = 2
        visited = [False] * self._n

        pathCount = [0, 0]
        self.countPathsUtil(s, d, visited, pathCount)
        return pathCount[0]

    def cost(self, u, v, k):
        # here we check the existence of negative cycles
        dist = [[math.inf for x in range(self._n)] for y in range(self._n)]
        for i in range(self._n):
            for j in range(self._n):
                dist[i][j] = self._vector[i][j]
        for k in range(self._n):
            for i in range(self._n):
                for j in range(self._n):
                    dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])
        for h in range(self._n):
            if dist[h][h] < 0:
                print("We have negative cycles!")
                return

        sp = [[None] * self._n for i in range(self._n)]
        for i in range(self._n):
            for j in range(self._n):
                sp[i][j] = [None] * (k + 1)

                # Loop for number of edges from 0 to k
        for e in range(k + 1):
            for i in range(self._n):  # for source
                for j in range(self._n):  # for destination

                    # initialize value
                    sp[i][j][e] = math.inf

                    # from base cases
                    if (e == 0 and i == j):
                        sp[i][j][e] = 0
                    if (e == 1 and self._vector[i][j] != math.inf):
                        sp[i][j][e] = self._vector[i][j]

                        # go to adjacent only when number
                    # of edges is more than 1
                    if (e > 1):
                        for a in range(self._n):

                            # There should be an edge from
                            # i to a and a should not be
                            # same as either i or j
                            if (self._vector[i][a] != math.inf and i != a and
                                    j != a and sp[a][j][e - 1] != math.inf):
                                # if(sp[i][j][e]<self._vector[i][a] +
                                # sp[a][j][e - 1]):
                                #   print(a)
                                sp[i][j][e] = min(sp[i][j][e], self._vector[i][a] +
                                                  sp[a][j][e - 1])

        for e in range(1, k + 1):
            sp[u][v][e] = min(sp[u][v][e], sp[u][v][e - 1])
        # print(sp[u][v][k])
        return sp[u][v][k]

    def addActivity(self, x, y, l):
        pass

    def sort(self):
        sorted = []
        q = queue.Queue(maxsize=20)
        count = {}
        for x in range(self._n):
            count[x] = self.getInDegree(x)
            # print(x,count[x])
            if count[x] == 0:
                q.put(x)
        print(list(q.queue))
        while not q.empty():
            x = q.get()
            sorted.append(x)
            for y in self.getOutboundVertices(x):
                count[y] = count[y] - 1
                if count[y] == 0:
                    q.put(y)
        if len(sorted) < self._n:
            sorted = NULL
        return sorted

    def times(self):
        a = self.sort()
        for i in a:
            for j in self.getInboundVertices(i):
                # if i!=0:
                self._eb[i] = max(self._eb[i], self._ee[j])
                # print(j,self._lb[j])
            if i != 0 and i != 1:
                self._ee[i] = self._eb[i] + self._costs[i]
            elif i == 1:
                self._lb[i] = self._eb[i]
                self._le[i] = self._eb[i]
                self._ee[i] = self._eb[i]
            # print(i,self._eb[i])

        # print(a)
        # for i in reversed(a):
        #    print(i)
        for i in reversed(a):
            if i != 0 and i != 1:
                for j in self.getOutboundVertices(i):
                    # if i!=0:
                    self._le[i] = min(self._le[i], self._lb[j])
                    # print(j,self._lb[j])

                self._lb[i] = self._le[i] - self._costs[i]
                # print(i,self._le[i])

        for i in range(0, self._n):
            print(i, "starts earliest at ", self._eb[i], " and starts latest at ", self._lb[i])
        print("Total execution time", self._eb[1])

    def critical(self):
        a = self.sort()
        for i in a:
            for j in self.getInboundVertices(i):
                # if i!=0:
                self._eb[i] = max(self._eb[i], self._ee[j])
                # print(j,self._lb[j])
            if i != 0 and i != 1:
                self._ee[i] = self._eb[i] + self._costs[i]
            elif i == 1:
                self._lb[i] = self._eb[i]
                self._le[i] = self._eb[i]
                self._ee[i] = self._eb[i]
            # print(i,self._eb[i])

        # print(a)
        # for i in reversed(a):
        #    print(i)
        for i in reversed(a):
            if i != 0 and i != 1:
                for j in self.getOutboundVertices(i):
                    # if i!=0:
                    self._le[i] = min(self._le[i], self._lb[j])
                    # print(j,self._lb[j])

                self._lb[i] = self._le[i] - self._costs[i]
        for i in range(0, self._n):
            if self._ee[i] == self._le[i]:
                print(i, "is a critical activity")


def solve(t):
    n = len(t)
    t.sort()
    if n == 0:
        return 0, []
    elif n == 1:
        return t[0], [t[0]]
    elif n == 2:
        return t[1], [(t[0], t[1])]
    total = (n - 2) * t[0] + sum(t[1:])

    ''' 
    x = n
    index = 2 * t[1] - t[0]    
    while t[x - 2] > index:
        total -= t[x - 2] - index
        x -= 2
    seq = []

    i = n - 1                    
    while i > 1:
        if i >= x:
            seq += [(t[0], t[1]), t[1], (t[i - 1], t[i]), t[0]]
            i -= 2
        else:
            seq += [(t[0], t[i]), t[0]]
            i -= 1
    seq.append((t[0], t[1]))  

    return total, seq
    '''
    return total


def createSubgraph(result):
    nrVertices = max(result[0])

    subgraph = Graph(nrVertices + 1)
    for edge in result[1]:
        subgraph.addEdge(edge[0], edge[1], 0)
    return subgraph


def printMenu():
    print("1.Check whether a pair is an edge")
    print("2.Add an edge")
    print("3.Delete an edge")
    print("4.Check whether a point is a vertex")
    print("5.Add a vertex")
    print("6.Delete a vertex")
    print("7.Print number of vertices")
    print("8.Print the in-degree of a given vertex")
    print("9.Print the out-degree of a given vertex")
    print("10.Parse vertices")
    print("11.Parse inbound vertices")
    print("12.Parse outbound vertices")
    print("13.Make a copy of the graph")
    print("14.See the cost between 2 edges")
    print("15.Modify the cost between 2 edges")
    print("16.Create random")
    print("17.Print connected components")
    print("18.Min cost between 2 given vertices")
    print("19.Print the number of distinct walks of minimum cost between 2 vertices")
    print("20.Print number of all paths between 2 vertices")
    print("21.Minimum time for crossing the bridge")
    print("22.Print matrix")
    print("23.Sort activities")
    print("24.prints the earliest and the latest starting time for each activity")
    print("25.Print critical activites")


def menu():
    nrVertices = 9
    graph = Graph(nrVertices)
    graph.readFromFile()
    # a=graph.makeCopy()
    # graph
    while True:
        printMenu()
        # print(graph._dictOut)
        # print(graph._dictIn)
        cmd = input("Enter a command:")
        if int(cmd) == 1:
            x = int(input("Enter starting point of edge:"))
            y = int(input("Enter the end point:"))
            print(graph.isEdge(x, y))
        elif int(cmd) == 2:
            x = int(input("Enter starting point of edge:"))
            y = int(input("Enter the end point:"))
            z = int(input("Enter the cost:"))
            graph.addEdge(x, y, z)
        elif int(cmd) == 3:
            x = int(input("Enter starting point of edge:"))
            y = int(input("Enter the end point:"))
            graph.deleteEdge(x, y)
        elif int(cmd) == 4:
            vertex = int(input("Enter a vertex"))
            print(graph.isVertex(vertex))
        elif int(cmd) == 5:
            vertex = int(input("Enter a vertex"))
            graph.addVertex(vertex)
        elif int(cmd) == 6:
            vertex = int(input("Enter a vertex"))
            graph.deleteVertex(vertex)
        elif int(cmd) == 7:
            print(graph.getNumberOfVertices())
        elif int(cmd) == 8:
            vertex = int(input("Enter a vertex"))
            print("In degree:", graph.getInDegree(vertex))
        elif int(cmd) == 9:
            vertex = int(input("Enter a vertex"))
            print("Out degree:", graph.getOutDegree(vertex))
        elif int(cmd) == 10:
            print("Vertices:")
            for i in graph.getVertices():
                print(i)
        elif int(cmd) == 11:
            vertex = int(input("Enter a vertex:"))
            print("Inbound vertices:")

            if (graph.getInboundVertices(vertex) == False):
                print("No vertex")
            else:
                for i in graph.getInboundVertices(vertex):
                    print(i)
        elif int(cmd) == 12:
            print("Outbound vertices:")
            vertex = int(input("Enter a vertex:"))
            if (graph.getOutboundVertices(vertex) == False):
                print("No vertex")
            else:
                for i in graph.getOutboundVertices(vertex):
                    print(i)
        elif int(cmd) == 13:
            # for i in a[0][1]:
            #   print(i)
            a = graph.makeCopy()
        elif int(cmd) == 14:
            x = int(input("Enter starting point of edge:"))
            # y=int(input("Enter the end point:"))
            print(graph.seeCost(x))

            # if(graph.seeCost(x,y)==False):
            #   print("NO edge between the 2 edges")
            # else:
            #    print("The cost is: ")
            #    print(graph.seeCost(x,y))
        elif int(cmd) == 15:
            x = int(input("Enter starting point of edge:"))
            y = int(input("Enter the end point:"))
            z = int(input("Enter the new cost:"))
            if (graph.isEdge(x, y) == False):
                print("NO edge between the 2 edges")
            else:
                graph.modifyCost(x, y, z)
        elif int(cmd) == 16:
            x = int(input("Enter nr of vertices:"))
            y = int(input("Enter nr of edges:"))

            a = graph.createRandom(x, y)

            if (a == 1):
                print("Too many edges!")
                return
        elif int(cmd) == 17:
            list = []
            result = graph.BFS(list, 0)
            list = result[0]

            print(result[1])
            subgraph = createSubgraph(result)
            for i in range(1, nrVertices):
                if i not in list:
                    result = graph.BFS(list, i)
                    l = result[0]
                    for x in l:
                        if x not in list:
                            list.append(x)
                elif len(list) == nrVertices:
                    break
        elif int(cmd) == 18:
            x = int(input("Enter starting point:"))
            y = int(input("Enter the end point:"))
            print(graph.costOfPath([x, y]))
        elif int(cmd) == 19:
            x = int(input("Enter starting point:"))
            y = int(input("Enter the end point:"))
            minCost = graph.cost(x, y, 200)
            graph.printAllPaths(x, y, minCost)
            print(minCost)
        elif int(cmd) == 20:
            x = int(input("Enter starting point:"))
            y = int(input("Enter the end point:"))
            print(graph.allPaths(x, y))
        elif int(cmd) == 21:
            t = [10, 20, 30, 40]
            print(solve(t))
        elif int(cmd) == 22:
            graph.printMatrix()

        elif int(cmd) == 23:
            a = graph.sort()
            if (a == 0):
                print("The graph is not a DAG")
            else:
                print("Our graph is a DAG")
                print("The order of the activites is: ", a)
        elif int(cmd) == 24:
            graph.times()
        elif int(cmd) == 25:
            graph.critical()
        elif cmd == exit:
            return


menu()