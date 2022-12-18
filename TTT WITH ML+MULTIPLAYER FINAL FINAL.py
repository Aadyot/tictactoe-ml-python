'''EDITABLE VARIABLES'''

filename="gamedata1.csv"

#if true, comp will play only randommoves
trial=False

#if true, comp will play against itself indefinitely
playingfordata=False

#if true, program will check entire database for redundancy after every game
checkandadd=True

#how much i want to punish for losing as compared to reward for winning
number =1.8

import pygame
import random as r
import csv

pygame.init()
h=600

#mode button values
height=int(h/4)
width=int(h/3)
xcoor=int(h/10)
ycoor=int(h/5)

#fonts
verybigfont=pygame.font.SysFont(None,80)
bigfont=pygame.font.SysFont(None,45)
medfont=pygame.font.SysFont(None,35)
smolfont=pygame.font.SysFont(None,26)


'''PYGAME FUNCTIONS'''

def putbigtext(text,colour,pos,window):
    screentext=bigfont.render(text,True,colour)
    pos=int(pos[0]),int(pos[1])
    window.blit(screentext,pos)
def putmedtext(text,colour,pos,window):
    screentext=medfont.render(text,True,colour)
    pos=int(pos[0]),int(pos[1])
    window.blit(screentext,pos)
def putsmoltext(text,colour,pos,window):
    screentext=smolfont.render(text,True,colour)
    pos=int(pos[0]),int(pos[1])
    window.blit(screentext,pos)   
    
     
def modesel(choosewin,game_no):
    #chooses mode on a separate window
    putsmoltext("AADYOT & ISHAN",[255,255,255],(h-376*h/600,h-h/20),choosewin)
   
    """displaying greeting  for first game and "one more" for after"""
    if game_no==0:
        putbigtext("TIC TAC TOE",[255,215,0],(h/2.5-10-25,h/10),choosewin)
    else:
        putbigtext("PLAY AGAIN?",[255,215,0],(h/3,h/8),choosewin)    
    
    #multiplayer button
    pygame.draw.rect(choosewin,[0,255,0],(xcoor-5,ycoor+30,width+20,height))
    pygame.draw.rect(choosewin,[0,179,30],(xcoor+10-5,ycoor+10+30,width,height-20))
    putmedtext("MULTIPLAYER",[0,0,0],((xcoor+width/8)-5,ycoor+height/2.5+30),choosewin)

    #singleplayer button
    pygame.draw.rect(choosewin,[0,225,255],(h-xcoor-width-5-8,ycoor+30,width+20,height))
    pygame.draw.rect(choosewin,[30,144,255],(h-xcoor-width+10-5-8,ycoor+10+30,width,height-20))
    putmedtext("SINGLEPLAYER",[0,0,0],((h-xcoor-7*width/8)-22,ycoor+height/2.5+30),choosewin)

    #quit button
    pygame.draw.rect(choosewin,[255,120,0],(int(h/2-width/2-13),3*ycoor,width+20,height))
    pygame.draw.rect(choosewin,[230,0,0],(int(h/2-width/2+10-13),3*ycoor+10,width,height-20))
    putmedtext("QUIT",[0,0,0],(int(h/2-width/6),int(3*ycoor+height/2.5)),choosewin)

    pygame.display.update()    
    a=True
    while a:
        while True:
            pygame.event.get()
            if pygame.mouse.get_pressed()[0]:
                coord=(pygame.mouse.get_pos())
                pygame.time.wait(250) 
                break
        #click on a mode    
        if (ycoor) < coord[1]<(ycoor + height):
            if xcoor < coord[0]<(xcoor+width):
                mode="m"
                a=False
            elif (h-xcoor-width) < coord[0]<(h-xcoor):
                mode="s"
                a=False
        #click on exit
        elif (ycoor*3) < coord[1]<(ycoor*3+height) and (h/2-width/2) < coord[0]<(h/2+width/2):
            mode="q"
            a=False 
    
    pygame.display.quit()
    return mode


