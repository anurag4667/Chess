import pygame
import mysql.connector
import pickle
import os
mydb = mysql.connector.connect(host = "localhost",user = "root",passwd = "anurag4667",database = "Chess")
mycur = mydb.cursor()

mycur.execute("use Chess")

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
playerid = ""
player2 = ""
matchno = ""
player1rating = 0
player2rating = 0
def rating(main,opponent,result):
    if result:
        if main >= opponent:
            if (main - opponent) <= 200:
                main += 5
        else:
            if (opponent - main) <= 100:
                main += 10
            elif (opponent - main) > 100 and (opponent - main) <= 500:
                main += 30
            elif (opponent - main) > 500 and (opponent - main) <= 1000:
                main += 100
            else :
                main += 200
    else:
        if main >= opponent:
            if (main - opponent) <= 100:
                main -= 10
            elif (main - opponent) > 100 and (main - opponent) <= 500:
                main -= 30
            elif (main - opponent) > 500 and (main - opponent) <= 1000:
                main -= 100
            else :
                main -= 200
        else:
            if (opponent - main ) <= 200:
                main -= 5
    return main
def searchplayer(playerid):
    query = "select playerid from players where playerid = '"+playerid+"'"
    mycur.execute(query)
    data = mycur.fetchone()

    if data:
        return True
    else:
        return False
def binarybackup():
    global board
    global whitecheckmate
    global blackcheckmate
    global whitekingpos
    global blackkingpos
    global whitetomove
    global blackkingcastling
    global br1castling
    global br2castling
    global whitekingcastling
    global wr1castling
    global wr2castling
    global blackcheckmate
    global whitecheckmate
    global whitecheck
    global blackcheck
    os.chdir("C://Users//prach//Desktop//python game//Players"+"//"+playerid+"//INCOMPLETE_MATCH//")
    backup = open(matchno + ".dat","wb")
    data = [board,whitecheckmate,blackcheckmate,whitekingpos,blackkingpos,whitetomove,blackkingcastling,br1castling,br2castling,whitekingcastling,wr1castling,wr2castling,blackcheckmate,whitecheckmate,whitecheck,blackcheck]
    pickle.dump(data,backup)
    backup.close()
def setup(playerid):
    global board
    global whitecheckmate
    global blackcheckmate
    global whitekingpos
    global blackkingpos
    global whitetomove
    global blackkingcastling
    global br1castling
    global br2castling
    global whitekingcastling
    global wr1castling
    global wr2castling
    global blackcheckmate
    global whitecheckmate
    global whitecheck
    global blackcheck
    os.chdir("C://Users//prach//Desktop//python game//Players"+"//"+playerid+"//INCOMPLETE_MATCH//")
    backup = open(matchno + ".dat","rb")

    while True:
        try:
            data = pickle.load(backup)
            board = data[0]
            whitecheckmate = data[1]
            blackcheckmate = data[2]
            whitekingpos = data[3]
            blackkingpos = data[4]
            whitetomove = data[5]
            blackkingcastling = data[6]
            br1castling = data[7]
            br2castling = data[8]
            whitekingcastling = data[9]
            wr1castling = data[10]
            wr2castling = data[11]
            blackcheckmate = data[12]
            whitecheckmate = data[13]
            whitecheck = data[14]
            blackcheck = data[15]
        except:
            break
def setrank(rating):
    rating = str(rating)
    query = "select max(rank) from players where rating = "+rating+""
    mycur.execute(query)
    data = mycur.fetchone()

    if data[0] == None:
        query = "select min(rank) from players where rating < "+rating+""
        mycur.execute(query)
        data = mycur.fetchone()
        if data[0] == None:
            query = "select max(rank) from players where rating > "+rating+""
            mycur.execute(query)
            data = mycur.fetchone()
            if data[0] != None:
                return data[0]+1
            else:
                return 1
        else:    
            query = "update players set rank = rank + 1 where rating < "+rating+""
            mycur.execute(query)
            mydb.commit()
    return data[0]
