import math

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def show(self):
        print(self.x , self.y)

    def move(self,x ,y):
        self.x = x
        self.y = y
    def dist(self, other_point):
        return math.sqrt((self.x - other_point.x) ** 2 + (self.y - other_point.y) ** 2)
    
point1 = Point (5, 2)
point2 = Point (10, 5)

print(point1.dist(point2))
