import math


def ballPath(startx, starty, power, ang, time):
    angle = ang
    velx = math.cos(angle) * power
    vely = math.sin(angle) * power

    distX = velx * time
    distY = (vely * time) + ((-9.8 * (time ** 2)) / 2)

    newx = round(distX + startx)
    newy = round(starty - distY)

    return (newx, newy)
