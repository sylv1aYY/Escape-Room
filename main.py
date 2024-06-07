
from pygame import*
init()
import random

# colors
RED = (255, 0, 0)
WHITE=(255,255,255)
GREEN = (0,255,0)
BLACK = (0,0,0)
BLUE = (0,0,255)
CYAN = (0,150,150)
DARKBLUE = (15, 66, 148)
PINK = (255, 97, 158)
YELLOW = (255, 236, 61)
SKYBLUE = (71, 182, 255)

# background setting
SIZE = (800, 600)
screen = display.set_mode(SIZE)
background=image.load("escape room 1.jpg")
background = transform.scale(background,(800,600))
# some default settings
flowerX = 205
flowerY = 338
waterpotX = 341
waterpotY = 335
girlX = 40
girlY = 320
rotation = 0
direction = 1
coinX = random.randint(10,740)
coinY = 10
coinX1 = random.randint(10,70)
# rects for checking collision
magazineRect = Rect(35,404,78,34)
pictureRect = Rect(255,282,29,21)
booksRect = Rect(604,302,49,39)
vaseRect = Rect(171,380,50,45)
waterpotimageRect = Rect(waterpotX,waterpotY,80,80)
flowerimageRect = Rect(flowerX,flowerY,70,70)

# images
parkingimage = image.load("parking number.JPG")
parkingimage = transform.scale(parkingimage,(200,80))
flowerimage = image.load("flower.PNG")
flowerimage = transform.scale(flowerimage,(70,70))
waterpotimage = image.load("water pot.PNG")
waterpotimage = transform.scale(waterpotimage,(80,80))
spritesheet = image.load("dance.png") 
spritesheet = transform.scale(spritesheet,(1200,1500))
spritesheet1 = image.load("dance2.png")
spritesheet1 = transform.scale(spritesheet1,(1200,1500))
# images for inventory
magazineimage = image.load("magazine.PNG")
magazineimage = transform.scale(magazineimage,(80,80))
booksimage = image.load("books.PNG")
booksimage = transform.scale(booksimage,(80,80))
pictureimage = image.load("picture.PNG")
pictureimage = transform.scale(pictureimage,(80,80))
vaseimage = image.load("vase.PNG")
vaseimage = transform.scale(vaseimage,(80,80))

coinimage = image.load("coin.png")
coinimage = transform.scale(coinimage,(60,60))
# images for "click" effect
clickpictureimage = image.load("picture(fx).PNG")
clickpictureimage = transform.scale(clickpictureimage,(40,40))
clickvaseimage = image.load("vase(fx).PNG")
clickvaseimage = transform.scale(clickvaseimage,(55,55))
clickbooksimage = image.load("books(fx).PNG")
clickbooksimage = transform.scale(clickbooksimage,(43,43))
# boolean variables for interactions
running = True
CLICKMAGAZINE = False
CLICKBOOKS = False
CLICKPICTURE = False
CLICKVASE = False
DRAGFLOWER = False
DRAGPOT = False
GIVEHINT = False
TEXTIN = False
CONGRATS = False
# boolean variables for inventory
FINDMAGAZINE = False
FINDBOOKS = False
FINDPICTURE = False
FINDHINT = False
# boolean variables for "click" effect
ADDPICTURE = False
ADDVASE = False
ADDBOOKS = False

# read password in password file 
passwordFile = open("exit password.txt","r")
password = passwordFile.readline()
passwordFile.close()

# string input
text = ""
result = ""




myClock = time.Clock()
framecount = 0

# from introduction to spritesheets lesson
def load_sprites(spritesheet, DIMw,DIMh,offset):
    sprites = []
    W = spritesheet.get_width()//DIMw  #frame width
    H = spritesheet.get_height()//DIMh  #frame height
    for i in range(DIMw*DIMh-offset):

        x = i%DIMw*W    #x coordinate of frame
        y = i//DIMw*H   #y coordinate of frame
        sprites.append(spritesheet.subsurface(Rect(x, y, W, H))) 
        #cuts out the frame onto a subsurface then added to list
    return sprites  #sends the list back to the main program
sprites = load_sprites(spritesheet,8,10,0)
sprites1 = load_sprites(spritesheet1,8,10,0)

