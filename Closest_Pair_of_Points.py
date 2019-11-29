# Isaac Brinkman
# Algorithms assignment

# Using a list of points (Vector) finds the two closest points through brute force
# and a divide-and-conquer approach
from typing import Tuple, List
from math import sqrt
import random


# simple vector class
# has an x and y value and knows how to compute magnitude with another vector
class Vector:
   def __init__(self, x1, y1):
       self.x = x1
       self.y = y1
       self.vect = (x1, y1)


   # returns a tuple of the x and y coordinates
   def get_coordinates(self):
       return self.vect

   # computes the magnitude of self and another vector
   def magnitude(self, v2) -> float:
       xcomp = abs(v2.get_coordinates()[0] - self.x)
       ycomp = abs(v2.get_coordinates()[1] - self.y)
       return sqrt((xcomp**2)+(ycomp**2))

   def __eq__(self, other):
       return self.y == other.y

   def __lt__(self, other):
       return self.y < other.y




# Brute force algorithm
# get a list of all the points and compute how far they are from every other point
# keep a closest variable
# O(n^2)
def bruteforce(points: List[Vector]) -> Tuple:
    # initialize the closest points as the first two points
    closest_val = points[0].magnitude(points[1])
    closest_points = (points[0].get_coordinates(), points[1].get_coordinates())

    # go through each point and compare it with every other point and
    # see if the magnitude is smaller than the current smallest
    for i in range(len(points)-1):
       for j in range(i+1, len(points)):
           if points[i].magnitude(points[j]) < closest_val:
               closest_val = points[i].magnitude(points[j])
               closest_points = (points[i].get_coordinates(), points[j].get_coordinates())

    # at the end of the loop return the closest points
    return closest_points, closest_val


# divide-and-conquer algorithm
# works by sorting the list and then splitting the list in half and checking the closest pairs
# within each section
# O(nlogn)
def dac(points1: List[Vector]) -> Tuple:
    # sort the list by x-axis
    lst = []
    # sorting is O(nlogn)
    lst = sorted(points1, key=lambda tup:tup.get_coordinates())


    # distance between closest points over a strip
    # O(n)
    def strip(s: List[Vector], size: int, dist: float) -> Tuple[float, Tuple]:
       min = dist
       coordinates = None
       s = sorted(s)

       # this loop runs at most 7 times so O(n)
       for i in range(size):
           for j in range(i+1, size):
               if (s[j].y - s[i].y) < min:
                   if s[j].magnitude(s[i]) < min:
                       min = s[j].magnitude(s[i])
                       coordinates = (s[j].get_coordinates(), s[i].get_coordinates())
       return min, coordinates

    # main function
    # splits the list in half and checks the closest pair in each
    def dac_helper(lst: List[Vector], n, coor) -> Tuple[Tuple[float, float], Tuple[float,float], float]:

       # base case:
       # if n is less than or equal to 3 compute it brute force
       if n <= 3:
           return bruteforce(lst)

       # get a midpoint of the list
       mid = n//2
       mid_point = lst[mid]

        # two recursive calls
       d1 = dac_helper(lst[:len(lst) // 2], mid, coor)      # splitting a list is O(1)
       d2 = dac_helper(lst[len(lst) // 2:], n - mid, coor)

        #O(1)
       #dist = min(d1, d2)
       if d1[1] < d2[1]:
           dist = d1
       else:
           dist = d2

       # check values over each strip
       # O(n)
       s = []
       for i in range(n):
           if abs(lst[i].x - mid_point.x) < dist[1]:
               s.append(lst[i])

       st = strip(s, len(s), dist[1])
       # see which is smaller the new strip min or the old smallest distance
       m = min(dist[1], st[0])
       if m == dist[1]:
           coor = (dist[0])
       else:
           coor = st[1]

       coor = (coor[0], coor[1])
       return coor, m

    return dac_helper(lst, len(lst), (Vector(0, 0), Vector(0, 0)))


if __name__ == '__main__':
    # generate n random points
    n = 1000
    p = []
    for i in range(n):
        x = random.randrange(-1000,1000)
        y = random.randrange(-1000,1000)
        p.append(Vector(x,y))

    print(bruteforce(p))
    print(dac(p))
