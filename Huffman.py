# Isaac Brinkman
# Algorithms project
# takes a text file and encodes it using the huffman algorithm
from typing import Dict
import sys
# my own implemented version of the heap class
from myheap import heap



# loads a file and returns a dictionary with the char and the frequency
def load_file(fn: str) -> Dict[str, int]:
    freq = dict()
    f = open(fn)
    for line in f:
        for ch in line:
            if ch not in freq:
                freq.update({ch: 0})
            freq[ch] += 1
    return freq


# tree class
# has a left child and right child
class Tree:
    def __init__(self, left=None, right= None):
        self.left = left
        self.right = right

    def __lt__(self, other):
        return self


# turns the heap into a huffman tree
def huffman(h: heap):
    while len(h._h) > 1:
        # delete the root
        root1 = h.delete_root()
        # heapify (turns the list into a heap)
        h.heapify()
        # delete the root again
        root2 = h.delete_root()

        # make a new tree root is empty the left and right are old roots
        new_tree = Tree(root1[1], root2[1])
        # val is the root values added
        val = root1[0] + root2[0]

        # append to the heap
        h._h.append((val,new_tree))
        # heapify it
        h.heapify()


# make a min heap of char freq
def build_heap(freq) -> heap:
    # each element in the heap is a tuple of (freq, tree)
    h = heap([(freq[k],k) for k in freq])
    return h

# goes through the finished heap and encodes
# this makes it so the most frequent character is 1 bit long
# and less frequent characters are longer
def encode_rec(root, code = ""):
    # base case
    if type(root) is str:
        return {root: code}

    if type(root) is tuple:
        root = root[1]

    left = root.left
    right = root.right

    encoding_dict = dict()
    encoding_dict.update(encode_rec(left, (code + "0")))
    encoding_dict.update(encode_rec(right, (code + "1")))

    return encoding_dict

# computes the amount of space needed to store the encoded text
def encoded_length(freq: Dict, encoded: Dict) -> int:
    count = 0
    for k in encoded:
        count += len(encoded[k]) * freq[k]
    # change from bits to bytes
    return count//8

# computes amount of space to store the text as is
def reg_len(freq: Dict) -> int:
    count = 0
    for k in freq:
        count += freq[k]
    return count


if __name__ == '__main__':
    # allows this program to be run from the command line
    sysarg = sys.argv
    freq = load_file(sys.argv[1])

    heaper = build_heap(freq)

    # run huffman
    huffman(heaper)
    # prints the huffman encoding length uncompressed and length compressed
    print("Traversal: ", encode_rec(heaper._h[0][1]))
    print(reg_len(freq), "Bytes uncompressed")
    print(encoded_length(freq, encode_rec(heaper._h[0][1])), "Bytes compressed")



