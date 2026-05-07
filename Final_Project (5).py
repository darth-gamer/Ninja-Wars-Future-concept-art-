import pygame,random,math,json
from pygame.locals import *
from pygame.math import Vector2
pygame.init()
pygame.mixer.init()
font = pygame.font.SysFont(None, 60)
gameMode = 0
gameLoop = True
playerSpeed = 5
grounded = False
fallSpeed = 5
momentum = pygame.math.Vector2(0,0)
pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_CROSSHAIR)#Simple cursor replace
grass = pygame.image.load("grass1.png")
dirt = pygame.image.load("dirt.png")
brimstone = pygame.image.load("brimstone.png")
lavarock = pygame.image.load("lavarock.png")
laceration = pygame.image.load("laceration.png")
weakness = pygame.image.load("weakness.png")
hero = pygame.image.load("hero.png")
impGreen = pygame.image.load("impGreen.png")
impRed = pygame.image.load("impRed.png")
impBlue = pygame.image.load("impBlue.png")
impGold = pygame.image.load("impGold.png")

class Image:
    def __init__(self, sheetW,sheetH,sheetRows,sheetColumns,X,Y,counter, directionFacing):
        self.sheetW = sheetW,
        self.sheetH = sheetH,
        self.sheetW, self.sheetH = self.get_size()
        self.sheetRows = sheetRows,
        self.sheetColumns = sheetColumns,
        self.X = X,
        self.Y = Y,
        self.counter = counter,
        self.directionFacing = directionFacing
    def draw(self):
        pass

heroSheetW, heroSheetH = hero.get_size()
heroSheetRows = 4
heroSheetColumns = 8
heroImageX = 0
heroImageY = 0
heroSheetCounter = 0
directionFacing = "right"

walking = True

boost = 0
boostVector = (0,0)
boostingNewVector = False
inRange=False
slashing = False
reticle = pygame.Rect(0,0,0,0)
reticle2 = pygame.Rect(0,0,0,0)
reticle3 = pygame.Rect(0,0,0,0)

FPS = 100
clock = pygame.time.Clock()
screen = pygame.display.set_mode((800, 1000),pygame.RESIZABLE)
screenRect = pygame.Rect(0,0,800,1000)
w, h = pygame.display.get_surface().get_size()
mousePos = pygame.mouse.get_pos()
offset = pygame.math.Vector2(-100,-300)
world = pygame.Rect(w/2,h/2,50,50)
playerRect = pygame.Rect(w/2,h/2,50,50)
data = {}

class Enemy:
    def __init__(self, position, size, brain, offset, speed):
        self.position = Vector2(position)
        self.size = size
        self.rect = pygame.Rect(position, size)
        self.brain = brain
        self.offset = Vector2(0,0)
        self.speed = speed
        
    def draw(self):
        global impGreen,impRed,impBlue,impGold

        if self.brain == 1:
            screen.blit(impGreen,self.rect)
        if self.brain == 2:
            screen.blit(impBlue,self.rect)
        if self.brain == 3:
            screen.blit(impRed,self.rect)
        if self.brain == 4:
            screen.blit(impGold,self.rect)
    def hunt(self):
        global blocks,paths,screenRect,pathTarget
        self.rect.center = (world.x + self.offset.x,world.y + self.offset.y)
        if self.brain < 3:
            if playerRect.centerx > self.rect.centerx:
                self.offset.x += self.speed * self.brain
            if playerRect.centerx < self.rect.centerx:
                self.offset.x -= self.speed * self.brain
            if playerRect.centery > self.rect.centery:
                self.offset.y += self.speed * self.brain
            if playerRect.centery < self.rect.centery:
                self.offset.y -= self.speed * self.brain
        if self.brain >= 1:
                pass
        if self.brain >= 2:
            for block in blocks:
                if block.rect.colliderect(self.rect)& block.rect.colliderect(screenRect):
                    
                    
                    leftOverlap = block.rect.right + self.rect.left
                    rightOverlap = self.rect.right + block.rect.left
                    topOverlap = block.rect.bottom + self.rect.top
                    bottomOverlap = self.rect.bottom + block.rect.top
                    min_overlap = min(leftOverlap, rightOverlap, topOverlap, bottomOverlap)
                    
                    if min_overlap == topOverlap:
                        self.offset.y += topOverlap
                        
                    elif min_overlap == bottomOverlap:
                        self.offset.y -= bottomOverlap
                        
                    elif min_overlap == leftOverlap:
                        self.offset.x += leftOverlap
                    elif min_overlap == rightOverlap:
                        self.offset.x -= rightOverlap
                    
        if self.brain >= 3:
            if pathTarget.x > self.rect.centerx:
                self.offset.x += self.speed * self.brain
            if pathTarget.x < self.rect.centerx:
                self.offset.x -= self.speed * self.brain
            if pathTarget.y > self.rect.centery:
                self.offset.y += self.speed * self.brain
            if pathTarget.y < self.rect.centery:
                self.offset.y -= self.speed * self.brain
        if self.brain == 4:
            pass
           