def updaterank():
    query = "select rating from players order by rating desc"
    mycur.execute(query)
    data = mycur.fetchall()

    rating = data[0][0]
    rating = str(rating)
    query = "update players set rank = "+str(1)+" where rating = "+rating+""
    mycur.execute(query)
    rank = 1
    for i in range(2,len(data)+1):
        if data[i-1][0] < data[i-2][0]:
            rank += 1
            rating = str(data[i-1][0])
            query = "update players set rank = "+str(rank)+" where rating = "+rating+""
            mycur.execute(query)
        else:
            rating = str(data[i-1][0])
            query = "update players set rank = "+str(rank)+" where rating = "+rating+""
            mycur.execute(query)
    mydb.commit()
def getrank(playerid):
    query = "select rank from players where playerid = '"+playerid+"'"
    mycur.execute(query)
    data = mycur.fetchone()

    return data[0]
    
def getrating(playerid):
    query = "select rating from players where playerid = '"+playerid+"'"
    mycur.execute(query)
    data = mycur.fetchone()

    return data[0]
def updaterating(playerid1,playerid2,result):
    playerrating1 = getrating(playerid1)
    playerrating2 = getrating(playerid2)
    
    newrating1 = rating(playerrating1,playerrating2,result)
    newrating2 = rating(playerrating2,playerrating1,not result)
    
    query1 = "update players set rating = "+str(newrating1)+" where playerid = '"+playerid1+"'"
    query2 = "update players set rating = "+str(newrating2)+" where playerid = '" +playerid2+"'"

    mycur.execute(query1)
    mycur.execute(query2)
    mydb.commit()
def updateplayers(playerid,rating,result):
    rank = setrank(rating)
    rank = str(rank)
    rating = str(rating)

    query = "update players set rank = "+rank+" and rating = "+rating+" where playerid = '"+playerid+"'"
    mycur.execute(query)
    mydb.commit()
    if result == True:
        query = "update players set matchwon = matchwon + 1 and totalmatches = totalmatches + 1 where playerid = '"+playerid+"'"
        mycur.execute(query)
    else:
        query = "update players set matchlost = matchlost + 1 and totalmatches = totalmatches + 1 where playerid = '"+playerid+"'"
        mycur.execute(query)
    mydb.commit()    
def newplayer2(playerid,rating):
    if searchplayer(playerid):
        return False
    else:
        rank = setrank(rating)
        rank = str(rank)
        rating = str(rating)
        query = "insert into players values ('"+playerid+"',"+rating+","+rank+",0,0,0,0)"
        mycur.execute(query)
        mydb.commit()
        os.chdir("C://Users//prach//Desktop//python game//Players")
        os.makedirs("C://Users//prach//Desktop//python game//Players"+"//"+playerid+"/MATCHESPLAYED")
        os.makedirs("C://Users//prach//Desktop//python game//Players"+"//"+playerid+"/INCOMPLETE_MATCH")
        return True
def matchcreated(playerid1,playerid2):
    query = "select max(matchno) from matches "
    mycur.execute(query)
    data = mycur.fetchone()
    if data[0] == None:
        data = 1
        matchno = data
    else:
        matchno = data[0]+1
    matchno = str(matchno)
    query = "insert into matches values ("+matchno+",'"+playerid1+"','"+playerid2+"',NULL,TRUE)"
    mycur.execute(query)
    mydb.commit()
    query = "update players set incomplete = incomplete + 1 where playerid = '"+playerid1+"'"
    mycur.execute(query)
    mydb.commit()
    query = "update players set incomplete = incomplete + 1 where playerid = '"+playerid2+"'"
    mycur.execute(query)
    mydb.commit()
    return matchno
def matchended(winner,loser,matchno):
    global score
    global scoreno
    global playerid
    os.chdir("C://Users//prach//Desktop//python game//Players"+"//"+playerid+"//INCOMPLETE_MATCH")
    os.remove(matchno + ".dat")
    updaterating(winner,loser,True)
    scoreno = getrating(winner)
    score = "score : " + str(scoreno)
    winnerrating = getrating(winner)
    rank = setrank(winnerrating)
    query = "update players set rank = "+str(rank)+" where playerid = '"+winner+"'"
    mycur.execute(query)
    mydb.commit()
    query = "update players set matchwon = matchwon + 1 where playerid = '"+winner+"'"
    mycur.execute(query)
    
    loserrating = getrating(loser)
    rank = setrank(loserrating)
    query = "update players set rank = "+str(rank)+" where playerid = '"+loser+"'"
    mycur.execute(query)
    mydb.commit()
    query = "update players set matchlost = matchlost + 1 where playerid = '"+loser+"'"
    mycur.execute(query)
    
    query = "update players set incomplete = incomplete - 1 where playerid in ('"+loser+"','"+winner+"')"
    mycur.execute(query)
    
    query = "update players set totalmatches = totalmatches + 1 where playerid in ('"+loser+"','"+winner+"')"
    mycur.execute(query)

    query = "update matches set matchwon = '"+winner+"' where matchno = "+matchno+""
    mycur.execute(query)

    query = "update matches set incomplete = FALSE where matchno = "+matchno+""
    mycur.execute(query)
    updaterank()
    mydb.commit()
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
def addtext(text,textx,texty,color = (0,0,0),size = 50):
    font = pygame.font.SysFont("comicsans",size)
    txt = font.render(text,True,color)
    screen.blit(txt,(textx,texty))
