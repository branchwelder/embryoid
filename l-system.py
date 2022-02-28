import pygame
import math

# other = variables
# F,A = move n forward
# G = move n forward without drawing a line
# B = move n backwards
# - = turn left by angle
# + = turn right by angle
# [ = push position and angle
# ] = pop position and angle
# a,b,c,d = color 1,2,3,4
# 1-4 line size (std = 1)
#

rules = {}

rules["F"] = "F-F++F-F"
axiom = "F++F++F"
angle = 60

# rules['A'] = '+F-A-F+' # Sierpinsky
# rules['F'] = '-A+F+A-'
# axiom = 'A'
# angle = 60

# rules['F'] = 'F+F-F-F+F' # Koch curve 1
# axiom = 'F'
# angle = 60

# rules['F'] = 'F+F--F+F' # Koch curve 2
# axiom = 'F'
# angle = 60

# rules["X"] = "X+YF+"  # Dragon curve
# rules["Y"] = "-FX-Y"
# axiom = "FX"
# angle = 90

# rules['X'] = 'F-[[X]+X]+F[+FX]-X'  # Wheat
# rules['F'] = 'FF'
# axiom = 'X'
# angle = 25

# rules['F'] = 'a2FF-[c1-F+F+F]+[c1+F-F-F]'  # Tree - colored
# axiom = 'F'
# angle = 23

# rules['X'] = 'F-[[X]-1X]+2F-[+3FX]+1X'  # Wheat
# rules['F'] = 'X'
# axiom = 'X'
# angle = 25

iterations = 7  # number of iterations
step = 15  # step size / line length

color1 = (105, 46, 26)  # brown 1
color2 = (201, 146, 127)  # brown 2
color3 = (101, 250, 52)  # green
color4 = (255, 255, 255)  # white

angleoffset = 90

size = width, height = 10000, 10000  # display with/height
pygame.init()  # init display
screen = pygame.Surface(size)  # open screen

# startpos = 100, height - 225
# startpos = 50, height / 2 - 50
startpos = width / 2, height / 2
# startpos = 100, height / 2
# startpos = 10,10


def applyRule(input):
    output = ""
    for (
        rule,
        result,
    ) in rules.items():  # applying the rule by checking the current char against it
        if input == rule:
            output = result  # Rule 1
            break
        else:
            output = input  # else ( no rule set ) output = the current char -> no rule was applied
    return output


def processString(oldStr):
    newstr = ""
    for character in oldStr:
        newstr = newstr + applyRule(character)  # build the new string
    return newstr


def createSystem(numIters, axiom):
    startString = axiom
    endString = ""
    for i in range(numIters):  # iterate with appling the rules
        print("Iteration: {0}".format(i))
        endString = processString(startString)
        startString = endString
    return endString


def polar_to_cart(theta, r, offx, offy):
    x = r * math.cos(math.radians(theta))
    y = r * math.sin(math.radians(theta))
    return tuple([x + y for x, y in zip((int(x), int(y)), (offx, offy))])


def cart_to_polar(x, y):
    return (math.degrees(math.atan(y / x)), math.sqrt(math.pow(x, 2) + math.pow(y, 2)))


def drawTree(input, oldpos):
    a = 0  # angle
    i = 0  # counter for processcalculation
    processOld = 0  # old process
    newpos = oldpos
    num = []  # stack for the brackets
    color = (255, 255, 255)
    linesize = 1
    xmax = 0
    xmin = 0
    ymax = 0
    ymin = 0
    for (
        character
    ) in input:  # process for drawing the l-system by writing the string to the screen

        i += 1  # print process in percent
        process = i * 100 / len(input)
        if not process == processOld:
            print(process, "%")
            processOld = process

        if character == "A":  # magic happens here
            newpos = polar_to_cart(a + angleoffset, step, oldpos[0], oldpos[1])
            pygame.draw.line(screen, color, oldpos, newpos, linesize)
            oldpos = newpos
        elif character == "F":
            newpos = polar_to_cart(a + angleoffset, step, oldpos[0], oldpos[1])
            pygame.draw.line(screen, color, oldpos, newpos, linesize)
            oldpos = newpos
        elif character == "B":
            newpos = polar_to_cart(-a + angleoffset, -step, oldpos[0], oldpos[1])
            pygame.draw.line(screen, color, oldpos, newpos, linesize)
            oldpos = newpos
        elif character == "G":
            newpos = polar_to_cart(a + angleoffset, step, oldpos[0], oldpos[1])
            oldpos = newpos
        elif character == "a":
            color = color1
        elif character == "b":
            color = color2
        elif character == "c":
            color = color3
        elif character == "d":
            color = color4
        elif character == "1":
            linesize = 1
        elif character == "2":
            linesize = 2
        elif character == "3":
            linesize = 3
        elif character == "4":
            linesize = 4
        elif character == "+":
            a += angle
        elif character == "-":
            a -= angle
        elif character == "[":
            num.append((oldpos, a))
        elif character == "]":
            oldpos, a = num.pop()
        if xmax < oldpos[0] - width / 2:
            xmax = oldpos[0] - width / 2
        if xmin > oldpos[0] - width / 2:
            xmin = oldpos[0] - width / 2
        if ymax < oldpos[1] - height / 2:
            ymax = oldpos[1] - height / 2
        if ymin > oldpos[1] - height / 2:
            ymin = oldpos[1] - height / 2
    crop = pygame.Surface((abs(xmax - xmin) + 100, abs(ymax - ymin) + 100))
    crop.blit(
        screen,
        (50, 50),
        (xmin + width / 2, ymin + height / 2, xmax + width / 2, ymax + height / 2),
    )
    pygame.image.save(crop, "screenshot.png")


if __name__ == "__main__":
    # drawTree(createSystem(iterations, axiom), startpos)
    tree = createSystem(iterations, axiom)
    drawTree(tree, startpos)
    # pygame.display.flip()
    # pygame.image.save(screen, "screenshot.png")
    # print "Finished"
    while 1:
        pass
        exit()  # uncommand
