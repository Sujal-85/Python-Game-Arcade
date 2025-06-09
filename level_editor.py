import pygame
import button
import csv
import messagebox
# import pickle

pygame.init()

clock =pygame.time.Clock()
FPS = 60

width = 800
height = 640

Lower_margin = 100
side_margin = 300

screen = pygame.display.set_mode((width + side_margin, height + Lower_margin))
pygame.display.set_caption('Level Editor')

rows = 16
columns = 150
tile_size = height // rows
tile_types = 22
current_tile = 0
level = 0

scroll_left = False
scroll_right = False
scroll = 0
scroll_speed = 1




pine1_img = pygame.image.load('images/pine1.png').convert_alpha()
pine2_img = pygame.image.load('images/pine2.png').convert_alpha()
mountain_img = pygame.image.load('images/mountain.png').convert_alpha()
sky_img = pygame.image.load('images/sky_cloud.png').convert_alpha()

img_list = []
for x in range(tile_types):
    img = pygame.image.load(f'images/tiles/{x}.png')
    img = pygame.transform.scale(img, (tile_size, tile_size))
    img_list.append(img)
save_img = pygame.image.load('images/save_btn.png').convert_alpha()
load_img = pygame.image.load('images/load_btn.png').convert_alpha()


green = (144, 201, 120)
red = (200, 25, 25)
white = (255, 255, 255)
black = (0, 0, 0)

font = pygame.font.SysFont('Futura', 30)

world_data = []

for row in range(rows):
    r = [-1] * columns
    world_data.append(r)

for tile in range(0, columns):
    world_data[rows -1][tile] = 0

def draw_text(text,  font , text_col, x, y):
     img = font.render(text, True, text_col)
     screen.blit(img , (x,y))




def draw_bg():
    screen.fill(green)
    Width1 = sky_img.get_width()
    for x in range(4):
        screen.blit(sky_img, ((x * Width1) - scroll * 0.5, 0))
        screen.blit(mountain_img, ((x * Width1) - scroll * 0.6, height - mountain_img.get_height() - 300))
        screen.blit(pine1_img, ((x * Width1) - scroll * 0.7, height - pine1_img.get_height() - 150))
        screen.blit(pine2_img, ((x * Width1) - scroll * 0.8, height - pine2_img.get_height()))

def draw_grid():
    for c in range(columns +1):
        pygame.draw.line(screen, white, (c * tile_size - scroll, 0), (c * tile_size - scroll, height))

    for c in range(rows +1):
        pygame.draw.line(screen, white, (0, c * tile_size), (width, c * tile_size))


def draw_world():
    for y ,row in enumerate(world_data):
        for x, tile in enumerate(row):
            if tile >= 0:
                screen.blit(img_list[tile], (x * tile_size - scroll, y * tile_size))

save_button = button.Button(width // 2, height + Lower_margin -50 ,save_img, 1)
load_button = button.Button(width // 2+200, height + Lower_margin -50 ,load_img, 1)


button_list = []
button_col = 0
button_row = 0
for i in range(len(img_list)):
    tile_button = button.Button(width + (75 * button_col) + 50, 75 * button_row + 50, img_list[i],  1)
    button_list.append(tile_button)
    button_col += 1
    if button_col == 3:
        button_row += 1
        button_col = 0


run = True

while run:
     clock.tick(FPS)

     draw_bg()
     draw_grid()
     draw_world()
     draw_text(f'Level : {level}', font, black, 10, height + Lower_margin - 90)
     draw_text('Press Up or Down to Change level', font, black, 10, height + Lower_margin - 60)

     if save_button.draw(screen):
         # pickle_out = open(f"level{level}_data.csv", 'wb')
         # pickle.dump(world_data, pickle_out)
         # pickle_out.close()

         with open(f"csv files/level{level}_data.csv", 'w', newline='') as csvfile:
             writer = csv.writer(csvfile, delimiter=',')
             messagebox.showinfo("Success", "Changes are saved Successfully!")

         #
             for row in world_data:
                 writer.writerow(row)

     if load_button.draw(screen):
         scroll = 0
         with open(f"csv files/level{level}_data.csv", newline='') as csvfile:
             reader = csv.reader(csvfile, delimiter=',')
             # messagebox.showinfo("Success", f"Level {level} is Loaded Successfully! ")

             for x, row in enumerate(reader):
                 for y, tile in enumerate(row):
                     world_data[x][y] = int(tile)






     pygame.draw.rect(screen , white, (width, 0, side_margin, height))

     button_count = 0
     for button_count, i in enumerate(button_list):
         if i.draw(screen):
             current_tile = button_count

     pygame.draw.rect(screen, red, button_list[current_tile].rect, 3)

     if scroll_left and scroll > 0:
         scroll -= 5 * scroll_speed
     if scroll_right and scroll < (columns * tile_size) - width:
         scroll += 5 * scroll_speed

     pos = pygame.mouse.get_pos()
     x = (pos[0] + scroll) // tile_size
     y = pos[1] // tile_size

     if pos[0] < width and pos[1] < height:
         if pygame.mouse.get_pressed()[0] == 1:
             if world_data[y][x] != current_tile:
                 world_data[y][x] = current_tile
         if pygame.mouse.get_pressed()[2] == 1:
             world_data[y][x] = -1

     for event in pygame.event.get():
         if event.type == pygame.QUIT:
             run = False
         if event.type == pygame.KEYDOWN:
             if event.key == pygame.K_UP:
                 level += 1
             if event.key == pygame.K_DOWN and level > 0:
                 level -= 1
             if event.key == pygame.K_LEFT:
                 scroll_left = True
             if  event.key == pygame.K_RIGHT:
                 scroll_right = True
             if event.key == pygame.K_RSHIFT:
                 scroll_speed = 5


         if event.type == pygame.KEYUP:
             if event.key == pygame.K_LEFT:
                 scroll_left = False
             if event.key == pygame.K_RIGHT:
                 scroll_right = False
             if event.key == pygame.K_RSHIFT:
                 scroll_speed = 1
     pygame.display.update()

pygame.quit()

    