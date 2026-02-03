from tkinter import *
from Pixel import Pixel
import numpy as np

class Dino(Pixel): 
    def __init__(self, canv, nrow, ncol, scale, c=2): #sets all the attributes with self so they can be called later 
        self.canv = canv
        self.nrow = nrow
        self.ncol = ncol
        self.scale = scale
        self.c = c
        self.jumpflag = False #Initializes the value of the jump so we can alter it later 
        self.Pixels=[]
    # Remove the pass statement and implement the __init__ method as described in the PDF.


    def get_pattern(self):# this creates the dinosaur pixel art
        self.Dinosaur = np.array([[0,0,1,1,1,1],[0,0,1,1,0,1],[0,0,1,1,1,1],[0,0,1,1,0,0],[1,0,1,1,1,1],[1,0,1,1,0,0],[1,1,1,1,0,0],[0,1,0,1,0,0],[0,1,0,1,0,0]])

        return self.Dinosaur
    
    def get_pattern2(self):# this is for the beast pixel art
        self.Dinosaur = np.array([[0,0,1,1,1,0],[0,0,1,1,0,0],[0,0,1,1,1,0],[0,0,0,1,0,0],[1,0,1,1,1,1],[1,0,1,1,0,0],[1,1,1,1,0,0],[0,1,0,1,0,0],[0,1,0,1,0,0]])

        return self.Dinosaur
    # Remove the pass statement and implement the get_pattern method as described in the PDF.


    def activate(self):# this binds the 2 pixel arts to a key so you can choose between the 2
        self.canv.bind("j", lambda e: self.spawn_dino())
        self.canv.bind("k", lambda e: self.spawn_evil_beast())
        self.canv.focus_set()# this focuses the keybinds earlier to actually trigger and choose between the options this is a tkner function

    def spawn_dino(self): #spawns dino
        self.get_pattern()
        self.Pixels = []
        rows,col = self.Dinosaur.shape

        beginrow= self.nrow //2 #sets the dino in the right space
        begincol = self.ncol//4

        self.w = rows
        self.j = col
        for i in range(rows):
            for j in range(col):
        
                if self.Dinosaur[i][j] != 0:
                    self.Pixels.append(Pixel(self.canv,beginrow+i,begincol+j,self.nrow,self.ncol,self.scale,self.c,[0,0]))
                    self.canv.update()

    def spawn_evil_beast(self): #the same thing as the dino one but for the beast
        self.get_pattern2()
        self.Pixels = []
        rows,col = self.Dinosaur.shape

        beginrow= self.nrow //2
        begincol = self.ncol//4

        self.w = rows
        self.j = col
        for i in range(rows):
            for j in range(col):
        
                if self.Dinosaur[i][j] != 0:
                    self.Pixels.append(Pixel(self.canv,beginrow+i,begincol+j,self.nrow,self.ncol,self.scale,self.c,[0,0]))
                    self.canv.update()#puts a piel anywhere where a 0 does not exist

    # Remove the pass statement and implement the activate method as described in the PDF.
        

    def down(self):#moves the characters down
        for pixel in self.Pixels:
            pixel.down()
            pixel.next()
    # Remove the pass statement and implement the down method as described in the PDF.


    def up(self):# calls functions from pixel.py that moves characters up
        for pixel in self.Pixels:
            pixel.up()
            pixel.next()
    # Remove the pass statement and implement the up method as described in the PDF.


    def jump(self):#this changes the initial value so we can use it now
        if not self.jumpflag:
            self.jumpflag = True
            self.activate_jump(step=0)

    # Remove the pass statement and implement the jump method as described in the PDF.


    def activate_jump(self, step): #implements a jump function that allows the dino and beast to jump
        if step <10: #it checks if the step count is below 10 so it can jump
            self.up()
        elif step <20:#counts another 10 steps as it goes back down so it checks if it is now less than 20 so it knows were back at the origin so it can prepare the next jump animation
            self.down()
        else:
            self.jumpflag = False
            return
        self.canv.after(50,self.activate_jump,step + 1)

    # Remove the pass statement and implement the perform_jump method as described in the PDF.
    

#=============================================================================
# Testing Functions for Dinosaur Class - DO NOT MODIFY
#=============================================================================

def delete_all(canvas):
    canvas.delete("all")

def test1(root, canvas, nrow, ncol, scale):
    d = Dino(canvas, nrow, ncol, scale)
    # Activate the dino in the middle left of the canvas
    d.activate()
    
    # Bind only up and down arrow keys to test basic movement
    root.bind("<Up>", lambda e: d.up())
    root.bind("<Down>", lambda e: d.down())
    
    # Add a visual indicator for test1
    print("\nPress Up/Down arrow keys to move the dinosaur up and down.\n")

def test2(root, canvas, nrow, ncol, scale):
    d = Dino(canvas, nrow, ncol, scale)
    # Activate the dino in the middle of the canvas.
    d.activate()
    
    # Bind arrow keys to move the dino
    root.bind("<space>", lambda e: d.jump())  # Bind spacebar to jump

    print("\nPress Spacebar to make the dinosaur jump.\n")



def main():
    """Initialize the game window and start the application."""
    root = Tk()
    nrow = 40
    ncol = 80
    scale = 20
    canvas = Canvas(root, width=ncol * scale, height=nrow * scale, bg="black")
    canvas.pack()

    # Bind a key for clearing the canvas.
    root.bind("1", lambda e: test1(root, canvas, nrow, ncol, scale))
    root.bind("2", lambda e: test2(root, canvas, nrow, ncol, scale))
    root.bind("d", lambda e: delete_all(canvas))

    instructions = """
    Press '1' to test basic up/down movement.
    Press '2' to test jump movement.
    Press 'd' to clear the canvas.
    """
    print(instructions)

    root.mainloop()

if __name__ == "__main__":
    main()