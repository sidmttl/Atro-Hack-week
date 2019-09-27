import random
import pygame
import PyParticles
from math import *

yellow = (255,255,0)
white=(255,255,255)
black=(0,0,0)
blue = (0,255,255)

pygame.init()
(width, height) = (1900, 1000)
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Star formation')

universe = PyParticles.Environment((width, height))
universe.colour = (0,0,0)
universe.addFunctions(['move', 'attract', 'combine'])

def calculateRadius(mass):
    return 0.5 * mass ** (1/3)

def planet_creator(mass,speed,angle,pos,colour):
    particle_mass= mass
    particle_size = calculateRadius(mass)
    #speed
    c=colour
    universe.addParticles(mass=particle_mass, x=pos[0],y=pos[1],size=particle_size,speed=speed,angle=angle,tup=pos,colour=c)
    
planet_creator(10000,0,0,[900,500],yellow)
planet_creator(5,4,0,[800,500],white)
planet_creator(10,-2.5,0,[600,500],yellow)
planet_creator(10,2,0,[400,500],blue)
planet_creator(1,2.5,0,[410,500],white)

def rectangle(screen,height,width,pos,color):
    pygame.draw.rect(screen,color,(pos[0],pos[1],height,width))


def fontt(txt):
    font = pygame.font.Font('freesansbold.ttf',32)
    text = font.render(txt,True, (255,255,0) , (0,0,0))
    textRect = text.get_rect()
    textRect.center = (45,50)
    return text,textRect

#for p in range(100):
#    particle_mass = random.randint(1,4)
#    particle_size = calculateRadius(particle_mass)
#    universe.addParticles(mass=particle_mass, size=particle_size, speed=0, colour=(255,255,255))

#######################
posdown = None
posup = None
parti = False
running = True
y_comp = 200
#######################
while running:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
            running = False
            break;
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pos()[0]<=70 and pygame.mouse.get_pos()[0]>=20 and pygame.mouse.get_pos()[1]<=900 and pygame.mouse.get_pos()[1]>=100:
                y_comp = pygame.mouse.get_pos()[1]
            
            elif parti == False:
                posdown = pygame.mouse.get_pos()
                parti = True
        
        if pygame.mouse.get_pressed()[0] and pygame.mouse.get_pos()[0]<=70 and pygame.mouse.get_pos()[0]>=20 and pygame.mouse.get_pos()[1]<=900 and pygame.mouse.get_pos()[1]>=100:
                y_comp = pygame.mouse.get_pos()[1]
        
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
                planet_creator((y_comp- 100)*2,speed,angle,posdown,(255,255,255))
            parti = False
    

    universe.update()
    screen.fill(universe.colour)
    rectangle(screen,50,800,[20,100],(246, 173, 207))
    rectangle(screen,50,900-y_comp,[20,y_comp],(0,255,255))
    text,textRect = fontt(str(y_comp))
    screen.blit(text,textRect)

    
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