def matrix(wind,h):    
    #initialises grid only on screen 
    wind.fill((0,0,0))
    colour=[255,255,255]
    pygame.draw.line(wind,colour,(width,0),(width,h),5)
    pygame.draw.line(wind,colour,(2*width,0),(2*width,h),5)
    pygame.draw.line(wind,colour,(0,width),(h,width),5)
    pygame.draw.line(wind,colour,(0,2*width),(h,2*width),5)
    pygame.display.update()


def click(grid):
    '''
    takes coordinates when screen is clicked and returns position of click in form of coord=(y,x)
    tuple after converting to grid coordinates
    '''
    a=True
    while a:
        while True:
            pygame.event.get()
            if pygame.mouse.get_pressed()[0]:
                coord=(pygame.mouse.get_pos())
                break
    
        if coord[0]<h/3:
            if coord[1]<h/3:
                yx=(0,0)
            elif coord[1]<2*h/3:
                yx=(1,0)
            elif coord[1]<h:
                yx=(2,0)
                
        elif coord[0]<2*h/3:
            if coord[1]<h/3:
                yx=(0,1)
            elif coord[1]<2*h/3:
                yx=(1,1)
            elif coord[1]<h:
                yx=(2,1)
                
        elif coord[0]<h:
            if coord[1]<h/3:
                yx=(0,2)
            elif coord[1]<2*h/3:
                yx=(1,2)
            elif coord[1]<h:
                yx=(2,2)

        if grid[yx[0]][yx[1]]==None:
            return yx
            a=False
   

def cross(coord):
    #draw a cross [PYGAME] and stores it as 1 in matrix
    y,x=coord
    if mode=="s":
        pygame.time.wait(500)
    pygame.draw.line(wind,[0,75,255],(int(x*h/3+h/20),int(y*h/3+h/20)),(int(x*h/3+(h/3-h/20)),int(y*h/3+(h/3-h/20))),4)
    pygame.draw.line(wind,[0,75,255],(int(x*h/3+h/20),int(y*h/3+(h/3-h/20))),(int(x*h/3+(h/3-h/20)),int(y*h/3+h/20)),4)
    pygame.display.update()
    grid[y][x]="x"
    
def zero(coord):
    #draw a zero [PYGAME] and stores it as 0 in matrix
    y,x=coord
    pygame.draw.circle(wind,[0,225,75],(int(x*h/3+h/6),int(y*h/3+h/6)),int(h/8),4)
    pygame.display.update()
    grid[y][x]="o"
    

'''COMMON FUNCTIONS'''

def winreporter(status):
    """reports the winner
    win=None means in progress
    win=0 means draw
    win=1 means player one (cross) wins
    win=-1 means player two(zero) wins
    """
    pygame.time.wait(500)
    if status==1:
        screentext=verybigfont.render("CROSS WINS!!",True,[255,0,0])
        wind.blit(screentext,(int(h/5.5),int(h/2-h/10)))
    elif status==-1:
        screentext=verybigfont.render("ZERO WINS!!",True,[255,0,0])
        wind.blit(screentext,(int(h/5),int(h/2-h/10)))
    elif status==0:
        screentext=verybigfont.render("DRAW!!",True,[255,0,0])
        wind.blit(screentext,(int(h/3),int(h/2-h/10)))
        
    pygame.display.update()
    pygame.time.wait(2000)

    
def decisionmaker(grid):
    #makes decision of win,draw,loss using grid[]
    win=None
    #0 is draw, 1 is cross(comp) win, -1 is zero(user) win
    
    #cross's victory
    for i in range(3):
        if grid[0][i]==grid[1][i]==grid[2][i]=="x" or grid[i][0]==grid[i][1]==grid[i][2]=="x":
            win=1
    if grid[0][0]==grid[1][1]==grid[2][2]=="x":
        win=1
    if grid[2][0]==grid[1][1]==grid[0][2]=="x":
        win=1

    #zero's victory
    for i in range(3):
        if grid[0][i]==grid[1][i]==grid[2][i]=="o" or grid[i][0]==grid[i][1]==grid[i][2]=="o":
            win=-1
    if grid[0][0]==grid[1][1]==grid[2][2]=="o":
        win=-1
    if grid[2][0]==grid[1][1]==grid[0][2]=="o":
        win=-1

    #draw
    if win==None:
        full=True
        for i in range(3):
            for j in range(3):
                if grid[i][j]==None:
                    full=False
                    break
            if full==False:
                break
        if full==True:
            win=0
    return win


