'''
Name: Jasmine Som
UCINetID: 60264498
'''

############## SERVER MODULE ##############
import socket
import tkinter as tk
import gameboard as gb
import threading
from tkinter import messagebox

player = "O"
opponentbttn = {"Player1"}
userbttn_set = {"Player2"}
button_lst = []
bttnPushed = 0
p1username = ""
p2username = ""
winval = False
data = ""
p1move = True
statsmem = [0, 0, 0, 0, 0] # [p1win, p1loss, p2win, p2loss, ties]
turninfo = []
tienum = 0
names = ["", ""]
numgame = 0
countmove = 0
bttnsendinfo = []
winsets = [{'1', '2', '3'}, {'4', '5', '6'}, {'7', '8', '9'}, #all horizontal wins
           {'1', '4', '7'}, {'2', '5', '8'}, {'3', '6', '9'}, #all vertical wins
           {'1', '5', '9'}, {'3', '5', '7'}] #all diagonal wins



########## FOR TKINTER IU ############
class gameRun(tk.Frame):
    global names, winsets, p1username, numgame, bttnPushed, p1Socket, countmove, tienum, statsmem, turninfo, opponentbttn, button_lst, winval, p1move, player, userbttn_set
    tttr = 0
    iswinoutput = []


    def __init__(self, master=None):
        global names
        tk.Frame.__init__(self, master)
        self.tttr = gb.BoardClass()
        self.canvasSetup()
        self.createbuttons()


    def canvasSetup(self):
        self.master.title("Tic-Tac-Toe: Player 2")
        self.master.geometry("430x300+800+100")
        self.welcome = tk.Label(self.master, text="Tic-Tac-Toe", font=("Verdana", "25")).grid(row=0, column=1, columnspan=3)
        self.spacer1 = tk.Label(self.master, text="  ", font=("Verdana", "20")).grid(row=0, column=0, rowspan=5)
        self.spacer = tk.Label(self.master, text="  ", font=("Verdana", "20")).grid(row=0, column=4, rowspan=5)
        self.stattitle = tk.Label(self.master, text="Game Stats", font=("Verdana", "20")).grid(row=0, column=5, columnspan=2)
        self.spacer2 = tk.Label(self.master, text="  ", font=("Verdana", "9")).grid(row=4, column=1, columnspan=3)
        self.tttr.getusernames(names[0], names[1], self.master)


    def buttonaction(self, button):
        global winval, p1move, countmove, bttnPushed, turninfo, names, data
        button.config(text="O", bg="MistyRose3", fg="MistyRose2", state="disabled")
        self.iswinoutput = self.tttr.isWinner(userbttn_set, winsets, button_lst, winval, bttnsendinfo, button)
        winval = self.iswinoutput[0]
        if winval:
            for index in range(2, 6):
                statsmem[index-2] = statsmem[index-2] + self.iswinoutput[index]
        data = str(self.iswinoutput[1])
        userbttn_set.add(data)
        print()
        print("Your Move:", data)  # bttn info will need to be sent to opponent after bttn is pushed
        p1Socket.send(data.encode('ascii'))
        turninfo = self.tttr.manageTurns(p1move, countmove, player, button_lst)
        countmove = turninfo[1]
        p1move = turninfo[0]
        self.checkgameend()