def quitwindow():
    while True:
        screen.fill((255,255,255))
        addtext("Are you sure you want to quit?",0,200)
        yes.draw(screen,(0,0,0))
        no.draw(screen,(0,0,0))
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if yes.isOver(pos):
                    print('You Quit')
                    pygame.display.quit()
                    pygame.quit()
                    return False
                elif no.isOver(pos):
                    return True
            if event.type == pygame.MOUSEMOTION:
                if yes.isOver(pos):
                    yes.color = (255,0,0)
                elif no.isOver(pos):
                    no.color = (0,255,0)
                else:
                    yes.color = (0,0,255)
                    no.color = (0,0,255)
            pygame.display.update()
def newgameinput():
    global playerid
    global player2
    global player2rating
    input_rect2 = pygame.Rect(200,100,200,50)
    font = pygame.font.SysFont("comicsans",32)
    color_active = (0,255,0)
    color_passive = (255,0,0)
    
    active = False
    run = True
    while run:
        addtext("Enter Player2",140,50)
        Enter.draw(screen,(0,0,0))
        createplayer.draw(screen,(0,0,0))
        main_menu.draw(screen,(0,0,0))
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                run = quitwindow()
                if run == False:
                    return False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_rect2.collidepoint(event.pos):
                    active = True
                elif Enter.isOver(pos):
                    if player2 != "" and player2 != playerid:
                        verify = searchplayer(player2)
                        if verify:
                            player2rating = getrating(player2)
                            return True
                        else:
                            print("Player does not exist")
                elif main_menu.isOver(pos):
                    player2 = ""
                    return True
                elif createplayer.isOver(pos):
                    player2 = newplayer()
                    if player2 == False:
                        player2 = ""
                        run = False
                        return False
                    elif player2:
                        player2 = ""
                        run = True
                        return True
                    else:
                        player2rating = getrating(player2)
                        return True
                else:
                    active = False
            if event.type == pygame.MOUSEMOTION:
                if Enter.isOver(pos):
                    Enter.color = (0,255,0)
                elif main_menu.isOver(pos):
                    main_menu.color = (0,255,0)
                elif createplayer.isOver(pos):
                    createplayer.color = (0,255,0)
                else:
                    Enter.color = (0,0,255)
                    createplayer.color = (0,0,255)
                    main_menu.color = (0,0,255)
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_BACKSPACE:
                        player2 = player2[:-1]
                    else:
                        player2 += event.unicode

        if active:
            color2 = color_active
        else:
            color2 = color_passive
        
        pygame.draw.rect(screen,color2,input_rect2,2)
        text_surface = font.render(player2,True,(0,0,0))
        screen.blit(text_surface,(input_rect2.x + 5,input_rect2.y + 5))
        input_rect2.w = max(100,text_surface.get_width() + 10)
        pygame.display.update()
        screen.fill((255,255,255))
def newplayer():
    global mainmenu
    input_rect = pygame.Rect(200,100,200,50)
    font = pygame.font.SysFont("comicsans",32)
    color_active = (0,255,0)
    color_passive = (255,0,0)
    run = True
    active = False
    playerid = ""
    while run:
        addtext("Enter ID",185,50)
        Enter.draw(screen,(0,0,0))
        main_menu.draw(screen,(0,0,0))
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                run = quitwindow()
                if run == False:
                    return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_rect.collidepoint(event.pos):
                    active = True
                elif Enter.isOver(pos):
                    if playerid != "":
                        create = newplayer2(playerid,200)
                        if create:
                            return playerid
                        else:
                            print("This Player already exist Please choose again")
                elif main_menu.isOver(pos):
                    mainmenu = True
                    return True
                else:
                    active = False
            if event.type == pygame.MOUSEMOTION:
                if Enter.isOver(pos):
                    Enter.color = (0,255,0)
                elif main_menu.isOver(pos):
                    main_menu.color = (0,255,0)
                else:
                    Enter.color = (0,0,255)
                    main_menu.color = (0,0,255)
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_BACKSPACE:
                        playerid = playerid[:-1]
                    else:
                        playerid += event.unicode
        if active:
            color = color_active
        else:
            color = color_passive
        pygame.draw.rect(screen,color,input_rect,2)
        text_surface = font.render(playerid,True,(0,0,0))
        screen.blit(text_surface,(input_rect.x + 5,input_rect.y + 5))
        input_rect.w = max(100,text_surface.get_width() + 10)
        pygame.display.update()
        screen.fill((255,255,255))
def matches(player2):
    global playerid

    query = "select matchno from matches where playerid = '"+playerid+"' and playerid2 = '"+player2+"' and incomplete = True "
    mycur.execute(query)
    d = mycur.fetchall()
    data = [] 
    for i in range(len(d)):
        data.append(d[i][0])
    return data

def loadgame():
    global playerid
    global player2
    global player2rating
    global matchno
    input_rect1 = pygame.Rect(200,90,200,50)
    input_rect2 = pygame.Rect(200,200,200,50)
    font = pygame.font.SysFont("comicsans",32)
    color_active = (0,255,0)
    color_passive = (255,0,0)

    active1 = False
    active2 = False
    run = True
    while run:
        addtext("Enter Player2",140,50)
        addtext("Enter Matchno",140,150)
        Enter3.draw(screen,(0,0,0))
        main_menu.draw(screen,(0,0,0))
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                run = quitwindow()
                if run == False:
                    return False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_rect1.collidepoint(event.pos):
                    active1 = True
                elif input_rect2.collidepoint(event.pos):
                    active2 = True
                elif Enter3.isOver(pos):
                    if player2 != "" and player2 != playerid:
                        verify = searchplayer(player2)
                        if verify:
                            player2rating = getrating(player2)
                            incomplete_matches = matches(player2)
                            if matchno != "" and matchno.isdigit():
                                if int(matchno) in incomplete_matches:
                                    return True
                                else:
                                    print("Wrong Matchno")
                                    print(incomplete_matches)
                        else:
                            print("Player does not exist")
                elif main_menu.isOver(pos):
                    player2 = ""
                    matchno = ""
                    return True
                else:
                    active1 = active2 = False
            if event.type == pygame.MOUSEMOTION:
                if Enter3.isOver(pos):
                    Enter3.color = (0,255,0)
                elif main_menu.isOver(pos):
                    main_menu.color = (0,255,0)
                else:
                    Enter3.color = (0,0,255)
                    main_menu.color = (0,0,255)
            if event.type == pygame.KEYDOWN:
                if active1:
                    if event.key == pygame.K_BACKSPACE:
                        player2 = player2[:-1]
                    else:
                        player2 += event.unicode
                elif active2:
                    if event.key == pygame.K_BACKSPACE:
                        matchno = matchno[:-1]
                    else:
                        matchno += event.unicode
        if active1:
            color1 = color_active
        elif active2:
            color2 = color_active
        else:
            color1 = color_passive
            color2 = color_passive
        pygame.draw.rect(screen,color1,input_rect1,2)
        text_surface = font.render(player2,True,(0,0,0))
        screen.blit(text_surface,(input_rect1.x + 5,input_rect1.y + 5))
        input_rect1.w = max(100,text_surface.get_width() + 10)
        pygame.draw.rect(screen,color2,input_rect2,2)
        text_surface = font.render(matchno,True,(0,0,0))
        screen.blit(text_surface,(input_rect2.x + 5,input_rect2.y + 5))
        input_rect2.w = max(100,text_surface.get_width() + 10)
        pygame.display.update()
        screen.fill((255,255,255))