'''MULTIPLAYER FUNCTION'''

def multiplayer():
    matrix(wind,h)
    """first click gets cross. value of "i" will be o for "zero" and 1 for cross"""
    win=None
    """win=0 means in progress
        win=1 means draw
        win=2 means player one (cross) wins
        win=3 means player two(zero) wins
    """
    i=1
    gamerecord=[]
    while win==None:
        if i==1:
            yx=click(grid)
            cross(yx)
            gamerecord.append((yx[0],yx[1]))
            i=0
        elif i==0:
            yx=click(grid)
            zero(yx)
            gamerecord.append((yx[0],yx[1]))
            i=1
        win=decisionmaker(grid)
    winreporter(win)
    storegame(gamerecord,win,"s",False)


'''DATABASE RELATED FUNCTIONS'''

def randommove():
    while True:
        yx=(r.randint(0,2),r.randint(0,2))
        if grid[yx[0]][yx[1]]==None:
            return yx
        
def storegame(lis,win,mode,playerstarts):
    #first element of gamerecord stores "1" is the starter wins and stores"-1" if starter loses
    #0 is stored in case of draw

    #deciding first element
    if mode=="s":
        if (win==1 and not playerstarts) or (win==-1 and playerstarts):
            lis=[1]+lis
        elif (win==-1 and not playerstarts) or (win==1 and playerstarts):
            lis=[-1]+lis
        elif win==0:
            lis=[0]+lis
    elif mode=="m":
        lis=[win]+lis
        
    #making remaining elements as "-1" 
    lis=lis+([-1]*(10-len(lis)))

    
    if checkandadd:  
        with open(filename,"r",newline="") as file:
            rows=csv.reader(file)
            
            #checking if same game has been played before
            for row in rows:
                f=0
                for i in range(10):
                    if row and row[i]==str(lis[i]):
                        f+=1
                if f==10:
                    print("i have played this exact game once before")
                    break
            else:
                with open (filename,"a",newline='')as file1:
                    writer=csv.writer(file1,delimiter=",")
                    writer.writerow(lis)
    else:
        with open (filename,"a",newline='')as file1:
            writer=csv.writer(file1,delimiter=",")
            writer.writerow(lis)
                        
       
def movedb(trial,gamerecord,playerstarts):
    if trial or (not gamerecord and not playerstarts): #if trial or firstmove
        return randommove() 
    else:

        #----------reading
        m=len(gamerecord)
        with open(filename,"r")as file:
            rows=csv.reader(file)

            usefulrows=[]
            for row in rows:
                #first element of row is win/loss. rest are the moves
                if len(row)==10:
                    for i in range(1,m+1):
                        p=row[i]
                        if str(p) not in "-10" and str2tup(p)!=gamerecord[i-1]:                        
                                break
                            
                    else:       #checking for rows having all same previous moves
                        usefulrows.append(row)
            
            #----------deciding next best move
            if usefulrows:
                l1=[] #list of possible next moves
                
                for i in range(len(usefulrows)):
                    row=list(usefulrows[i])
                    nextmove=row[m+1]
                    #m is no of moves already happened
                    reverseofnumberofmovesleft= m+row.count("-1")

                    wl=int(usefulrows[i][0]) #p:PUNISH MORE FOR LOSING THAN REWARD FOR WINNING
                    if (playerstarts and wl==1) or (not playerstarts and wl==-1):
                        p=number
                    else :
                        p=1
                    
                    usefulrows[i][0]=int(wl)*reverseofnumberofmovesleft*p
                    if nextmove not in l1 and nextmove!="-1":                        
                        l1.append(nextmove)
                   
                l2=[0 for i in range(len(l1))] #list of corresponing averages
                for i in range(len(l1)):
                    avg=0
                    n=0
                    for row in usefulrows:
                        if row[m+1]==l1[i]:
                            avg=((avg*n)+int(row[0]))/(n+1)
                            n+=1
                    l2[i]=avg

            #----------doing the best move    
                if playerstarts:
                    #IF player STARTS
                    k=min(l2)                   
                    if k!=9:
                        move=(l1[l2.index(k)]) #it is in string format
                        return(str2tup(move))
                    else:
                        return randommove()
                else:
                    #if comp starts
                    k=max(l2)                    
                    if k!=-9:
                        move=(l1[l2.index(k)])
                        return(str2tup(move))
                    else:
                        return randommove()

            else: #there are no useful rows
                return randommove()
            