# from pygame string input lesson
def popup_drawer(screen,textRect,message,tColour,bColour,size):
    """
    function draws a dialogue box

    :param screen: screen to draw to
    :param textRect: rect object to display text in
    :param message: string containing message
    :param tColour: text foreground colour
    :param bColour: dialogue box background colour
    :param size: font size
    """
    fonts = font.SysFont("New Times Roman",size)
    
    draw.rect(screen,bColour,textRect)
    
    linecount = 0
    linelength = 0
    padding = 5
    lines = message.split("\n")
    
    for line in lines:
        words = line.split()
        for word in words:
            forDisplay = fonts.render(word+" ",True,tColour,bColour)
            wordRect = forDisplay.get_rect()
            if padding + linelength + wordRect.width > textRect.width:
                linecount += 1.5
                linelength = 0
            x = textRect.left + padding + linelength
            y = textRect.top + padding + linecount*wordRect.height
            wordRect.topleft=(x,y)
            screen.blit(forDisplay,wordRect)
            linelength += wordRect.width
        linecount += 1.5
        linelength = 0

def make_rotation(screen):
  global rotation,direction,magazineimage
  magazineimage1 = transform.scale(magazineimage,(90,90))
  rotated_image = transform.rotate(magazineimage1,rotation)
  image_rect = rotated_image.get_rect(center = (75,406))
  rotation += direction
  if rotation >= 5 or rotation <= -5:  #reverse rotation
    direction *= -1

  screen.blit(rotated_image,image_rect)
  

def interactions(screen):
  global flowerX, flowerY, waterpotX, waterpotY,text,result,girlX,girlY,coinX,coinY,coinX1
  # click magazine
  message1 = "check out the line of brown books on the white shelf.\nClick the same item to close."
  if CLICKMAGAZINE == True:
    popup_drawer(screen,Rect(80,350,150,100),message1,BLACK,WHITE,20)
  # line of yellow books
  if CLICKBOOKS == True:
    draw.rect(screen, WHITE,(480,343,200,150))
    for i in range(490,640,60):
      for j in range(350,460,35):     
        draw.rect(screen,DARKBLUE,(i,j,60,35),3)
    draw.rect(screen,YELLOW,(565,433,30,20))
  # picture on the dark blue shelf
  if CLICKPICTURE == True:
    
    message2 = "Enter your answer. Press return when you are done.\nYou typed: %s%s"%(text,result)
    popup_drawer(screen,Rect(233,208,200,80),message2,BLACK,WHITE,23)
    screen.blit(parkingimage,(233,305,200,80))
    message3 = "IN WHAT PARKING SPOT NUMBER IS THE CAR PARKED?\nNo clue? Try to find some hints on the tables."
    popup_drawer(screen,Rect(233,385,200,120),message3,BLACK,WHITE,23)
