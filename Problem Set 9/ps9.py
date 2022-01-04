# 6.00 Problem Set 9
#
# Name: Yichen Dai
# Collaborators:
# Time:

from string import *

class Shape(object):
    def area(self):
        raise AttributeException("Subclasses should override this method.")

class Square(Shape):
    def __init__(self, h):
        """
        h: length of side of the square
        """
        self.side = float(h)
    def area(self):
        """
        Returns area of the square
        """
        return self.side**2
    def __str__(self):
        return 'Square with side ' + str(self.side)
    def __eq__(self, other):
        """
        Two squares are equal if they have the same dimension.
        other: object to check for equality
        """
        return type(other) == Square and self.side == other.side

class Circle(Shape):
    def __init__(self, radius):
        """
        radius: radius of the circle
        """
        self.radius = float(radius)
    def area(self):
        """
        Returns approximate area of the circle
        """
        return 3.14159*(self.radius**2)
    def __str__(self):
        return 'Circle with radius ' + str(self.radius)
    def __eq__(self, other):
        """
        Two circles are equal if they have the same radius.
        other: object to check for equality
        """
        return type(other) == Circle and self.radius == other.radius

#
# Problem 1: Create the Triangle class
#
## TO DO: Implement the `Triangle` class, which also extends `Shape`.

class Triangle(Shape):
    def __init__(self, base, height):
        self.base = base
        self.height = height
    def area(self):
        return self.base*self.height/2
    def __str__(self):
        return 'Triangle with base ' + str(self. base) + ' and height ' + str(self.height)
    def __eq__(self, other):
        return type(other) == Triangle and self.base == other.base and self.height == other.height

#
# Problem 2: Create the ShapeSet class
#
## TO DO: Fill in the following code skeleton according to the
##    specifications.

class ShapeSet:
    def __init__(self):
        """
        Initialize any needed variables
        """
        self.shapes = []
        self.place = None
    def addShape(self, sh):
        """
        Add shape sh to the set; no two shapes in the set may be
        identical
        sh: shape to be added
        """
        if type(sh) != Square and type(sh) != Circle and type(sh) != Triangle:
            raise TypeError('Not a shape')
        elif sh in self.shapes:
            raise ValueError('shape already exists')
        self.shapes.append(sh)
    def __iter__(self):
        """
        Return an iterator that allows you to iterate over the set of
        shapes, one shape at a time
        """
        for shape in self.shapes:
            yield shape
        return self
    def __str__(self):
        """
        Return the string representation for a set, which consists of
        the string representation of each shape, categorized by type
        (circles, then squares, then triangles)
        """
        setRep = ""
        for shape in self.shapes:
            setRep += str(shape) + "\n"
        return setRep
        
#
# Problem 3: Find the largest shapes in a ShapeSet
#
def findLargest(shapes):
    """
    Returns a tuple containing the elements of ShapeSet with the
       largest area.
    shapes: ShapeSet
    """
    largest = (0,)
    for shape in shapes:
        try:
            if shape.area() > largest[-1].area():
                largest = (shape,)
            elif shape.area() == largest[-1].area():
                largest += (shape,)
        except AttributeError:
            largest = (shape,)
    return largest

#
# Problem 4: Read shapes from a file into a ShapeSet
#
def readShapesFromFile(filename):
    """
    Retrieves shape information from the given file.
    Creates and returns a ShapeSet with the shapes found.
    filename: string
    """
    shapes = ShapeSet()
    file = open(filename, "r").readlines()
    for line in file:
        line = line.strip('\n')
        obj_para = line.split(",")
        if obj_para[0] == "circle":
            shape = Circle(obj_para[1])
        elif obj_para[0] == "square":
            shape = Square(obj_para[1])
        else:
            shape = Triangle(obj_para[1], obj_para[2])
        shapes.addShape(shape)
    return shapes

filename = 'shapes.txt'
shapes = readShapesFromFile(filename)
print(shapes)