def str2tup(s1):
    #csv stores tuples as string so we need to convert back
    return (int(s1[1]),int(s1[4]))


def whostarts():
    #interface for choosing starter
    W=pygame.display.set_mode((h,h))
    
    pygame.draw.line(W, [0,0,255], (300,0), (300,600), 5)

    c1=[0,255,255]  
    c2=[123,123,123]

    putbigtext("USER",c1,(int(h/6)+8,int(4.6*h/10)-20),W)
    putbigtext("STARTS",c1,(int(h/6)-8,int(5.4*h/10)-20),W)

    putbigtext("COMPUTER",c1,(int(2*h/3)-35,int(4.6*h/10)-20),W)
    putbigtext("STARTS",c1,(int(2*h/3)-8,int(5.4*h/10)-20),W)

    pygame.display.update()

    while True:
        while True:
            pygame.event.get()
            if pygame.mouse.get_pressed()[0]:
                coord=(pygame.mouse.get_pos())
                pygame.time.wait(250)
                break
        #click on a mode    
        if 0 < coord[0]<int(h/2):
            #player starts
            pygame.display.quit()
            return True
            
        else:
            pygame.display.quit()
            return False
        
    
def mlgame(playerstarts):
    #game starts
    matrix(wind,h)
    gamerecord=[]
    mover=playerstarts
    win=None#game in progress

    while win == None:
        if mover == False:
            yx=movedb(trial,gamerecord,playerstarts)
            cross(yx)
            gamerecord.append((yx[0],yx[1]))
        else:
            yx=click(grid)
            zero(yx)
            gamerecord.append((yx[0],yx[1]))
        mover=not mover
        
        win=decisionmaker(grid)
    winreporter(win)
    storegame(gamerecord,win,"s",playerstarts)


def compplaysagainstitslef():
    #for developers only
    win=None
    i=True
    gamerecord=[]
    while win==None:
        '''CAN CHOOSE IF COMPUTER CAN USE DATABASE WHILE PLAYING ITSELF'''
        if i==True:
            #yx=movedb(trial,gamerecord,False)
            y,x=randommove()
            grid[y][x]="x"
            gamerecord.append((y,x))
            i=not i
        elif i==False:
            #yx=movedb(trial,gamerecord,True)
            y,x=randommove()
            grid[y][x]="o"
            gamerecord.append((y,x))
            i=not i
        win=decisionmaker(grid)
    storegame(gamerecord,win,"m",False)
    if game_no%50==0:
        print(game_no)
        
    
#----------------------------------------------------------- 


'''RUNNING THE GAME'''

game_no=0

#for data collection purposes
if playingfordata: 
    while True:
        grid=[[None for i in range (3)] for j in range (3)]        
        compplaysagainstitslef()
        game_no+=1

while True:
    #choosing window
    choosewin=pygame.display.set_mode((h,h))
    mode=modesel(choosewin,game_no)
    
    while True:
        #main window
        
        '''
        create grid
        (0,0)  (0,1)  (0,2)
        (1,0)  (1,1)  (1,2)
        (2,0)  (2,1)  (2,2)
        '''
        grid=[[None for i in range (3)] for j in range (3)]
        
        #running multiplayer
        if mode=="m":
            wind=pygame.display.set_mode((h,h))
            pygame.display.update()
            
            multiplayer()
            game_no+=1
            break

        #running singleplayer
        elif mode=="s":
            playerstarts=whostarts()
            wind=pygame.display.set_mode((h,h))
            pygame.display.update()
            
            mlgame(playerstarts)
            game_no+=1
            break
        
        elif mode=="q":
            break       
    if mode=="q":
        pygame.quit()
        quit()

    pygame.display.quit()

'''END'''
    
