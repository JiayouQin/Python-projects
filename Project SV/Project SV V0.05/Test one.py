#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import sys, pygame

def beam(beamfps):
    global ship1health
    if beamfps != 0:
        if beamfps == 180: # frame length of the beam
            beamfps = 0
        else:
            if beamfps == 1:
                lasersfx = pygame.mixer.Sound('Laser.mp3')
                lasersfx.play()
            if beamfps < 60:
                pygame.draw.aaline(screen,(255, 0, 0), (630,220), (630,0))
                pygame.draw.aaline(screen,(255, 0, 0), (1620,0), (1620,300))
            beamfps = beamfps + 1
    return beamfps

def enemybeam(enemybeamfps):
    global ship1health
    global ship2health
    if enemybeamfps == 480: # frame length of the beam
        enemybeamfps = 0
    if ship2health > 0:
        if 1 < enemybeamfps < 60:
            pygame.draw.aaline(screen,(0, 0, 255), (630,470), (630,0))
            pygame.draw.aaline(screen,(0, 0, 255), (1516,180), (1516,0))
        if enemybeamfps == 1:
            lasersfx = pygame.mixer.Sound('Laser.mp3')
            lasersfx.play()
            ship1health = ship1health - 1
            
    enemybeamfps = enemybeamfps + 1
    return enemybeamfps

def healthcheck(fps):
    global ship1
    if ship1health <= 0: #enemy ship refreshing on UI
        if fps >= 0:
            fps = fps + 1
        if fps == 91: # frame length of the beam
            fps = -1
        if fps == 2:
            sfx = pygame.mixer.Sound('ExplosionSFX.mp3')
            sfx.play()
        if 9 < fps < 30:
            screen.blit(explosion,(560,390))
        if fps == 15:
            ship1 = pygame.image.load("Ship1wreck.png")
            
    return fps

def enemyhealthcheck(fps):
    global ship2
    if ship2health <= 0: #enemy ship refreshing on UI
        if fps >= 0:
            fps = fps + 1
        if fps == 91: # frame length of the beam
            fps = -1
        if fps == 2:
            sfx = pygame.mixer.Sound('ExplosionSFX.mp3')
            sfx.play()
        if 9 < fps <30:
            screen.blit(explosion,(1620,300))
        if ship2fps == 15:
            ship2 = pygame.image.load("Ship2wreck.png")
            
    return fps
    
def inputcheck():
    global beamfps
    global ship1health
    global ship2health
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_m:
            if beamfps == 0:
                if ship1health > 0:
                    beamfps = 1 #once the fps is set to one it will goes on to the 180th frame
                    ship2health = ship2health - 1
    
pygame.init() #-------------------------init-------------------
clock = pygame.time.Clock()
size = width, height = 1920, 1080
pygame.display.set_caption("Project SV")
bgcolor = 255, 255, 255
beamcolor = pygame.Color(255, 0, 0)
beamfps = 0
ship1fps = 0
ship2fps = 0
enemybeamfps = 0
screen = pygame.display.set_mode(size)

ship1health = 2
ship2health = 3
bg = pygame.transform.smoothscale(pygame.image.load("bg.png"), (1920,1080))
ship1 = pygame.image.load("Ship1.png")
ship2 = pygame.image.load("Ship2.png")
explosion = pygame.image.load("explosion.png")
ship1rect = (420,220)
ship2rect = (1400,160)

#---------------------------------------------------------------

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        inputcheck()

    screen.fill(bgcolor)
    screen.blit(bg,(0,0))
    screen.blit(ship1,ship1rect)
    screen.blit(ship2,ship2rect)
    ship1fps = healthcheck(ship1fps)
    ship2fps = enemyhealthcheck(ship2fps)#check status of the enemy ship
    beamfps = beam(beamfps)#shipfire
    enemybeamfps = enemybeam(enemybeamfps)
    pygame.display.flip()
    clock.tick(60)


# In[ ]:




