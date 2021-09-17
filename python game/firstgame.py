import pygame

pygame.init()

screen = pygame.display.set_mode((512,512))
screen.fill((255,255,255))
pygame.display.set_caption("Chess")

run = True

board = [["r","n","b","q","k","b","n","r"],
         ["p","p","p","p","p","p","p","p"],
         ["0","0","0","0","0","0","0","0"],
         ["0","0","0","0","0","0","0","0"],
         ["0","0","0","0","0","0","0","0"],
         ["0","0","0","0","0","0","0","0"],
         ["wp","wp","wp","wp","wp","wp","wp","wp"],
         ["wr","wn","wb","wq","wk","wb","wn","wr"]]

whitekingpos = (7,4)
blackkingpos = (0,4)
whitetomove = True
blackkingcastling = True
br1castling = br2castling = True
whitekingcastling = True
wr1castling = wr2castling = True
whiteradius = []
blackradius = []
undomovepre = None
undomoveaft = None
blackcheckmate = False
whitecheckmate = False
whitecheck = False
blackcheck = False
class button():
    def __init__(self, color, x,y,width,height, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self,win,outline=None):
        if outline:
            pygame.draw.rect(screen, outline, (self.x-2,self.y-2,self.width+4,self.height+4),0)
            
        pygame.draw.rect(screen, self.color, (self.x,self.y,self.width,self.height),0)
        
        if self.text != '':
            font = pygame.font.SysFont('comicsans', 50)
            text = font.render(self.text, 1, (0,0,0))
            win.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))

    def isOver(self, pos):
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
            
        return False
def redrawWindow():
    screen.fill((255,255,255))
    New_game.draw(screen,(0,0,0))
    Load_game.draw(screen,(0,0,0))
    Players.draw(screen,(0,0,0))
    Quit.draw(screen,(0,0,0))
New_game = button((0,0,255),160,106,200,50,'New Game')
Load_game = button((0,0,255),160,206,200,50,'Load Game')
Players = button((0,0,255),160,306,200,50,'Players')
Quit = button((0,0,255),160,406,200,50,'Quit')
def createboard():
    global board
    x = 0
    y = 0
    d =64
    for i in range(8):
        for j in range(8):
            if (i+j)%2 == 0:
                pygame.draw.rect(screen,(235,235,239),(x,y,d,d))
            else:
                pygame.draw.rect(screen,(125,130,150),(x,y,d,d))
            x+= 64
        x = 0
        y+=64
def createpictures():
    x = 0
    y = 0
    d = 64
    for i in board:
        for j in i:
            if j == "0":
                y+= 1
            else:
                image = pygame.image.load("C:/Users/yogendra/Desktop/python game/images/" + j + ".png")
                screen.blit(image,(y*d,x*d))
                y+= 1
        y = 0
        x+=1
            
def reverse():
    global whitetomove
    if whitetomove:
        whitetomove = False
    else:
        whitetomove = True
def chancetomove(p1):
    global whitetomove
    if "w" in p1 and whitetomove == True:
        whitetomove = False
        return True
    if "w" not in p1 and whitetomove == False:
        whitetomove = True
        return True
    return False
