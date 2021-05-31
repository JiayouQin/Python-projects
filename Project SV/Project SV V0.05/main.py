import sys, pygame

def cooldown():
    if playership.slots[0].cooldown > 0:
        playership.slots[0].cooldown -= 1
    



class ships(object):
    def __init__(self,pos,health,weaponpos,hitpos,img,slots):
        self.health = health
        self.pos = pos
        self.weaponpos = weaponpos
        self.hitpos = pos
        self.img = img
        self.slots = slots
        
        
        
    def draw(self,screen):
        screen.blit(self.img,self.pos)
        screen.blit(playership.slots[0].img,playership.slots[0].pos)
    

class weapons(object):
    def __init__(self,pos,firepos,hitpos,health,img,cooldown,code):
        self.pos = pos
        self.firepos = firepos
        self.hitpos = hitpos
        self.health = health
        self.img = img
        self.fps = 0
        self.cooldown = cooldown
        self.cooldown_stat = cooldown
        self.code = code
        self.projectile = []
        
    def fire(self):
        vfxlist.append(vfx(self.firepos,(0,0,0),(0,0,0),2))
        enemyship.health -= 1

        
class vfx(object):
    def __init__(self,pos,endpos,color,vfxtype):
        self.vfxtype = vfxtype
        self.pos = pos
        self.fps = 0
        self.endpos = endpos
        self.color = color
        self.explosion = [pygame.image.load("Explosion/1.png"),pygame.image.load("Explosion/2.png"),
                     pygame.image.load("Explosion/3.png"),pygame.image.load("Explosion/4.png"),
                     pygame.image.load("Explosion/5.png"),pygame.image.load("Explosion/6.png"),
                     pygame.image.load("Explosion/7.png")]
        self.minigunfire = [pygame.image.load("Minigunfire/1.png"),pygame.image.load("Minigunfire/2.png"),
                            pygame.image.load("Minigunfire/3.png"),pygame.image.load("Minigunfire/4.png"),
                            pygame.image.load("Minigunfire/5.png"),pygame.image.load("Minigunfire/6.png")]

    def explosion01(self,screen):
        self.fps += 1
        if 0 <= self.fps < 28:
            screen.blit(self.explosion[int(self.fps/4)],self.pos)
        if self.fps == 1:
            sfx = pygame.mixer.Sound('ExplosionSFX.mp3')
            sfx.play()
        if self.fps == 28:
            self.fps = -1
    def minigunfire01(self,screen):
        self.fps += 1
        if 0 <= self.fps < 120:
            self.temp = self.fps
            while self.temp > 5:
                self.temp -= 6
            screen.blit(self.minigunfire[int(self.temp)],self.pos)
        if self.fps == 1:
            sfx = pygame.mixer.Sound('minigun.mp3')
            sfx.play()
        if self.fps == 121:
            self.fps = -1
            
    def laser(self,screen):
        
        self.fps += 1
        if self.fps < 45:
            pygame.draw.aaline(screen,self.color, self.pos, (self.pos[0],0))
            pygame.draw.aaline(screen,self.color, self.endpos, (self.endpos[0],0))
            if self.fps == 1:
                lasersfx = pygame.mixer.Sound('Laser.mp3')
                lasersfx.play()
        if self.fps ==45:
            
            self.fps = -1
        
def refresh():
    
    screen.blit(bg,(0,0))
    playership.draw(screen)
    enemyship.draw(screen)
    for i in vfxlist:
        if i.vfxtype == 0:
            i.laser(screen)
        elif i.vfxtype ==1:
            i.explosion01(screen)
        elif i.vfxtype ==2: # gunfire
            i.minigunfire01(screen)
        if i.fps == -1:
            vfxlist.pop(vfxlist.index(i))
    screen.blit(ui,(0,0))
    pygame.display.update()

    
    
def beam(beamfps):
    if beamfps != 0:
        if beamfps == 180: # frame length of the beam
            beamfps = 0
        else:
            if beamfps == 1:
                vfxlist.append(vfx((630,220),(1620,300),(255,0,0),0)) #Laser VFX
            beamfps += 1
    return beamfps

