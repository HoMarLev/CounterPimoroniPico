import picounicorn
import utime

picounicorn.init()


# From CPython Lib/colorsys.py
def hsv_to_rgb(h, s, v):
    if s == 0.0:
        return v, v, v
    i = int(h * 6.0)
    f = (h * 6.0) - i
    p = v * (1.0 - s)
    q = v * (1.0 - s * f)
    t = v * (1.0 - s * (1.0 - f))
    i = i % 6
    if i == 0:
        return v, t, p
    if i == 1:
        return q, v, p
    if i == 2:
        return p, v, t
    if i == 3:
        return p, q, v
    if i == 4:
        return t, p, v
    if i == 5:
        return v, p, q

# w widht, h height
w = picounicorn.get_width()
h = picounicorn.get_height()

# Clear the display function
def clearDisplay():
    for x in range(w):
        for y in range(h):
            picounicorn.set_pixel(x, y, 0, 0, 0)

# storing numbers


title=[["RRR R  R RRR R R"],
       ["R   R  R R   R R"],
       ["R   R  R R   RR "],
       ["RR  R  R R   R  "],
       ["R   R  R R   RR "],
       ["R   R  R R   RR "],
       ["R   RRRR RRR R R"]]


NUMZERO=["   ",
         "XXX",
         "X X",
         "X X",
         "X X",
         "XXX",
         "   "]
         
NUMONE=["   ",
        " X ",
        "XX ",
        " X ",
        " X ",
        "XXX",
        "   "]
        
NUMTWO=["   ",
        "XXX",
        "  X",
        "XXX",
        "X  ",
        "XXX",
        "   "]
        
NUMTHREE=["   ",
          "XXX",
          "  X",
          "XXX",
          "  X",
          "XXX",
          "   "]

NUMFOUR=["   ",
         "X X",
         "X X",
         "XXX",
         "  X",
         "  X",
         "   "]

NUMFIVE=["   ",
          "XXX",
          "X  ",
          "XXX",
          "  X",
          "XXX",
          "   "]

NUMSIX=["   ",
          "XXX",
          "X  ",
          "XXX",
          "X X",
          "XXX",
          "   "]


NUMSEVEN=["   ",
          "XXX",
          "  X",
          "  X",
          "  X",
          "  X",
          "   "]


NUMEIGHT=["   ",
          "XXX",
          "X X",
          "XXX",
          "X X",
          "XXX",
          "   "]

NUMNINE=["   ",
          "XXX",
          "X X",
          "XXX",
          "  X",
          "XXX",
          "   "]

DASH=["    ",
      "    ",
      "    ",
      " XX ",
      "    ",
      "    ",
      "    "]

#Create dictionaries to store scoring numbers/text
scoredict={0:NUMZERO,1:NUMONE,2:NUMTWO,3:NUMTHREE,4:NUMFOUR,5:NUMFIVE,6:NUMSIX,7:NUMSEVEN,8:NUMEIGHT,9:NUMNINE,"dash":DASH}

# create list of width/height pixels
listW=[]#makes a list 0-15
for i in range(w):
    listW.append(i)

listH=[]#makes a list 0-6
for i in range(h):
    listH.append(i)

# update display
BLANKSECTION= ["   " for i in range(h)]

def updatedisplay(displaymap):
    x=0
    y=0
    for row in displaymap: 
        for line in row:
            for char in line:
                if x < w and y <h:
                    if char == "X":
                        r, g, b = 255,255,255
                    elif char == "R":  
                        r, g, b = [int(c * 255) for c in hsv_to_rgb(x / w, y / h, 1.0)]
                    elif char == "D":
                        r, g, b = 200,200,40
                    elif char == "A":
                        r, g, b = playerABcolours
                    elif char == "Y":
                        r, g, b = playerXYcolours
                    else:
                        r,g,b=0,0,0
                    picounicorn.set_pixel(x, y, r, g, b)    
                x+=1
            x=0
        y+=1
    return displaymap

# generate "score"

playerXYcolours=(0,114,178)
playerABcolours=(255,70,160)

scoreAB = 0
scoreXY = 0

def generatescore(scoreAB,scoreXY):
    if scoreAB > 99:
        scoreAB = 99
    if scoreXY > 99:
        scoreXY = 99
    if scoreAB > 9 or scoreXY > 9:
        if scoreAB > 9:
            AB = [int(A) for A in str(scoreAB)]
            BLANKSECTION1 = [item.replace("X","A") for item in scoredict[AB[0]]]
            scoreABpix = [item.replace("X","A") for item in scoredict[AB[1]]]
        else:
            scoreABpix = [item.replace("X","A") for item in scoredict[scoreAB]]
            BLANKSECTION1 = BLANKSECTION
    
        if scoreXY > 9:
            XY = [int(X) for X in str(scoreXY)]
            BLANKSECTION2 = [item.replace("X","Y") for item in scoredict[XY[0]]] 
            scoreXYpix = [item.replace("X","Y") for item in scoredict[XY[1]]]
        else:
            scoreXYpix = [item.replace("X","Y") for item in scoredict[scoreXY]]
            BLANKSECTION2 = BLANKSECTION
            
        dashpix = [item.replace("X","D") for item in scoredict["dash"]]
        fulldisplay = [["{}{}{}{}{}".format(BLANKSECTION1[i],scoreABpix[i],dashpix[i],BLANKSECTION2[i],scoreXYpix[i])] for i in range(h)]
    else:
        scoreABpix = [item.replace("X","A") for item in scoredict[scoreAB]]
        scoreXYpix = [item.replace("X","Y") for item in scoredict[scoreXY]]
        dashpix = [item.replace("X","D") for item in scoredict["dash"]]
        fulldisplay = [["{}{}{}{}{}".format(BLANKSECTION[i],scoreABpix[i],dashpix[i],BLANKSECTION[i],scoreXYpix[i])] for i in range(h)]
    return fulldisplay

#show title for first time

updatedisplay(title)
utime.sleep(2.0)

# loop while not Buttons A & X are pressed together
while not (picounicorn.is_pressed(picounicorn.BUTTON_A) and (picounicorn.is_pressed(picounicorn.BUTTON_X))):  # Wait for Button A & X to be pressed
    
    updatedisplay(generatescore(scoreAB,scoreXY))
    while picounicorn.is_pressed(picounicorn.BUTTON_A):
        scoreAB += 1
        utime.sleep(0.3)
    while picounicorn.is_pressed(picounicorn.BUTTON_B):
        if scoreAB > 0:
            scoreAB -= 1
        utime.sleep(0.3)
    while picounicorn.is_pressed(picounicorn.BUTTON_X):
        scoreXY += 1
        utime.sleep(0.3)
    while picounicorn.is_pressed(picounicorn.BUTTON_Y):
        if scoreXY > 0:
            scoreXY -= 1
        utime.sleep(0.3)
    pass

# Below here executing exit statement
clearDisplay()

print("Buttons A & X pressed! Exiting!")