def printchessnotation(initialpos,finalpos,p1,p2):
    global whitecheck
    global blackcheck
    global whitecheckmate
    global blackcheckmate
    dictrow = {0:"8",1:"7",2:"6",3:"5",4:"4",5:"3",6:"2",7:"1"}
    dictcol = {0:"A",1:"B",2:"C",3:"D",4:"E",5:"F",6:"G",7:"H"}

    if "w" in p1:
        if p2 == "0":
            if "p" in p1:
                if finalpos[0] == 0:
                    if blackcheck:
                        if blackcheckmate:
                            print(dictcol[finalpos[1]]+dictrow[finalpos[0]]+"="+p2+"++",end = " ")
                        else:
                            print(dictcol[finalpos[1]]+dictrow[finalpos[0]]+"="+p2+"+",end = " ")
                    else:
                        print(dictcol[finalpos[1]]+dictrow[finalpos[0]]+"="+p2,end = " ")
                else:
                    if blackcheck:
                        if blackcheckmate:
                            print(dictcol[finalpos[1]]+dictrow[finalpos[0]]+"++",end = " ")
                        else:
                            print(dictcol[finalpos[1]]+dictrow[finalpos[0]]+"+",end = " ")
                    else:
                        print(dictcol[finalpos[1]]+dictrow[finalpos[0]],end = " ")
            else:
                if blackcheck:
                    if blackcheckmate:
                        print(p1+dictcol[finalpos[1]]+dictrow[finalpos[0]]+"++",end = " ")
                    else:
                        print(p1+dictcol[finalpos[1]]+dictrow[finalpos[0]]+"+",end = " ")
                else:
                    print(p1+dictcol[finalpos[1]]+dictrow[finalpos[0]],end = " ")
        elif p2 != "0":
            if "p" in p1:
                if finalpos[0] == 0:
                    if blackcheck:
                        if blackcheckmate:
                            print(dictcol[finalpos[1]]+dictrow[finalpos[0]]+"="+p2+"++",end = " ")
                        else:
                            print(dictcol[finalpos[1]]+dictrow[finalpos[0]]+"="+p2+"+",end = " ")
                    else:
                        print(dictcol[finalpos[1]]+dictrow[finalpos[0]]+"="+p2,end = " ")
                else:
                    if blackcheck:
                        if blackcheckmate:
                            print(dictcol[initialpos[1]]+"x"+dictcol[finalpos[1]]+dictrow[finalpos[0]]+"++",end = " ")
                        else:
                            print(dictcol[initialpos[1]]+"x"+dictcol[finalpos[1]]+dictrow[finalpos[0]]+"+",end = " ")
                    else:
                        print(dictcol[initialpos[1]]+"x"+dictcol[finalpos[1]]+dictrow[finalpos[0]],end = " ")
            else:
                if blackcheck:
                    if blackcheckmate:
                        print(p1+"x"+dictcol[finalpos[1]]+dictrow[finalpos[0]]+"++",end = " ")
                    else:
                        print(p1+"x"+dictcol[finalpos[1]]+dictrow[finalpos[0]]+"+",end = " ")
                else:
                    print(p1+"x"+dictcol[finalpos[1]]+dictrow[finalpos[0]],end = " ")
    else:
        if p2 == "0":
            if "p" in p1:
                if finalpos[0] == 7:
                    if whitecheck:
                        if whitecheckmate:
                            print(dictcol[finalpos[1]]+dictrow[finalpos[0]]+"="+p2+"++")
                        else:
                            print(dictcol[finalpos[1]]+dictrow[finalpos[0]]+"="+p2+"+")
                    else:
                        print(dictcol[finalpos[1]]+dictrow[finalpos[0]]+"="+p2)
                else:
                    if whitecheck:
                        if whitecheckmate:
                            print(p1+dictcol[finalpos[1]]+dictrow[finalpos[0]]+"++")
                        else:
                            print(p1+dictcol[finalpos[1]]+dictrow[finalpos[0]]+"+")
                    else:
                        print(dictcol[finalpos[1]]+dictrow[finalpos[0]])
            else:
                if whitecheck:
                    if whitecheckmate:
                        print(p1+dictcol[finalpos[1]]+dictrow[finalpos[0]]+"++")
                    else:
                        print(p1+dictcol[finalpos[1]]+dictrow[finalpos[0]]+"+")
                else:
                    print(p1+dictcol[finalpos[1]]+dictrow[finalpos[0]])
        elif p2 != "0":
            if "p" in p1:
                if finalpos[0] == 7:
                    if whitecheck:
                        if whitecheckmate:
                            print(dictcol[finalpos[1]]+dictrow[finalpos[0]]+"="+p2+"++")
                        else:
                            print(dictcol[finalpos[1]]+dictrow[finalpos[0]]+"="+p2+"+")
                    else:
                        print(dictcol[finalpos[1]]+dictrow[finalpos[0]]+"="+p2)
                else:
                    if whitecheck:
                        if whitecheckmate:
                            print(dictcol[finalpos[1]]+dictrow[finalpos[0]]+"++")
                        else:
                            print(dictcol[finalpos[1]]+dictrow[finalpos[0]]+"+")
                    else:
                        print(dictcol[finalpos[1]]+dictrow[finalpos[0]])
            else:
                if whitecheck:
                    if whitecheckmate:
                        print(p1+"x"+dictcol[finalpos[1]]+dictrow[finalpos[0]]+"++")
                    else:
                        print(p1+"x"+dictcol[finalpos[1]]+dictrow[finalpos[0]]+"+")
                else:
                    print(p1+"x"+dictcol[finalpos[1]]+dictrow[finalpos[0]])
def validmove(positions):
    global board
    s = positions[0]
    f = positions[1]
    p1 = board[s[0]][s[1]]
    p2 = board[f[0]][f[1]]
    global whitetomove
    if chancetomove(p1):
        if "w" in p1 and "w" in p2:
            reverse()
            return False
        if "w" not in p1 and "0" not in p2:
            if "w" not in p1 and "w" not in p2:
                reverse()
                return False
            
            return True
        return True

def castling(p1,ip,fp):
    global board
    global blackkingcastling
    global br1castling
    global br2castling
    global whitekingcastling
    global wr1castling
    global wr2castling
    global whitekingpos
    global blackkingpos

    if "w" in p1:
        if fp == (7,6):
            if whitekingcastling:
                if board[fp[0]][fp[1]+1] == "wr" and wr2castling == True:
                    for j in range(5,7):
                        if board[7][j] != "0":
                            break
                    else:
                        print("O-O",end = " ")
                        board[7][6] = "wk"
                        board[7][5] = "wr"
                        board[7][4] = board[7][7] = "0"
                        whitekingpos = fp
                        whitekingcastling = wr1castling = wr2castling = False
                        return True
        if fp == (7,1):
            if whitekingcastling:
                if board[fp[0]][fp[1]-1] == "wr" and wr1castling == True:
                    for j in range(1,4):
                        if board[7][j] != "0":
                            break
                    else:
                        print("O-O-O",end = " ")
                        board[7][1] = "wk"
                        board[7][2] = "wr"
                        board[7][0] = board[7][4] = "0"
                        whitekingpos = fp
                        whitekingcastling = wr1castling = wr2castling = False
                        return True
    if "w" not in p1:
        if fp == (0,6):
            if blackkingcastling:
                if board[fp[0]][fp[1]+1] == "r" and br2castling == True:
                    for j in range(5,7):
                        if board[0][j] != "0":
                            break
                    else:
                        print("O-O")
                        board[0][6] = "k"
                        board[0][5] = "r"
                        board[0][4] = board[0][7] = "0"
                        blackkingpos = fp
                        blackkingcastling = br1castling = br2castling = False
                        return True
        if fp == (0,1):
            if blackkingcastling:
                if board[fp[0]][fp[1]-1] == "r" and br1castling == True:
                    for j in range(1,4):
                        if board[0][j] != "0":
                            break
                    else:
                        print("O-O-O")
                        board[0][1] = "k"
                        board[0][2] = "r"
                        board[0][0] = board[0][4] = "0"
                        blackkingpos = fp
                        blackkingcastling = br1castling = br2castling = False
                        return True
    return False
