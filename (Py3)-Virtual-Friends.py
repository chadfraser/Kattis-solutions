"""
https://open.kattis.com/problems/virtualfriends
A program to determine the number of people in various disjoint sets of friends.
"""

# Initialize the dictionary we'll be using in our tests
# This dictionary will store names inputted by the user, as well as the disjoint set of friends to that person
disjoint_friends_dict = {}


class DisjointSet:
    # Initialized disjoint sets have themselves as their parent (i.e., they are alone in the set)
    def __init__(self):
        self.parent = self
        self.size = 1

    # Find the root of the disjoint set
    def find(self):
        # If the node points to itself, it is the root
        if self.parent == self:
            return self
        # Otherwise, reiterate through this function with this node's parent
        # This compresses the path, such that all nodes in the path end up pointing directly to the root
        else:
            self.parent = DisjointSet.find(self.parent)
            return self.parent

    # Merge the two sets passed to it (self and second_set)
    def union(self, second_set):
        first_root = DisjointSet.find(self)
        second_root = DisjointSet.find(second_set)
        # If these two sets have the same root, they are already in the same disjoint set
        if first_root == second_root:
            return first_root.size

        # Otherwise, we compare the sizes of our sets, and connect the root of the smaller set to the other root
        elif first_root.size > second_root.size:
            second_root.parent = first_root
            first_root.size += second_root.size
            return first_root.size
        else:
            first_root.parent = second_root
            second_root.size += first_root.size
            return second_root.size


# Take in user input to see how many cases to test
amount_of_inputs = input()
for __ in range(int(amount_of_inputs)):
    friendships_formed = input()

    # Take in as many inputs of friends as requested by the user
    for friends_to_test in range(int(friendships_formed)):
        friends_added = input()
        first_name, second_name = friends_added.split(" ")

        # If either name is not already in our disjointFriendsDict (i.e., the user hasn't passed that name
        # to us yet), add it to the dictionary with a new DisjointSet class assigned to it
        if first_name not in disjoint_friends_dict:
            disjoint_friends_dict[first_name] = DisjointSet()
        if second_name not in disjoint_friends_dict:
            disjoint_friends_dict[second_name] = DisjointSet()

        # Then, take the union of the two DisjointSet classes and print its size
        union_size = disjoint_friends_dict[first_name].union(disjoint_friends_dict[second_name])
        print(union_size)

    # After running through all of the friendships formed in the test case, reset our disjoint_friends_dict
    # to its default empty state
    disjoint_friends_dict = {}
