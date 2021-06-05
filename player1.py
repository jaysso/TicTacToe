'''
Name: Jasmine Som
UCINetID: 60264498
'''

################# CLIENT MODULE ##################
import socket
import tkinter as tk
import gameboard as gb
from tkinter import messagebox
import threading

player = "X"
opponentbttn = {"Player2"} #to keep track of opponent wins
userbttn_set = {"Player1"}
bttnPushed = 0 #data to be sent and added to P2 oppponentbttn lst
button_lst = [] #lst of all buttons to access outside of class
winval = False
p1move = True
p1username = ""
p2username = ""
statsmem = [0,0,0,0,0]  # [p1win, p1loss, p2win, p2loss, ties]
tienum = 0
turninfo = []  # holder for manageTurns return values
names = ["", ""]  # lst of usernames
checker = []  # holder for isWinner return values
countmove = 0
data = ""
bttnsendinfo = []
winsets = [{'1', '2', '3'}, {'4', '5', '6'}, {'7', '8', '9'}, #all horizontal wins
           {'1', '4', '7'}, {'2', '5', '8'}, {'3', '6', '9'}, #all vertical wins
           {'1', '5', '9'}, {'3', '5', '7'}] #all diagonal wins


###################### TKINTER IU ######################
class gameRun(tk.Frame):
    global names, winsets, data, bttnPushed, p1Socket, countmove, turninfo, opponentbttn, p1move, button_lst, winval, player, userbttn_set, statsmem, tienum
    tttr = 0
    iswinoutput = []
    entryvalue = None
    numgame = 0


    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.tttr = gb.BoardClass()
        self.canvasSetup()
        self.canvasSetup()
        self.createbuttons()


    def canvasSetup(self):
        self.master.title("Tic-Tac-Toe: Player 1")
        self.master.geometry("430x300+100+100")
        self.welcome = tk.Label(self.master, text="Tic-Tac-Toe", font=("Verdana", "25")).grid(row=0, column=1, columnspan=3)
        self.spacer1 = tk.Label(self.master, text="  ", font=("Verdana", "20")).grid(row=0, column=0, rowspan=5)
        self.spacer = tk.Label(self.master, text=" ", font=("Verdana", "30")).grid(row=0, column=4, rowspan=5)
        self.stattitle = tk.Label(self.master, text="Game Stats", font=("Verdana", "20")).grid(row=0, column=5, columnspan=2)
        self.spacer2 = tk.Label(self.master, text="  ", font=("Verdana", "9")).grid(row=4, column=1, columnspan=3)
        self.tttr.getusernames(names[0], names[1], self.master)


    def buttonaction(self, button): ######  Pressing buttons will prompt actions and send info to opponent
        global winval, p1move, countmove, bttnPushed, turninfo, names, data
        winval = False
        button.config(text="X",bg="MistyRose3", fg="MistyRose2", state="disabled")
        self.iswinoutput = self.tttr.isWinner(userbttn_set, winsets, button_lst, winval, bttnsendinfo, button)
        winval = self.iswinoutput[0]
        bttnPushed = str(self.iswinoutput[1])
        if winval:
            for index in range(2,6):
                statsmem[index-2] = statsmem[index-2] + self.iswinoutput[index]
        p1Socket.send(bttnPushed.encode('ascii'))
        userbttn_set.add(bttnPushed)
        print()
        print("Your Move:", bttnPushed)
        turninfo = self.tttr.manageTurns(p1move, countmove, player, button_lst)
        countmove = turninfo[1]
        p1move = turninfo[0]
        self.checkgameend()


    def checkgameend(self): ## prints stats at the end of a game
        global tienum, countmove, player, winval
        if winval == True:
            self.tttr.endgame(button_lst)
            self.tttr.printStats(player, self.master, names, statsmem, p1move)
            self.call_popup(self)
            self.interpretuserentry()
            self.numgame = self.tttr.updateGamesPlayed()
            print()
            print("------ End of Game {} ------".format(self.numgame))
        elif winval == False and countmove == 9:
            self.tttr.endgame(button_lst)
            tienum = self.tttr.boardIsFull()
            statsmem[4] = tienum
            self.tttr.printStats(player, self.master, names, statsmem, p1move)
            self.call_popup(self)
            self.interpretuserentry()
            self.numgame = self.tttr.updateGamesPlayed()
            print()
            print("------ End of Game {} ------".format(self.numgame))


    def interpretuserentry(self):
        if self.entryvalue == "y" or self.entryvalue == "Y":
            self.pressedPlayAgain()
        if self.entryvalue == "n" or self.entryvalue == "N":
            self.windowquit()

    def createbuttons(self): ###### creating buttons and storing them in a global list to call later

        self.button1 = tk.Button(self.master, text="", bg="gray80", fg="white", activebackground="MistyRose3", activeforeground="MistyRose2", height=4, width=8)
        self.button1.configure(command=lambda: self.buttonaction(self.button1))
        self.button1.grid(row=1, column=1)
        button_lst.append(self.button1)
        bttnsendinfo.append('1')

        self.button2 = tk.Button(self.master, text="", bg="gray80", fg="white", activebackground="MistyRose3", activeforeground="MistyRose2", height=4, width=8)
        self.button2.configure(command=lambda: self.buttonaction(self.button2))
        self.button2.grid(row=1, column=2)
        button_lst.append(self.button2)
        bttnsendinfo.append('2')
        
        self.button3 = tk.Button(self.master, text="", bg="gray80", fg="white", activebackground="MistyRose3", activeforeground="MistyRose2", height=4, width=8)
        self.button3.configure(command=lambda: self.buttonaction(self.button3))
        self.button3.grid(row=1, column=3)
        button_lst.append(self.button3)
        bttnsendinfo.append('3')
        
        self.button4 = tk.Button(self.master, text="", bg="gray80", fg="white", activebackground="MistyRose3", activeforeground="MistyRose2", height=4, width=8)
        self.button4.configure(command=lambda: self.buttonaction(self.button4))
        self.button4.grid(row=2, column=1)
        button_lst.append(self.button4)
        bttnsendinfo.append('4')
        
        self.button5 = tk.Button(self.master, text="", bg="gray80", fg="white", activebackground="MistyRose3", activeforeground="MistyRose2", height=4, width=8)
        self.button5.configure(command=lambda: self.buttonaction(self.button5))
        self.button5.grid(row=2, column=2)
        button_lst.append(self.button5)
        bttnsendinfo.append('5')
        
        self.button6 = tk.Button(self.master, text="", bg="gray80", fg="white", activebackground="MistyRose3", activeforeground="MistyRose2", height=4, width=8)
        self.button6.configure(command=lambda: self.buttonaction(self.button6))
        self.button6.grid(row=2, column=3)
        button_lst.append(self.button6)
        bttnsendinfo.append('6')
        
        self.button7 = tk.Button(self.master, text="", bg="gray80", fg="white", activebackground="MistyRose3", activeforeground="MistyRose2", height=4, width=8)
        self.button7.configure(command=lambda: self.buttonaction(self.button7))
        self.button7.grid(row=3, column=1)
        button_lst.append(self.button7)
        bttnsendinfo.append('7')
        
        self.button8 = tk.Button(self.master, text="", bg="gray80", fg="white", activebackground="MistyRose3", activeforeground="MistyRose2", height=4, width=8)
        self.button8.configure(command=lambda: self.buttonaction(self.button8))
        self.button8.grid(row=3, column=2)
        button_lst.append(self.button8)
        bttnsendinfo.append('8')
        
        self.button9 = tk.Button(self.master, text="", bg="gray80", fg="white", activebackground="MistyRose3", activeforeground="MistyRose2", height=4, width=8)
        self.button9.configure(command=lambda: self.buttonaction(self.button9))
        self.button9.grid(row=3, column=3)
        button_lst.append(self.button9)
        bttnsendinfo.append('9')

        self.createquitbttn()


    def pressedPlayAgain(self): #######  action that occurs when typing "y/Y" in play again pop up window
        global opponentbttn, userbttn_set, winval, p1move, countmove
        global winval, countmove, opponentbttn, userbttn_set, p1Socket, p1move
        p1Socket.send("Play Again".encode('ascii'))  ### sending info to opponent to prompt their reset
        self.tttr.resetGameBoard(player, button_lst)   ### resetting all moves
        #### resetting global variables
        opponentbttn = {"Player2"}
        userbttn_set = {"Player1"}
        winval = False
        p1move = True
        countmove = 0
        self.__init__(self.master)


    def createquitbttn(self):
        self.quitbutton = tk.Button(self.master,text="  Quit  ", padx=3, font="Verdana",command=self.windowquit).grid(row=5, column=1, columnspan=3)


    def windowquit(self):
        p1Socket.send("Fun Times".encode('ascii'))
        self.master.destroy()
        p1Socket.close()


    def call_popup(self, master):
        self.again_popup = playAgain(master)
        self.again_popup.wait_window()