def pawnpromotion(p1,ip,fp):
    global board
    promotion = input("enter q,n,b,r to promote")
    if "w" in p1:
        if promotion == "q":
            printchessnotation(None,fp,p1,"wq")
            board[fp[0]][fp[1]] = "wq"
            board[ip[0]][ip[1]] = "0"
        elif promotion == "n":
            printchessnotation(None,fp,p1,"wn")
            board[fp[0]][fp[1]] = "wn"
            board[ip[0]][ip[1]] = "0"
        elif promotion == "b":
            printchessnotation(None,fp,p1,"wb")
            board[fp[0]][fp[1]] = "wb"
            board[ip[0]][ip[1]] = "0"
        elif promotion == "r":
            printchessnotation(None,fp,p1,"wr")
            board[fp[0]][fp[1]] = "wr"
            board[ip[0]][ip[1]] = "0"
        else:
            print("pls type again")
    else:
        if promotion == "q":
            printchessnotation(None,fp,p1,"q")
            board[fp[0]][fp[1]] = "q"
            board[ip[0]][ip[1]] = "0"
        elif promotion == "n":
            printchessnotation(None,fp,p1,"n")
            board[fp[0]][fp[1]] = "n"
            board[ip[0]][ip[1]] = "0"
        elif promotion == "b":
            printchessnotation(None,fp,p1,"b")
            board[fp[0]][fp[1]] = "b"
            board[ip[0]][ip[1]] = "0"
        elif promotion == "r":
            printchessnotation(None,fp,p1,"r")
            board[fp[0]][fp[1]] = "r"
            board[ip[0]][ip[1]] = "0"
        else:
            print("pls type again")

def pawnmovementvalid(p1,ip,fp):
    #black pawn
    validmoves = []
    if "w" not in p1:
        x = ip
        if x[0]+1 < 8:
            if board[x[0]+1][x[1]] == "0":
                x = x[0]+1,x[1]
                validmoves.append(x)
            x = ip
            if x[0] == 1:
                if board[x[0]+1][x[1]] == "0":
                    if board[x[0]+2][x[1]] == "0":
                        x = x[0]+2,x[1]
                        validmoves.append(x)
            x = ip
            if x[1] -1 >= 0:
                if "w" in board[x[0]+1][x[1]-1]:
                    x = x[0]+1,x[1]-1
                    validmoves.append(x)
            x = ip
            if x[1]+1 < 8:
                if "w" in board[x[0]+1][x[1]+1]:
                    x = x[0]+1,x[1]+1
                    validmoves.append(x)
            x = ip
            if fp is not None:
                if fp in validmoves:
                    if fp[0] == 7:
                        pawnpromotion(p1,ip,fp)
                    else:
                        return validmoves
            else:
                return validmoves
    #white pawn
    if "w" in p1:
        x = ip
        if x[0]-1 >= 0:
            if board[x[0]-1][x[1]] == "0":
                x = x[0]-1,x[1]
                validmoves.append(x)
            x = ip
            if x[0] == 6:
                if board[x[0]-1][x[1]] == "0":
                    if board[x[0]-2][x[1]] == "0":
                        x = x[0]-2,x[1]
                        validmoves.append(x)
            x = ip
            if x[1]-1 >= 0:
                if board[x[0]-1][x[1]-1] != "0" and "w" not in board[x[0]-1][x[1]-1]:
                    x = x[0]-1,x[1]-1
                    validmoves.append(x)
            x = ip
            if x[1]+1 < 8:
                if board[x[0]-1][x[1]+1] != "0" and "w" not in board[x[0]-1][x[1]+1]:
                    x = x[0]-1,x[1]+1
                    validmoves.append(x)
                x = ip
            if fp is not None:
                if fp in validmoves:
                    if fp[0] == 0:
                        pawnpromotion(p1,ip,fp)
                    else:
                        return validmoves
            else:
                return validmoves