def statsinfo():
    global playerid
    query = "select * from players where playerid = '"+playerid+"'"
    mycur.execute(query)
    data = mycur.fetchone()
    run = True
    while run:
        addtext("Rank: "+str(data[2]),140,20,(0,0,0),30)
        addtext("Player ID: "+playerid,140,55,(0,0,0),30)
        addtext("Rating: "+str(data[1]),140,90,(0,0,0),30)
        addtext("Matchwon: "+str(data[3]),140,130,(0,0,0),30)
        addtext("Matchlost: "+str(data[4]),140,170,(0,0,0),30)
        addtext("Totalmatches: "+str(data[5]),140,210,(0,0,0),30)
        addtext("incomplete: "+str(data[6]),140,250,(0,0,0),30)
        changeid.draw(screen,(0,0,0))
        main_menu.draw(screen,(0,0,0))
        pygame.display.update()
        screen.fill((255,255,255))
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                run = quitwindow()
                if run == False:
                    return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if changeid.isOver(pos):
                    run = False
                    return playerinfoinput()
                elif main_menu.isOver(pos):
                    run = False
                    return True
            if event.type == pygame.MOUSEMOTION:
                if changeid.isOver(pos):
                    changeid.color = (0,255,0)
                elif main_menu.isOver(pos):
                    main_menu.color = (0,255,0)
                else:
                    changeid.color = (0,0,255)
                    main_menu.color = (0,0,255)
                    
def playerinfoinput():
    global playerid
    global score
    global player1rating
    input_rect = pygame.Rect(200,100,200,50)
    font = pygame.font.SysFont("comicsans",32)
    color_active = (0,255,0)
    color_passive = (255,0,0)
    run = True
    active = False
    while run:
        addtext("Enter PlayerID",140,50)
        Enter.draw(screen,(0,0,0))
        createplayer.draw(screen,(0,0,0))
        main_menu.draw(screen,(0,0,0))
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                run = quitwindow()
                if run == False:
                    return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_rect.collidepoint(event.pos):
                    active = True
                elif Enter.isOver(pos):
                    if playerid != "":
                        verify = searchplayer(playerid)
                        if verify:
                            scoreno = getrating(playerid)
                            player1rating = scoreno
                            score ="score :"+ str(scoreno)
                            return True
                        else:
                            print("This player does not exist")
                elif main_menu.isOver(pos):
                    playerid = ""
                    return True
                elif createplayer.isOver(pos):
                    playerid = newplayer()
                    if playerid == False:
                        playerid = ""
                        run = False
                        return False
                    elif playerid:
                        playerid = ""
                        run = True
                        return True
                    else:
                        scoreno = getrating(playerid)
                        player1rating = scoreno
                        score ="score :"+ str(scoreno)
                        return True
                else:
                    active = False
            if event.type == pygame.MOUSEMOTION:
                if Enter.isOver(pos):
                    Enter.color = (0,255,0)
                elif main_menu.isOver(pos):
                    main_menu.color = (0,255,0)
                elif createplayer.isOver(pos):
                    createplayer.color = (0,255,0)
                else:
                    Enter.color = (0,0,255)
                    createplayer.color = (0,0,255)
                    main_menu.color = (0,0,255)
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_BACKSPACE:
                        playerid = playerid[:-1]
                    else:
                        playerid += event.unicode
        if active:
            color = color_active
        else:
            color = color_passive
        pygame.draw.rect(screen,color,input_rect,2)
        text_surface = font.render(playerid,True,(0,0,0))
        screen.blit(text_surface,(input_rect.x + 5,input_rect.y + 5))
        input_rect.w = max(100,text_surface.get_width() + 10)
        pygame.display.update()
        screen.fill((255,255,255))
        
def redrawWindow():
    screen.fill((255,255,255))
    New_game.draw(screen,(0,0,0))
    Load_game.draw(screen,(0,0,0))
    Players.draw(screen,(0,0,0))
    Quit.draw(screen,(0,0,0))
def againorquit():
    global mainmenu
    while True:
        screen.fill((255,255,255))
        addtext("Do You Want To Play Again?",10,200)
        yes.draw(screen,(0,0,0))
        no.draw(screen,(0,0,0))
        main_menu.draw(screen,(0,0,0))

        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if yes.isOver(pos):
                    return True
                elif no.isOver(pos):
                    mainmenu = False
                    pygame.display.quit()
                    pygame.quit()
                    return False
                elif main_menu.isOver(pos):
                    mainmenu = True
                    return False
            if event.type == pygame.MOUSEMOTION:
                if yes.isOver(pos):
                    yes.color = (0,255,0)
                elif no.isOver(pos):
                    no.color = (255,0,0)
                elif main_menu.isOver(pos):
                    main_menu.color = (0,255,0)
                else:
                    yes.color = (0,0,255)
                    no.color = (0,0,255)
                    main_menu.color = (0,0,255)
            pygame.display.update()
            
