import math
import logging
import sys

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler(sys.stdout))

def parseInput(lines):
    board = {}
    x = y = 0
    for line in lines:
        x = 0
        for value in line:
            board[(x, y)] = True if value == '#' else False
            x += 1
        y += 1
    return board, (x, y)

def compute_hcf(x, y):
   while(y):
       x, y = y, x % y
   return x

def getAllDirections(board, location, dimensions):
    maxx, maxy = dimensions
    x, y = location
    directions = []
    for i in range(0, maxx):
        for j in range(0, maxy):
            if (i, j) != (x, y):
                checkDirection(board, location, (i, j), dimensions, directions, False)
    logger.debug('All directions: {}'.format(directions))
    angles = getAngles(directions, location)
    shootTheLaser(board, location, dimensions, angles)

def shootTheLasterAtDirection(board, location, dimensions, direction, counter):
    x, y = location
    dx, dy = direction
    maxx, maxy = dimensions
    a = x + dx
    b = y + dy
    while a >= 0 and a < maxx and b >= 0 and b < maxy:
        if board[(a, b)] == True:
            logger.debug('Shoot asteroid #{} at location: {}'.format(counter + 1, (a, b)))
            if counter + 1 == 200:
                logger.info('Shoot asteroid #{} at location: {}'.format(counter + 1, (a, b)))
            board[(a, b)] = False
            return True
        else:
            a = a + dx
            b = b + dy
    return False

def shootTheLaser(board, location, dimenstions, angles):
    shootedAstros = 0
    while shootedAstros < 200:
        for angle, direction in angles:
            if shootTheLasterAtDirection(board, location, dimenstions, direction, shootedAstros):
                shootedAstros += 1
                if shootedAstros == 200:
                    break

def getAngles(directions, coordinates):
    angles = {}
    for direction in directions:
        x, y = coordinates
        a, b = direction
        a = x + a
        b = y + b
        angle = math.atan2(a - x, y - b) * 180 / math.pi
        if angle < 0:
            angle = 360 + angle
        logger.debug('For direction: {}, points: {} - {}, angle is: {}'.format(direction, (a, b), coordinates, angle))
        angles[angle] = direction
    angles = sorted(angles.items())
    return angles


def checkDirection(board, location, coordinate, dimensions, directions, count=True):
    x, y = location
    cx, cy = coordinate
    maxx, maxy = dimensions
    dx = cx - x
    dy = cy - y

    logger.debug('Checking direction: {}'.format((dx, dy)))

    divisor = compute_hcf(abs(dx), abs(dy))
    if divisor > 1:
        dx = int(dx / divisor)
        dy = int(dy / divisor)
        logger.debug('Simplified direction to: {}'.format((dx, dy)))
    if (dx, dy) in directions:
        logger.debug('Already did that direction')
        return False
    else:
        directions.append((dx, dy))

    if not count:
        return False

    a = x + dx
    b = y + dy
    while a >= 0 and a < maxx and b >= 0 and b < maxy:
        if board[(a, b)] == True:
            logger.debug('Found asteroid')
            return True
        else:
            a = a + dx
            b = b + dy
    logger.debug('Didnt find asteroid')
    return False

def countAsteroids(board, location, dimensions):
    x, y = location
    directions = []
    astros = 0
    maxx, maxy = dimensions
    for i in range(0, maxx):
        for j in range(0, maxy):
            if (i, j) != (x, y):
                if checkDirection(board, location, (i, j), dimensions, directions):
                    astros += 1
    return astros


def fromFileFindBestAsteroid():
    with open('aoc10.txt', 'r') as file:
        lines = []
        for line in file.readlines():
            lines.append(line)
        testBestAsteroid(lines)

def fromFileShootTheLaser():
    with open('aoc10.txt', 'r') as file:
        lines = []
        for line in file.readlines():
            lines.append(line)
        testLaser(lines, (31, 20))

def findBestAsteroid(board, dimensions):
    max = 0
    x, y = dimensions
    for i in range(0, x):
        for j in range(0, y):
            if board[(i, j)] == True:
                asteroids = countAsteroids(board, (i, j), dimensions)
                logger.debug('For asteroid: {} count is: {}'.format((i, j), asteroids))
                if asteroids > max:
                    logger.info('New max: {} for coordination: {}'.format(asteroids, (i, j)))
                    max = asteroids

    logger.info('Found max: {}'.format(max))


def testBestAsteroid(lines):
    board, dimension = parseInput(lines)
    logger.warning('\nRunning Find Best Asteroid Test with board of dimension: {}'.format(dimension))
    findBestAsteroid(board, dimension)

def testLaser(lines, location):
    board, dimension = parseInput(lines)
    logger.warning('\nRunning Shoot the Laser Test with board of dimension: {}'.format(dimension))
    getAllDirections(board, location, dimension)

def testCountVisibleAsteroids(lines, coordinates):
    board, dimension = parseInput(lines)
    logger.warning('\nRunning Count Visible Asteroids Test with board of dimension: {}'.format(dimension))
    asteroids = countAsteroids(board, coordinates, dimension)
    logger.info('For asteroid: {} count is: {}'.format(coordinates, asteroids))


def runTests():
    testBestAsteroid(['.#..#',
          '.....',
          '#####',
          '....#',
          '...##'])

    testBestAsteroid([
        '......#.#.',
        '#..#.#....',
        '..#######.',
        '.#.#.###..',
        '.#..#.....',
        '..#....#.#',
        '#..#....#.',
        '.##.#..###',
        '##...#..#.',
        '.#....####']
    )

    testCountVisibleAsteroids([
        '......#.#.',
        '#..#.#....',
        '..#######.',
        '.#.#.###..',
        '.#..#.....',
        '..#....#.#',
        '#..#....#.',
        '.##.#..###',
        '##...#..#.',
        '.#....####']
        ,(5, 8))

    testLaser([
        '.#..##.###...#######',
        '##.############..##.',
        '.#.######.########.#',
        '.###.#######.####.#.',
        '#####.##.#.##.###.##',
        '..#####..#.#########',
        '####################',
        '#.####....###.#.#.##',
        '##.#################',
        '#####.##.###..####..',
        '..######..##.#######',
        '####.##.####...##..#',
        '.#####..#.######.###',
        '##...#.##########...',
        '#.##########.#######',
        '.####.#.###.###.#.##',
        '....##.##.###..#####',
        '.#.#.###########.###',
        '#.#.#.#####.####.###',
        '###.##.####.##.#..##']
        , (11, 13))


logger.setLevel(logging.INFO)

runTests()
fromFileFindBestAsteroid()
fromFileShootTheLaser()