def bishopmovementvalid(p1,ip,fp):
    validmoves = []
    #black bishop
    if "w" not in p1:
        x = ip
        x = x[0]-1,x[1]-1
        while x[0] >= 0 and x[1] >= 0:
            if board[x[0]][x[1]] == "0":
                validmoves.append(x)
            elif "w" in board[x[0]][x[1]]:
                validmoves.append(x)
                break
            elif "w" not in board[x[0]][x[1]] and board[x[0]][x[1]] != "0":
                break
            x = x[0]-1,x[1]-1
        x = ip
        x = x[0]-1,x[1]+1
        while x[0] >= 0 and x[1] < 8:
            if board[x[0]][x[1]] == "0":
                validmoves.append(x)
            elif "w" in board[x[0]][x[1]]:
                validmoves.append(x)
                break
            elif "w" not in board[x[0]][x[1]] and board[x[0]][x[1]] != "0":
                break
            x = x[0]-1,x[1]+1
        x = ip
        x = x[0]+1,x[1]-1
        while x[0] < 8 and x[1] >= 0:
            if board[x[0]][x[1]] == "0":
                validmoves.append(x)
            elif "w" in board[x[0]][x[1]]:
                validmoves.append(x)
                break
            elif "w" not in board[x[0]][x[1]] and board[x[0]][x[1]] != "0":
                break
            x = x[0]+1,x[1]-1
        x = ip
        x = x[0]+1,x[1]+1
        while x[0] < 8 and x[1] < 8:
            if board[x[0]][x[1]] == "0":
                validmoves.append(x)
            elif "w" in board[x[0]][x[1]]:
                validmoves.append(x)
                break
            elif "w" not in board[x[0]][x[1]] and board[x[0]][x[1]] != "0":
                break
            x = x[0]+1,x[1]+1
        x = ip

        return validmoves
    #white bishop
    if "w" in p1:
        x = ip
        x = x[0]-1,x[1]-1
        while x[0] >= 0 and x[1] >= 0:
            if board[x[0]][x[1]] == "0":
                validmoves.append(x)
            elif "w" not in board[x[0]][x[1]] and board[x[0]][x[1]] != "0":
                validmoves.append(x)
                break
            elif "w" in board[x[0]][x[1]]:
                break
            x = x[0]-1,x[1]-1
        x = ip
        x = x[0]-1,x[1]+1
        while x[0] >= 0 and x[1] < 8:
            if board[x[0]][x[1]] == "0":
                validmoves.append(x)
            elif "w" not in board[x[0]][x[1]] and board[x[0]][x[1]] != "0":
                validmoves.append(x)
                break
            elif "w" in board[x[0]][x[1]]:
                break
            x = x[0]-1,x[1]+1
        x = ip
        x = x[0]+1,x[1]-1
        while x[0] < 8 and x[1] >= 0:
            if board[x[0]][x[1]] == "0":
                validmoves.append(x)
            elif "w" not in board[x[0]][x[1]] and board[x[0]][x[1]] != "0":
                validmoves.append(x)
                break
            elif "w" in board[x[0]][x[1]]:
                break
            x = x[0]+1,x[1]-1
        x = ip
        x = x[0]+1,x[1]+1
        while x[0] < 8 and x[1] < 8:
            if board[x[0]][x[1]] == "0":
                validmoves.append(x)
            elif "w" not in board[x[0]][x[1]] and board[x[0]][x[1]] != "0":
                validmoves.append(x)
                break
            elif "w" in board[x[0]][x[1]]:
                break
            x = x[0]+1,x[1]+1
        x = ip
        return validmoves
def knightmovementvalid(p1,ip,fp):
    #black knight
    validmoves = []
    if "w" not in p1:
        x = ip
        if x[0] >=2:
            if x[1]-1 >= 0:
                if "w" in board[x[0]-2][x[1]-1] or board[x[0]-2][x[1]-1] == "0":
                    x = x[0]-2,x[1]-1
                    validmoves.append(x)
            x = ip
            if x[1]+1 < 8:
                if "w" in board[x[0]-2][x[1]+1] or board[x[0]-2][x[1]+1] == "0":
                    x = x[0]-2,x[1]+1
                    validmoves.append(x)
            x = ip
        if x[0] < 6:
            if x[1] -1 >= 0:
                if "w" in board[x[0]+2][x[1]-1] or board[x[0]+2][x[1]-1] == "0":
                    x = x[0]+2,x[1]-1
                    validmoves.append(x)
            x = ip
            if x[1]+1 < 8:
                if "w" in board[x[0]+2][x[1]+1] or board[x[0]+2][x[1]+1] == "0":
                    x = x[0]+2,x[1]+1
                    validmoves.append(x)
            x = ip
        if x[1] >=2:
            if x[0]-1 >= 0:
                if "w" in board[x[0]-1][x[1]-2] or board[x[0]-1][x[1]-2] == "0":
                    x = x[0]-1,x[1]-2
                    validmoves.append(x)
            x = ip
            if x[0]+1 < 8:
                if "w" in board[x[0]+1][x[1]-2] or board[x[0]+1][x[1]-2] == "0":
                    x = x[0]+1,x[1]-2
                    validmoves.append(x)
            x = ip
        if x[1] < 6:
            if x[0] -1 >= 0:
                if "w" in board[x[0]-1][x[1]+2] or board[x[0]-1][x[1]+2] == "0":
                    x = x[0]-1,x[1]+2
                    validmoves.append(x)
            x = ip
            if x[0]+1 < 8:
                if "w" in board[x[0]+1][x[1]+2] or board[x[0]+1][x[1]+2] == "0":
                    x = x[0]+1,x[1]+2
                    validmoves.append(x)
            x = ip
        return validmoves
    #white knight
    if "w" in p1:
        x = ip
        if x[0] >=2:
            if x[1]-1 >= 0:
                if "w" not in board[x[0]-2][x[1]-1] or board[x[0]-2][x[1]-1] == "0":
                    x = x[0]-2,x[1]-1
                    validmoves.append(x)
            x = ip
            if x[1]+1 < 8:
                if "w" not in board[x[0]-2][x[1]+1] or board[x[0]-2][x[1]+1] == "0":
                    x = x[0]-2,x[1]+1
                    validmoves.append(x)
            x = ip
        if x[0] < 6:
            if x[1] -1 >= 0:
                if "w" not in board[x[0]+2][x[1]-1] or board[x[0]+2][x[1]-1] == "0":
                    x = x[0]+2,x[1]-1
                    validmoves.append(x)
            x = ip
            if x[1]+1 < 8:
                if "w" not in board[x[0]+2][x[1]+1] or board[x[0]+2][x[1]+1] == "0":
                    x = x[0]+2,x[1]+1
                    validmoves.append(x)
            x = ip
        if x[1] >=2:
            if x[0]-1 >= 0:
                if "w" not in board[x[0]-1][x[1]-2] or board[x[0]-1][x[1]-2] == "0":
                    x = x[0]-1,x[1]-2
                    validmoves.append(x)
            x = ip
            if x[0]+1 < 8:
                if "w" not in board[x[0]+1][x[1]-2] or board[x[0]+1][x[1]-2] == "0":
                    x = x[0]+1,x[1]-2
                    validmoves.append(x)
            x = ip
        if x[1] < 6:
            if x[0] -1 >= 0:
                if "w" not in board[x[0]-1][x[1]+2] or board[x[0]-1][x[1]+2] == "0":
                    x = x[0]-1,x[1]+2
                    validmoves.append(x)
            x = ip
            if x[0]+1 < 8:
                if "w" not in board[x[0]+1][x[1]+2] or board[x[0]+1][x[1]+2] == "0":
                    x = x[0]+1,x[1]+2
                    validmoves.append(x)
            x = ip
        return validmoves
