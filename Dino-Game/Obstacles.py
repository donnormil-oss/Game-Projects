from tkinter import *
from Pixel import Pixel
import random
import numpy as np

class Obstacles:
    def __init__(self, canv, nrow, ncol, scale, c=2, pattern=None):
        self.canv =canv
        self.nrow =nrow
        self.ncol = ncol
        self.scale = scale
        self.c = c
        self.pattern = pattern
        self.speed=1
    # Remove the pass statement and implement the __init__ method as described in the PDF.


    def get_pattern(self):
        return np.array(self.pattern)  #returns numpy array of the current pattern
    
    # Remove the pass statement and implement the get_pattern method as described in the PDF.
    

    def activate(self): # creates patterns from the arrays we make by iterating through and placing a pixel every time there is a 1
        self.Pixels = []
        rows,col = self.pattern.shape

        center = self.nrow //2
        beginrow = center - rows  # spawns patterns in the right position
        begincol = self.ncol - col

        self.w = rows
        self.j = col
        for i in range(rows):
            for j in range(col):
        
                if self.pattern[i][j] != 0:
                    self.Pixels.append(Pixel(self.canv,beginrow+i,begincol+j,self.nrow,self.ncol,self.scale,self.c,[0,0]))

    # Remove the pass statement and implement the activate method as described in the PDF.
            

    def left(self): #moves the pixels to the left 
        for pixel in self.Pixels:
            pixel.j-=self.speed #this is later used to control the speed of the obstacles 
            pixel.next()
            
        
    # Remove the pass statement and implement the left method as described in the PDF.


    @staticmethod
    def random_select(canv, nrow, ncol, scale): #randomly selects a pattern to spawn as an obstacle on the screen between pencil box and tree
        
            Pencil = np.array([[1],[1],[1],[1]]) 
            box = np.array([[1,1,1],[1,1,1],[1,1,1]])
            tree = np.array([[1,1,1],[1,1,1],[0,1,0]])
            patterns = [Pencil,box,tree]
            randompattern = random.choice(patterns)
            return Obstacles(canv,nrow,ncol,scale,2,randompattern)
        
    # Remove the pass statement and implement the random_select method as described in the PDF.


#=============================================================================
# All Child Classes
#=============================================================================

class Box(Obstacles): #creates the shape of a box with the arrays 
    def __init__(self, canv, nrow, ncol, scale):
        box = np.array([[1,1,1],[1,1,1],[1,1,1]])
        super().__init__(canv,nrow,ncol,scale,c=2,pattern=box) #super is used when calling the parent atrributes in a child class
    # Remove the pass statement and implement the __init__ method as described in the PDF.


class Tree(Obstacles): #creates the shape of a tree with the arrays 
    def __init__(self, canv, nrow, ncol, scale,):
        tree = np.array([[1,1,1],[1,1,1],[0,1,0]]) #the ones are where a pixel can be and the 0 are where they cant be we used this method to create various shapes like tree
        super().__init__(canv,nrow,ncol,scale,c=3,pattern=tree)
    # Remove the pass statement and implement the __init__ method as described in the PDF.

        
class Pencil(Obstacles):# creates the shape of a pencil with the arrays
    def __init__(self, canv, nrow, ncol, scale):
        pencil = np.array([[1],[1],[1],[1]])
        super().__init__(canv,nrow,ncol,scale,c=5,pattern=pencil)
    # Remove the pass statement and implement the __init__ method as described in the PDF.



#=============================================================================
# Testing Functions for Obstacles Class - DO NOT MODIFY
#=============================================================================

def delete_all(canvas):
    """Clear all elements from the canvas."""
    canvas.delete("all")
    print("Canvas cleared")


def test1(root, canvas, nrow, ncol, scale):
    print("\nPress left arrow key to move the obstacle left\n")
    obs = Obstacles.random_select(canvas, nrow, ncol, scale)
    obs.activate()

    def left():
        obs.left()  # Move the obstacle left

    root.bind("<Left>", lambda e: left())  # Bind left arrow key to move obstacle

def test2(root, canvas, nrow, ncol, scale):
    obstacle = None  # Only one obstacle active at a time
    paused = False   # Pause flag
    print("\nPress 'p' to pause/resume the obstacle movement\n")

    def toggle_pause(event=None):
        nonlocal paused
        paused = not paused
        print("Paused" if paused else "Resumed")

    # Bind the "p" key to toggle pause
    root.bind("<p>", toggle_pause)

    def update():
        nonlocal obstacle, paused
        if not paused:
            if obstacle is None:
                obstacle = Obstacles.random_select(canvas, nrow, ncol, scale)
                obstacle.activate()
            else:
                obstacle.left()  # Move the obstacle one step left using your updated left() method
                # Check if the obstacle is completely off-screen
                if obstacle.j + obstacle.w <= 0:  # Clear the canvas when the obstacle leaves
                    obstacle = None
                    
        # Schedule the next update after 20 milliseconds (adjust as needed)
        root.after(20, update)

    update()  # Start the update loop


def main():
    """
    Main function to set up and run the obstacle testing interface.
    """
    root = Tk()
    root.title("Obstacle Test")
    nrow = 40
    ncol = 80
    scale = 10
    canvas = Canvas(root, width=ncol*scale, height=nrow*scale, bg="black")
    canvas.pack()

    # Key bindings
    root.bind("1", lambda e: test1(root, canvas, nrow, ncol, scale))
    root.bind("2", lambda e: test2(root, canvas, nrow, ncol, scale))
    root.bind("<d>", lambda e: delete_all(canvas))

    instructions = """
    Press '1' to simulate Dino Run obstacles moving left
    Press '2' to simulate Dino Run obstacles continuously moving left
    Press 'd' to clear the canvas
    """
    print(instructions)
    
    root.mainloop()

if __name__ == "__main__":
    main()