class Block:
    def __init__(self, position, size, color):
        self.position = Vector2(position)
        self.size = size
        self.rect = pygame.Rect(position, size)
        self.color = color
    def draw(self):
        global dirt,grass,lavarock,brimstone,laceration,weakness,tilemap

        screen.blit(grass,block)
        
    def collide(self,player):
        global offset,grounded,mousePos,fallSpeed,momentum,boost,reticle,playerSpeed
        keys = pygame.key.get_pressed()
        leftOverlap = player.right - self.rect.left
        rightOverlap = self.rect.right - player.left
        topOverlap = player.bottom - self.rect.top
        bottomOverlap = self.rect.bottom - player.top
        min_overlap = min(leftOverlap, rightOverlap, topOverlap, bottomOverlap)
        #Which of these overlaps is smallest?
        
        if min_overlap == topOverlap:
            if grounded==False:
                momentum.y=0
                offset.y += topOverlap
                grounded=True
            
        elif min_overlap == bottomOverlap:
            momentum.y=0
            offset.y -= bottomOverlap 
            boost=0#wall clime head
            
        elif min_overlap == leftOverlap:

            offset.x += leftOverlap - playerSpeed

            
        elif min_overlap == rightOverlap:
            offset.x -= rightOverlap - playerSpeed
            
def handleInputs():
    global gameLoop,world,boostingNewVector,inRange,playerSpeed
    keys = pygame.key.get_pressed()
    playerSpeed = 0
    if keys[pygame.K_w]:
        pass
        #offset.y += playerSpeed
    if keys[pygame.K_s]:
        playerSpeed = 5
        offset.y -= playerSpeed
    if keys[pygame.K_a]:
        directionFacing = "left"
        playerSpeed = 5
        offset.x += playerSpeed
    if keys[pygame.K_d]:
        directionFacing = "right"
        playerSpeed = 5
        offset.x -= playerSpeed
    for event in events:
        if event.type == pygame.MOUSEBUTTONDOWN:
            #print(f"Mouse button {event.button} clicked at {event.pos}")
            if inRange==True:
                inRange = False
                boostingNewVector = True
                
        if event.type == pygame.QUIT:
            gameLoop = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                gameLoop = False
hero = pygame.transform.scale(hero,playerRect.size)
imp = pygame.Rect(200,200,200,200)
enemy1 = Enemy((100,100),(imp.size),1,(0,0),1)
enemy2 = Enemy((100,100), (imp.size), 2, (0,0),1)
enemy3 = Enemy((100,100),(imp.size),3,(0,0),1)
enemy4 = Enemy((100,100), (imp.size), 4, (0,0),1)
pathTarget = Vector2(0,0)
pathCounter=0
paths=[]
#paths.append(Vector2(playerRect.center))
paths.append(Vector2(world.center))

#subArea = hero.subsurface((heroImageX,heroImageY,(heroSheetW/heroSheetColumns),(heroSheetH/heroSheetRows)))
#scaledHero = pygame.transform.scale(subArea,playerRect.size)
def animate():
    global heroImageX,heroImageY,heroSheetCounter,playerRect,heroSheetW
    global humanSheetH,humanSheetColumns,scaledHuman,subArea,directionFacing,walking

    heroSheetCounter +=8
    
    if heroSheetCounter % (heroSheetW/heroSheetColumns) == 0:
        heroImageX=humanSheetCounter
    if heroSheetCounter>=heroSheetW-(heroSheetW/heroSheetColumns):
        heroSheetCounter=0
        
    if not walking:
        humanImageX=0
    
    if directionFacing == "left":
        heroImageY = (heroSheetH/heroSheetRows)*3
    if directionFacing == "right":
        heroImageY = (humanSheetH/heroSheetRows)*2
    subArea = hero.subsurface((heroImageX,heroImageY,(heroSheetW/heroSheetColumns),(heroSheetH/heroSheetRows)))
    scaledHero = pygame.transform.scale(subArea,playerRect.size)
    screen.blit(scaledHero,playerRect)