def rookmovementvalid(p1,ip,fp):
    validmoves = []
    #black rook
    if "w" not in p1:
        x = ip
        x = x[0],x[1] -1
        while x[1] >= 0:
            if board[x[0]][x[1]] == "0":
                validmoves.append(x)
            elif "w" in board[x[0]][x[1]]:
                validmoves.append(x)
                break
            elif "w" not in board[x[0]][x[1]] and board[x[0]][x[1]] != "0":
                break
            x = x[0],x[1] -1
        x = ip
        x = x[0],x[1] + 1
        while x[1] < 8:
            if board[x[0]][x[1]] == "0":
                validmoves.append(x)
            elif "w" in board[x[0]][x[1]]:
                validmoves.append(x)
                break
            elif "w" not in board[x[0]][x[1]] and board[x[0]][x[1]] != "0":
                break
            x = x[0],x[1] +1
        x = ip
        x = x[0]-1,x[1]
        while x[0] >= 0:
            if board[x[0]][x[1]] == "0":
                validmoves.append(x)
            elif "w" in board[x[0]][x[1]]:
                validmoves.append(x)
                break
            elif "w" not in board[x[0]][x[1]] and board[x[0]][x[1]] != "0":
                break
            x = x[0]-1,x[1]
        x = ip
        x = x[0]+1,x[1]
        while x[0] < 8:
            if board[x[0]][x[1]] == "0":
                validmoves.append(x)
            elif "w" in board[x[0]][x[1]]:
                validmoves.append(x)
                break
            elif "w" not in board[x[0]][x[1]] and board[x[0]][x[1]] != "0":
                break
            x = x[0]+1,x[1]
        x = ip
        return validmoves
    #white rook
    if "w" in p1:
        x = ip
        x = x[0],x[1]-1
        while x[1] >= 0:
            if board[x[0]][x[1]] == "0":
                validmoves.append(x)
            elif "w" in board[x[0]][x[1]] :
                break
            elif "w" not in board[x[0]][x[1]] and board[x[0]][x[1]] != "0":
                validmoves.append(x)
                break
            x = x[0],x[1]-1
        x = ip
        x = x[0],x[1]+1
        while x[1] < 8:
            if board[x[0]][x[1]] == "0":
                validmoves.append(x)
            elif "w" in board[x[0]][x[1]] :
                break
            elif "w" not in board[x[0]][x[1]] and board[x[0]][x[1]] != "0":
                validmoves.append(x)
                break
            x = x[0],x[1]+1
        x = ip
        x = x[0] -1,x[1]
        while x[0] >= 0:
            if board[x[0]][x[1]] == "0":
                validmoves.append(x)
            elif "w" in board[x[0]][x[1]] :
                break
            elif "w" not in board[x[0]][x[1]] and board[x[0]][x[1]] != "0":
                validmoves.append(x)
                break
            x = x[0]-1,x[1]
        x = ip
        x = x[0]+1,x[1]
        while x[0] < 8:
            if board[x[0]][x[1]] == "0":
                validmoves.append(x)
            elif "w" in board[x[0]][x[1]] :
                break
            elif "w" not in board[x[0]][x[1]] and board[x[0]][x[1]] != "0":
                validmoves.append(x)
                break
            x = x[0] + 1,x[1]
        x = ip
        return validmoves
def queenmovementvalid(p1,ip,fp):
    moveset1 = bishopmovementvalid(p1,ip,fp)
    moveset2 = rookmovementvalid(p1,ip,fp)
    totalmoves = moveset1 + moveset2

    return totalmoves
