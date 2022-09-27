import math
import numpy
from time import sleep
from datetime import datetime
import random


class cube:
    DEBUG = False
    gridLines = False
    fixedHeight = 0
    starttime = datetime.now()
    debugLetters = "abcdefgh"
    debugLettersLines = "CTS"
    thetaInt = -180
    theta = math.pi / thetaInt
    thetaX = theta
    thetaY = theta
    thetaZ = theta
    gridHeight = 90
    gridWidth = 120
    xAxis = int(gridWidth/2)
    eye = [0, 0, 200]
    windowZ = 50
    center = [0, 0, 0]
    points = [[-1, -1, -1], [1, -1, -1], [-1, 1, -1], [1, 1, -1], [-1, -1, 1], [1, -1, 1], [-1, 1, 1], [1, 1, 1]]
    connectedPoints = [[0, 1], [0, 2], [1, 3], [2, 3], [0, 4], [1, 5], [2, 6], [3, 7], [4, 5], [4, 6], [5, 7], [6, 7]]
    # random.shuffle(points)
    transX = 0
    transY = 0
    transZ = 0
    scaleX = 40
    scaleY = 40
    scaleZ = 40

    XYratio = 0.5
    drawingHeight = 0
    backgroundChar = ' '
    numPoints = len(points)
    connectChar1 = '@'
    connectChar2 = '0'
    connectChar3 = 'o'
    pushUp = 5
    pushRight = 10
    zoom = 2.5
    obscured = 0
    thetaCounter = 0
    for i in range(0, numPoints):
        points[i] = [(points[i][0] + transX) * scaleX, (points[i][1] + transY) * scaleY,
                     (points[i][2] + transZ) * scaleZ]
    targetLineLength = points[1][0] - points[0][0]
    print("TLL" , targetLineLength)
    sleep(1)
    CA0 = 0
    CG0 = 0
    CD0 = 0
    distancePointFromCenter = 0
    TwoDDistanceFromCenter = 0
    projection = []
    canvas = []
    linestr = ""
    alternate = 0
    rotateXposNeg = 1

    def __init__(self):
        self.distancePointFromCenter = self.distance(self.center, self.points[0])
        self.CA0 = self.distance(self.points[0], self.points[2])
        self.CG0 = self.distance(self.points[2], self.points[6])
        self.CD0 = self.distance(self.points[2], self.points[3])
        self.TwoDDistanceFromCenter = self.distanceTwo([self.points[0][0], self.points[0][1]], [0, 0])
        #print(self.distancePointFromCenter)

    def run(self, num, sleepNum):
        count = num * 1000
        if not sleepNum:
            sleepNum = 0
        for i in range(0, count):
            displayData = self.display()
            print(self.linestr)
            if self.DEBUG:
                print("draw:", displayData[2])
                for item in displayData[1]:
                    print(item)
                print(displayData[3])
            sleep(sleepNum)

    def display(self):
        self.thetaCounter += self.thetaY
        projectData = self.project()
        vertical = self.paint()
        rotYstring = self.rotateY()
        self.rotateX()
        self.rotateZ()
        self.fixDistanceFromCenter()
        fixPointsString = self.fixSideLengths()

