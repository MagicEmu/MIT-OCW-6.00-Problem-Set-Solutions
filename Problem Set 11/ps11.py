# Problem Set 11: Simulating robots
# Name: Yichen Dai
# Collaborators:
# Time:

import math
import random
import ps11_visualize
import numpy

# === Provided classes
from matplotlib import pylab


class Position(object):
    """
    A Position represents a location in a two-dimensional room.
    """
    def __init__(self, x, y):
        """
        Initializes a position with coordinates (x, y).

        x: a real number indicating the x-coordinate
        y: a real number indicating the y-coordinate
        """
        self.x = x
        self.y = y
    def getX(self):
        return self.x
    def getY(self):
        return self.y
    def getNewPosition(self, angle, speed):
        """
        Computes and returns the new Position after a single clock-tick has
        passed, with this object as the current position, and with the
        specified angle and speed.

        Does NOT test whether the returned position fits inside the room.

        angle: integer representing angle in degrees, 0 <= angle < 360
        speed: positive float representing speed

        Returns: a Position object representing the new position.
        """
        old_x, old_y = self.getX(), self.getY()
        # Compute the change in position
        delta_y = speed * math.cos(math.radians(angle))
        delta_x = speed * math.sin(math.radians(angle))
        # Add that to the existing position
        new_x = old_x + delta_x
        new_y = old_y + delta_y
        return Position(new_x, new_y)


# === Problems 1 and 2

class RectangularRoom(object):
    """
    A RectangularRoom represents a rectangular region containing clean or dirty
    tiles.

    A room has a width and a height and contains (width * height) tiles. At any
    particular time, each of these tiles is either clean or dirty.
    """
    def __init__(self, width, height):
        """
        Initializes a rectangular room with the specified width and height.
        Initially, no tiles in the room have been cleaned.

        width: an integer > 0
        height: an integer > 0
        """
        self.width = width
        self.height = height
        self.cleanTiles = {}
    def cleanTileAtPosition(self, pos):
        """
        Mark the tile under the position POS as cleaned.
        Assumes that POS represents a valid position inside this room.

        pos: a Position
        """
        intPosition = (int(pos.getX()), int(pos.getY()))
        self.cleanTiles[intPosition] = self.cleanTiles.get(intPosition, 0) + 1
    def isTileCleaned(self, m, n):
        """
        Return True if the tile (m, n) has been cleaned.

        Assumes that (m, n) represents a valid tile inside the room.

        m: an integer
        n: an integer
        returns: True if (m, n) is cleaned, False otherwise
        """
        questionedPosition = (int(m),int(n))
        return questionedPosition in self.cleanTiles
    def getNumTiles(self):
        """
        Return the total number of tiles in the room.

        returns: an integer
        """
        return self.height*self.width
    def getNumCleanedTiles(self):
        """
        Return the total number of clean tiles in the room.

        returns: an integer
        """
        return len(self.cleanTiles)
    def getRandomPosition(self):
        """
        Return a random position inside the room.

        returns: a Position object.
        """
        return Position(random.randrange(self.width), random.randrange(self.height))
    def isPositionInRoom(self, pos):
        """
        Return True if POS is inside the room.

        pos: a Position object.
        returns: True if POS is in the room, False otherwise.
        """
        return pos.getX() <= self.width and pos.getX() >= 0 and pos.getY() <= self.height and pos.getY() >= 0


class BaseRobot(object):
    """
    Represents a robot cleaning a particular room.

    At all times the robot has a particular position and direction in
    the room.  The robot also has a fixed speed.

    Subclasses of BaseRobot should provide movement strategies by
    implementing updatePositionAndClean(), which simulates a single
    time-step.
    """
    def __init__(self, room, speed):
        """
        Initializes a Robot with the given speed in the specified
        room. The robot initially has a random direction d and a
        random position p in the room.

        The direction d is an integer satisfying 0 <= d < 360; it
        specifies an angle in degrees.

        p is a Position object giving the robot's position.

        room:  a RectangularRoom object.
        speed: a float (speed > 0)
        """
        self.speed = speed
        self.position = Position(random.randrange(room.width), random.randrange(room.height))
        self.direction = random.randrange(360)
        self.room = room
    def getRobotPosition(self):
        """
        Return the position of the robot.

        returns: a Position object giving the robot's position.
        """
        return self.position
    def getRobotDirection(self):
        """
        Return the direction of the robot.

        returns: an integer d giving the direction of the robot as an angle in
        degrees, 0 <= d < 360.
        """
        return self.direction
    def setRobotPosition(self, position):
        """
        Set the position of the robot to POSITION.

        position: a Position object.
        """
        self.position = position
    def setRobotDirection(self, direction):
        """
        Set the direction of the robot to DIRECTION.

        direction: integer representing an angle in degrees
        """
        self.direction = direction