def kingmovementvalid(p1,ip,fp):
    global whitekingpos
    global blackkingpos
    global whiteradius
    global blackradius
    validmoves = []
    #black king
    if "w" not in p1:
        x = ip
        x =x[0]-1,x[1]
        if x[0] >= 0:
            blackradius.append(x)
            if board[x[0]][x[1]] == "0" or "w" in board[x[0]][x[1]]:
                validmoves.append(x)
            x = x[0],x[1]-1
            if x[1] >= 0:
                blackradius.append(x)
                if board[x[0]][x[1]] == "0" or "w" in board[x[0]][x[1]]:
                    validmoves.append(x)
            x = x[0],x[1]+2
            if x[1] < 8:
                blackradius.append(x)
                if board[x[0]][x[1]] == "0" or "w" in board[x[0]][x[1]]:
                    validmoves.append(x)
        x = ip
        x = x[0]+1,x[1]
        if x[0] < 8:
            blackradius.append(x)
            if board[x[0]][x[1]] == "0" or "w" in board[x[0]][x[1]]:
                validmoves.append(x)
            x = x[0],x[1]-1
            if x[1] >= 0:
                blackradius.append(x)
                if board[x[0]][x[1]] == "0" or "w" in board[x[0]][x[1]]:
                    validmoves.append(x)
            x = x[0],x[1]+2
            if x[1] < 8:
                blackradius.append(x)
                if board[x[0]][x[1]] == "0" or "w" in board[x[0]][x[1]]:
                    validmoves.append(x)
        x = ip
        x = x[0],x[1]+1
        if x[1] < 8 :
            blackradius.append(x)
            if board[x[0]][x[1]] == "0" or "w" in board[x[0]][x[1]]:
                validmoves.append(x)
        x = ip
        x = x[0],x[1]-1
        if x[1] >= 0:
            blackradius.append(x)
            if board[x[0]][x[1]] == "0" or "w" in board[x[0]][x[1]]:
                validmoves.append(x)
        x = ip
        return validmoves
    #white king
    if "w" in p1:
        x = ip
        x =x[0]-1,x[1]
        if x[0] >= 0:
            whiteradius.append(x)
            if "w" not in board[x[0]][x[1]]:
                validmoves.append(x)
            x = x[0],x[1]-1
            if x[1] >= 0:
                whiteradius.append(x)
                if "w" not in board[x[0]][x[1]]:
                    validmoves.append(x)
            x = x[0],x[1]+2
            if x[1] < 8:
                whiteradius.append(x)
                if "w" not in board[x[0]][x[1]]:
                    validmoves.append(x)
        x = ip
        x = x[0]+1,x[1]
        if x[0] < 8:
            whiteradius.append(x)
            if "w" not in board[x[0]][x[1]]:
                validmoves.append(x)
            x = x[0],x[1]-1
            if x[1] >= 0:
                whiteradius.append(x)
                if "w" not in board[x[0]][x[1]]:
                    validmoves.append(x)
            x = x[0],x[1]+2
            if x[1] < 8:
                whiteradius.append(x)
                if "w" not in board[x[0]][x[1]]:
                    validmoves.append(x)
        x = ip
        x = x[0],x[1]+1
        if x[1] < 8 :
            whiteradius.append(x)
            if "w" not in board[x[0]][x[1]]:
                validmoves.append(x)
        x = ip
        x = x[0],x[1]-1
        if x[1] >= 0:
            whiteradius.append(x)
            if "w" not in board[x[0]][x[1]]:
                validmoves.append(x)
        x = ip
        return validmoves

def kingmovementvalid2(p1,moves):
    global board
    whtking = whitekingpos
    blkking = blackkingpos
    limit = len(moves)
    if p1 == "wk":
        for n in range(limit-1,-1,-1):
            move = moves[n]
            for i in range(8):
                for j in range(8):
                    if move in moves:
                        if "w" not in board[i][j] and board[i][j] != "0" and board[i][j]!= "k" : 
                            p = board[move[0]][move[1]]
                            board[move[0]][move[1]] = "wk"
                            board[whtking[0]][whtking[1]] = "0"
                            if chessvalidmove(board[i][j],(i,j),move):
                                moves.remove(move)
                                board[move[0]][move[1]] = p
                                board[whtking[0]][whtking[1]] = "wk"
                            else:
                                reverse()
                                board[move[0]][move[1]] = p
                                board[whtking[0]][whtking[1]] = "wk"
        return moves
                        
    elif p1 == "k":
        for n in range(limit-1,-1,-1):
            move = moves[n]
            for i in range(8):
                for j in range(8):
                    if move in moves:
                        if "w" in board[i][j] and board[i][j] != "wk":
                            p = board[move[0]][move[1]]
                            board[move[0]][move[1]] = "k"
                            board[blkking[0]][blkking[1]] = "0"
                            if chessvalidmove(board[i][j],(i,j),move):
                                board[move[0]][move[1]] = p
                                board[blkking[0]][blkking[1]] = "k"
                                moves.remove(move)
                            else:
                                reverse()
                                board[move[0]][move[1]] = p
                                board[blkking[0]][blkking[1]] = "k"
        return moves

def validmovegiver(p1,ip,fp):
    global board
    if "p" in p1:
        moves = pawnmovementvalid(p1,ip,fp)
        return moves
    elif "r" in p1:
        moves = rookmovementvalid(p1,ip,fp)
        return moves
    elif "b" in p1:
        moves = bishopmovementvalid(p1,ip,fp)
        return moves
    elif "n" in p1:
        moves = knightmovementvalid(p1,ip,fp)
        return moves
    elif "q" in p1:
        moves = queenmovementvalid(p1,ip,fp)
        return moves
    elif "k" in p1:
        moves = kingmovementvalid(p1,ip,fp)
        moves = kingmovementvalid2(p1,moves)
        return moves
    return []