New_game = button((0,0,255),160,106,200,50,'New Game')
Load_game = button((0,0,255),160,206,200,50,'Load Game')
Players = button((0,0,255),160,306,200,50,'Players')
Quit = button((0,0,255),160,406,200,50,'Quit')
yes = button((0,0,255),100,250,100,30,"YES")
no = button((0,0,255),300,250,100,30,"NO")
Enter = button((0,0,255),130,206,250,50,"PROCEED")
Enter2 = button((0,0,255),130,406,250,50,"PROCEED")
Enter3 = button((0,0,255),130,306,250,50,"PROCEED")
main_menu = button((0,0,255),130,406,250,50,"MAIN MENU")
createplayer = button((0,0,255),130,306,250,50,"CREATE NEW")
changeid = button((0,0,255),130,306,250,50,"CHANGE ID")
playerid = ""
scoreno = 0
score = "score : " + str(scoreno)
def createboard():
    global board
    x = 0
    y = 0
    d = 64
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
                image = pygame.image.load("C:/Users/prach/Desktop/python game/images/" + j + ".png")
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
    record = open("C://Users//prach//Desktop//python game//Players"+"//"+playerid+"//MATCHESPLAYED//"+matchno+".txt","a")

    if "w" in p1:
        if p2 == "0":
            if "p" in p1:
                if finalpos[0] == 0:
                    if blackcheck:
                        if blackcheckmate:
                            print(dictcol[finalpos[1]]+dictrow[finalpos[0]]+"="+p2+"++",end = " ")
                            record.write(dictcol[finalpos[1]]+dictrow[finalpos[0]]+"="+p2+"++ ")
                        else:
                            print(dictcol[finalpos[1]]+dictrow[finalpos[0]]+"="+p2+"+",end = " ")
                            record.write(dictcol[finalpos[1]]+dictrow[finalpos[0]]+"="+p2+"+ ")
                    else:
                        print(dictcol[finalpos[1]]+dictrow[finalpos[0]]+"="+p2,end = " ")
                        record.write(dictcol[finalpos[1]]+dictrow[finalpos[0]]+"="+p2+" ")
                else:
                    if blackcheck:
                        if blackcheckmate:
                            print(dictcol[finalpos[1]]+dictrow[finalpos[0]]+"++",end = " ")
                            record.write(dictcol[finalpos[1]]+dictrow[finalpos[0]]+"++ ")
                        else:
                            print(dictcol[finalpos[1]]+dictrow[finalpos[0]]+"+",end = " ")
                            record.write(dictcol[finalpos[1]]+dictrow[finalpos[0]]+"+ ")
                    else:
                        print(dictcol[finalpos[1]]+dictrow[finalpos[0]],end = " ")
                        record.write(dictcol[finalpos[1]]+dictrow[finalpos[0]]+" ")
            else:
                if blackcheck:
                    if blackcheckmate:
                        record.write(p1+dictcol[finalpos[1]]+dictrow[finalpos[0]]+"++ " )
                        print(p1+dictcol[finalpos[1]]+dictrow[finalpos[0]]+"++",end = " ")
                    else:
                        record.write(p1+dictcol[finalpos[1]]+dictrow[finalpos[0]]+"+ ")
                        print(p1+dictcol[finalpos[1]]+dictrow[finalpos[0]]+"+",end = " ")
                else:
                    record.write(p1+dictcol[finalpos[1]]+dictrow[finalpos[0]]+" ")
                    print(p1+dictcol[finalpos[1]]+dictrow[finalpos[0]],end = " ")
        elif p2 != "0":
            if "p" in p1:
                if finalpos[0] == 0:
                    if blackcheck:
                        if blackcheckmate:
                            record.write(dictcol[finalpos[1]]+dictrow[finalpos[0]]+"="+p2+"++ ")
                            print(dictcol[finalpos[1]]+dictrow[finalpos[0]]+"="+p2+"++",end = " ")
                        else:
                            record.write(dictcol[finalpos[1]]+dictrow[finalpos[0]]+"="+p2+"+ ")
                            print(dictcol[finalpos[1]]+dictrow[finalpos[0]]+"="+p2+"+",end = " ")
                    else:
                        record.write(dictcol[finalpos[1]]+dictrow[finalpos[0]]+"="+p2+" ")
                        print(dictcol[finalpos[1]]+dictrow[finalpos[0]]+"="+p2,end = " ")
                else:
                    if blackcheck:
                        if blackcheckmate:
                            record.write(dictcol[initialpos[1]]+"x"+dictcol[finalpos[1]]+dictrow[finalpos[0]]+"++ ")
                            print(dictcol[initialpos[1]]+"x"+dictcol[finalpos[1]]+dictrow[finalpos[0]]+"++",end = " ")
                        else:
                            record.write(dictcol[initialpos[1]]+"x"+dictcol[finalpos[1]]+dictrow[finalpos[0]]+"+ ")
                            print(dictcol[initialpos[1]]+"x"+dictcol[finalpos[1]]+dictrow[finalpos[0]]+"+",end = " ")
                    else:
                        record.write(dictcol[initialpos[1]]+"x"+dictcol[finalpos[1]]+dictrow[finalpos[0]]+" ")
                        print(dictcol[initialpos[1]]+"x"+dictcol[finalpos[1]]+dictrow[finalpos[0]],end = " ")
            else:
                if blackcheck:
                    if blackcheckmate:
                        record.write(p1+"x"+dictcol[finalpos[1]]+dictrow[finalpos[0]]+"++"+" ")
                        print(p1+"x"+dictcol[finalpos[1]]+dictrow[finalpos[0]]+"++",end = " ")
                    else:
                        record.write(p1+"x"+dictcol[finalpos[1]]+dictrow[finalpos[0]]+"+"+" ")
                        print(p1+"x"+dictcol[finalpos[1]]+dictrow[finalpos[0]]+"+",end = " ")
                else:
                    record.write(p1+"x"+dictcol[finalpos[1]]+dictrow[finalpos[0]]+" ")
                    print(p1+"x"+dictcol[finalpos[1]]+dictrow[finalpos[0]],end = " ")
    else:
        if p2 == "0":
            if "p" in p1:
                if finalpos[0] == 7:
                    if whitecheck:
                        if whitecheckmate:
                            record.write(dictcol[finalpos[1]]+dictrow[finalpos[0]]+"="+p2+"++\n")
                            print(dictcol[finalpos[1]]+dictrow[finalpos[0]]+"="+p2+"++")
                        else:
                            record.write(dictcol[finalpos[1]]+dictrow[finalpos[0]]+"="+p2+"+\n")
                            print(dictcol[finalpos[1]]+dictrow[finalpos[0]]+"="+p2+"+")
                    else:
                        record.write(dictcol[finalpos[1]]+dictrow[finalpos[0]]+"="+p2+"\n")
                        print(dictcol[finalpos[1]]+dictrow[finalpos[0]]+"="+p2)
                else:
                    if whitecheck:
                        if whitecheckmate:
                            record.write(p1+dictcol[finalpos[1]]+dictrow[finalpos[0]]+"++\n")
                            print(p1+dictcol[finalpos[1]]+dictrow[finalpos[0]]+"++")
                        else:
                            record.write(p1+dictcol[finalpos[1]]+dictrow[finalpos[0]]+"+\n")
                            print(p1+dictcol[finalpos[1]]+dictrow[finalpos[0]]+"+")
                    else:
                        record.write(dictcol[finalpos[1]]+dictrow[finalpos[0]]+"\n")
                        print(dictcol[finalpos[1]]+dictrow[finalpos[0]])
            else:
                if whitecheck:
                    if whitecheckmate:
                        record.write(p1+dictcol[finalpos[1]]+dictrow[finalpos[0]]+"++\n")
                        print(p1+dictcol[finalpos[1]]+dictrow[finalpos[0]]+"++")
                    else:
                        record.write(p1+dictcol[finalpos[1]]+dictrow[finalpos[0]]+"+\n")
                        print(p1+dictcol[finalpos[1]]+dictrow[finalpos[0]]+"+")
                else:
                    record.write(p1+dictcol[finalpos[1]]+dictrow[finalpos[0]]+"\n")
                    print(p1+dictcol[finalpos[1]]+dictrow[finalpos[0]])
        elif p2 != "0":
            if "p" in p1:
                if finalpos[0] == 7:
                    if whitecheck:
                        if whitecheckmate:
                            record.write(dictcol[finalpos[1]]+dictrow[finalpos[0]]+"="+p2+"++\n")
                            print(dictcol[finalpos[1]]+dictrow[finalpos[0]]+"="+p2+"++")
                        else:
                            record.write(dictcol[finalpos[1]]+dictrow[finalpos[0]]+"="+p2+"+\n")
                            print(dictcol[finalpos[1]]+dictrow[finalpos[0]]+"="+p2+"+")
                    else:
                        record.write(dictcol[finalpos[1]]+dictrow[finalpos[0]]+"="+p2+"\n")
                        print(dictcol[finalpos[1]]+dictrow[finalpos[0]]+"="+p2)
                else:
                    if whitecheck:
                        if whitecheckmate:
                            record.write(dictcol[finalpos[1]]+dictrow[finalpos[0]]+"++\n")
                            print(dictcol[finalpos[1]]+dictrow[finalpos[0]]+"++")
                        else:
                            record.write(dictcol[finalpos[1]]+dictrow[finalpos[0]]+"+\n")
                            print(dictcol[finalpos[1]]+dictrow[finalpos[0]]+"+")
                    else:
                        record.write(dictcol[finalpos[1]]+dictrow[finalpos[0]]+"\n")
                        print(dictcol[finalpos[1]]+dictrow[finalpos[0]])
            else:
                if whitecheck:
                    if whitecheckmate:
                        record.write(p1+"x"+dictcol[finalpos[1]]+dictrow[finalpos[0]]+"++\n")
                        print(p1+"x"+dictcol[finalpos[1]]+dictrow[finalpos[0]]+"++")
                    else:
                        record.write(p1+"x"+dictcol[finalpos[1]]+dictrow[finalpos[0]]+"+\n")
                        print(p1+"x"+dictcol[finalpos[1]]+dictrow[finalpos[0]]+"+")
                else:
                    record.write(p1+"x"+dictcol[finalpos[1]]+dictrow[finalpos[0]]+"\n")
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
mainmenu = True
def maingame():
    createboard()
    createpictures()
    run = True
    global matchno
    global mainmenu
    global sqselected
    global playerclicks
    global board
    global whitecheckmate
    global blackcheckmate
    global playerid
    global player2
    while run:
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = quitwindow()
                if run == False:
                    binarybackup()
                    return False
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
                        choise = againorquit()
                        if choise:
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
                            if whitecheckmate:
                                matchended(player2,playerid,matchno)
                            else:
                                matchended(playerid,player2,matchno)
                            run = False
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
                            if mainmenu == True:
                                return True
                            else:
                                return False
                if run:
                    createboard()
                    highlightsquare(validmoves,sqselected)
                    createpictures()
                    pygame.display.flip()
            
