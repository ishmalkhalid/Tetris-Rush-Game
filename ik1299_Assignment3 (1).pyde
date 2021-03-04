import random

#define global variables
WIDTH = 200
HEIGHT = 400
CELLDIM = 20
 
Num_of_rows = HEIGHT/CELLDIM #20
Num_of_cols = WIDTH/CELLDIM #10

#declare a dictionary of all the colors and a dictionary for the number of blocks per column
colors = {'Red':[255,51,52], 'Blue':[12,150,228], 'Green':[30,183,66], 'Yellow':[246,187,0], 'Purple':[76,0,153], 'White':[255,255,255], 'Black':[0,0,0]}
blocksPerCol = {}

#******************************************************************************************************************************************************************************#

#block class
class Block:
    
    #intialization
    def __init__(self):
        self.x = 0
        self.y = (-CELLDIM)
        self.vx = 0
        self.vy = CELLDIM
        self.colnum = 0
        self.key_code = {LEFT: False, RIGHT: False} #initialize key codes
        self.bcolor = random.choice(list(colors.values()))
        self.randompos()
        
    #stop the block when it reaches ground of another block in the same column
    def stopblock(self):
        if(self.y == HEIGHT-CELLDIM or self.y == (HEIGHT - ((blocksPerCol[self.x/CELLDIM])*CELLDIM))):
            self.vy = 0
        else:
            self.y += self.vy
            
    #move the block left and right    
    def moveblock(self):
        self.prevx = self.x
        
        #move block to the right
        if self.key_code[RIGHT] == True:
            #check that block does not leave game dimensions
            if self.x == (WIDTH-CELLDIM):
                self.vx = 0
            elif self.y >= HEIGHT - blocksPerCol.get((self.x + 20)/CELLDIM, 0)*CELLDIM - CELLDIM:
                self.vx = 0
            else:
                self.vx = CELLDIM
        #move block to the left
        elif self.key_code[LEFT] == True:
            #check that block does not leave game dimensions
            if self.x == 0:
                self.vx = 0
            elif self.y >= HEIGHT - blocksPerCol.get((self.x - 20)/CELLDIM, 0)*CELLDIM - CELLDIM:
                self.vx = 0
            else:
                self.vx = (-CELLDIM)
    
        else: 
            self.vx = 0
        #remove the block from the previous column in the dictionary
        blocksPerCol[self.prevx/CELLDIM] = blocksPerCol.get(self.prevx/CELLDIM, 0) - 1
        self.x += self.vx
        #add the block to the new column in the dictionary
        blocksPerCol[self.x/CELLDIM] = blocksPerCol.get(self.x/CELLDIM, 0) + 1
        self.colnum = (self.x/CELLDIM)
        
    #random starting column of block
    def randompos(self):
        self.x = random.randint(0, Num_of_cols - 1)*CELLDIM 
        #increment the number of blocks in that particular column in the dictionary
        blocksPerCol[self.x/CELLDIM] = blocksPerCol.get(self.x/CELLDIM, 0) + 1
        
    #display random color blocks
    def display(self):
        self.moveblock()
        self.stopblock()
        fill(self.bcolor[0], self.bcolor[1], self.bcolor[2])
        square(self.x,self.y,CELLDIM)
        
#********************************************************************************************************************************************************************************************#

#game class
class Game(list):
    
    #initialization
    def __init__(self):
        self.score = 0
        self.speed = 0
        self.gameover = False
        self.append(Block())
        
    #add a new block when the previous block lands
    def addblock(self):
        
        #add a new block if the previous block's speed is less than or equal to 0
        if(self[len(self)-1].vy <= 0):
             self.append(Block())
             self.checkgameover()
    
    #check if game over
    def checkgameover(self):
        if len(self) == (WIDTH*HEIGHT)/(CELLDIM*CELLDIM):
            self.gameover = True

                
    #display the scoreboard at the top       
    def scoreboard(self):
        fill(0)
        textSize(15)
        text("Score: " + str(self.score), WIDTH-70, CELLDIM-5)
    
    #remove four consecutive blocks of the same color
    def removeblocks(self):
        
        removed = False
        removeblock = []
        
        if len(self) >= 4:
            
            #add all the blocks in the same column to the list called removeblock
            for block in self:
                if block.colnum == self[len(self)-1].colnum:
                    removeblock.append(block)
                    
            #if length of list removeblock is greater than or equal to 4 remove elements of the same color
            if len(removeblock) >= 4:
                if removeblock[len(removeblock)-1].bcolor == removeblock[len(removeblock)-2].bcolor == removeblock[len(removeblock)-3].bcolor == removeblock[len(removeblock)-4].bcolor and removeblock[len(removeblock)-1].vy == 0: 
                    blocksPerCol[removeblock[len(removeblock)-1].x/CELLDIM] = blocksPerCol[removeblock[len(removeblock)-1].x/CELLDIM] - 4
                    self.remove(removeblock[len(removeblock)-1])
                    self.remove(removeblock[len(removeblock)-2])
                    self.remove(removeblock[len(removeblock)-3])   
                    self.remove(removeblock[len(removeblock)-4])
                    self.score = self.score + 1
                    self.speed = 0
                    removed = True
                    
        #increment speed if blocks are not removed       
        if removed == False and self[len(self)-1].vy == 0:
            if frameCount % 0.25 == 0:
                self.speed = self.speed + 0.25
           
        del removeblock[:]
    
    #display the game
    def display(self):

        #if game is not over
        if self.gameover == False:
            setbackground()
           # self.scoreboard()
            self.addblock()
            
            for b in self:
                b.display()
            
            self.removeblocks()
            self.scoreboard()
        
        #if game is over       
        else:
            background(0)
            fill(255)
            textSize(26)
            textAlign(CENTER)
            text("GAME OVER", WIDTH//2, HEIGHT//2)
            text("Score: " + str(self.score), WIDTH//2, (HEIGHT//2)+ 25)  
                    
#************************************************************************************************************************************************************************************************************************************#
            
game = Game()

def setup():
    #set board dimensions, background color and line color
    size(WIDTH, HEIGHT)
    
def draw():
 
    #slowdown the game by not displaying every frame
    if frameCount%(max(1, int(8 - game.speed))) == 0 or frameCount == 1:
        background(210)
        
        #this calls the display method of the game class
        game.display()
        
def setbackground():
        #set background color and line color
        background(210)   
        stroke(180)
        
        x = 0
        y = 0
        
        #draw vertical lines
        for i in range(Num_of_cols):
            line(x, 0, x, HEIGHT)
            x += CELLDIM 
        
        #draw horizontal lines   
        for i in range(Num_of_rows):
            line(0, y, WIDTH, y)
            y += CELLDIM 
            
def keyPressed():
    if keyCode == LEFT:
        game[len(game)-1].key_code[LEFT] = True
    if keyCode == RIGHT:
        game[len(game)-1].key_code[RIGHT] = True
        
def keyReleased():
    if keyCode == LEFT:
        game[len(game)-1].key_code[LEFT] = False
    if keyCode == RIGHT:
        game[len(game)-1].key_code[RIGHT] = False
        
def mouseClicked():
    global game
    if game.gameover == True:
        size(WIDTH, HEIGHT)
        blocksPerCol.clear()
        game = Game()