def drawPlayer():
    #pygame.draw.rect(screen, ('orange'), (playerRect),0,5)
    screen.blit(hero,playerRect)
def parallax():
    background1= pygame.Rect(world.x/2,world.y/2,500,500)
    background2= pygame.Rect(world.x/3,world.y/3,800,800)
    background3= pygame.Rect(world.x/4,world.y/4,1500,1500)
    #pygame.draw.rect(screen, ('indigo'), (background3),0,0)
    #screen.blit(tree,background2)
    #pygame.draw.rect(screen, ('violet'), (background2),0,0)
    #pygame.draw.rect(screen, ('maroon'), (background1),0,0)
direction_vector = Vector2(mousePos) - playerRect.center
boostVector = direction_vector
def angleCalc():
    global playerRect,boost,offset,boostingNewVector,boostVector,mousePos,reticle,reticle2,reticle3,slashing
    direction_vector = Vector2(mousePos) - playerRect.center
    if direction_vector.length() > 0:
        direction_vector = direction_vector.normalize()
    square_pos = playerRect.center + (direction_vector * 40)
    square_pos2 = playerRect.center + (direction_vector * 60)
    square_pos3 = playerRect.center + (direction_vector * 80)
    reticleD = 15
    reticle = pygame.Rect(square_pos.x-7.5,square_pos.y-7.5,reticleD,reticleD)
    reticle2 = pygame.Rect(square_pos2.x-7.5,square_pos2.y-7.5,reticleD,reticleD)
    reticle3 = pygame.Rect(square_pos3.x-7.5,square_pos3.y-7.5,reticleD,reticleD)
    color = 'lightgray'
    if slashing:
        color = 'lightblue'
    for i in [reticle,reticle2,reticle3]:
        pygame.draw.rect(screen, (color), i,0,5)
    
    if (boostingNewVector):
        boost = 30
        boostVector = direction_vector
        boostingNewVector = False
        
    velocity = boostVector * boost
    offset += velocity
    if boost > 0:
        boost -= 1
def fall():
    global offset,grounded,fallSpeed,momentum
    
    if grounded == False:
        if momentum.y<fallSpeed:
            momentum.y += 1
        offset.y-=momentum.y

tilemap = [
    'BBBBB__________________________________________BBBB_BBBBBBBBBB',
    'B____B_________________________________________B____________BBB',
    'B____B_________________________________________B____________BBB',
    'B____BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB_____BBBB___BBBB',
    'B___________________BBB____________________________B___B___B',
    'B___________________BBB________________________________B___B',
    'B___________________BBB________________________________B___B',
    'B___________________BBB_____BBBBBBBBBBBBBBBBBBBB_______B___B',
    'B___________________BBB________________________________B___B',
    'B___________________BBB________________________________B___B',
    'B______________________________B_______________________B___B',
    'B___________________________BBB________________________B___B',
    'B___________________________BB_________________________B___B',
    'B___________________________BB_________________________B___B',
    'B____________________________B__________________________B___B',
    'B____________________________B___________________________B___B',
    'B____________________________B_____B________________BBBBB___B',
    'B____________B___B______BBB__B_____B_______B__________B____B',
    'B_________B______B___________B_____B__________________B___B',
    'B______B_________B_________________B__________________B___B',
    'B______B_________B__________BBB____B__________________B___B',
    'BBBB_____________B_________________B__________________B___B',
    'BBBBBB___________B_________________B__________________B___B',
    'BBBBBBB__________B_________________B__________________B___B',
    'BBBBBBBB_________B____________B_______________________B___B',
    'BBBBBBBBB________B____________________________________B___B',
    'BBBBBBBBBBBBBBBBBB____________________________________B___B',
    'B_____________BBB_____________________________________B___B',
    'B_______________B_____________________________________B___B',
    'B_____________BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB___B',
    'B________________________________________B________________B',
    'B________________________________________B________________B',
    'B________________________________________B______BBBBBBBBBBB',
    'B_______________________________________________B_______',
    'B________________________________________B______B_______',
    'B________________________________________B______B_______',
    'B________________________________________B______B_______',
    'B________________________________________B______B_______',
    'B________________________________________B______B_______',
    'B________________________________________B______B_______',
    'B________________________________________B______B_______',
    'B________________________________________B______B_______',
    'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB_______',
    

            ]
blocks = []

for y, row in enumerate(tilemap):
    for x, tile in enumerate(row):
        if tile == 'B':
            blocks.append(Block((x * world.w, y * world.h), (world.w, world.h), 'red'))

