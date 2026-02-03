from tkinter import *
import time, random
from Obstacles import Obstacles
from Dino import Dino
import pygame.mixer



class DinoGame:
    
    #-------------------------------------------------------------------------
    # Initialization and Setup
    #-------------------------------------------------------------------------
    
    def __init__(self, root, nrow, ncol, scale):
        self.root = root
        self.nrow = nrow 
        self.ncol = ncol
        self.scale = scale
        self.__game_over = False
        self.__pause = False
        self.__started = False
        self.__next_spawn_time = time.time() + random.randint(1,3)  #time.time() keeps track of the time throughout the game
        self.__score = 0
        self.__pause_time = 0
        self.canv = Canvas(root, width=ncol*scale,height=nrow*scale,bg="black")
        self.canv.pack()
        self.obstacles=[]
        self.dino = Dino(self.canv,nrow,ncol//9,scale)
        self.dino.activate()
        self.__spawn_time = 3
        self.character_message = self.canv.create_text(self.ncol*self.scale//2,self.nrow*self.scale//7,text="Press J for Dino and K for the Beast",font=("Arial",24),fill="red")#creates text on the canvas
        self.start_message = self.canv.create_text(self.ncol*self.scale//2,self.nrow*self.scale//2,text="Press S to Start",font=("Arial",24),fill="red")
        self.pause_message = self.canv.create_text(self.ncol*self.scale//2,self.nrow*self.scale//3,text="Press P to pause",font=("Arial",24),fill="red")
        self.jump_message = self.canv.create_text(self.ncol*self.scale//2,self.nrow*self.scale//4,text="Press Space to jump",font=("Arial",24),fill="red")
        self.restart_message = self.canv.create_text(self.ncol*self.scale//2,self.nrow*self.scale//5,text="Press R to restart",font=("Arial",24),fill="red")
            


        pygame.mixer.init()#initializes special function from pygame.mixer that allows you to add sounds
        self.jump_sound = pygame.mixer.Sound(r"C:\Users\donno\Downloads\ECE122_Project3_updated\ECE122_Project3\Code Template\jump.wav")#calls the souhnd file from my files
        self.Game_Over_sound = pygame.mixer.Sound(r"C:\Users\donno\Downloads\ECE122_Project3_updated\ECE122_Project3\Code Template\GameOver.wav")
        self.clear_obstacle_sound = pygame.mixer.Sound(r"C:\Users\donno\Downloads\ECE122_Project3_updated\ECE122_Project3\Code Template\dinoroar.wav")
        self.root.bind("<r>", lambda e: self.game_restart())  #binds key r to restart the game
        
        

        
        
        
        
    # Remove the pass statement and implement the __init__ method as described in the PDF.
    
    #-------------------------------------------------------------------------
    # Game State Methods
    #-------------------------------------------------------------------------
    
    def is_game_over(self): #this is part of my getter/setter method 
        return self.__game_over
    # Remove the pass statement and implement the is_game_over method as described in the PDF.
    
    def set_game_over(self, value):
        self.__game_over = value
    # Remove the pass statement and implement the set_game_over method as described in the PDF.
    
    def is_pause(self):
        return self.__pause
    # Remove the pass statement and implement the is_pause method as described in the PDF.
    
    def set_pause(self, value):
        self.__pause = value
    # Remove the pass statement and implement the set_pause method as described in the PDF.
    
    def is_started(self):
        return self.__started
    # Remove the pass statement and implement the is_started method as described in the PDF.
    
    def set_started(self, value):
        self.__started = value
    # Remove the pass statement and implement the set_started method as described in the PDF.
    
    def get_next_spawn_time(self):
        return self.__next_spawn_time
    # Remove the pass statement and implement the get_next_spawn_time method as described in the PDF.
    
    def set_next_spawn_time(self, value):
        self.__next_spawn_time = value
    # Remove the pass statement and implement the set_next_spawn_time method as described in the PDF.

    def get_score(self):
        return self.__score
    # Remove the pass statement and implement the get_score method as described in the PDF.
    
    def set_score(self, value):
        self.__score = value
    # Remove the pass statement and implement the set_score method as described in the PDF.

    def get_pause_time(self):
        return self.__pause_time
    # Remove the pass statement and implement the get_pause_time method as described in the PDF.
    
    def set_pause_time(self, value):
        self.__pause_time = value
    # Remove the pass statement and implement the set_pause_time method as described in the PDF.
    
    #-------------------------------------------------------------------------
    # Game Logic
    #-------------------------------------------------------------------------
    
    def start_game(self):
        """
        starts the game by setting the flag to true and keeps track of time for the score
        deletes all starting text
        """
        if not self.is_started():
            self.__started = True
            self.__next_spawn_time = time.time() + random.randint(1,3)
            self.__start_time=time.time()
            self.canv.delete(self.start_message)
            self.canv.delete(self.restart_message)
            self.canv.delete(self.pause_message)
            self.canv.delete(self.jump_message)
            self.canv.delete(self.character_message)
            self.score_message=self.canv.create_text(self.ncol*self.scale//17,self.nrow*self.scale//10,text=f"Score:{int(self.__score)}",font=("Arial",15),fill="red")
            pygame.mixer.music.load(r"C:\Users\donno\Downloads\ECE122_Project3_updated\ECE122_Project3\Code Template\start.wav")  #plays the music when our bount key S is pressed
            pygame.mixer.music.play(-1) #this loops the the sound
        
           
            
            
    # Remove the pass statement and implement the start_game method as described in the PDF.

    
    def next(self):# the motherboard this constantly updates every important funtion as the game runs
    
       current_time = time.time() #time.time() is a function that keeps track of the time throughout the game. It is special to tkner

       for obstacle in self.obstacles[:]:
           obstacle.left()

           if not hasattr(obstacle, 'sound_played'):#hassattr checks to see if attributes are present and if they are it returns true
            obstacle.sound_played = False

           if not obstacle.sound_played:
            for obs_pixel in obstacle.Pixels:
                for dino_pixel in self.dino.Pixels:
                    if obs_pixel.j == dino_pixel.j:
                        self.clear_obstacle_sound.play() #check to see if the dino has pixels in the same colomn as the obstacle, plays clear sound if true
                        obstacle.sound_played = True
                        break

       decrease = current_time - self.__start_time
       speed = min(1,1 + decrease*0.1)#the speed of the objects
       self.current_speed=speed
       interval = random.uniform(1,max(3,self.__spawn_time-decrease*2))#this makes the game get progressively faster 

       if current_time> self.get_next_spawn_time():# this chunk controls all the movements of the obstacles
            knobstacle = Obstacles.random_select(self.canv,self.nrow*1.24,self.ncol,self.scale)
            knobstacle.speed = speed #modify the speed
            knobstacle.activate()
            self.obstacles.append(knobstacle)
            self.set_next_spawn_time(current_time+random.uniform(1,interval))#randomizes the space between obstacles

       if self.check_collision():#this looks at our checkcollision function below and actually allows us to use it 
           self.set_game_over(True)
           self.start_message = self.canv.create_text(self.ncol*self.scale//2,self.nrow*self.scale//2,text="Game Over",font=("Arial",24),fill="red")
           pygame.mixer.music.stop()
           self.Game_Over_sound.play()
       self.update_survival_score()#keeps updating the new score so it runs with the time accumilated
        
        
        
            #create game over text

        

    # Possibly spawn obstacles based on timing
    # self.spawn_obstacle_if_needed()

    # Remove the pass statement and implement the next method as described in the PDF.

    
    def check_collision(self):# checks if the pixels of the obstacles and the pixels of the characters overlap which allows you to call it in the next() function
       for obstacle in self.obstacles:
           for obs_pixel in obstacle.Pixels:
               for dino_pixel in self.dino.Pixels:
                   if obs_pixel.i == dino_pixel.i and obs_pixel.j == dino_pixel.j:
                       return True
       return False
    


    # Remove the pass statement and implement the check_collision method as described in the PDF.
    

    def jump(self):#allows the characters to jump if the game is not over or paused
        if not self.is_game_over() and not self.is_pause():
            self.dino.jump()
            self.jump_sound.play()#plays the jump soundeffect everytime space is pressed
            
    # Remove the pass statement and implement the jump method as described in the PDF.


    def pause(self):#allows you to pause the game 
        if self.is_started():
            current_time = time.time()
            if self.__pause:
                self.__pause = False
                self.__pause_time += current_time - self.pause_start
            else:
             self.__pause = True
             self.pause_start = current_time
        
    # Remove the pass statement and implement the pause method as described in the PDF.

    def update_survival_score(self):#actively updates the score and keeps track of time 
        if self.__pause == False:
            current_time = time.time()
            self.__score =(current_time-self.__start_time-self.__pause_time)*self.current_speed
            self.canv.itemconfigure(self.score_message,text=f"Score: {int(self.__score)}")
        
    def game_restart(self):#allows you to restart the game when r is pressed
        self.canv.delete("all")
        self.__game_over = False
        self.__pause = False
        self.__started = False
        self.__next_spawn_time = time.time() + random.randint(1, 3)
        self.__score = 0
        self.__pause_time = 0

        self.obstacles=[]
        self.dino = Dino(self.canv, self.nrow, self.ncol // 9, self.scale)
        self.dino.activate()# activates the dino after the restart
        self.__score = 0#resets score ecery instance after the restart

        self.start_message = self.canv.create_text(self.ncol*self.scale//2,self.nrow*self.scale//2,text="Press S to Start",font=("Arial",24),fill="red")
        self.root.after(10, update_obstacles,self,self.root)#updates the state of the obstacles every 10 milliseconds because the main function doesnt update the game after the game is over so we have to do it manually
    # Remove the pass statement and implement the update_survival_score method as described in the PDF.


#=============================================================================
# Main Game Runner - DO NOT MODIFY
#=============================================================================

def update_obstacles(game, root):
    if not game.is_pause() and (game.is_started() or game.is_game_over()):
        game.next()  # Unified method with feature flag
            
        if game.is_game_over():
            return  # Don't schedule another update if game is over
    
    # Schedule next update (50ms = 20 FPS)
    root.after(50, update_obstacles, game, root)

def main():
    """
    Main function to set up and run the game.
    """
    # Create the main window
    root = Tk()
    root.title("Dino Run Game")
    
    # Create the game instance
    game = DinoGame(root, nrow=80, ncol=160, scale=10)

    # Set up key bindings
    root.bind("<space>", lambda e: game.jump())
    root.bind("<p>", lambda e: game.pause())
    root.bind("<s>", lambda e: game.start_game())
    # Start the game loop
    root.after(10, update_obstacles, game, root)
    
    # Start Tkinter event loop
    root.mainloop()

if __name__ == "__main__":
    main()