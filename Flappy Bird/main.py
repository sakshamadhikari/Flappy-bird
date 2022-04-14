import random # for generating random numbers
import sys
import pip  # we will use sys.exit to exit the program
import pygame
from pygame.locals import *
from scipy import rand  #basix pygame imports

#global variables for the game

FPS = 32
Screenwidth = 289
Screenheight = 511

screen = pygame.display.set_mode((Screenwidth, Screenheight))
groundY =  Screenheight * 0.8
game_images = {}
game_audio = {}
player = 'Gallery/images/bird.png'
background = 'Gallery/images/background.png'
PIPE = 'Gallery/images/pipe.png'

def welcomescreen():
    #show welcome image on the screen
    playerx = int(Screenwidth/5)
    playery = int((Screenheight - game_images['player'].get_height())/2)
    messagex = int((Screenwidth - game_images['message'].get_width())/2)
    messagey = int(Screenheight * 0.13)
    basex = 0
    while True:
        for event in pygame.event.get():
        #if user clicks on Cross button, close the game
            if event.type == QUIT or (event.type==KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
          # if user press space or up key , start the game
            elif event.type == KEYDOWN and (event.key==K_SPACE or event.key == K_UP):
                return
            else:
                screen.blit(game_images['background'],(0, 0))
                screen.blit(game_images['player'],(playerx, playery)) 
                screen.blit(game_images['message'],(messagex, messagey))
                screen.blit(game_images['base'],(basex, groundY))
                pygame.display.update()
                FPSCLOCK.tick(FPS)
def mainGame():
    score = 0
    playerx = int(Screenwidth/5)
    playery = int(Screenwidth/2)
    basex = 0
     #create two pipe for blitting on screen

    newPipe1 = getRandomPipe()
    newPipe2 = getRandomPipe()
    
    upperPipes = [
        {'x': Screenwidth + 200, 'y': newPipe1[0]['y']},
        {'x': Screenwidth + 200 + (Screenwidth / 2), 'y': newPipe2[0]['y']},
    ]
    # my List of lower pipes
    lowerPipes = [
        {'x': Screenwidth + 200, 'y': newPipe1[1]['y']},
        {'x': Screenwidth + 200 + (Screenwidth / 2), 'y': newPipe2[1]['y']},
    ]

    pipevelX = -4
    
    playerVelY = -9
    PlayerMaxVelY = 10
    PlayerMinVelY = -8
    PlayerAccY= 1

    PlayerFlappAccv = -8 #velocity while flapping
    PlayerFlapped = False # it is only tre when the bird is flapping

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key ==K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if player>0:
                    playerVelY = PlayerFlappAccv
                    PlayerFlapped = True
                    game_audio['wing'].play()
        
        crashTest = isCollide(playerx , playery,upperPipes, lowerPipes) #this func will return true if the player is crashed

        if crashTest:
            return

        PlayerMidPos = playerx + game_images['plaayer'].get_width()/2
        for pipe in upperPipes:
            pipeMidPos = pipe['x'] + game_images['PIPE'][0].get_width()/2
            if pipeMidPos<= PlayerMidPos < pipeMidPos:
                score +=1
                print(f"your score is {score}")
                game_audio['point'].play()

        if playerVelY< PlayerMaxVelY and not PlayerFlapped:
            playerVelY += PlayerAccY

        if PlayerFlapped:
            PlayerFlapped = False
        playerHeight = game_images['player'].get_height()
        playery = playery + min(playerVelY, groundY - playery - playerHeight)

        #move pipes to the left

        for upperPipe , lowerPipe in zip(upperPipes,lowerPipes):
            upperPipes['x'] += pipevelX
            lowerPipes['x'] += pipevelX

        #if the pipe is out of the screen , remove it
        if 0< upperPipes[0]['x']<5:
            newpipe = getRandomPipe()
            upperPipes.append(newpipe[0])
            lowerPipes.append(newpipe[1])
        
        if upperPipes[0]['x'] < -game_images['PIPE'][0].get_width():
            upperPipes.pop(0)
            lowerPipes.pop(0)

        #Lets blits our images
        
        screen.blit(game_images['background'],(0, 0))

        for upperpipe , lowerpipe in zip(upperPipes , lowerPipes):
            screen.blit(game_images['PIPE'][0], (upperPipe['x'], upperPipe['y']))
            screen.blit(game_images['PIPE'][1], (lowerPipe['x'], lowerPipe['y']))

        screen.blit(game_images['base'],(basex, groundY))
        screen.blit(game_images['player'],(playerx, playery))
        myDigits = [int(x) for x in list(str(score))]
        width = 0
        for digit in myDigits:
            width += game_images['numbers'][digit].get_width()
        Xoffset = (Screenwidth - width)/2
        
        for digit in myDigits:
            screen.blit(game_images['numbers'][digit],(Xoffset , Screenheight*0.12))
            Xoffset += game_images['numbers'][digit].get_width()
        
        pygame.display.update()
        FPSCLOCK.tick(FPS)
def isCollide(playerx , playery,upperPipes, lowerPipes):
    if playery > groundY - 25 or playery<0:
        game_audio['hit'].play()
        return True
    
    for pipe in upperPipes:
        pipeHeight = game_images['PIPE'][0].get_height()
        if(playery <pipeHeight + pipe['y'] and abs(playerx - pipe['x'])< game_images['pipe'][0].get_width()):
            game_audio['hit'].play()
            return True
        
    for pipe in lowerPipes:
        if(playery + game_images['player'].get_height()> pipe['y']) and abs(playerx - pipe['x']) < game_images['pipe'][0].get_width():
            game_audio['hit'].play()
            return True


def getRandomPipe():
    """
    generate position of two pipe
    """
    pipeheight = game_images['PIPE'][0].pygame.font.get_height()
    offset = Screenheight/3
    y2 = offset + random.randrange(0,int(Screenheight - game_images['base'].get_height() - 1.2 *offset))
    pipeX = Screenwidth + 10
    y1 = pipeheight - y2 + offset
    pipe = [
        {'x':pipeX, 'y': -y1},
        {'x':pipeX, 'y':y2}
    ]
    return pipe

if __name__== "__main__":
    pygame.init() #initialize all pygames module
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption('Flappy bird by Saksham')
    game_images['numbers'] = (
        pygame.image.load('Gallery/images/0.png').convert_alpha(),
        pygame.image.load('Gallery/images/1.png').convert_alpha(),
        pygame.image.load('Gallery/images/2.png').convert_alpha(),
        pygame.image.load('Gallery/images/3.png').convert_alpha(),
        pygame.image.load('Gallery/images/4.png').convert_alpha(),
        pygame.image.load('Gallery/images/5.png').convert_alpha(),
        pygame.image.load('Gallery/images/6.png').convert_alpha(),
        pygame.image.load('Gallery/images/7.png').convert_alpha(),
        pygame.image.load('Gallery/images/8.png').convert_alpha(),
        pygame.image.load('Gallery/images/9.png').convert_alpha(),
    )

    game_images['message'] = pygame.image.load('Gallery/images/message.png').convert_alpha()
    game_images['base'] = pygame.image.load('Gallery/images/base.png').convert_alpha()
    game_images['pipe'] =(
        pygame.transform.rotate(pygame.image.load(PIPE).convert_alpha(), 180),
        pygame.image.load(PIPE).convert_alpha()
    )
    
    game_audio['die'] = pygame.mixer.Sound('Gallery/audio/die.mp3')
    game_audio['hit'] = pygame.mixer.Sound('Gallery/audio/hit.mp3')
    game_audio['swoosh'] = pygame.mixer.Sound('Gallery/audio/swoosh.mp3')
    game_audio['point'] = pygame.mixer.Sound('Gallery/audio/points.mp3')
    game_audio['wing'] = pygame.mixer.Sound('Gallery/audio/swing.mp3')

    game_audio['background'] = pygame.image.load(background).convert()
    game_audio['player'] = pygame.image.load(background).convert_alpha()

    while True:
        welcomescreen()
        mainGame()