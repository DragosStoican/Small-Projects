# node class with state, parent, action that got you there from the parent and path cost to this node
# make a func that takes the problem repr and creates a tree with no repeating states
# seach with increasing limit dfs

# I used iterative DLS so I didn't need to check the visited states

# the problem representation can be found at problem representation.png
import copy
import random
import sys

sys.setrecursionlimit(200000)


class Node:
    state = dict()  # A dictionary with each tile as a key and the location (1 - 9) it is in
    parent = None
    action = ""  # The action that was performed to get from the parent to the current state (Left/Right/Up/Down)
    depth = 0  # The depth of the node

    def __init__(self, state, parent, action, pathCost):
        self.state = state
        self.parent = parent
        self.action = action
        self.depth = pathCost

    # Two nodes are the same if they represent the same state
    def isGoal(self, goal):
        return self.state == goal

    # Returns a set of nodes to which you can get from the current node
    def actions(self):
        actionsSet = set()

        # Get the current location of the blank tile
        blankLocation = self.state["blank"]

        # 1. Move the blank space to the left, if possible
        child = self.__getChildFromMove__(blankLocation, "Left")
        if child is not None: actionsSet.add(child)

        # 2. Move the blank space to the right, if possible
        child = self.__getChildFromMove__(blankLocation, "Right")
        if child is not None: actionsSet.add(child)

        # 3. Move the blank space up, if possible
        child = self.__getChildFromMove__(blankLocation, "Up")
        if child is not None: actionsSet.add(child)

        # 4. Move the blank space down, if possible
        child = self.__getChildFromMove__(blankLocation, "Down")
        if child is not None: actionsSet.add(child)

        return actionsSet

    def __getChildFromMove__(self, blankLocation, move):
        childNode = Node(copy.copy(self.state), self, "", self.depth + 1)
        invalidLocations = {"Left": [1, 4, 7], "Right": [3, 6, 9], "Up": [1, 2, 3], "Down": [7, 8, 9]}
        if blankLocation not in invalidLocations[move]:
            # Get the new location of the blank space
            newLocations = {"Left": -1, "Right": 1, "Up": -3, "Down": 3}
            newBlankLocation = blankLocation + newLocations[move]
            # Check which tile is the blank swapped with
            swapTile = self.__getTileAtLocation__(newBlankLocation)

            # Swap the 2 tiles in the childNode and add it to the list
            childNode.state["blank"] = newBlankLocation
            childNode.state[swapTile] = blankLocation
            childNode.action = move
            return childNode
        return None

    # Returns the tile at a location in the current state
    def __getTileAtLocation__(self, location):
        for key, value in self.state.items():
            if value == location:
                return key

    # Returns the list of actions needed to reach the current state
    def solution(self):
        solution = ""
        parent = self
        while parent is not None:
            solution = parent.action + " " + solution
            parent = parent.parent
        return solution

    def __str__(self):
        return str(self.state)


def depthLimitedSearch(fringe, goal, limit, visited):
    while len(fringe) > 0:
        node = fringe.pop()
        if node.isGoal(goal):
            return node.solution()
        if node.depth < limit:
            for child in node.actions():
                if child.state not in visited:
                    visited.append(child.state)
                    fringe.append(child)
    return None


# def recursive_depthLimitedSearch(fringe, goal, limit, visited):
#     if len(fringe) == 0:
#         return None
#     node = fringe.pop()
#
#     if node.isGoal(goal):
#         return node.solution()
#     #print(node.solution(), limit, node.depth)
#     if node.depth < limit:
#         for child in node.actions():
#             print(child.depth)
#             if child.state not in visited:
#                 #print("added child")
#                 fringe.append(child)
#                 visited.append(child.state)
#     return recursive_depthLimitedSearch(fringe, goal, limit, visited)


def iterativeDFS(root, goal):
    if root.isGoal(goal):
        return root.solution()
    result = None
    limit = 0
    while result is None:
        result = depthLimitedSearch([root], goal, limit, [root])
        limit += 1
    return result


def nrInversions(state):
    count = 0
    for i in range(1, len(state)):
        for j in range(1, len(state)):
            if j < i and state[str(j)] > state[str(i)]:
                count += 1
    return count


# Create the goal state so we can perform the goal test
goalState = {"1": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "blank": 9}

# To create the initial state we need a shuffled list of all possible locations
shuffledList = random.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], 9)
# Create the initial state
initialState = {"1": shuffledList[0], "2": shuffledList[1], "3": shuffledList[2],
                "4": shuffledList[3], "5": shuffledList[4], "6": shuffledList[5],
                "7": shuffledList[6], "8": shuffledList[7], "blank": shuffledList[8]}

# We need to check if the nr of inversions is ever, otherwise the puzzle is not solvable
while nrInversions(initialState) % 2 != 0:
    shuffledList = random.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], 9)
    initialState = {"1": shuffledList[0], "2": shuffledList[1], "3": shuffledList[2],
                    "4": shuffledList[3], "5": shuffledList[4], "6": shuffledList[5],
                    "7": shuffledList[6], "8": shuffledList[7], "blank": shuffledList[8]}

# Create the root node of the searchTree
root = Node(initialState, None, "", 0)
print(str(initialState))
print(nrInversions(initialState))
print(iterativeDFS(root, goalState))