#
        return projectData, fixPointsString, vertical, rotYstring

    def project(self):
        self.projection = []
        returnList = []
        for point in self.points:
            projx = (((self.eye[0] - point[0]) / (self.eye[2] - point[2])) * self.windowZ + self.eye[0]) * self.zoom + self.pushRight
            projy = (((self.eye[1] - point[1]) / (self.eye[2] - point[2])) * self.windowZ + self.eye[1]) * self.zoom
            projectedPoint = [int(projx), int(projy * self.XYratio), point[2]]
            # print("point:", point, "\nProj:",projectedPoint)
            self.projection.append(projectedPoint)
        for conn in self.connectedPoints:
            p1 = self.points[conn[0]]
            p2 = self.points[conn[1]]
            diff = math.fabs(p1[1] - p2[1])
            returnList.append(self.debugLetters[conn[0]] + self.debugLetters[conn[1]] + " " + str(int(diff)))
        return returnList
    def vectorSpread(self, p1, p2):
        cent = [(p1[0] + p2[0])/2, (p1[1] + p2[1])/2, (p1[2] + p2[2])/2]
        distance = self.distance(p1, cent)
        vector1 = [p1[0] - cent[0], p1[1] - cent[1], p1[2] - cent[2]]
        vector2 = [p2[0] - cent[0], p2[1] - cent[1], p2[2] - cent[2]]
        vecCoef1 = [(i/distance)*(self.targetLineLength/2-distance) for i in vector1]
        vecCoef2 = [(i/distance)*(self.targetLineLength/2-distance) for i in vector2]
        q1 = [p1[0] + vecCoef1[0], p1[1] + vecCoef1[1], p1[2] + vecCoef1[2]]
        q2 = [p2[0] + vecCoef2[0], p2[1] + vecCoef2[1], p2[2] + vecCoef2[2]]
        # print('distance', distance)
        # print('center', cent)
        # print('v1:', vecCoef1, 'v2', vecCoef2)
        # print(p1, '->', q1)
        # print(p2, '->', q2, '\n')

        return q1, q2


    def OldvectorSpread(self, p1, p2):
        vectorDifference = [p2[0]-p1[0], p2[1]-p1[1], p2[2] - p1[2]]
        distance = self.distance(p1, p2)
        vecCoef = [(i / distance)*((self.targetLineLength - distance)/2) for i in vectorDifference]
        q1 = [p1[0] + vecCoef[0], p1[1] + vecCoef[1], p1[2] + vecCoef[2]]
        q2 = [p2[0] + vecCoef[0], p2[1] + vecCoef[1], p2[2] + vecCoef[2]]
        #print(p1, '->', q1)
        #sleep(1)
        return q1, q2

    def distance(self, p1, p2):
        return math.sqrt(pow(p1[0] - p2[0], 2) + pow(p1[1] - p2[1], 2) + pow(p1[2] - p2[2], 2))

    def distanceTwo(self, p1, p2):
        return math.sqrt(pow(p1[0] - p2[0], 2) + pow(p1[1] - p2[1], 2))

    def rotateZ(self):
        theta = self.thetaZ * 0.3 * (numpy.sin(((datetime.now() - self.starttime).total_seconds())) + 1)
        sinTheta = numpy.sin(theta)
        cosTheta = numpy.cos(theta)
        for i in range(0, len(self.points)):
            point = self.points[i]
            newX = point[0]
            newY = point[1]
            newZ = point[2]
            newX = newX * cosTheta - newY * sinTheta
            newY = newY * cosTheta + newX * sinTheta
            self.points[i] = [newX, newY, newZ]

    def rotateX(self):
        theta = self.thetaX * (numpy.cos(((datetime.now() - self.starttime).total_seconds()+ 13/12)))*0.3
        sinTheta = numpy.sin(theta)
        cosTheta = numpy.cos(theta)
        for i in range(0, len(self.points)):
            point = self.points[i]
            newX = point[0]
            newY = point[1]
            newZ = point[2]
            newY = newY * cosTheta - newZ * sinTheta
            newZ = newZ * cosTheta + newY * sinTheta
            self.points[i] = [newX, newY, newZ]

    def rotateY(self):
        theta = self.thetaY * (numpy.sin(((datetime.now() - self.starttime).total_seconds()/5)) + 1)*0.5
        sinTheta = numpy.sin(theta)
        cosTheta = numpy.cos(theta)
        avgX = 0
        avgY = 0
        avgZ = 0
        avgDistance = 0
        for i in range(0, len(self.points)):
            point = self.points[i]
            avgX += point[0]
            avgY += point[1]
            avgZ += point[2]
            newX = point[0]
            newY = point[1]
            newZ = point[2]
            newX = newX * cosTheta - newZ * sinTheta
            newZ = newZ * cosTheta + newX * sinTheta
            newpoint = [newX, newY, newZ]
            avgDistance += self.distance(self.center, newpoint)
            self.points[i] = newpoint
        avgX = int(avgX / len(self.points))
        avgY = int(avgY / len(self.points))
        avgZ = int(avgZ / len(self.points))
        avgDistance = avgDistance / len(self.points)
        if (datetime.now() - self.starttime).total_seconds() != 0:
            distanceLossPerSecond = (self.distancePointFromCenter - avgDistance) / (
                    datetime.now() - self.starttime).total_seconds()
        return str(avgX) + " " + str(avgY) + " " + str(avgZ) + 'Avg Distance from Center ' + str(
            avgDistance) + '/' + str(self.distancePointFromCenter) + ' Distance Change/min: ' + str(
            distanceLossPerSecond * 60)
        # *1.00013736767

    def fixSideLengths(self):
        lineLengths = {}
        squarePoints = []
        squareLength = 0
        circlePoints = []
        circleLength = 0
        trianglePoints = []
        triangleLength = 0
        for connection in self.connectedPoints:
            if connection[1] - connection[0] == 1:
                if "circle" not in lineLengths:
                    lineLengths["circle"] = []
                lineLengths["circle"].append(self.distance(self.points[connection[0]], self.points[connection[1]]))
                circlePoints.append(connection)
            elif connection[1] - connection[0] == 2:
                if "square" not in lineLengths:
                    lineLengths["square"] = []
                lineLengths["square"].append(self.distance(self.points[connection[0]], self.points[connection[1]]))
                squarePoints.append(connection)
            elif connection[1] - connection[0] == 4:
                if "triangle" not in lineLengths:
                    lineLengths["triangle"] = []
                lineLengths["triangle"].append(self.distance(self.points[connection[0]], self.points[connection[1]]))
                trianglePoints.append(connection)
            else:
                quit()
        for item in lineLengths:
            total = 0
            for length in lineLengths[item]:
                total += length
            average = total/4
            lineLengths[item] = average
        for connection in trianglePoints + circlePoints + squarePoints:
            p1, p2 = self.vectorSpread(self.points[connection[0]], self.points[connection[1]])
            self.points[connection[0]] = p1
            self.points[connection[1]] = p2
        # pwr = 0.5
        # for p in trianglePoints:
        #     for s in p:
        #         point0 = self.points[s]
        #         coeff = pow(self.targetLineLength / lineLengths["triangle"], pwr)
        #         x = point0[0] * coeff
        #         y = point0[1] * coeff
        #         z = point0[2] * coeff
                #elf.points[s] = [x, y, z]
        # for p in squarePoints:
        #     for s in p:
        #         point0 = self.points[s]
        #         coeff = pow(self.targetLineLength / lineLengths["square"], pwr)
        #         x = point0[0] * coeff
        #         y = point0[1] * coeff
        #         z = point0[2] * coeff
        #         print(coeff)
        #         self.points[s] = [x, y, z]
        #         if point0 == self.points[s]:
        #             print("x = " + str(point0[0] * coeff) + "?" )
        #             sleep(5)
        # for p in circlePoints:
        #     for s in p:
        #         point0 = self.points[s]
        #         coeff = pow(self.targetLineLength / lineLengths["circle"], pwr)
        #         x = point0[0] * coeff
        #         y = point0[1] * coeff
        #         z = point0[2] * coeff
        #         self.points[s] = [x, y, z]
        #         print(coeff)
        #         if point0 == self.points[s]:
        #             print("x = " + str(point0[0] * coeff) + "?" )
        #             sleep(5)
        return ["square: " + str(int(lineLengths["square"])) + " circle:" + str(int(lineLengths["circle"])) + " triangle:" + str(int(lineLengths["triangle"])),]

    def fixDistanceFromCenter(self):
        returnList = []
        for i in range(0, len(self.points)):
            point = self.points[i]
            h = self.distance(point, self.center)
            xSign = 1
            ySign = 1
            zSign = 1
            if point[0] < 0:
                xSign = -1
            if point[1] < 0:
                ySign = -1
            if point[2] < 0:
                zSign = -1
            x = math.fabs(point[0])
            y = math.fabs(point[1])
            z = math.fabs(point[2])
            xTheta = numpy.arcsin(x / h)
            yTheta = numpy.arcsin(y / h)
            zTheta = numpy.arcsin(z / h)
            x = math.fabs(self.distancePointFromCenter * numpy.sin(xTheta)) * xSign
            y = math.fabs(self.distancePointFromCenter * numpy.sin(yTheta)) * ySign
            z = math.fabs(self.distancePointFromCenter * numpy.sin(zTheta)) * zSign
            returnList.append(str(point) + "->" + str([x, y, z]))
            self.points[i] = [x, y, z]

        return returnList


    def paint(self):
        self.canvas = []
        wasVertical = False
        for i in range(0, self.gridHeight):
            self.canvas.append(self.backgroundChar * int(self.gridWidth / len(self.backgroundChar)))
        for pair in self.connectedPoints:
            if self.projection[pair[0]][0] > self.projection[pair[1]][0]:
                p1 = self.projection[pair[1]]
                p2 = self.projection[pair[0]]
            else:
                p1 = self.projection[pair[0]]
                p2 = self.projection[pair[1]]

            xDiff = p1[0] - p2[0]
            yDiff = p1[1] - p2[1]
            vertical = False
            if math.fabs(xDiff) == 0:
                xDiff = 0.000001
                vertical = True
                wasVertical = True
            slope = yDiff / xDiff
            lastploty = None
            xShift = self.xAxis
            yAxis = int(self.gridHeight / 2)
            if vertical:
                x = p1[0]
                # print(self.debugLetters[pair[0]], 'to', self.debugLetters[pair[1]], 'vertical', p2[1] - p1[1], l)
                if p2[1] - p1[1] < 0:
                    l = -1
                else:
                    l = 1
                # print(self.debugLetters[pair[0]], 'to', self.debugLetters[pair[1]], 'vertical', p2[1] - p1[1], l)
                # print(range(p1[1], p2[1], l))
                for y in range(p1[1] - 1, p2[1] + 1, l):
                    # print(self.debugLetters[pair[0]], 'to', self.debugLetters[pair[1]], x, y)
                    if self.DEBUG:
                        if pair[1] - pair[0] == 4:
                            connectChar = 'T'
                        elif pair[1] - pair[0] == 2:
                            connectChar = 'S'
                        else:
                            connectChar = "C"
                    else:
                        if p1[2] > 0 and p2[2] > 0:
                            connectChar = self.connectChar1
                        elif p1[2] > 0 or p2[2] > 0:
                            connectChar = self.connectChar2
                        else:
                            connectChar = self.connectChar3
                    currentChar = self.canvas[yAxis - y][x + xShift]
                    if currentChar == self.backgroundChar or (connectChar == self.connectChar1 and (
                            currentChar == self.connectChar3 or currentChar == self.connectChar2) or (
                                                                      connectChar == self.connectChar2 and currentChar == self.connectChar3)):
                        self.canvas[yAxis - y] = self.canvas[yAxis - y][
                                                 :x + xShift] + connectChar * 2 + \
                                                 self.canvas[yAxis - y][x + xShift + 1:]
            else:
                for x in range(p1[0], p2[0]):
                    if self.DEBUG:
                        if pair[1] - pair[0] == 4:
                            connectChar = 'T'
                        elif pair[1] - pair[0] == 2:
                            connectChar = 'S'
                        else:
                            connectChar = "C"
                    else:
                        if p1[2] > 0 and p2[2] > 0:
                            connectChar = self.connectChar1
                        elif p1[2] or p2[2] > 0:
                            connectChar = self.connectChar2
                        else:
                            connectChar = self.connectChar3
                    y = int((x - p1[0]) * slope)
                    if not lastploty:
                        lastploty = y
                    for i in range(lastploty - 1, y + 1):
                        #if lastploty != i or lastploty == y:
                        currentChar = self.canvas[yAxis - i - p1[1]][x + xShift]
                        if currentChar == self.backgroundChar or (connectChar == self.connectChar1 and (
                                currentChar == self.connectChar3 or currentChar == self.connectChar2) or (
                                                                          connectChar == self.connectChar2 and currentChar == self.connectChar3)):
                            self.canvas[yAxis - i - p1[1]] = self.canvas[yAxis - i - p1[1]][
                                                             :x + xShift] + connectChar + \
                                                             self.canvas[yAxis - i - p1[1]][x + xShift + 1:]
                        lastploty = i


            # else:
            #     for x in range(0, p2[0] - p1[0]):
            #         if self.DEBUG:
            #             if pair[1] - pair[0] == 4:
            #                 connectChar = 'T'
            #             elif pair[1] - pair[0] == 2:
            #                 connectChar = 'S'
            #             else:
            #                 connectChar = "C"
            #         else:
            #             if p1[2] > 0 and p2[2] > 0:
            #                 connectChar = self.connectChar1
            #             elif p1[2] or p2[2] > 0:
            #                 connectChar = self.connectChar2
            #             else:
            #                 connectChar = self.connectChar3
            #         y = int(x * slope)
            #         if not lastploty:
            #             lastploty = y
            #         for i in range(lastploty - 1, y + 1):
            #             if lastploty != i or lastploty == y:
            #                 currentChar = self.canvas[yAxis - i - p1[1]][x + xShift + p1[0]]
            #                 if currentChar == self.backgroundChar or (connectChar == self.connectChar1 and (
            #                         currentChar == self.connectChar3 or currentChar == self.connectChar2) or (
            #                                                                   connectChar == self.connectChar2 and currentChar == self.connectChar3)):
            #                     self.canvas[yAxis - i - p1[1]] = self.canvas[yAxis - i - p1[1]][
            #                                                      :x + xShift + p1[0]] + connectChar + \
            #                                                      self.canvas[yAxis - i - p1[1]][x + xShift + p1[0] + 1:]
            #             lastploty = i

        for point in self.projection:
             if point[2] > 0:
                 connectChar = '0'
             else:
                 connectChar = 'o'
             self.canvas[yAxis - point[1]] = self.canvas[yAxis - point[1]][:point[0] + xShift] + self.debugLetters[self.projection.index(point)].upper() + \
                                             self.canvas[yAxis - point[1]][point[0] + xShift + 1:]
        if self.gridLines:
            self.canvas[yAxis] = self.canvas[yAxis].replace(self.backgroundChar, '-')
        i = 0
        for line in self.canvas:
            fixedLine = line[:self.gridWidth]
            if self.gridLines and fixedLine[xShift] == self.backgroundChar:
                fixedLine = fixedLine[:xShift] + '|' + fixedLine[xShift + 1:]
            self.canvas[i] = fixedLine
            i += 1
        self.linestr = ""
        firstText = False
        countFromXaxis = 0
        counting = False
        heightCounter = 0
        pushUpLine = ("\n" + self.backgroundChar * self.gridWidth)
        pushUpLine = pushUpLine[:xShift + 1] + '|'*self.gridLines + ' '*(not self.gridLines) + pushUpLine[xShift + 2:]
        inCube = False
        emptyCount = 0
        maxEmptyCount = 0
        ticker = 0
        for line in self.canvas:
            if ticker == yAxis:
                counting = True
            ticker += 1
            if emptyCount > 10:
                inCube = False
            if inCube or (self.connectChar3 in line or self.connectChar2 in line or self.connectChar1 in line or 'T' in line or 'C' in line or 'S' in line):
                if not (self.connectChar3 in line or self.connectChar2 in line or self.connectChar1 in line or 'T' in line or 'C' in line or 'S' in line):
                    emptyCount += 1
                else:
                    emptyCount = 0
                if not inCube:
                    inCube = True
                if emptyCount > 10:
                    inCube = False
                if not firstText:
                    firstText = True
                if len(line) > self.gridWidth:
                    line = line[:self.gridWidth]
                self.linestr += "\n" + line
                if counting:
                    countFromXaxis += 1
            elif not firstText:
                if len(line) > self.gridWidth:
                    line = line[:self.gridWidth]
                self.linestr += "\n" + line
                if counting:
                    countFromXaxis += 1
        if countFromXaxis > self.fixedHeight:
            self.fixedHeight = countFromXaxis
        if countFromXaxis < self.fixedHeight:
            self.linestr += pushUpLine * (self.fixedHeight - countFromXaxis)

        return f"countFromXaxis:{countFromXaxis}, emptyCount:{emptyCount}, fixedHeight:{self.fixedHeight}"


q = cube()
# q.fixSideLengths()
# q.project()
# q.paint()
# print(q.linestr)
q.run(1000, False)
# q.project()
# q.paint()
# print(q.linestr)

print(q.points)
