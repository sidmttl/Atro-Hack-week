import random
import pygame
import PyParticles
from math import *


(width, height) = (1900, 1000)
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Star formation')

universe = PyParticles.Environment((width, height))
universe.colour = (0,0,0)
universe.addFunctions(['move', 'attract', 'combine'])

def calculateRadius(mass):
    return 0.5 * mass ** (1/2)

def planet_creator(mass,speed,angle,pos,colour):
    particle_mass= mass
    particle_size = calculateRadius(mass)
    #speed
    c=colour
    universe.addParticles(mass=particle_mass, x=pos[0],y=pos[1],size=particle_size,speed=speed,angle=angle,tup=pos,colour=c)
    
planet_creator(1000,0,0,[900,500],(100,0,255))
planet_creator(1,1,0,[800,500],(255,255,255))


#for p in range(100):
#    particle_mass = random.randint(1,4)
#    particle_size = calculateRadius(particle_mass)
#    universe.addParticles(mass=particle_mass, size=particle_size, speed=0, colour=(255,255,255))

#######################
posdown = None
posup = None
parti = False
running = True    
#######################
while running:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
            running = False
            break;
        if event.type == pygame.MOUSEBUTTONDOWN:
            if parti == False:
                posdown = pygame.mouse.get_pos()
                parti = True
            
        
        if event.type == pygame.MOUSEBUTTONUP:
            posup = pygame.mouse.get_pos()
            if(parti):
                dx=posup[0]-posdown[0]
                dy=posup[1]-posdown[1]
                if(dy==0):
                    dy+=1
                angle=0
                if(dy>0):
                    angle = pi
                angle += -atan(dx/dy)
                speed = sqrt(dx*dx + dy*dy)/200
                planet_creator(1,speed,angle,posdown,(255,255,255))
            parti = False
            

    universe.update()
    screen.fill(universe.colour)
    
    particles_to_remove = []
    for p in universe.particles:
        if 'collide_with' in p.__dict__:
            particles_to_remove.append(p.collide_with)
            p.size = calculateRadius(p.mass)
            del p.__dict__['collide_with']

        if p.size < 2:
            pygame.draw.rect(screen, p.colour, (int(p.x), int(p.y), 2, 2))
        else:
            pygame.draw.circle(screen, p.colour, (int(p.x), int(p.y)), int(p.size), 0)
    
    for p in particles_to_remove:
        universe.particles.remove(p)

    pygame.display.flip()
    
pygame.quit()