### After playing again, p2 does not display button1 is pressed on p1 interface. problem with communication?

    def createquitbttn(self):
            self.quitbutton = tk.Button(self.master,text="  Quit  ", padx=3, font="Verdana",command=self.windowquit).grid(row=5, column=1, columnspan=3)


    def windowquit(self):
            p1Socket.send("Quit".encode('ascii'))
            self.master.destroy()
            p1Socket.close()


    def checkgameend(self):
        global tienum, countmove, player, p1move, numgame
        if winval == True:
            self.tttr.printStats(player, self.master, names, statsmem, p1move)
            numgame = self.tttr.updateGamesPlayed()
            print()
            print("------ End of Game ------")
            print()
        elif winval == False and countmove == 9:
            tienum = self.tttr.boardIsFull()
            statsmem[4] = tienum
            self.tttr.printStats(player, self.master, names, statsmem, p1move)
            numgame = self.tttr.updateGamesPlayed()
            print()
            print("------ End of Game ------")
            print()


    def createbuttons(self):

        self.button1 = tk.Button(self.master, text="", bg="gray80", fg="white", activebackground="MistyRose3", activeforeground="MistyRose2", height=4, width=8)
        self.button1.configure(state="disabled",command=lambda: self.buttonaction(self.button1))
        self.button1.grid(row=1, column=1)
        button_lst.append(self.button1)
        bttnsendinfo.append('1')

        self.button2 = tk.Button(self.master, text="", bg="gray80", fg="white", activebackground="MistyRose3", activeforeground="MistyRose2", height=4, width=8)
        self.button2.configure(state="disabled",command=lambda: self.buttonaction(self.button2))
        self.button2.grid(row=1, column=2)
        button_lst.append(self.button2)
        bttnsendinfo.append('2')
        
        self.button3 = tk.Button(self.master, text="", bg="gray80", fg="white", activebackground="MistyRose3", activeforeground="MistyRose2", height=4, width=8)
        self.button3.configure(state="disabled",command=lambda: self.buttonaction(self.button3))
        self.button3.grid(row=1, column=3)
        button_lst.append(self.button3)
        bttnsendinfo.append('3')

        self.button4 = tk.Button(self.master, text="", bg="gray80", fg="white", activebackground="MistyRose3", activeforeground="MistyRose2", height=4, width=8)
        self.button4.configure(state="disabled",command=lambda: self.buttonaction(self.button4))
        self.button4.grid(row=2, column=1)
        button_lst.append(self.button4)
        bttnsendinfo.append('4')
        
        self.button5 = tk.Button(self.master, text="", bg="gray80", fg="white", activebackground="MistyRose3", activeforeground="MistyRose2", height=4, width=8)
        self.button5.configure(state="disabled",command=lambda: self.buttonaction(self.button5))
        self.button5.grid(row=2, column=2)
        button_lst.append(self.button5)
        bttnsendinfo.append('5')
        
        self.button6 = tk.Button(self.master, text="", bg="gray80", fg="white", activebackground="MistyRose3", activeforeground="MistyRose2", height=4, width=8)
        self.button6.configure(state="disabled",command=lambda: self.buttonaction(self.button6))
        self.button6.grid(row=2, column=3)
        button_lst.append(self.button6)
        bttnsendinfo.append('6')
        
        self.button7 = tk.Button(self.master, text="", bg="gray80", fg="white", activebackground="MistyRose3", activeforeground="MistyRose2", height=4, width=8)
        self.button7.configure(state="disabled", command=lambda: self.buttonaction(self.button7))
        self.button7.grid(row=3, column=1)
        button_lst.append(self.button7)
        bttnsendinfo.append('7')
        
        self.button8 = tk.Button(self.master, text="", bg="gray80", fg="white", activebackground="MistyRose3", activeforeground="MistyRose2", height=4, width=8)
        self.button8.configure(state="disabled",command=lambda: self.buttonaction(self.button8))
        self.button8.grid(row=3, column=2)
        button_lst.append(self.button8)
        bttnsendinfo.append('8')
        
        self.button9 = tk.Button(self.master, text="", bg="gray80", fg="white", activebackground="MistyRose3", activeforeground="MistyRose2", height=4, width=8)
        self.button9.configure(state="disabled", command=lambda: self.buttonaction(self.button9))
        self.button9.grid(row=3, column=3)
        button_lst.append(self.button9)
        bttnsendinfo.append('9')

        self.createquitbttn()