while run:
    redrawWindow()
    addtext(playerid,10,0)
    addtext(score,300,0)
    pygame.display.update()
    for event in pygame.event.get():
        redrawWindow()
        addtext(playerid,10,0)
        addtext(score,300,0)
        pygame.display.update()
        pos = pygame.mouse.get_pos()

        if event.type == pygame.QUIT:
            run = quitwindow()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if New_game.isOver(pos):
                if playerid == "":
                    run = playerinfoinput()
                else:
                    if player2 == "":
                        run = newgameinput()
                        if player2 != "":
                            matchno = matchcreated(playerid,player2)
                            record = open("C://Users//prach//Desktop//python game//Players"+"//"+playerid+"//MATCHESPLAYED//"+matchno+".txt","a")
                            backup = open("C://Users//prach//Desktop//python game//Players"+"//"+playerid+"//INCOMPLETE_MATCH//"+matchno+".dat","wb")
                            backup.close()
                            mainmenu = False
                            run = maingame()
                            player2 = ""                    
            elif Load_game.isOver(pos):
                if playerid == "":
                    run = playerinfoinput()
                else:
                    run = loadgame()
                    if run:
                        if player2 != "":
                            setup(playerid)
                            run = maingame()
                            player2 = ""
            elif Players.isOver(pos):
                if playerid == "":
                    run = playerinfoinput()
                else:
                    run = statsinfo()
            elif Quit.isOver(pos):
                run = quitwindow()               
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