def enemybeam(enemybeamfps):
    if enemybeamfps == 480: # Cool down, 8s in 60 fps
        enemybeamfps = 0
    if enemyship.health > 0:
        if enemybeamfps == 1:
            vfxlist.append(vfx((1516,180),(630,470),(0,255,0),0)) #Laser VFX
            playership.health -= 1
    enemybeamfps = enemybeamfps + 1
    return enemybeamfps



def healthcheck(fps):
    global ship1
    global ship1stat
    
    if playership.health <= 0: #enemy ship refreshing on UI
        if fps >= 0:
            fps = fps + 1
        if fps == 91:
            fps = -1
        if fps == 1:
            vfxlist.append(vfx((560,390),(0,0,0),(0,0,0),1))# Explosion VFX
        if fps == 15:
            playership.img = pygame.image.load("Ship1wreck.png")
    return fps

def enemyhealthcheck(fps):
    global ship2
    global ship2stat
    
    if enemyship.health <= 0: #enemy ship refreshing on UI
        if fps >= 0:
            fps = fps + 1
        if fps == 1:
            vfxlist.append(vfx((1620,300),(0,0,0),(0,0,0),1))# Explosion VFX
        if ship2fps == 15:
            enemyship.img = pygame.image.load("Ship2wreck.png")
    return fps
    
def inputcheck():
    global beamfps
    global run
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_x:
            if beamfps == 0 and playership.health > 0:
                beamfps = 1 #once the fps is set to one it will goes on to the 180th frame
                enemyship.health -= 1
        if event.key == pygame.K_z:
            if playership.health > 0 and playership.slots[0].cooldown == 0:
                playership.slots[0].fire()
                playership.slots[0].cooldown = playership.slots[0].cooldown_stat

#-------------------------init-------------------
ship1 = pygame.transform.smoothscale(pygame.image.load("shiphull.png"), (420,610))
ship2 = pygame.image.load("Ship2.png")
minigun = pygame.transform.smoothscale(pygame.image.load("minigun.png"), (56,120))
ship1rect = (420,220)
ship2rect = (1400,160)
playerweaponpos = (630,220)
enemyweaponpos = (1516,180)

playerhitpos = (630,470)
enemyhitpos = (1620,300)

playerhealth = 3
enemyhealth = 2

vfxlist = []
run = True


#weapon class: pos,firepos,hitpos,health,img,cooldown,code
weapon1 = weapons((ship1rect[0]+367,ship1rect[1]+372),(805,570),(ship1rect[0]+395,ship1rect[1]+372),2,minigun,180,2)
playership = ships(ship1rect,playerhealth,playerweaponpos,playerhitpos,ship1,[weapon1])
enemyship = ships(ship2rect,enemyhealth,enemyweaponpos,enemyhitpos,ship2,[])

pygame.init() 
clock = pygame.time.Clock()
size = width, height = 1920, 1080
pygame.display.set_caption("Project SV")
bgcolor = 255, 255, 255
beamcolor = pygame.Color(255, 0, 0)
beamfps = 0
enemybeamfps = 100
ship1fps = 0
ship2fps = 0
screen = pygame.display.set_mode(size)

#-------------------------load image----------------------------

bg = pygame.transform.smoothscale(pygame.image.load("bg.jpg"), (1920,1080))
ui = pygame.transform.smoothscale(pygame.image.load("ui.png"), (1920,1080))
ui.set_colorkey((255,255,255))
ui = pygame.Surface.convert_alpha(ui)

screen.blit(bg,(0,0))
playership.draw(screen)
enemyship.draw(screen)

pygame.display.update()
#---------------------------------------------------------------

while run:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        inputcheck()

    cooldown()
    ship1fps = healthcheck(ship1fps)
    ship2fps = enemyhealthcheck(ship2fps)#check status of the enemy ship
    beamfps = beam(beamfps)#shipfire
    enemybeamfps = enemybeam(enemybeamfps)
    
    refresh()
    
pygame.quit
