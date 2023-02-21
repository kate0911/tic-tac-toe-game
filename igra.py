from tkinter import *
import random
import time

class Player:
    name = "Player"
    isPC = False   
    history = []
    cr=" "
   
    def __init__(self):
        self.isPC=False
    def getName(self):
        return self.name
    def getIsPC(self):
        return self.isPC
    def historyAppend(self, turn):
        self.history.append(turn)
    def getHistory(self):
        return self.history
    def getCr(self):
        return self.cr
    def setName(self,NAME):
        self.name=NAME
    def setCr(self,CR):
        self.cr=CR
    def setPC(self,is_pc):
        self.isPC=is_pc
        print (self.name,self.isPC)
    def setHistory(self,history):
        self.history=history[:]
    def clear(self):
        self.history=[]
        
        

class Game:
    player1=""
    player2=""
    n = 0
    p = 0
    currentPlayer = 1
    field = []
    root=""
    game_run=True
    PC=False
    row=0
    col=0
    strategy=False
    steps=0
    lab_curPl=""
    mainmenu=""
    menuBG=""
    menuXOcol=""
    result=0
    turn=0
    def __init__(self,Pl1,Pl2,N,P,CurPl,strategy):
        self.player1=Pl1
        self.player2 = Pl2
        self.n = N
        self.p = P
        self.currentPlayer = CurPl
        self.turn=CurPl
        self.PC=self.player2.getIsPC()
        self.strategy=strategy
        self.root = Tk()
        self.widg()
        
    def getCurPl(self):
        #print ("curr",self.currentPlayer)
        if self.currentPlayer==1:
            return self.player1
        if self.currentPlayer==2:
            return self.player2

    def getCurPlnum(self):
        return self.currentPlayer
        
        
    def click(self,row, col):
        self.row=row
        self.col=col
        if self.game_run and self.field[row][col]['text'] == ' ':
            self.field[row][col]['text'] = self.getCurPl().getCr()
            self.steps+=1
            list1=self.getCurPl().getHistory()[:]
            list1.append((self.row,self.col))
            self.getCurPl().history=list1[:]
            list1=[]
            if self.check_win(self.getCurPl().getCr()):
                self.result=self.currentPlayer
                self.game_run=False
            if self.game_run and self.steps<self.n*self.n:
                if self.PC==True:
                    self.computer_move()
                    self.steps+=1
                    if self.check_win(self.player2.getCr()):
                        self.result=2
                        self.game_run=False
                    list1=self.player2.getHistory()[:]
                    list1.append((self.row,self.col))
                    self.player2.history=list1[:]
                    list1=[]
                else:
                    self.switchCurrentPlayer()
                    #print("vhkvvhv")
        if self.game_run==False:
            self.win()


    def win(self):
        text=""
        if self.result==1:
            text=self.player1.getName()+" выиграл!"
        if self.result==2:
            text=self.player2.getName()+" выиграл!"
        self.lab_curPl['text']=text
        for row in range (self.n):
            for col in range (self.n):
                self.field[row][col]['state']='disabled'
        self.root.update()
        for row in range (self.n):
            for col in range (self.n):
                if self.field[row][col]['text']!=" ":
                    time.sleep(0.5)
                    self.field[row][col]['text']=" "
                    self.root.update()
        for row in range (self.n):
            for col in range (self.n):
                self.field[row][col]['state']='normal'
        self.game_run=True
        self.result=0
        self.player1.clear()
        #print(self.player1.getHistory())
        self.player2.clear()
        self.steps=0
        for row in range (self.n):
            for col in range (self.n):
                self.field[row][col]['bg']='lavender'
        self.lab_curPl['text']=self.getCurPl().getName()+" "+self.getCurPl().getCr()
        
        
                
    def can_win(self,a,smb):
        #print("zashel9")
        res = False
        checkSpace=0
        checkSmb=0
        iSpace=0
        #print("zashel7")
        for i in a:
            if i['text']==smb:
                checkSmb+=1
            elif i['text']==' ':
                #
                checkSpace+=1
                iSpace=i
                if checkSpace==2:
                    break
        c=0
        if checkSmb==len(a)-1 and checkSpace==1:
            iSpace['text']=self.player2.getCr()
            for i in range (self.n):
                for j in range (self.n):
                    if self.field[i][j]==iSpace:
                        self.comp_x=i
                        self.row=i
                        self.col=j
                        c=1
                        break
                if c==1:
                    break
            res=True
        return res

    def get_result(self):
        if self.game_run and self.steps<self.n*self.n:
            return 3
        return self.result


    def computer_move(self):
        #print("Выиграю",self.strategy)
        if self.n==3 and self.p==3 and self.strategy:
            if self.field[1][1]['text']==' ':
                self.field[1][1]['text']=self.player2.getCr()
                self.row=1
                self.col=1
                return
            #print("Выиграю")
            for n in range(3):
                if self.can_win([self.field[n][0], self.field[n][1], self.field[n][2]], self.player2.getCr()):
                    return
                if self.can_win([self.field[0][n], self.field[1][n], self.field[2][n]], self.player2.getCr()):
                    return
                if self.can_win([self.field[0][0], self.field[1][1], self.field[2][2]], self.player2.getCr()):
                    return
                if self.can_win([self.field[2][0], self.field[1][1], self.field[0][2]], self.player2.getCr()):
                    return
            for n in range(3):
                if self.can_win([self.field[n][0], self.field[n][1], self.field[n][2]], self.player1.getCr()):
                    return
                if self.can_win([self.field[0][n], self.field[1][n], self.field[2][n]], self.player1.getCr()):
                    return
                if self.can_win([self.field[0][0], self.field[1][1], self.field[2][2]], self.player1.getCr()):
                    return
                if self.can_win([self.field[2][0], self.field[1][1], self.field[0][2]], self.player1.getCr()):
                    return
        while True:
            #print("zashel4")
            row = random.randint(0, self.n-1)
            col = random.randint(0, self.n-1)
            self.row=row
            self.col=col
            #print(row,col)
            if self.field[row][col]['text'] == ' ':
                self.field[row][col]['text'] = self.player2.getCr()
                break

    def widg(self):
        self.root.title('Criss-cross')
        self.mainmenu=Menu(self.root)
        self.root.config(menu=self.mainmenu)
        self.menuBG=Menu(self.mainmenu,tearoff=0)
        self.menuXOcol=Menu(self.mainmenu,tearoff=0)
        self.mainmenu.add_cascade(label='Цвет поля',menu=self.menuBG)
        self.menuBG.add_command(label='Персиковый', command=lambda a=1:self.changeBGcolour(a))
        self.menuBG.add_command(label='Голубой', command=lambda a=2:self.changeBGcolour(a))
        self.mainmenu.add_cascade(label='Цвет X и O',menu=self.menuXOcol)
        self.menuXOcol.add_command(label='Бордовый', command=lambda a=1:self.changeXOcol(a))
        self.menuXOcol.add_command(label='Черный', command=lambda a=2:self.changeXOcol(a) )
        for row in range(self.n):
            line = []
            for col in range(self.n):
                self.button = Button(self.root, text=' ', width=4, height=2, 
                                font=('Verdana', 20, 'bold'),
                                background='lavender',
                                command=lambda row=row, col=col: self.click(row,col))
                self.button.grid(row=row, column=col, sticky='nsew')
                line.append(self.button)
            self.field.append(line)
        #print(type(self.player1),type(self.player2),type(self.getCurPl()))
        self.lab_curPl=Label(self.root,
                        text=self.getCurPl().getName()+" "+self.getCurPl().getCr(),
                        font=('Verdana', 10, 'bold'),background='lavender')
        self.lab_curPl.grid(row=self.n,column=0,columnspan=self.n)
        if len(self.player1.getHistory())>0 or len(self.player1.getHistory())>0:
            for i in self.player1.getHistory():
                row=i[0]
                col=i[1]
                self.field[row][col]['text']=self.player1.getCr()
            self.row=i[0]
            self.col=i[1]
            self.check_win(self.player1.getCr())
            print(self.player1.getCr())
            for i in self.player2.getHistory():
                row=i[0]
                col=i[1]
                self.field[row][col]['text']=self.player2.getCr()
            self.row=i[0]
            self.col=i[1]
            self.check_win(self.player2.getCr())
        self.root.mainloop()

    def changeBGcolour(self,a):
        if a==1:
            for i in range(len(self.field)):
                for j in range(len(self.field)):
                    if self.field[i][j]['bg']!='pink':
                        self.field[i][j]['bg']='peach puff'
        else:
            for i in range(len(self.field)):
                for j in range(len(self.field)):
                    if self.field[i][j]['bg']!='pink':
                        self.field[i][j]['bg']='lavender'

    def changeXOcol(self,a):
        if a==1:
            for i in range(len(self.field)):
                for j in range(len(self.field)):
                    self.field[i][j]['fg']='crimson'
        else:
            for i in range(len(self.field)):
                for j in range(len(self.field)):
                    self.field[i][j]['fg']='black'
        
    def switchCurrentPlayer(self):
        if self.currentPlayer == 1:
            self.currentPlayer = 2
        elif self.currentPlayer == 2:
            self.currentPlayer = 1
        #print ("switch",self.currentPlayer)
        self.lab_curPl['text']=self.getCurPl().getName()+" "+self.getCurPl().getCr()

    def check_win(self,smb):
        c=0
        k=smb
        row=self.row
        col=self.col
        row1=row
        col1=col
        list1=[]
        list1.append(self.field[row1][col1])
        #по строчкам
        while k==smb:
            c+=1
            list1.append(self.field[row1][col1])
            if col1>0:
                col1-=1
                k=self.field[row1][col1]['text']
                #print("Vlevo",row1,col1)
            else:
                k="g"
        if col+1<self.n:
            col1=col+1
            k=self.field[row1][col1]['text']
            #print("Vpravo",row1,col1)
        while k==smb:
            list1.append(self.field[row1][col1])
            c+=1
            if col1<self.n-1:
                col1+=1
                k=self.field[row1][col1]['text']
                #print("Vpravo",row1,col1)
            else:
                k="g"
        if c>=self.p:
            self.game_run=False
            for i in list1:
                i['background']='pink'
            return True
        #по столбцам
        list1=[]
        c=0
        k=smb
        row1=row
        col1=col
        while k==smb:
            c+=1
            list1.append(self.field[row1][col1])
            if row1>0:
                row1-=1
                #print("gkjhgkjhfg",self.field[row1][col1])
                k=self.field[row1][col1]['text']
                #print("Vverh",row1,col1)
            else:
                k="g"
        if row+1<self.n:
            row1=row+1
            k=self.field[row1][col1]['text']
        while k==smb:
            c+=1
            list1.append(self.field[row1][col1])
            if row1<self.n-1:
                row1+=1
                k=self.field[row1][col1]['text']
                #print("Vniz",row1,col1)
            else:
                k="g"
        if c>=self.p:
            for i in list1:
                i['background']='pink'
            self.game_run=False
            return True
        #по диагонали
        c=0
        k=smb
        list1=[]
        col1=col
        row1=row
        while k==smb:
            c+=1
            list1.append(self.field[row1][col1])
            if row1>0 and col1>0:
                row1-=1
                col1-=1
                k=self.field[row1][col1]['text']
                #print("Diag1",row1,col1)
            else:
                k="g"
        if row<self.n-1 and col<self.n-1:
            row1=row+1
            col1=col+1
            #print(self.field[row1][col1])
            k=self.field[row1][col1]['text']
        while k==smb:
            list1.append(self.field[row1][col1])
            c+=1
            if row1<self.n-1 and col1<self.n-1:
                row1+=1
                col1+=1
                k=self.field[row1][col1]['text']
                #print(row1,col1)
            else:
                k="g"
        if c>=self.p:
            #print (list1)
            for i in list1:
                i['background']='pink'
            self.game_run=False
            return True
        #по другой диагонали
        c=0
        k=smb
        col1=col
        row1=row
        list1=[]
        while k==smb:
            list1.append(self.field[row1][col1])
            c+=1
            if row1>0 and col1+1<self.n:
                row1-=1
                col1+=1
                k=self.field[row1][col1]['text']
                #print("Diag2",row1,col1)
            else:
                k="g"
        if row<self.n-1 and col>0:
            row1=row+1
            col1=col-1
            k=self.field[row1][col1]['text']
        while k==smb:
            list1.append(self.field[row1][col1])
            c+=1
            if row1<self.n-1 and col1>0:
                row1+=1
                col1-=1
                k=self.field[row1][col1]['text']
                #print(row1,col1)
            else:
                k="g"
        if c>=self.p:
            self.game_run=False
            #print(list1)
            for i in list1:
                i['background']='pink'
            return True
        #print("pl1",self.player1.getHistory())
        #print("pl2",self.player2.getHistory())
        return False
  
