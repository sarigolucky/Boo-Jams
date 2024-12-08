import pygame
import sys
from pygame import mixer

pygame.init()
mixer.init()

#setting images - Stage
stage_img = pygame.image.load("assets/art/stage.png")
stage_img = pygame.transform.scale(stage_img,(1280, 720))
#setting images - Icons
high_icon = pygame.image.load("assets/art/icons/high.png")
mid_icon = pygame.image.load("assets/art/icons/mid.png")
low_icon = pygame.image.load("assets/art/icons/low.png")
drum_icon = pygame.image.load("assets/art/icons/drum.png")
#setting images - ghost
high_ghost_img = [pygame.image.load("assets/art/ghosts/high0001.png"),pygame.image.load("assets/art/ghosts/high0002.png")]
mid_ghost_img = [pygame.image.load("assets/art/ghosts/middle0001.png"), pygame.image.load("assets/art/ghosts/middle0002.png")]
low_ghost_img = [pygame.image.load("assets/art/ghosts/low0001.png"), pygame.image.load("assets/art/ghosts/low0002.png")]
beat_ghost_img = [pygame.image.load("assets/art/ghosts/beat0001.png"),pygame.image.load("assets/art/ghosts/beat0002.png")]



#Setting Screen
pygame.display.set_icon(drum_icon)
screen_width = 1280
screen_height = 720

screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
pygame.display.set_caption("Boo Jams")
run = True


#setting sounds + volume
high_sound = mixer.Sound("assets/music/high.wav")
mid_sound = mixer.Sound("assets/music/middle.wav")
low_sound = mixer.Sound("assets/music/low.wav")
beat_sound = mixer.Sound("assets/music/beat.wav")

high_sound.set_volume(0)
mid_sound.set_volume(0)
low_sound.set_volume(0)
beat_sound.set_volume(0)

high_sound.play(-1)
mid_sound.play(-1)
low_sound.play(-1)
beat_sound.play(-1)

class Ghost():
    def __init__(self, x, y, img, audioname):
        self.img = img
        self.img = [pygame.transform.scale(frame, (300, 300)) for frame in img]
        self.rect = self.img[0].get_rect()
        self.rect.topleft = (x,y)
        #animation stuff
        self.current_frame = 0
        self.animation_time = 500
        self.last_update = pygame.time.get_ticks()
    def animate(self):
        now = pygame.time.get_ticks()

        if (now - self.last_update >= self.animation_time):
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.img)

    def sing(self, audioname,level):
        audioname.set_volume(level)

    def draw(self):
        screen.blit(self.img[self.current_frame], (self.rect.x, self.rect.y))
        return self


#class Ghost()
high_ghost = Ghost(125, 250, high_ghost_img, high_sound)
mid_ghost = Ghost(350, 225, mid_ghost_img, mid_sound)
low_ghost = Ghost(600, 270, low_ghost_img, low_sound)
beat_ghost = Ghost(850, 270, beat_ghost_img, beat_sound)

class Button():
    def __init__(self, x, y, img):
        self.img = img
        self.img = pygame.transform.scale(img, (60,60))
        self.rect = self.img.get_rect()
        self.rect.topleft = (x,y)
        self.clicked = False
        self.toggle = "off"
    def draw(self):
        #get mouse
        pos = pygame.mouse.get_pos()
        #check mouse over and clicked
        if self.rect.collidepoint(pos):
            if (pygame.mouse.get_pressed()[0] == 1 and not self.clicked):
                self.clicked = True
                #toggling
                if self.toggle == "off":
                    self.toggle = "on"
                    print("Turned on!")
                else:
                    self.toggle = "off"
                    print("Turned off!")
        if (pygame.mouse.get_pressed()[0] == 0):
            self.clicked = False

        screen.blit(self.img, (self.rect.x, self.rect.y))


#buttons
high_button = Button(1175,100,high_icon)
mid_button = Button(1175,200,mid_icon)
low_button = Button(1175,300,low_icon)
drum_button = Button(1175, 400, drum_icon)

#menus
def draw_start_menu():
    screen.fill((0,0,0))
    tiny_font = pygame.font.SysFont("Futura", 20)
    body_font = pygame.font.SysFont("Futura", 40)
    title_font = pygame.font.SysFont("Chalkboard SE", 140)


    title_message =title_font.render("BOO JAMS", True, (255,255,255))
    start_message = body_font.render("Press Space to Start!", True, (255,255,255))
    credit_message = tiny_font.render("Created by Sarika. Alpha Build", True, (255,255,255))
    
    screen.blit(title_message, (screen_width/2 - title_message.get_width()/2, screen_height/2 + title_message.get_height()/2  - 275))
    screen.blit(start_message, (screen_width/2 - start_message.get_width()/2, screen_height/2 + start_message.get_height()/2))
    screen.blit(credit_message, (screen_width/2 - credit_message.get_width()/2, screen_height/2 + credit_message.get_height()/2  + 100))
    #TODO: change "screen_width" to get the current screen with
    pygame.display.update()

def draw_game():
    screen.blit(stage_img,(0,0)) 
    high_button.draw()
    mid_button.draw()
    low_button.draw()
    drum_button.draw()

    #Checking if the buttons were pressed
    if (high_button.toggle == "on"):
        high_ghost.draw().animate()
        high_ghost.sing(high_sound,0.1)
    else:
        high_sound.set_volume(0)

    if (mid_button.toggle == "on"):
        mid_ghost.draw().animate()
        mid_ghost.sing(mid_sound, 0.1)
    else:
        mid_sound.set_volume(0)

    if (low_button.toggle == "on"):
        low_ghost.draw().animate()
        low_ghost.sing(low_sound, 0.15)
    else:
        low_sound.set_volume(0)

    if (drum_button.toggle == "on"):
        beat_ghost.draw().animate()
        beat_ghost.sing(beat_sound, 0.1)
    else:
        beat_sound.set_volume(0)

    pygame.display.update()



game_state = "start_menu"
#the game itself!
while run:
    for event in pygame.event.get():
        if (event.type == pygame.KEYDOWN):
            if (event.key == pygame.K_SPACE):
                game_state = "game"
            if (event.key == pygame.K_ESCAPE):
                game_state = "start_menu"
    #Start Menu
    if (game_state == "start_menu"):
        draw_start_menu()

    if (game_state == "game"):
        draw_game()

    if (event.type == pygame.QUIT):
        run = False
    pygame.display.flip()

pygame.quit()