########## CLASS FOR GETTING USERNAME IN NEW WINDOW ##########
class getName(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.bind('<Return>',self.pressed)
        self.master.title("Register Username: Player 1")
        self.master.geometry("300x120+100+100")
        self.ask = tk.Label(self.master, text="Enter Username:", font=("Verdana", "12")).pack()
        self.name = tk.Entry(self.master)
        self.name.pack()
        self.okbttn = tk.Button(self.master, text="  OK  ", command=self.pressed).pack()
        self.info = tk.Label(self.master, text="Window will close and the game will begin\nwhen both players click OK.", font=("Verdana", "9")).pack()

    def pressed(self):
        global p1username
        p1username = self.name.get()
        self.master.destroy()
        p1Socket.send(p1username.encode('ascii'))



############## CLASS FOR PLAY AGAIN DIALOG WINDOW #############
class playAgain(tk.Toplevel):
    def __init__(self, master):
        tk.Toplevel.__init__(self, master)
        self.transient(master)
        self.master = master
        self.bind('<Return>',self.buttonpressed)
        self.ask = tk.Label(self, text="Would you like to play again?", font=("Verdana", "10")).pack()
        self.dir = tk.Label(self, text="Please enter \"y/Y\" or \"n/N\":", font=("Verdana", "10")).pack()
        self.e1 = tk.Entry(self)
        self.e1.pack()
        self.okbttn = tk.Button(self, text="  OK  ", command=self.buttonpressed).pack()

    def buttonpressed(self):
        self.master.entryvalue = self.e1.get()
        if self.master.entryvalue in validresponse:
            self.master.destroy()




###################### SOCKET CONNECTION ######################
print("------- Welcome Player 1 -------\n")
GB = gb.BoardClass()
loop = True
clientConnected = False



def createThread(target):
    thread = threading.Thread(target=target)
    thread.daemon = True
    thread.start()

##### COMMUNICATION AND INTERPRETATION #####
def receiveData(): #receiving a single button num pushed from the opponent (1 == "n")
    global opponentbttn, winsets, names, button_lst, winval, player, data, countmove, statsmem, p1move, checker
    while True:
        try:
            data = p1Socket.recv(1024).decode('ascii')
            if data == "Quit": ### closing window if opponent quits game
                messagebox.showinfo(title="Information", message="Player 2 has quit.\nThank you for playing.")
                ttt.destroy()
                p1Socket.close()
            elif data in ['1', '2', '3', '4', '5', '6', '7', '8', '9']:
                opponentbttn.add(data)
                print("Opponent Move:", data)
                GB.updateGameBoard(opponentbttn, button_lst, bttnsendinfo) # using button to disable the button opponent pressed
                checker = GB.isWinner(opponentbttn, winsets, button_lst, winval, bttnsendinfo) #checking if there is a winner
                winval = checker[0]
                if winval:
                    for index in range(2,6):
                        statsmem[index-2] = statsmem[index-2] + checker[index]
                turninfo = GB.manageTurns(p1move, countmove, player, button_lst)
                countmove = turninfo[1]
                p1move = turninfo[0]
                tictactoe.checkgameend()
            else:
                messagebox.showinfo(title="Error", message="Player 2 has lost connection. Closing window.")
                ttt.destroy()

        except:
            messagebox.showinfo(title="Error", message="Player 2 has lost connection. Closing window.")
            ttt.destroy()
            break







if __name__ == '__main__':
    while loop:
        validresponse = ["y","Y","n","N"]
        p1Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            p2IP = input("Please provide the IP address of Player 2: ")
            p2port = int(input("Please provide the port number of Player 2: "))
            p1Socket.connect((p2IP, p2port))
            print("\nWaiting to Connection...")
            namewindow = tk.Tk()
            getName(namewindow)
            namewindow.mainloop()
            p2username = p1Socket.recv(1024).decode('ascii')
            names = [p1username, p2username]
            createThread(receiveData)
            ttt = tk.Tk()
            tictactoe = gameRun(ttt)
            ttt.mainloop()
            p1Socket.close()
            loop = False

        except:
            print()
            userresponse = input("Error has occurred.\nWould you like to try again?\n")
            if userresponse == "y" or userresponse == "Y":
                loop = True
            elif userresponse == "n" or userresponse == "N":
                p1Socket.close()
                print("Connection attempt terminated.")
                loop = False
            else:
                while userresponse not in validresponse:
                    userresponse = input("Please enter \"y/Y\" or \"n/N\": ")
                if userresponse == "n" or userresponse == "N":
                    p1Socket.close()
                    print("Connection atttempt terminated")
                    loop = False