# click the vase on the table
  if CLICKVASE == True and GIVEHINT == False:
    message4 = "I'm thirsty, can you feed me some water please?\nI will give you a hint in return."
    draw.rect(screen,WHITE,(200,325,250,200))
    popup_drawer(screen,Rect(200,423,250,1),message4,BLACK,WHITE,23)
    screen.blit(flowerimage,(flowerX,flowerY,70,70))
    screen.blit(waterpotimage,(waterpotX,waterpotY,80,80))
  # give hint 
  if GIVEHINT == True:
    message5 = "Thank You! Try viewing the numbers upside down."
    popup_drawer(screen, Rect(200,325,150,90),message5,BLACK,WHITE,23)
  # congrats 
  if CONGRATS == True:
    message6 = "CONGRATULATIONS!!!"
    draw.rect(screen,SKYBLUE,(135,230,460,90))
    popup_drawer(screen,Rect(150,250,430,50),message6,WHITE,PINK,52)
    screen.blit(sprites[framecount//5%len(sprites)],(40,230))
    screen.blit(sprites1[framecount//5%len(sprites1)],(540,230))    
    screen.blit(coinimage,(coinX,coinY))
    screen.blit(coinimage,(coinX1,coinY))
    coinY += 3
    if coinY>600:
      coinX = random.randint(10,740)
      coinX1 = random.randint(10,740)
      coinY = 10
      


def draw_inventory(screen):
  for i in range(400,641,80): 
     draw.rect(screen,WHITE,(i,500,80,80),3)
  if FINDMAGAZINE == True:
    screen.blit(magazineimage,(400,500,80,80))
  if FINDBOOKS == True:
    screen.blit(booksimage,(480,500,80,80))
  if FINDPICTURE == True:
    screen.blit(pictureimage,(560,500,80,80))
  if FINDHINT == True:
    screen.blit(vaseimage,(640,500,80,80))

def add_images(screen):
  if ADDPICTURE == True:
    screen.blit(clickpictureimage,(249,270))
  if ADDVASE == True:
    screen.blit(clickvaseimage,(166,370))
  if ADDBOOKS == True:
    screen.blit(clickbooksimage,(610,300))




def draw_background(screen):
  screen.blit(background,(0,0))


    

def scene_draw(screen):
    draw_background(screen)  
    make_rotation(screen)
    add_images(screen)
    draw_inventory(screen)
    interactions(screen)
    #add your drawing functions here
    
    display.flip()
    
    
#main
while running:
    framecount += 1
    scene_draw(screen)
    x,y = mouse.get_pos()
    #checks if user has clicked 'x' to exit program
    for evnt in event.get():
        
        
        if evnt.type == QUIT:
            running = False
        if evnt.type == MOUSEBUTTONDOWN:
          # magazine on the sofa
          if magazineRect.collidepoint(x,y) == True:    
            CLICKMAGAZINE = not(CLICKMAGAZINE)
            FINDMAGAZINE = True
          # books on the white shelf
          if booksRect.collidepoint(x,y) == True:
            CLICKBOOKS = not(CLICKBOOKS)
            FINDBOOKS = True
          # picture on the blue shelf
          if pictureRect.collidepoint(x,y) == True:
            CLICKPICTURE = not(CLICKPICTURE)
            FINDPICTURE = True
          if CLICKPICTURE == False:
            text = ""
            result = ""
          # click vase on the table       
          if vaseRect.collidepoint(x,y) == True:
            CLICKVASE = not(CLICKVASE) 
          # dragging the flower & water pot
          if CLICKVASE == True and flowerimageRect.collidepoint(x,y) == True: 
            DRAGFLOWER = True
          if CLICKVASE == True and waterpotimageRect.collidepoint(x,y) == True:
            DRAGPOT = True
          # type in the answer:
          if Rect(233,208,200,80).collidepoint(x,y) == True and CLICKPICTURE == True:           
            TEXTIN = True
        if evnt.type == KEYDOWN:

          if TEXTIN == True:
            if evnt.key == K_RETURN:
              result = text
              text = ""
              TEXTIN = False
            elif evnt.key == K_BACKSPACE:
              text = text[:-1]
            else:
              text += evnt.unicode
        # if result is the correct password, congrats the user.
        if result == password:
          CONGRATS = True
          CLICKMAGAZINE = False
          CLICKBOOKS = False
          CLICKPICTURE = False  
          CLICKVASE = False
                  
        if evnt.type == MOUSEMOTION:
          # flower pic moves with x,y if dragflower is true
          if DRAGFLOWER == True:
            flowerX,flowerY = x-25,y-25
            flowerimageRect = Rect(flowerX,flowerY,70,70)
          # water pot pic moves with x,y if dragpot is true
          if DRAGPOT == True:
            waterpotX,waterpotY = x-35,y-20
            waterpotimageRect = Rect(waterpotX,waterpotY,80,80)
          # add picture if mouse moves on certain objects
          # picture on the blue shelf
          if pictureRect.collidepoint(x,y) == True:
            ADDPICTURE = True
          else: 
            ADDPICTURE = False 
          # vase on the table
          if vaseRect.collidepoint(x,y) == True:
            ADDVASE = True
          else:
            ADDVASE = False
          # books on the white shelf
          if booksRect.collidepoint(x,y) == True:
            ADDBOOKS = True
          else:
            ADDBOOKS = False


        if evnt.type == MOUSEBUTTONUP:
          # if the user releases the button and clickvase is true, dragging all becomes false
          if CLICKVASE == True:
            DRAGFLOWER = False
            DRAGPOT = False
          # if the flower and pot collide when the user releases the button and clickvase is true
          if flowerimageRect.colliderect(waterpotimageRect) == True and CLICKVASE == True:
            GIVEHINT = not(GIVEHINT)
            CLICKVASE = False
            FINDHINT = True
          
          
  
    myClock.tick(60)
pygame.quit()

