import pygame
import sys
import random
import time
import threading
import path
import particule

#---------- Settings ----------
PARTICULE_COUNT = 100
SELECTION_RATE = 0.05
MUTATION_RATE = 0.01
MOVE_COUNT = 300
MOVEMENT_RANGE = 50
GENERATION_STOP = 100

#---------- Initialization ----------
path = path.Path([(100, 100), (1500, 100), (1500, 800), (1000, 800), (1000, 500), (500, 500), (500, 800), (100, 800)], (255, 0, 0), (0, 255, 0), (255, 255, 255), 50)
particules = []

for i in range(PARTICULE_COUNT):
    particules.append(particule.Particule(path.get_start()[0], path.get_start()[1]))
    particules[i].set_moves([(random.randint(-MOVEMENT_RANGE, MOVEMENT_RANGE), random.randint(-MOVEMENT_RANGE, MOVEMENT_RANGE)) for _ in range(MOVE_COUNT)])

#---------- Functions ----------
def isOnSegment(particule, start, end):
    x, y = particule.get_x(), particule.get_y()
    xs, ys = start[0], start[1]
    xe, ye = end[0], end[1]
    width = path.get_path_width() // 2
    if (x <= max(xs, xe) + width and x >= min(xs, xe) - width and y <= max(ys, ye) + width and y >= min(ys, ye) - width):
        return True
    return False

def isOnPath(particule):
    for i in range(path.get_corner_count() - 1):
        if (isOnSegment(particule, path.get_corner(i), path.get_corner(i + 1))):
            return True
    return False

def getDistance(particule, target):
    x, y = particule.get_x(), particule.get_y()
    xt, yt = target[0], target[1]
    return ((x - xt) ** 2 + (y - yt) ** 2) ** 0.5

def getScore(particule):
    global run
    score = 0
    if (getDistance(particule, path.get_corners()[particule.score[0]]) < path.get_path_width() // 2):
        particule.score[0] += 1
        if (particule.score[0] == path.get_corner_count()):
            run = False
            return [particule.score[0], 1000000]
    if (isOnPath(particule)):
        particule.set_onPath(particule.get_onPath() + 1)
    if (particule.get_onPath() > (int) (MOVE_COUNT * 0.9)):
        score += 5000
    score +=  particule.get_onPath() * 0 + particule.score[0] * 2000 - getDistance(particule, path.get_corners()[particule.score[0]])
    return [particule.score[0], score]

def updateparticules(moveNumber):
    for i in range(PARTICULE_COUNT):
        particules[i].set_x(particules[i].get_x() + particules[i].get_move(moveNumber)[0])
        particules[i].set_y(particules[i].get_y() + particules[i].get_move(moveNumber)[1])
        particules[i].set_score(getScore(particules[i]))
        
def drawparticules():
    for i in range(PARTICULE_COUNT):
        if (particules[i].get_x() > 0 and particules[i].get_x() < 1600 and particules[i].get_y() > 0 and particules[i].get_y() < 900):
            particules[i].draw(screen)

def drawBestParticule():
    for i in range (MOVE_COUNT):
        pygame.draw.line(screen, (255, 0, 0), (bestParticule.get_x(), bestParticule.get_y()), (bestParticule.get_x() + bestParticule.get_move(i)[0], bestParticule.get_y() + bestParticule.get_move(i)[1]), 5)
        bestParticule.draw(screen)
        bestParticule.set_x(bestParticule.get_x() + bestParticule.get_move(i)[0])
        bestParticule.set_y(bestParticule.get_y() + bestParticule.get_move(i)[1])
        bestParticule.draw(screen)
        pygame.display.update()
        time.sleep(0.1)

def newGeneration(particules):
    # Selection
    particules.sort(key = lambda x: x.get_score()[1], reverse = True)
    particules = particules[:int(SELECTION_RATE * PARTICULE_COUNT)]
    # Crossover
    newParticules = []
    for i in range(PARTICULE_COUNT):
        parent1 = random.choice(particules)
        parent2 = random.choice(particules)
        moves = []
        for j in range(MOVE_COUNT):
            if (random.random() < 0.5):
                moves.append(parent1.get_move(j))
            else:
                moves.append(parent2.get_move(j))
        newParticules.append(particule.Particule(path.get_start()[0], path.get_start()[1]))
        newParticules[i].set_moves(moves)
    # Mutation
    for i in range(PARTICULE_COUNT):
        for j in range(MOVE_COUNT):
            if (random.random() < MUTATION_RATE):
                newParticules[i].set_move(j, (random.randint(-MOVEMENT_RANGE, MOVEMENT_RANGE), random.randint(-MOVEMENT_RANGE, MOVEMENT_RANGE)))
    return newParticules
    
#---------- Main Loop ----------
generation = 0
moveNumber = 0
run = True

pygame.init()
screen = pygame.display.set_mode((1600, 900))
pygame.display.set_caption("Genetic Path Tracking Algorithm - Generation " + str(generation))

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill((0, 0, 0))
    path.draw(screen)

    if (moveNumber < MOVE_COUNT):
        updateparticules(moveNumber)
        drawparticules()
        moveNumber += 1
    else:
        generation += 1
        if (generation > GENERATION_STOP):
            run = False
            break
        pygame.display.set_caption("Genetic Path Tracking Algorithm - Generation " + str(generation))
        moveNumber = 0
        particules = newGeneration(particules)
    pygame.display.update()

particules.sort(key = lambda x: x.get_score()[1], reverse = True)
bestParticule = particules[0]
bestParticule.set_x(path.get_start()[0])
bestParticule.set_y(path.get_start()[1])
bestParticule.set_color((0, 255, 0))
screen.fill((0, 0, 0))
path.draw(screen)
bestParticule.draw(screen)
thread = threading.Thread(target = drawBestParticule)
thread.start()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()