def chessvalidmove(p1,initialposition,finalposition):
    global br1castling
    global br2castling
    global wr1castling
    global wr2castling
    global blackkingpos
    global whitekingpos
    global board
    if "p" in p1:
        moves = pawnmovementvalid(p1,initialposition,finalposition)
        if moves is not None:
            if finalposition in moves:
                return True
            else:
                reverse()
                return False
        reverse()
        return False
    if "b" in p1:
        moves = bishopmovementvalid(p1,initialposition,finalposition)
        if finalposition in moves:
            return True
        else:
            reverse()
            return False
    if "n" in p1:
        moves = knightmovementvalid(p1,initialposition,finalposition)
        if finalposition in moves:
            return True
        else:
            reverse()
            return False
    if "r" in p1:
        moves = rookmovementvalid(p1,initialposition,finalposition)
        if finalposition in moves:
            if initialposition == (0,0):
                br1castling = False
            elif initialposition == (0,7):
                br2castling = False
            elif initialposition == (7,0):
                wr1castling = False
            elif initialposition == (7,7):
                wr2castling = False
            return True
        else:
            reverse()
            return False
    if "q" in p1:
        moves = queenmovementvalid(p1,initialposition,finalposition)
        if finalposition in moves:
            return True
        else:
            reverse()
            return False
    if "k" in p1:
        global blackkingcastling
        global whitekingcastling
        global blackradius
        global whiteradius
        global whitecheckmate
        global blackcheckmate
        castle = castling(p1,initialposition,finalposition)
        moves = kingmovementvalid(p1,initialposition,finalposition)
        moves = kingmovementvalid2(p1,moves)
        if finalposition in moves:
            if initialposition == (0,4):
                blackkingcastling = False
                blackkingpos = finalposition
            elif initialposition == (7,4):
                whitekingcastling = False
                whitekingpos = finalposition
            elif "w" in p1:
                move2 = kingmovementvalid("k",blackkingpos,finalposition)
                if finalposition in blackradius:
                    blackradius = []
                    reverse()
                    return False
                else:
                    whitekingpos = finalposition
            elif "w" not in p1:
                move2 = kingmovementvalid("wk",whitekingpos,finalposition)
                if finalposition in whiteradius:
                    whiteradius = []
                    reverse()
                    return False
                else:
                    blackkingpos = finalposition
            return True
        elif castle:
            if "w" in p1:
                whitekingpos = finalposition
            else:
                blackkingpos = finalposition
            return True
        else:
            reverse()
            return False


    #do the reversing in function only
        
def check():
    global whitekingpos
    global blackkingpos
    global whitecheck
    global blackcheck
    global board
    if whitetomove:
        for i in range(8):
            for j in range(8):
                if board[i][j] != "0" and "w" not in board[i][j]:
                    if chessvalidmove(board[i][j],(i,j),whitekingpos):
                        whitecheck = True
                        return True
                    else:
                        reverse()
        whitecheck = False
        return False
    else:
        for i in range(8):
            for j in range(8):
                if "w" in board[i][j]:
                    if chessvalidmove(board[i][j],(i,j),blackkingpos):
                        blackcheck = True
                        return True
                    else:
                        reverse()
        blackcheck = False
        return False
def check2():
    global whitekingpos
    global blackkingpos
    global whitecheck
    global blackcheck
    global whitetomove
    global board
    if whitetomove:
        whitetomove = False
        if check():
            whitetomove = True
            blackcheck = False
            reverse()
            undomove()
            return True
        whitetomove = True
        return False
    else:
        whitetomove = True
        if check():
            whitetomove = False
            whitecheck = False
            reverse()
            undomove()
            return True
        whitetomove = False
        return False
            
        
def checkfree():
    global blackcheck
    global whitecheck
    global board
    if blackcheck:
        for i in range(8):
            for j in range(8):
                if "w" in board[i][j]:
                    if chessvalidmove(board[i][j],(i,j),blackkingpos):
                        reverse()
                        undomove()
                        return False
                    else:
                        reverse()
        blackcheck = False
        return True
    elif whitecheck:
        for i in range(8):
            for j in range(8):
                if "w" not in board[i][j] and board[i][j] != "0":
                    if chessvalidmove(board[i][j],(i,j),whitekingpos):
                        reverse()
                        undomove()
                        return False
                    else:
                        reverse()
        whitecheck = False
        return True
    return True
def checkmate():
    global board
    global whitecheckmate
    global blackcheckmate
    global whitekingpos
    global blackkingpos
    global whitecheck
    global blackcheck
    whtkingpos = whitekingpos
    blkkingpos = blackkingpos
    if whitetomove:
        for i in range(8):
            for j in range(8):
                if "w" in board[i][j]:
                    moves = validmovegiver(board[i][j],(i,j),None)
                    for move in moves:
                        if chessvalidmove(board[i][j],(i,j),move):
                            if board[i][j] == "wk":
                                whitekingpos = whtkingpos
                            p = board[move[0]][move[1]]
                            board[move[0]][move[1]] = board[i][j]
                            board[i][j] = "0"
                            if check():
                                board[i][j] = board[move[0]][move[1]]
                                board[move[0]][move[1]] = p
                            else:
                                board[i][j] = board[move[0]][move[1]]
                                board[move[0]][move[1]] = p
                                whitecheck = True
                                return False
                        else:
                            reverse()
        whitecheckmate = True
        return True
    else:
        for i in range(8):
            for j in range(8):
                if "w" not in board[i][j] and board[i][j] != "0":
                    moves = validmovegiver(board[i][j],(i,j),None)
                    for move in moves:
                        if chessvalidmove(board[i][j],(i,j),move):
                            if board[i][j] == "k":
                                blackkingpos = blkkingpos
                            p = board[move[0]][move[1]]
                            board[move[0]][move[1]] = board[i][j]
                            board[i][j] = "0"
                            if check():
                                board[i][j] = board[move[0]][move[1]]
                                board[move[0]][move[1]] = p
                            else:
                                board[i][j] = board[move[0]][move[1]]
                                board[move[0]][move[1]] = p
                                blackcheck = True
                                return False
                        else:
                            reverse()
        blackcheckmate = True
        return True
        
        
