import pygame
import pandas as pd
from random import choice

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BUTTON_WIDTH = 200
BUTTON_HEIGHT = 100


# Load images
logo_image_path = "./sprites/start/title.png" 
button_image_path = './sprites/Start/btnstart.png'  

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Mushroom Kombat")
pygame.display.set_icon(pygame.image.load('./sprites/icon.ico'))


# Load images
logo_image = pygame.image.load(logo_image_path)
button_image = pygame.image.load(button_image_path)

# Scale images (optional, to fit the screen better)
logo_image = pygame.transform.scale(logo_image, (400, 200))
button_image = pygame.transform.scale(button_image, (BUTTON_WIDTH, BUTTON_HEIGHT))

# Get rects for positioning
logo_rect = logo_image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100))
button_rect = button_image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100))

# Main game loop
running = True
start_pressed = False
fill = pygame.image.load("./sprites/Start/bglarge.png")

pygame.mixer.init()
pygame.mixer.music.load("./sounds/track.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(loops=-1)

class Player():
    def __init__(self, player_sprite_path, name, health, attak) -> None:

        self.player_sprite_path = player_sprite_path
        self.player_name = name
        self.health = health
        self.attk = attak

        self.player_sprite = None
        self.player_rect = None
        
        #Name
        font = pygame.font.Font('freesansbold.ttf', 32)
        self.text = font.render(f'{name}', True, (0,235,0))
        self.textRect = self.text.get_rect()        

        #Life
        self.text_life = font.render(f'{health}', True, (0,0,150))
        self.textRect_life = self.text_life.get_rect()        



    def load_player_sprite(self, position):
        self.player_sprite = pygame.image.load(self.player_sprite_path)
        self.player_sprite = pygame.transform.scale(self.player_sprite, (100, 100))
        if position == "left":
            self.player_rect = self.player_sprite.get_rect(center=(800 // 4, 600 // 2))
            self.textRect.center = (800 // 4, 600 // 2.8)  
            self.textRect_life.center = (800 //4, 550)
        else:
            self.player_sprite = pygame.transform.flip(self.player_sprite, True, False)
            self.player_rect = self.player_sprite.get_rect(center=(800 // 1.47, 600 // 2))
            self.textRect.center = (800 // 1.47, 600 // 2.8)  
            self.textRect_life.center = (800 // 1.47, 550)

    def update_life(self, pos):

        screen.blit(fill, (0,0))
        player.display_sprites()
        oponent.display_sprites()
        pygame.display.update()
        font = pygame.font.Font('freesansbold.ttf', 32)
        self.text_life = font.render(f'{self.health}', True, (0,0,150))
        self.textRect_life = self.text_life.get_rect() 
        if pos == "left":
            self.textRect_life.center = (800 //4, 550)
        else:
            self.textRect_life.center = (800 // 1.47, 550)

        pygame.display.update()



        screen.blit(self.text_life, self.textRect_life)

    def display_sprites(self):
        screen.blit(self.text_life, self.textRect_life)
        screen.blit(self.text, self.textRect)
        screen.blit(self.player_sprite, self.player_rect)

class Battle(Player):
    def __init__(self, player, op):
        self.player = player
        self.op = op

    def attack(self, turn):
        font = pygame.font.Font('freesansbold.ttf', 32)
        if turn == 'player':
            p_att = choice(self.player.attk)
            self.op.health -= p_att
            self.turn = 'opponent'
            text_att = font.render(f'Att: {p_att}', True, (200,0,0))
            textRect_att = text_att.get_rect()  
            textRect_att.center = (200, 400)
        elif turn == 'opponent':
            op_att = choice(self.op.attk)
            self.player.health -= op_att
            self.turn = 'player'
            text_att = font.render(f'Att: {op_att}', True, (200,0,0))
            textRect_att = text_att.get_rect()  
            textRect_att.center = (550, 400)

        screen.blit(text_att, textRect_att)
        pygame.display.update()
        pygame.time.wait(500)
    

    def check_winner(self):
        if self.player.health <= 0:
            return 'opponent'
        elif self.op.health <= 0:
            return 'player'
        return None


def load_data(excel_file_path):
    return pd.read_excel(excel_file_path)
selected = list(range(6))

data = load_data("./data/char_data.xlsx")

def selected_player(selected):
    return choice(selected)

sel_pl = selected_player(selected)
selected.remove(sel_pl)
sel_op = selected_player(selected)
selected.remove(sel_op)

def load_attk(data, sel):
    attk = []
    for i in range(4):
        attk.append(data[f"Att{i + 1}"][sel])
    return attk

def show_winner(winner):
    font = pygame.font.Font('freesansbold.ttf', 32)
    text_win = font.render(f'{winner} WIN !!!', True, (200,0,0))
    textRect_winner = text_win.get_rect() 
    textRect_winner.center = (400, 100)
    screen.blit(text_win, textRect_winner)
    pygame.display.update()

iter = 1

while running:


    player = Player(f'./sprites/players/CHAR_{sel_pl + 1}.png', data["Name"][sel_pl], data["Health"][sel_pl], load_attk(data, sel_pl))
    oponent = Player(f'./sprites/players/CHAR_{sel_op + 1}.png', data["Name"][sel_op], data["Health"][sel_op], load_attk(data, sel_op))
    

    player.load_player_sprite("left")
    oponent.load_player_sprite("right")    

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if button_rect.collidepoint(event.pos):
                start_pressed = True

    # Fill the screen with a white background
    screen.blit(fill,(0,0))


    if not start_pressed:
        screen.blit(logo_image, logo_rect)
        screen.blit(button_image, button_rect)
    else:
        # Start the main game or next screen here
        # For now, we'll just fill the screen with a different color to indicate the change
        player.display_sprites()
        oponent.display_sprites()
        pygame.display.update()
        pygame.time.wait(100)

        bat = Battle(player, oponent)

        while not bat.check_winner():
            bat.attack('player')
            oponent.update_life("right")
            pygame.time.wait(600)
            bat.attack("opponent")
            player.update_life("left")
            pygame.time.wait(600)

        
        if bat.check_winner() == "opponent":
            sel_pl = selected_player(selected)
            show_winner(oponent.player_name)
            if iter >= 2 <= 5:
                selected.remove(sel_pl)
            player = Player(f'./sprites/players/CHAR_{sel_pl + 1}.png', data["Name"][sel_pl], data["Health"][sel_pl], load_attk(data, sel_pl))
        elif bat.check_winner() == 'player':
            show_winner(player.player_name)
            sel_op = selected_player(selected)
            if iter >= 2 <= 5:
                selected.remove(sel_op)
            oponent = Player(f'./sprites/players/CHAR_{sel_op + 1}.png', data["Name"][sel_op], data["Health"][sel_op], load_attk(data, sel_op))
        pygame.time.wait(2000)

        if len(selected) == 0:
            screen.blit(fill, (0,0))    
            font = pygame.font.Font('freesansbold.ttf', 32)
            for i in range(10):
                    text_exit = font.render(f'EXIT: {abs(i - 10)} ', True, (200,0,0))
                    textRect_exit = text_exit.get_rect() 
                    textRect_exit.center = (400, 400)
                    screen.blit(text_exit, textRect_exit)
                    pygame.display.update()
                    pygame.time.wait(1000)
                    screen.blit(fill, (0,0))
            pygame.quit()

        iter += 1

    pygame.time.Clock().tick(60)
    pygame.display.update()
    pygame.display.flip()