def loadGame():
    global data,gameMode
    try:
        # the file already exists
        with open('save.txt') as load_file:
            data = json.load(load_file)
            offset.x = data["x"] - playerRect.x
            offset.y = data["y"] - playerRect.y
            momentum.x = data["momentumX"]
            momentum.y = data["momentumY"]
            #world = pygame.Rect(Vector2(data["x"],data["y"]),50,50)
    except:
        # create the file and store initial values
        with open('save.txt', 'w') as store_file:
            json.dump(data, store_file)
    gameMode=1
def newGame():
    global data,gameMode
    with open('save.txt', 'w') as store_file:
        json.dump(data, store_file)
    gameMode=1
buttons = []
messages = []

button0 = buttons.append(pygame.Rect(100,100,300,50))
message0 = messages.append("New Game")

button1 = buttons.append(pygame.Rect(100,300,300,50))
message1 = messages.append("Load Game")

def drawButtons():
    global buttons,messages,data
    buttons[0] = pygame.Rect(w/2-buttons[0].w/2,h/2-buttons[0].h/2,500,50)
    buttons[1] = pygame.Rect(w/2-buttons[1].w/2,h/2+100,500,50)

    for button in buttons:
        pygame.draw.rect(screen, ('lightgray'), button,0,5)
        if button.contains(mousePos,(1,1)):
            pygame.draw.rect(screen, ('lightblue'), button,0,5)
            if button==buttons[0]:
                for event in events:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        newGame()
            if button==buttons[1]:
                for event in events:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        loadGame()
                    
            
        message = f"{messages[buttons.index(button)]}"
        textBox = font.render(message, True,'darkblue')
        screen.blit(textBox, (button.centerx - textBox.get_rect().w/2,button.centery - textBox.get_rect().h/2))  

setupTimer=0
while gameLoop:
    #perform all physics calculations first
    screen.fill('navy')
    clock.tick(FPS)
    mousePos = pygame.mouse.get_pos()
    events = pygame.event.get()
    handleInputs()
    
    w, h = pygame.display.get_surface().get_size()
    
    if gameMode == 0:
        drawButtons()

    if gameMode == 1:
        playerRect = pygame.Rect(w/2-playerRect.w/2,h/2-playerRect.h/2,playerRect.w,playerRect.h)
        world = pygame.Rect(playerRect.x+offset.x,playerRect.y+offset.y,playerRect.w,playerRect.h)
        if setupTimer<30:
            setupTimer+=1
            dirt = pygame.transform.scale(dirt,world.size)
            grass = pygame.transform.scale(grass,world.size)
            lavarock = pygame.transform.scale(lavarock,world.size)
            brimstone = pygame.transform.scale(brimstone,world.size)
            laceration = pygame.transform.scale(laceration,world.size)
            weakness = pygame.transform.scale(weakness,world.size)

            impGreen = pygame.transform.scale(impGreen,imp.size)
            impBlue = pygame.transform.scale(impBlue,imp.size)
            impRed = pygame.transform.scale(impRed,imp.size)
            impGold = pygame.transform.scale(impGold,imp.size)
        else:
            fall()
        inRange=False
        for block in blocks:
            #block.size = Vector2(world.w,world.h)
            block.rect.topleft = ((block.position.x+world.x),(block.position.y+world.y))
            if block.rect.colliderect(playerRect):
                block.collide(playerRect)
            if block.rect.colliderect(reticle)or block.rect.colliderect(reticle2)or block.rect.colliderect(reticle3):
                inRange = True
        pathCounter+=1
        if pathCounter % 200 == 0:
            paths.append(Vector2(world.x-offset.x,world.y - offset.y))
            pathTarget = paths[0]
            if len(paths)>5:
                del paths[0]
        for i in paths:
            i = Vector2((world.x + i.x),(world.y + i.y))
            screen.blit(lavarock, (i))
        #then do all your drawing
        parallax()
        for block in blocks:
            block.draw()
        grounded = False
        pygame.display.set_caption(f"{enemy3.position},paths:{paths}")
        drawPlayer()
        for enemy in [enemy3]:
            enemy.draw()
            enemy.hunt()

        angleCalc()
    pygame.display.flip()
if gameMode>0:
    data = {"x": int(world.x), "y": int(world.y+22),"momentumX":momentum.x,"momentumY":momentum.y}
    with open('save.txt', 'w') as file:
        json.dump(data,file)
pygame.quit()