class Robot(BaseRobot):
    """
    A Robot is a BaseRobot with the standard movement strategy.

    At each time-step, a Robot attempts to move in its current
    direction; when it hits a wall, it chooses a new direction
    randomly.
    """
    def updatePositionAndClean(self):
        """
        Simulate the passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        inRoom = True
        while inRoom:
            old_x, old_y = self.position.getX(), self.position.getY()
            delta_y = self.speed * math.cos(math.radians(self.direction))
            delta_x = self.speed * math.sin(math.radians(self.direction))
            new_x = old_x + delta_x
            new_y = old_y + delta_y
            new_position = Position(new_x, new_y)
            if self.room.isPositionInRoom(new_position):
                self.position = new_position
                self.room.cleanTileAtPosition(self.position)
                inRoom = False
            else:
                self.direction = random.randrange(360)


# === Problem 3

def runSimulation(num_robots, speed, width, height, min_coverage, num_trials,
                  robot_type, visualize):
    """
    Runs NUM_TRIALS trials of the simulation and returns a list of
    lists, one per trial. The list for a trial has an element for each
    timestep of that trial, the value of which is the percentage of
    the room that is clean after that timestep. Each trial stops when
    MIN_COVERAGE of the room is clean.

    The simulation is run with NUM_ROBOTS robots of type ROBOT_TYPE,
    each with speed SPEED, in a room of dimensions WIDTH x HEIGHT.

    Visualization is turned on when boolean VISUALIZE is set to True.

    num_robots: an int (num_robots > 0)
    speed: a float (speed > 0)
    width: an int (width > 0)
    height: an int (height > 0)
    min_coverage: a float (0 <= min_coverage <= 1.0)
    num_trials: an int (num_trials > 0)
    robot_type: class of robot to be instantiated (e.g. Robot or
                RandomWalkRobot)
    visualize: a boolean (True to turn on visualization)
    """
    room = RectangularRoom(width, height)
    trials = []
    trialsCollection = []
    for i in range(num_trials):
        robots = []
        for i in range(num_robots):
            robots.append(robot_type(room, speed))
        if visualize:
            anim = ps11_visualize.RobotVisualization(num_robots, width, height)
        percentClean = 0.0000000
        progressList = []
        while percentClean < min_coverage:
            for robot in robots:
                robot.updatePositionAndClean()
            percentClean = float(room.getNumCleanedTiles())/float(room.getNumTiles())
            progressList.append(percentClean)
            if visualize:
                anim.update(room, robots)
        if visualize:
            anim.done()
        trialsCollection.append(progressList)
    ##average = calcAvgLengthList(trialsCollection)
    ##print(str(num_robots), 'robots takes around', str(average), 'clock ticks to clean', str(min_coverage*100)+'% of a', str(width)+'x'+str(height), 'room')
    return trialsCollection

# === Provided function
def computeMeans(list_of_lists):
    """
    Returns a list as long as the longest list in LIST_OF_LISTS, where
    the value at index i is the average of the values at index i in
    all of LIST_OF_LISTS' lists.

    Lists shorter than the longest list are padded with their final
    value to be the same length.
    """
    # Find length of longest list
    longest = 0
    for lst in list_of_lists:
        if len(lst) > longest:
           longest = len(lst)
    # Get totals
    tots = [0]*(longest)
    for lst in list_of_lists:
        for i in range(longest):
            if i < len(lst):
                tots[i] += lst[i]
            else:
                tots[i] += lst[-1]
    # Convert tots to an array to make averaging across each index easier
    tots = pylab.array(tots)
    # Compute means
    means = tots/float(len(list_of_lists))
    return means

def calcAvgLengthList(list_of_lists):
    """
    Takes a list of lists and then calculates the average length of the lists
    """
    sumOfLengths = 0
    for eachList in list_of_lists:
        sumOfLengths += len(eachList)
    averageLength = sumOfLengths / len(list_of_lists)
    return averageLength

# === Problem 4
def showPlot1():
    """
    Produces a plot showing dependence of cleaning time on room size.
    """
    dimensions = [5, 10 ,15 ,20, 25]
    means = []
    pylab.title('Time to clean 75%')
    pylab.xlabel('Room Area')
    pylab.ylabel('Time')
    for dimension in dimensions:
        trialsCollection = runSimulation(1, 1.0, dimension, dimension, 0.75, 25, Robot, False)
        means.append(calcAvgLengthList(trialsCollection))
    data = numpy.array([[25, means[0]],
                       [100, means[1]],
                       [225, means[2]],
                       [400, means[3]],
                       [625, means[4]]])
    x, y = data.T
    pylab.scatter(x, y)
    pylab.show()

def showPlot2():
    """
    Produces a plot showing dependence of cleaning time on number of robots.
    """
    num_robots = range(1, 11)
    means = []
    pylab.title('Time to clean 75%')
    pylab.xlabel('Number of Robots')
    pylab.ylabel('Time')
    for robots in num_robots:
        trialsCollection = runSimulation(robots, 1.0, 25, 25, 0.75, 25, Robot, False)
        means.append(calcAvgLengthList(trialsCollection))
    data = numpy.array([[1, means[0]],
                        [2, means[1]],
                        [3, means[2]],
                        [4, means[3]],
                        [5, means[4]],
                        [6, means[5]],
                        [7, means[6]],
                        [8, means[7]],
                        [9, means[8]],
                        [10, means[9]]])
    x,y = data.T
    pylab.scatter(x, y)
    pylab.show()

def showPlot3():
    """
    Produces a plot showing dependence of cleaning time on room shape.
    """
    dimensions = [[20,20],[25,16],[40,10],[50,8],[80,5],[100,4]]
    means = []
    pylab.title('Time to clean 75%')
    pylab.xlabel('Width/Height Ratio')
    pylab.ylabel('Time')
    for dimension in dimensions:
        trialsCollection = runSimulation(2, 1.0, dimension[0], dimension[1], 0.75, 25, Robot, False)
        means.append(calcAvgLengthList(trialsCollection))
    data = numpy.array([[dimensions[0][0]/dimensions[0][1], means[0]],
                        [dimensions[1][0]/dimensions[1][1], means[1]],
                        [dimensions[2][0]/dimensions[2][1], means[2]],
                        [dimensions[3][0]/dimensions[3][1], means[3]],
                        [dimensions[4][0]/dimensions[4][1], means[4]],
                        [dimensions[5][0]/dimensions[5][1], means[5]]])
    x, y = data.T
    pylab.scatter(x, y)
    pylab.show()

def showPlot4():
    """
    Produces a plot showing cleaning time vs. percentage cleaned, for
    each of 1-5 robots.
    """
    min_coverages = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
    yMax = 0
    for robots in range(1, 6):
        means = []
        for min_coverage in min_coverages:
            trialsCollection = runSimulation(robots, 1.0, 25, 25, min_coverage, 25, Robot, False)
            means.append(calcAvgLengthList(trialsCollection))
        pylab.plot(means, label=str(robots)+' robots')
        yMax = max(yMax, means[-1])
    pylab.title('Time to Clean X Percent with Z Robots')
    pylab.xlabel('Percent Cleaned')
    pylab.ylabel('Time')
    pylab.legend()
    xAxis = list(range(len(min_coverages)))
    pylab.xticks(xAxis, min_coverages)
    pylab.show()

# === Problem 5

class RandomWalkRobot(BaseRobot):
    """
    A RandomWalkRobot is a robot with the "random walk" movement
    strategy: it chooses a new direction at random after each
    time-step.
    """
    def updatePositionAndClean(self):
        """
        Simulate the passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        inRoom = True
        while inRoom:
            old_x, old_y = self.position.getX(), self.position.getY()
            delta_y = self.speed * math.cos(math.radians(self.direction))
            delta_x = self.speed * math.sin(math.radians(self.direction))
            new_x = old_x + delta_x
            new_y = old_y + delta_y
            new_position = Position(new_x, new_y)
            if self.room.isPositionInRoom(new_position):
                self.position = new_position
                self.room.cleanTileAtPosition(self.position)
                self.direction = random.randrange(360)
                inRoom = False
            else:
                self.direction = random.randrange(360)

# === Problem 6

def showPlot5():
    """
    Produces a plot comparing the two robot strategies.
    """
    types = [Robot, RandomWalkRobot]
    for type in types:
        means = []
        for num_robots in range(1, 11):
            trialsCollection = runSimulation(num_robots, 1.0, 25, 25, 0.75, 25, type, False)
            means.append(calcAvgLengthList(trialsCollection))
        pylab.plot(means, label=str(type))
    pylab.title('Comparison of Performance of Two Different Robot Types')
    pylab.ylabel('Time')
    pylab.xlabel('Number of Robots')
    pylab.xlim(1, 9)
    pylab.legend()
    pylab.show()