class Dialog:
    PC=False
    N=0
    P=0
    player1=Player()
    player2=Player()
    name1=""
    name2=""
    dialog=Tk()
    dialog_comp=""
    dialog_hum=""
    cr=""
    widget=""
    window=""
    win_tac=False
    cond=0
    turn=0
    def __init__(self):
        self.dialog.title('PC or not')
        PC_but = Button(self.dialog, text='Компьютер', width=20, height=2, 
                                font=('Verdana', 20, 'bold'),
                                background='lavender',
                                command=self.PC_but_fun)
        hum_but = Button(self.dialog, text='Человек', width=20, height=2, 
                                font=('Verdana', 20, 'bold'),
                                background='lavender',
                                command=self.hum_but_fun)
        cont_but = Button(self.dialog, text='Продолжить', width=20, height=2, 
                                font=('Verdana', 20, 'bold'),
                                background='lavender',
                                command=self.cont_but_fun)
        PC_but.pack()
        hum_but.pack()
        cont_but.pack()
        self.dialog.mainloop()
    def getTurn(self):
        return self.turn
    def cont_but_fun(self):
        file = open("game.txt", "r")
        list1=file.readline().split(' ')
        self.N=int(list1[0])
        self.P=int(list1[1])
        self.turn=int(list1[2])
        self.cond=int(list1[3])
        list1=file.readline().split(' ')
        self.player1.setName(list1[0])
        self.player1.setPC(False)
        self.player1.setCr(list1[2])
        steps1=int(list1[3])
        list2=[]
        for i in range (steps1):
            list1=file.readline().split(' ')
            #print(list1)
            list2.append((int(list1[0]),int(list1[1])))
        self.player1.setHistory(list2)
        list1=[]
        list1=file.readline().split(' ')
        self.player2.setName(list1[0])
        print(list1[1],"ggggg")
        if int(list1[1])==1:
            self.player2.setPC(True)
            print(list1[1],"7777")
        else:
            self.player2.setPC(False)
            print(list1[1],"ggggg")
        print("4444",self.player2.getIsPC())
        self.player2.setCr(list1[2])
        steps1=int(list1[3])
        list2=[]
        for i in range (steps1):
            list1=file.readline().split(' ')
            #print(list1)
            list2.append((int(list1[0]),int(list1[1])))
        self.player2.setHistory(list2)
        #print(self.player1.getHistory())
        #print(self.player2.getHistory())
        file.close()
        self.dialog.destroy()
    def PC_but_fun(self):
        self.PC=True
        self.dialog.destroy()
        self.dial_comp_fun()
    def hum_but_fun(self):
        self.PC=False
        self.dialog.destroy()
        self.dial_hum_fun()
    def dial_comp_fun(self):
        self.player2.setPC(True)
        self.player1.setPC(False)
        self.dialog_comp=Tk()    
        self.dialog_comp.title('Game with PC')
        self.name1=StringVar()
        self.cr=IntVar()
        self.N=IntVar()
        self.N.set(3)
        self.P=IntVar()
        self.P.set(3)
        self.cr.set(0)
        lab_scale_n=Label(self.dialog_comp,text="n=",
                          font=('Verdana', 10, 'bold'),background='lavender')
        lab_scale_p=Label(self.dialog_comp,text="p=",
                          font=('Verdana', 10, 'bold'),background='lavender')
        scale_n = Scale(self.dialog_comp, orient="horizontal",
                        resolution=1, from_=2, to=7, variable=self.N)
        scale_p = Scale(self.dialog_comp, orient="horizontal",
                        resolution=1, from_=2, to=7, variable=self.P)
        lab_name = Label(self.dialog_comp,text="Имя",
                         font=('Verdana', 10, 'bold'),background='lavender')
        input_name_pl1=Entry(self.dialog_comp,textvariable=self.name1,
                             width=15,bg='pink',font=('Verdana', 20))
        self.name1.set("Player1")
        lab_cr = Label(self.dialog_comp,text="X или O",
                       font=('Verdana', 10, 'bold'),background='lavender')
        X_checkbutton = Radiobutton(text="X",variable=self.cr,value=0)
        O_checkbutton = Radiobutton(text="O",variable=self.cr,value=1)
        warning = Label(self.dialog_hum,
                        text="Внимание!\nЕсли Вы установите значение p>n,\nпо умолчанию будет принято p=n.",
                        font=('Verdana', 10, 'bold'),background='lavender')
        OK_but = Button(self.dialog_comp, text='OK', width=2, height=1, 
                                font=('Verdana', 10, 'bold'),
                                background='lavender',
                                command=self.OK_press)
        lab_name.pack()
        input_name_pl1.pack()
        lab_cr.pack()
        X_checkbutton.pack()
        O_checkbutton.pack()
        lab_scale_n.pack()
        scale_n.pack()
        lab_scale_p.pack()
        scale_p.pack()
        warning.pack()
        OK_but.pack()
        self.dialog_comp.mainloop()

    def dial_hum_fun(self):
        self.player2.setPC(False)
        self.player1.setPC(False)
        self.dialog_hum=Tk()
        self.dialog_hum.title('Game with human')
        self.name1=StringVar()
        self.name2=StringVar()
        self.cr=IntVar()
        self.cr.set(0)
        self.N=IntVar()
        self.N.set(3)
        self.P=IntVar()
        self.P.set(3)
        lab_scale_n=Label(self.dialog_hum,text="n=",
                          font=('Verdana', 10, 'bold'),background='lavender')
        lab_scale_p=Label(self.dialog_hum,text="p=",
                          font=('Verdana', 10, 'bold'),background='lavender')
        scale_n = Scale(self.dialog_hum, orient="horizontal",
                        resolution=1, from_=2, to=7, variable=self.N)
        scale_p = Scale(self.dialog_hum, orient="horizontal",
                        resolution=1, from_=2, to=7, variable=self.P )
        lab_name = Label(self.dialog_hum,text="Имя первого игрока",
                         font=('Verdana', 10, 'bold'),background='lavender')
        lab_name2 = Label(self.dialog_hum,text="Имя второго игрока",
                          font=('Verdana', 10, 'bold'),background='lavender')
        input_name_pl1=Entry(self.dialog_hum,textvariable=self.name1,
                             width=15,bg='pink',font=('Verdana', 20))
        self.name1.set("Player1")
        self.name2.set("Player2")
        input_name_pl2=Entry(self.dialog_hum,textvariable=self.name2,
                             width=15,bg='pink',font=('Verdana', 20))
        lab_cr = Label(self.dialog_hum,text="X или O, выбирает игрок 1",
                       font=('Verdana', 10, 'bold'),background='lavender')
        X_checkbutton = Radiobutton(text="X",variable=self.cr,value=0)
        O_checkbutton = Radiobutton(text="O",variable=self.cr,value=1)
        OK_but = Button(self.dialog_comp, text='OK', width=2, height=1, 
                                font=('Verdana', 10, 'bold'),
                                background='lavender',
                                command=self.OK_press)
        warning = Label(self.dialog_hum,
                        text="Внимание!\nЕсли Вы установите значение p>n,\nпо умолчанию будет принято p=n.",
                        font=('Verdana', 10, 'bold'),background='lavender')
        lab_name.pack()
        input_name_pl1.pack()
        lab_name2.pack()
        input_name_pl2.pack()
        lab_cr.pack()
        X_checkbutton.pack()
        O_checkbutton.pack()
        lab_scale_n.pack()
        scale_n.pack()
        lab_scale_p.pack()
        scale_p.pack()
        warning.pack()
        OK_but.pack()
        self.dialog_hum.mainloop()        

    def OK_press(self):
        self.N=self.N.get()
        if self.N>=self.P.get():
            self.P=self.P.get()
            if self.PC:
                self.dialog_comp.destroy()
                print("desstroyyy")
            else:
                self.dialog_hum.destroy()
                print("dddddesstroyyy")
        else:
            self.P=self.N
            if self.PC:
                self.dialog_comp.destroy()
                print("desstroyyy")
            else:
                self.dialog_hum.destroy()
                print("dddddesstroyyy")
            
        #print(self.N,self.P)
        if self.N==3 and self.P==3 and self.PC==True:
            self.win_tac_fun()
        self.player1.setName(self.name1.get())
        if self.PC:
            self.player2.setName("PC")
        else:
            self.player2.setName(self.name2.get())
            #self.dialog_hum.destroy()
        if self.cr.get()==0:
            self.player1.setCr("X")
            self.player2.setCr("O")
            #print("X")
        else:
            self.player1.setCr("O")
            self.player2.setCr("X")
            #print("O")
        #self.window.destroy()
    def get_player1(self):
        return self.player1
    def get_player2(self):
        return self.player2
    def is_PC(self):
        return self.PC
    def get_N(self):
        return self.N
    def get_P(self):
        return self.P
    def win_tac_fun(self):
        self.widget=Tk()
        label=Label(self.widget,text="Беспроигрышная стратегия?", font=('Verdana', 10, 'bold'),background='lavender')
        but1 = Button(self.widget, text='Да', width=2, height=1, 
                                font=('Verdana', 10, 'bold'),
                                background='lavender',
                                command=self.win_tac_yes)
        but2 = Button(self.widget, text='Нет', width=2, height=1, 
                                font=('Verdana', 10, 'bold'),
                                background='lavender',
                                command=self.win_tac_no)
        label.pack()
        but1.pack()
        but2.pack()
        self.widget.mainloop()
    def win_tac_yes(self):
        self.win_tac=True
        self.widget.destroy()
    def win_tac_no(self):
        self.widget.destroy()
    def get_tac(self):
        return self.win_tac
    def get_turn(self):
        return self.turn