########## CLASS FOR GETTING USERNAME IN NEW WINDOW
class getName(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.bind('<Return>',self.pressed)
        self.master.title("Register Username: Player 2")
        self.master.geometry("300x120+800+100")
        self.ask = tk.Label(self.master, text="Enter Username:", font=("Verdana", "12")).pack()
        self.name = tk.Entry(self.master)
        self.name.pack()
        self.okbttn = tk.Button(self.master, text="  OK  ", command=self.pressed).pack()
        self.info = tk.Label(self.master, text="Window will close and the game will begin\nwhen both players click OK.", font=("Verdana", "9")).pack()


    def pressed(self):
        global p2username
        p2username = self.name.get()
        self.master.destroy()
        p1Socket.send(p2username.encode('ascii'))


######## FOR SOCKET CONNECTION #########
print("------- Welcome Player 2 -------\n")
GB = gb.BoardClass()
loop = True
hostname = socket.gethostname()
hostIPAddress = socket.gethostbyname(hostname)
port = 8801
p1Socket,p1Address = None, None
print("IP Address: {}".format(hostIPAddress))
print("Port Number: {}\n".format(port))


def createThread(target):
    thread = threading.Thread(target=target)
    thread.daemon = True
    thread.start()

######### COMMUNICATION AND INTERPRETATION ###########
def receiveData():
    global opponentbttn, winsets, data, button_lst, numgame, userbttn_set, winval, turninfo, tienum, names, player, countmove, p1move, statsmem, p1username, p2username
    while True:
        try:
            data = p1Socket.recv(1024).decode('ascii')
            if data in ['1', '2', '3', '4', '5', '6', '7', '8', '9']:
                print("Opponent Move:", data)
                opponentbttn.add(data)
                GB.updateGameBoard(opponentbttn, button_lst, bttnsendinfo) ## disables buttons pressed by P1
                checker = GB.isWinner(opponentbttn, winsets, button_lst, winval, bttnsendinfo)
                turninfo = GB.manageTurns(p1move, countmove, player, button_lst)
                countmove = turninfo[1]
                p1move = turninfo[0]
                winval = checker[0]
                if winval:
                    for index in range(2, 6):
                        statsmem[index - 2] = statsmem[index - 2] + checker[index]
                    GB.printStats(player, ttt, names, statsmem, p1move)
                    numgame = GB.updateGamesPlayed()
                    print()
                    print("------ End of Game ------")
                    print()
                elif winval == False and countmove == 9:
                    tienum = GB.boardIsFull()
                    statsmem[4] = tienum
                    GB.printStats(player, ttt, names, statsmem, p1move)
                    numgame = GB.updateGamesPlayed()
                    print()
                    print("------ End of Game ------")
                    print()

            elif data == "Play Again":
                GB.printStats(player, ttt, names, statsmem, p1move)
                messagebox.showinfo(title="Message from Player 1", message="Player 1 would like to play again.")
                GB.resetGameBoard(player, button_lst)
                opponentbttn = {'Player1'}
                userbttn_set = {"Player2"}
                winval = False
                countmove = 0
                p1move = True
                tictactoe.__init__(ttt)

            elif data == "Fun Times":
                GB.printStats(player, ttt, names, statsmem, p1move)
                messagebox.showinfo(title="Message from Player 1", message="Fun Times.\nPlayer 1 has quit the game.")
                ttt.destroy()
                p1Socket.close()

            elif data == "Quit":
                messagebox.showinfo(title="Information", message="Player 1 has quit.\nThank you for playing.")
                ttt.destroy()
                p1Socket.close()

            else:
                messagebox.showinfo(title="Error", message="Player 1 has lost connection. Closing window.")
                ttt.destroy()
                p1Socket.close()

        except Exception as err:
            messagebox.showinfo(title="Error", message="Player 1 has lost connection. Closing window.")
            break



if __name__ == '__main__':
    try:
        p2connect = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        p2connect.bind((hostIPAddress, port))
        p2connect.listen(1)
        print("Waiting for Player 1...\n")
        p1Socket, p1Address = p2connect.accept()
        namewindow = tk.Tk()
        getName(namewindow)
        namewindow.mainloop()
        p1username = p1Socket.recv(1024).decode('ascii')
        names = [p1username, p2username]
        createThread(receiveData)
        ttt = tk.Tk()
        tictactoe = gameRun(ttt)
        ttt.mainloop()

    except Exception as e:
        print(e)
        print()

    finally:
        try:
            p1Socket.close()
            print("\nConnection terminated.\n")
        except:
            print("\nConnection terminated.\n")