def undomove():
    global undomovepre
    global undomoveaft
    global board
    ip = undomovepre[1]
    p1 = undomovepre[0]
    fp = undomoveaft[1]
    p2 = undomoveaft[0]
    board[ip[0]][ip[1]] = p1
    board[fp[0]][fp[1]] = p2
    undomovepre = undomoveaft = []


def movingpieces(playerclicks):
    global board
    global undomovepre
    global undomoveaft
    if validmove(playerclicks):
        t1 = playerclicks[0]
        t2 = playerclicks[1]
        if chessvalidmove(board[t1[0]][t1[1]],t1,t2):
            if board[t1[0]][t1[1]] != "0":
                undomovepre = [board[t1[0]][t1[1]],t1]
                undomoveaft = [board[t2[0]][t2[1]],t2]
                p1 = board[t1[0]][t1[1]]
                p2 = board[t2[0]][t2[1]]
                board[t2[0]][t2[1]] = board[t1[0]][t1[1]]
                board[t1[0]][t1[1]] = "0"
                if check2():
                    pass
                if checkfree():
                    if check():
                        if checkmate():
                            printchessnotation(t1,t2,p1,p2)
                    else:
                        printchessnotation(t1,t2,p1,p2)
def highlightsquare(validmoves,sqselected):
    global board
    if validmoves == None:
        validmoves = []
    if sqselected != ():
        r,c = sqselected
        if "w" in board[r][c] and whitetomove == True:
            s = pygame.Surface((64,64))
            s.set_alpha(100)
            s.fill(pygame.Color('pink'))
            screen.blit(s,(c*64,r*64))
            s.fill(pygame.Color('red'))
            for move in validmoves:
                screen.blit(s,(move[1]*64,move[0]*64))
        elif "w" not in board[r][c] and board[r][c] != "0"and whitetomove == False:
            s = pygame.Surface((64,64))
            s.set_alpha(100)
            s.fill(pygame.Color('pink'))
            screen.blit(s,(c*64,r*64))
            s.fill(pygame.Color('red'))
            for move in validmoves:
                screen.blit(s,(move[1]*64,move[0]*64))
sqselected = ()
playerclicks = []
validmoves = []    
createboard()
createpictures()
def maingame():
    createboard()
    createpictures()
    global run
    global sqselected
    global playerclicks
    global board
    global whitecheckmate
    global blackcheckmate
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                location = pygame.mouse.get_pos()
                col = location[0]//64
                row = location[1]//64
                if sqselected == (row,col):
                    sqselected = ()
                    playerclicks = []
                else:
                    sqselected = (row,col)
                    playerclicks.append(sqselected)
                    validmoves = validmovegiver(board[sqselected[0]][sqselected[1]],sqselected,None)
                    createboard()
                    highlightsquare(validmoves,sqselected)
                    createpictures()
                    pygame.display.flip()
                
                if len(playerclicks) == 2:
                    movingpieces(playerclicks)
                    playerclicks = []
                    sqselected = ()
                    if whitecheckmate == True or blackcheckmate == True:
                        createboard()
                        createpictures()
                        pygame.display.flip()
                        print("Game Over")
                        choise = input("Want to play again type y")
                        if choise == "y":
                            board = [["r","n","b","q","k","b","n","r"],
                                     ["p","p","p","p","p","p","p","p"],
                                     ["0","0","0","0","0","0","0","0"],
                                     ["0","0","0","0","0","0","0","0"],
                                     ["0","0","0","0","0","0","0","0"],
                                     ["0","0","0","0","0","0","0","0"],
                                     ["wp","wp","wp","wp","wp","wp","wp","wp"],
                                     ["wr","wn","wb","wq","wk","wb","wn","wr"]]
                            whitecheckmate = blackcheckmate = False
                            blackcheck = whitecheck = False
                            blackkingpos = (0,4)
                            whitekingpos = (7,4)
                        else:
                            run = False
                createboard()
                highlightsquare(validmoves,sqselected)
                createpictures()
                pygame.display.flip()
            
        pygame.display.flip()
while run:
    redrawWindow()
    pygame.display.update()
    for event in pygame.event.get():
        pos = pygame.mouse.get_pos()

        if event.type == pygame.QUIT:
            run = False
            pygame.display.quit()
            pygame.quit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if New_game.isOver(pos):
                maingame()
                pygame.quit()
            elif Load_game.isOver(pos):
                print('clicked the button')
            elif Players.isOver(pos):
                print('clicked the button')
            elif Quit.isOver(pos):
                print('You Quit')
                run = False
                pygame.display.quit()
                pygame.quit()
               
        if event.type == pygame.MOUSEMOTION:
            if New_game.isOver(pos):
                New_game.color = (0,255,0)
            elif Load_game.isOver(pos):
                Load_game.color = (0,255,0)
            elif Players.isOver(pos):
                Players.color = (0,255,0)
            elif Quit.isOver(pos):
                Quit.color = (255,0,0)
            else:
                New_game.color = (0,0,255)
                Load_game.color = (0,0,255)
                Players.color = (0,0,255)
                Quit.color = (0,0,255)
pygame.quit()
