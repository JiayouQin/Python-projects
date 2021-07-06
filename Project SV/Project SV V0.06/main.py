import sys, pygame

class coordinates(object): #calculate map coordinates, show maps etc.
    
    def __init__(self,playercoordinates,enemycoordinates):
        self.showmap = True
        self.mapbackground = (255,255,255)
        self.uicenter = (150,150)
        self.playerui = pygame.image.load("MapUI/playership.png")
        self.enemyui = pygame.image.load("MapUI/enemyship.png")
        self.projectileui = pygame.image.load("MapUI/projectiles.png")
        
    def draw_map(self):
        #get x and y in a list
        self.enemyvector = [enemyship.coordinates[0]-playership.coordinates[0],enemyship.coordinates[1]-playership.coordinates[1]]
        
        if self.showmap == True:
            pygame.draw.rect(screen,(self.mapbackground),pygame.Rect(0, 0, 300, 300))
            screen.blit(self.playerui,self.uicenter)
            # draw ui if within range of 1500m 
            if -1500 <=  self.enemyvector[0] <= 1500 and -1500 <=  self.enemyvector [1] <= 1500:
                screen.blit(self.enemyui,(self.uicenter[0]+int(self.enemyvector[0]/10)-11,self.uicenter[1]+int(self.enemyvector[1]/10)-10))
            for p in projectile_list:
                p_vector=[p.coordinates[0]-playership.coordinates[0],p.coordinates[1]-playership.coordinates[1]]
                if -1500 <=  p_vector[0] <= 1500 and -1500 <=  p_vector [1] <= 1500:
                    screen.blit(self.projectileui,(self.uicenter[0]+int(p_vector[0]/10)-11,self.uicenter[1]+int(p_vector[1]/10)-10))


def cooldown():
    for i in playership.slots:
        if i.cooldown > 0:
            i.cooldown -= 1
    for i in enemyship.slots:
        if i.cooldown > 0:
            i.cooldown -= 1

class ships(object):
    def __init__(self,pos,health,hitpos,img,slots,coordinates,speed):
        self.health = health
        self.pos = pos
        self.hitpos = pos
        self.img = img
        self.slots = slots
        self.coordinates = coordinates
        self.speed = speed
    def draw(self,screen):
        screen.blit(self.img,self.pos)
        screen.blit(playership.slots[0].img,playership.slots[0].pos)
        #1 is fake
        screen.blit(playership.slots[2].img,playership.slots[2].pos)
class weapons(object):
    def __init__(self,pos,firepos,hitpos,damage,health,img,cooldown,code):
        self.pos = pos
        self.firepos = firepos
        self.hitpos = hitpos
        self.damage = damage
        self.health = health
        self.img = img
        self.fps = 0
        self.cooldown = cooldown
        self.cooldown_stat = cooldown
        self.code = code
        self.projectile = []
        
    def fire(self):
        if self.code == -1:
            if self.cooldown == 0:
                vfxlist.append(vfx((1516,180),(630,470),(0,255,0),1)) # Enemmy VFX
                playership.health -= 1
                self.cooldown = self.cooldown_stat
        if self.code == 1:
            vfxlist.append(vfx(self.firepos,(1620,300),(255,0,0),1)) # Laser VFX
            enemyship.health -= self.damage
            self.cooldown = self.cooldown_stat
        if self.code == 2:
            vfxlist.append(vfx(self.firepos,(0,0,0),(0,0,0),2))# Minigun VFX
            enemyship.health -= self.damage
            self.cooldown = self.cooldown_stat
            
        if self.code == 3:
            vfxlist.append(vfx(self.firepos,(0,0,0),(0,0,0),3))
            projectile_list.append(projectiles(playership.coordinates[:],5,1,True))
            self.cooldown = self.cooldown_stat


class projectiles(object):
    def __init__(self,coordinates,velocity,damage,seeking):
        self.coordinates = coordinates
        self.velocity = velocity
        self.damage = damage
        self.seeking = seeking
        
    def update():
        for p in projectile_list:
            if p.seeking == True:
                vectorx=p.coordinates[0]-enemyship.coordinates[0]
                vectory=p.coordinates[1]-enemyship.coordinates[1]

                if abs(vectorx) + abs(vectory) <= p.velocity:
                    # impact
                    enemyship.health -= p.damage
                    projectile_list.pop(projectile_list.index(p))
                else:
                    speedx = vectorx/(vectorx+vectory)*p.velocity
                    speedy = vectory/(vectorx+vectory)*p.velocity
                    p.coordinates[0] += int(speedx)
                    p.coordinates[1] += int(speedy)
        else:# none-seeking projectiles, considering that it would be very hard to hit this is just a place holder at the moment
            #place holder
            pass
            
        
        pass
        
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
        
        self.missile = [pygame.image.load("missile/missile1.png"),pygame.image.load("missile/missile1.png"),
                        pygame.image.load("missile/missile3.png"),pygame.image.load("missile/missile4.png"),
                       pygame.image.load("missile/missile5.png"),pygame.image.load("missile/missile6.png"),
                       pygame.image.load("missile/missile7.png")]
        
    def vfx_draw():
        for i in vfxlist:
            if i.vfxtype == 1:
                i.laser(screen)
            elif i.vfxtype ==0:
                i.explosion01(screen)
            elif i.vfxtype ==2: # gunfire
                i.minigunfire01(screen)
            elif i.vfxtype ==3: #missile
                i.missile_vfx(screen)
            if i.fps == -1:
                vfxlist.pop(vfxlist.index(i))

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
            
    def missile_vfx(self,screen):
        self.fps += 1
        if 0 <= self.fps < 30:
            screen.blit(self.missile[6],(self.pos[0],self.pos[1]-int(self.fps)))
            
        elif 30 <= self.fps <=120:
            screen.blit(self.missile[int(self.fps%6)],(self.pos[0],self.pos[1]-self.fps*11+300))
        if self.fps == 1:
            sfx = pygame.mixer.Sound('missle.mp3')
            sfx.play()
        if self.fps == 60:
            pass
        if self.fps == 121:
            self.fps = -1
        
        
        
        
