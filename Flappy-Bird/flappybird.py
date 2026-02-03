import pygame
from sys import exit 
import random
# Main
width = 500
height = 750
pygame.init()
Background = pygame.image.load("Flappy Bird Background.jpg")
window = pygame.display.set_mode((width,height))
pygame.display.set_caption("Flappy Bird")
clock = pygame.time.Clock() 
pipe_timer = pygame.USEREVENT + 0
pygame.time.set_timer(pipe_timer,1000)

#Bird
bxpos = width/16
bypos = height/4
birdwidth = 50
birdheight = 50 
class Bird(pygame.Rect):
    def __init__(self, picture):
        pygame.Rect.__init__(self, bxpos, bypos, birdwidth, birdheight)
        self.pic = picture
birdimg = pygame.image.load("flappy-bird.png")
birdimg = pygame.transform.scale(birdimg,(birdwidth,birdheight))

#Pipes
pxpos = width
pypos = 0
pipewidth = 64
pipeheight = 512

class Pipes(pygame.Rect):
    def __init__(self, Pictures):
        pygame.Rect.__init__(self, pxpos,pypos,pipewidth,pipeheight)
        self.pictures = Pictures
        self.passed = False
Tpipe = pygame.image.load("toppipe.png")
Tpipe = pygame.transform.scale(Tpipe,(pipewidth,pipeheight))
Bpipe = pygame.image.load("botpipe.png")
Bpipe = pygame.transform.scale(Bpipe,(pipewidth,pipeheight))



#Logic
bird = Bird(birdimg)
pipes = []
velocity_x = -3
bird_Vel = 0
grav = 0.3
jump = -6
score = 0
font = pygame.font.Font(None,48)
#paste pics onto canvas
def screen():
    window.blit(Background,(0,0))
    window.blit(bird.pic,bird)
    for pipe in pipes:
        window.blit(pipe.pictures,pipe)
    
   #create pipes 
def create_pipes():
    random_pos_y = pypos - pipeheight/4 - random.random()*(pipeheight/2)
    space = height/4
    top_pipe = Pipes(Tpipe)
    top_pipe.y = random_pos_y
    pipes.append(top_pipe)

    bot_pipe = Pipes(Bpipe)
    bot_pipe.y = top_pipe.y + top_pipe.height + space
    pipes.append(bot_pipe)
    

def move():
    for pipe in pipes:
        pipe.x += velocity_x

def flap():
   global bird_Vel 
   bird_Vel= jump

def fall():
    global bird_Vel
    bird_Vel += grav
    bird.y += bird_Vel

def Isgameover():
    if bird.top <= 0 or bird.bottom>=height:
        pygame.quit()
        exit()
    for pipe in pipes:
        if bird.colliderect(pipe):
            pygame.quit()
            exit()
def scorecount():
    global score
    for pipe in pipes:
        if pipe.pictures == Bpipe and not pipe.passed:
            if pipe.right < bird.left:
                pipe.passed = True
                score+=1

def draw_score():
    score_surf = font.render(str(score), True, (255, 255, 255))
    score_rect = score_surf.get_rect(center=(width // 2, 50))
    window.blit(score_surf, score_rect)

#checks
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        
        if event.type == pipe_timer:
            create_pipes()
        if event.type == pygame.KEYDOWN:
            flap()
    move()
    fall() 
    scorecount() 
    Isgameover()
    screen()
    draw_score()
    pygame.display.update()
    clock.tick(60)
   


