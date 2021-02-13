'''
Name: Jasmine Som
UCINetID: 60264498
'''

import tkinter as tk

class BoardClass(): #TTT = TicTacToe
#---Defining my class variables:
    #Player user names:
    username = []
    p1name = ""
    p2name = ""
    #for checking if it is P1 turn:
    movep1 = True
    mvcnt = 0 #counts num of moves
    #Number of games played:
    gamesPlayed = 0
    #Number of wins:
    p1win = 0
    p2win = 0
    #Number of ties:
    numtie = 0
    #Number of losses:
    p1loss = 0
    p2loss = 0
    spacer = ""
    bttnnum = 0
    currentmove = 0
    
    def __inti__(self):
        self.spacer = ""
        self.p1name = ""
        self.p2name = ""
        self.gamesPlayed = 0
        self.p1win = 0
        self.p2win = 0
        self.numtie = 0
        self.p1loss = 0
        self.p2loss = 0
        self.movep1 = None
        self.mvcnt = 0
        self.bttnnum = 0
        self.currentmove = 0


    def getusernames(self, p1name, p2name, window):
        self.player1 = tk.Label(window, text="Player 1:\n{}".format(p1name), font=("Verdana", "12")).grid(row=1, column=5)
        self.player2 = tk.Label(window, text="Player 2:\n{}".format(p2name), font=("Verdana", "12")).grid(row=1, column=6)

    def updateGamesPlayed(self): #Keeps track how many games have started
        self.gamesPlayed = self.gamesPlayed + 1
        return self.gamesPlayed


    def resetGameBoard(self, playerval, fullbuttonlst): #Clear all the moves from game board
        if playerval == "X":
            for button in fullbuttonlst:
                if button["state"] == "disabled":
                    button.config(text="", state="normal") ##resets all disabled buttons
        if playerval == "O":
            for button in fullbuttonlst:
                if button["state"] == "disabled":
                    button.config(text="")
                if button["state"] == "normal":
                    button.config(text="", state="disabled")##resets all disabled buttons
        self.mvcnt = 0
        self.movep1 = True


    def manageTurns(self, p1turn, movecount, playervar, fullbuttonlst):
        self.mvcnt = movecount + 1
        if p1turn == True:
            if playervar == "O":
                self.enableBttn(fullbuttonlst)
            elif playervar == "X":
                self.disableBttn(fullbuttonlst)
        elif p1turn == False:
            if playervar == "X":
                self.enableBttn(fullbuttonlst)
            elif playervar == "O":
                self.disableBttn(fullbuttonlst)

        if p1turn == True:
            p1turn = False
        else:
            p1turn = True

        return [p1turn, self.mvcnt]


    def disableBttn(self, fullbuttonlst):
        for button in fullbuttonlst:
            if button["text"] == "" and button["state"] == "normal":
                button.config(state="disabled")


    def enableBttn(self, fullbuttonlst):
        for button in fullbuttonlst:
            if button["text"] == "" and button["state"] == "disabled":
                button.config(state="normal")


    def updateGameBoard(self, opponentbttnset, fullbuttonlst, bttnsendlst): #Updates the game board with the player's move
        for oppbutton in opponentbttnset:
            for button in fullbuttonlst:
                if (oppbutton == bttnsendlst[fullbuttonlst.index(button)]):
                    if {"Player1"}.issubset(opponentbttnset) == True:
                        button.config(text="X", bg="MistyRose3", fg="MistyRose2", state="disabled")
                    if {"Player2"}.issubset(opponentbttnset) == True:
                        button.config(text="O", bg="MistyRose3", fg="MistyRose2", state="disabled")
        '''if oppbutton == "1":
            if {"Player1"}.issubset(opponentbttnset) == True:
                fullbuttonlst[0].config(text="X", bg="MistyRose3", fg="MistyRose2", state="disabled")
            if {"Player2"}.issubset(opponentbttnset) == True:
                fullbuttonlst[0].config(text="O", bg="MistyRose3", fg="MistyRose2", state="disabled")
'''

    def endgame(self, fullbuttonlst):
        for button in fullbuttonlst: ##disables all remaining buttons
            if button["state"] == "normal":
                button.config(state="disabled")


### getting stats values here
    def isWinner(self, buttonset, winset, fullbuttonlst, pwin, bttnsendnum, button=None):
        if button != None:
            self.index = fullbuttonlst.index(button)
            self.bttnnum = bttnsendnum[self.index]
            buttonset.add(self.bttnnum) #making button set to check if there is a win
        for setToWin in winset: ##checking if the user button set is in the list of possible win sets
            if setToWin.issubset(buttonset) == True: # checks if all possible sets are a subset, and if player won
                self.endgame(fullbuttonlst) ##disabled all other buttons on board
                if {"Player2"}.issubset(buttonset) == True:
                    self.p2win = 1
                    self.p1loss = 1
                    self.movep1 = False  ## the winner who made the move is P2

                elif {"Player1"}.issubset(buttonset) == True:
                    self.p1win = 1
                    self.p2loss = 1
                    self.movep1 = True
                pwin = True
        return [pwin, self.bttnnum, self.p1win, self.p1loss, self.p2win, self.p2loss] ## lets program know if there is a winner after the button is clicked


### getting tie values here
    def boardIsFull(self):
        if self.mvcnt == 9:
            self.numtie = self.numtie + 1
        return self.numtie

    def printStats(self, playerval, window, lst_names, lst_stats, p1turn):
        if playerval == "X":
            self.p1stat = tk.Label(window, text="Wins: {}\n\nLosses: {}\n\nTies: {}".format(lst_stats[0], lst_stats[1], lst_stats[4]), font=("Verdana", "12"))
            self.p1stat.grid(row=2, column=5, rowspan=2, columnspan=2)
        elif playerval == "O":
            self.p2stat = tk.Label(window, text="Wins: {}\n\nLosses: {}\n\nTies: {}".format(lst_stats[2], lst_stats[3], lst_stats[4]), font=("Verdana", "12"))
            self.p2stat.grid(row=2, column=5, rowspan=2, columnspan=2)
        if p1turn == True:
            self.lastmove = tk.Label(window, text="Last Winning Move By:\n{}".format(lst_names[1]), font=("Verdana", "10"))
        else:
            self.lastmove = tk.Label(window, text="Last Winning Move By:\n{}".format(lst_names[0]), font=("Verdana", "10"))

        self.lastmove.grid(row=4, column=5, columnspan=2)