def refresh():
    screen.blit(bg,(0,0))
    playership.draw(screen)
    enemyship.draw(screen)
    vfx.vfx_draw()
    draw_ui()
    coordinatescheck.draw_map()
    pygame.display.update()


def enemyAI(frames):
    
    # fire immediatly if weapon has been cooled down
    if enemyship.health > 0:
        for i in enemyship.slots:
            i.fire()
    #moving
    speed = 60 #60m per sec, 216Km per hour
    #if range > 500m
    if (enemyship.coordinates[0]-playership.coordinates[0]) ** 2 + (enemyship.coordinates[1]-playership.coordinates[1]) ** 2 >= 250000 and enemyship.health > 0:
        vectorx=(playership.coordinates[0]-enemyship.coordinates[0])
        vectory=playership.coordinates[1]-enemyship.coordinates[1]
        speedx = vectorx/(vectorx+vectory)*speed
        speedy = vectory/(vectorx+vectory)*speed
        if frames == 0: #closing in every 60 frams
            enemyship.coordinates[0] -= int(speedx)
            enemyship.coordinates[1] -= int(speedy)
            frames = 60
        frames -= 1
    else:
        pass
    return frames


def healthcheck(fps):
    global ship1
    global ship1stat
    
    if playership.health <= 0: #enemy ship refreshing on UI
        if fps >= 0:
            fps = fps + 1
        if fps == 91:
            fps = -1
        if fps == 1:
            vfxlist.append(vfx((560,390),(0,0,0),(0,0,0),0))# Explosion VFX
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
            vfxlist.append(vfx((1620,300),(0,0,0),(0,0,0),0))# Explosion VFX
        if ship2fps == 15:
            enemyship.img = pygame.image.load("Ship2wreck.png")
            coordinatescheck.enemyui = pygame.image.load("MapUI/destroyedenemyship.png")
    return fps
    
def inputcheck():
    global beamfps
    global run
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_w:
            playership.coordinates[1] -= 100
        if event.key == pygame.K_s:
            playership.coordinates[1] += 100
        if event.key == pygame.K_a:
            playership.coordinates[0] -= 100
        if event.key == pygame.K_d:
            playership.coordinates[0] += 100
        
        #----------------------Arsenal
        if event.key == pygame.K_c:
            if playership.health > 0 and playership.slots[2].cooldown == 0:
                playership.slots[2].fire()
        
        if event.key == pygame.K_x:
            #only fire when cooldown is 0, set cooldown to a specific value and fire,unit is one frame
            if playership.health > 0 and playership.slots[1].cooldown == 0:
                playership.slots[1].fire()

        if event.key == pygame.K_z:
            if playership.health > 0 and playership.slots[0].cooldown == 0:
                playership.slots[0].fire()
                
        #----------------------map
        if event.key == pygame.K_m:
            if coordinatescheck == False:
                coordinatescheck = True
            else:
                coordinatescheck = False
        if event.key == pygame.K_p:
            run = False
            
def draw_ui():
    buttons =pygame.transform.scale(pygame.image.load("UI/Button(withgauge).png"), (200,90))
    screen.blit(ui,(0,0))
    weapons = len(playership.slots)
    pygame.draw.rect(screen,(0,0,0),pygame.Rect(0, 880, 1320, 200))
    if weapons > 0:
        pixels = int(playership.slots[0].cooldown/playership.slots[0].cooldown_stat*180)
        screen.blit(buttons,(10,890))
        pygame.draw.rect(screen,(195,195,195),pygame.Rect(200-pixels, 940, 0+pixels,20))
    if weapons > 1:
        pixels = int(playership.slots[1].cooldown/playership.slots[1].cooldown_stat*180)
        screen.blit(buttons,(10,980))
        pygame.draw.rect(screen,(195,195,195),pygame.Rect(200-pixels, 1030, 0+pixels,20))
    if weapons > 2:
        pixels = int(playership.slots[2].cooldown/playership.slots[2].cooldown_stat*180)
        screen.blit(buttons,(210,890))
        pygame.draw.rect(screen,(195,195,195),pygame.Rect(200-pixels+200, 940, 0+pixels,20))
