from numpy import log2, ceil
from hashlib import sha1 as sha

def readFile():
    with open("merkleHash.txt") as f:
        i, j = f.readline()[:-1], f.readline()[:-1]
        leaves = [line[:-1] for line in f]
        return int(i), int(j), leaves

def buildTree(nodes, parents):
    if(len(parents) == 1):
        return nodes
    temp = []
    for i in range(0, len(parents), 2):
        a, c = parents[i], parents[i + 1]
        print("A + C: " + a+c)
        parent = sha(bytearray.fromhex(a + c)).hexdigest()
        nodes.append(parent), temp.append(parent)
    if len(temp) != 1 and len(temp) % 2 != 0:
        nodes.append(temp[-1]), temp.append(temp[-1])
    return buildTree(nodes, temp)

def nrOfNodesPerDepth(nrOfLeaves, depth):
    nodesPerDepth = [nrOfLeaves if nrOfLeaves % 2 == 0 else nrOfLeaves + 1]
    for i in range(1, depth + 1):
        nbr_nodes = nodesPerDepth[i-1] // 2
        if(nbr_nodes != 1 and nbr_nodes % 2 != 0):
            nbr_nodes += 1
        nodesPerDepth.append(nbr_nodes)
    return nodesPerDepth

def buildPath(nodes, i, j, depth, nrOfLeaves):
    path, parentIndex, indexOfFirstNode = [], i, 0
    nodesPerDepth = nrOfNodesPerDepth(nrOfLeaves, depth)
    for k in range(depth):
        currentIndex = parentIndex + indexOfFirstNode
        if currentIndex % 2 == 0:
            node = "R" + nodes[currentIndex + 1]
        else:
            node = "L" + nodes[currentIndex - 1]
        path.append(node)
        parentIndex = (currentIndex - indexOfFirstNode) // 2
        indexOfFirstNode += nodesPerDepth[k]
    return list(reversed(path))

def solution():

    i, j, leaves = readFile()
    if len(leaves) % 2 == 1:
        leaves.append(leaves[-1])
    leafCount = len(leaves)
    depth, tree = int(ceil(log2(leafCount))), leaves

    tree = buildTree(tree, leaves)
    path = buildPath(tree, i, j, depth, leafCount)

    return "Test: " + path[j-1] + tree[-1]

print(solution())