dial=Dialog()
#print(turn)
if dial.is_PC():
    turn=1
else:
    turn=random.randint(1,2)
if len(dial.get_player1().getHistory())>0 or len(dial.get_player2().getHistory())>0:
    turn=dial.get_turn()
game=Game(dial.get_player1(),dial.get_player2(),dial.get_N(),dial.get_P(),turn,dial.get_tac())
if dial.is_PC():
    turn=1
else:
    turn=game.getCurPlnum()
print("11111")
file = open("game.txt", "w")
file.write(str(dial.get_N())+" "+str(dial.get_P())+" "+str(game.getCurPlnum())+" "+str(game.get_result())+"\n")
file.write(dial.get_player1().getName())
file.write(" 0 ")
file.write(dial.get_player1().getCr()+" ")
file.write(str(len(dial.get_player1().getHistory()))+"\n")
list1=dial.get_player1().getHistory()[:]
for i in list1:
    for j in i:
        file.write(str(j)+" ")
    file.write("\n")
file.write(dial.get_player2().getName()+" ")
if dial.get_player2().getIsPC()==True:
    file.write("1 ")
    print("65787658675")
else:
    file.write("0 ")
file.write(dial.get_player2().getCr()+" ")
file.write(str(len(dial.get_player2().getHistory()))+"\n")
list1=dial.get_player2().getHistory()[:]
for i in list1:
    for j in i:
        file.write(str(j)+" ")
    file.write("\n")
    
file.close()


        
