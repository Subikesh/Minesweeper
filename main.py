from tkinter import *
from random import randint

class Mines:
    
    def __init__(self, master):
        self.master = master
        self.button = []            #contains the matrix of Button objects
        self.mines = []             #list of position of mines
        self.flags = []             #list of flags by user
        self.mine_probablity = []   #contains a list of data behind the buttons
        self.no_of_mines = 20       #max number of mines in the grid
        self.no_of_flags = 20       #max number of flags in the grid
        self.row = 10               #no of rows in grid
        self.col = 15               #number of columns in the grid

        self.random_mines()
        self.place_mine_prob()
        self.init_buttons()

    #Placing a certain amount of mines in random places in the grid
    def random_mines(self):
        while(len(self.mines) < self.no_of_mines):
            r = randint(0, self.row-1)
            c = randint(0, self.col-1)
            if [r,c] in self.mines:
                continue
            else:
                self.mines.append([r,c])

    # To place all the numbers in self.mine_probablity
    def place_mine_prob(self):
        #initialising mineprobablity to zero
        self.mine_probablity = [[0 for x in range(self.col)] for y in range(self.row)]

        for a in self.mines:
            self.add_prob(a)

    #returns the elements rearest to the element at index a
    def get_boundaries(self, a):
        if a[0] == 0:
            top = a[0]
            bottom = a[0]+2
        elif a[0] == self.row-1:
            top = a[0]-1
            bottom = a[0]+1
        else:
            top = a[0]-1
            bottom = a[0]+2

        if a[1] == 0:
            left = a[1]
            right = a[1]+2
        elif a[1] == self.col-1:
            left = a[1]-1
            right = a[1]+1
        else:
            left = a[1]-1
            right = a[1]+2
        return (left, right, top, bottom)

    #Adding the probeblities of finding mines near a co-ordinates
    def add_prob(self, a):
        left, right, top, bottom = self.get_boundaries(a)
        #Iterating to adjescent elements of a
        for i in range(top, bottom):
            for j in range(left, right):
                #Checking if its the current element or a is a mine position
                if [i,j] in self.mines:
                    continue
                else:
                    self.mine_probablity[i][j] +=1

    #changes the color of the button in ath index
    def change_color(self, index):
        self.button[index[0]][index[1]].configure(
            fg = "blue",
            bg = "grey"
        )

    #When a mine is triggered
    def explode(self, index):
        for i in self.mines:
            self.button[i[0]][i[1]].configure(
                bg = "yellow",
                fg = "red",
                text = " * "
            )
        label = Label(text = "Game Over! Try again", fg = "red")
        label.grid(row = self.row +1, column = self.col//2-2, columnspan = 5)
        try_again = Button(text = "TRY AGAIN", command = lambda r = self.master : refresh(r))
        def refresh(root):
            root.destroy()
            execfile("main.py", globals())
        try_again.grid(row = self.row +2, column = 6, columnspan = 3)
        for i in self.button:
            for j in i:
                j.configure(state = "disabled")

    #right-clicking a mine (Marking the mine)
    def mark(self, index):
        if index in self.flags:
            self.demark(index)
        else:
            self.button[index[0]][index[1]].configure(
                fg = "red",
                bg = "grey",
                text = " F "
            )
            self.flags.append(index)
            self.no_of_flags -= 1
            if index in self.mines:
                self.no_of_mines -=1
        #To Check if all the flags are correctly placed
        if self.no_of_flags == 0 and self.no_of_mines == 0:
            label = Label(text="WELL DONE")
            label.grid(row = self.row+1, column = self.col//2-2, columnspan=4)
            play_again = Button(text = "PLAY AGAIN", command = lambda r = self.master : refresh(r))
            def refresh(root):
                root.destroy()
                execfile("main.py", globals())
            play_again.grid(row = self.row +2, column = 6, columnspan = 3)
        label = Label(text="Flags left "+ str(self.no_of_flags))
        label.grid(row = self.row, column = self.col-4, columnspan=4)
            
    #To remove the flag present at that place
    def demark(self, index):
        self.flags.remove(index)
        self.no_of_flags += 1
        if index in self.mines:
            self.no_of_mines += 1
        self.button[index[0]][index[1]].configure(
            fg = "black",
            bg = self.master.cget("background"), 
            text = "   "
        )

    #To show the number behind the button
    def show_num(self, index):
        self.button[index[0]][index[1]].configure(
            text = " "+ str(self.mine_probablity[index[0]][index[1]]) + " ", 
            bg = "white", 
            state = "disabled"
        )
    
    #when the pressed button is a blank space
    def show_spaces(self, index):
        self.button[index[0]][index[1]].configure(
            bg = "white",
            state = "disabled",
            text = "   "
        )
        left, right, top, bottom = self.get_boundaries(index)
        for i in range(top, bottom):
            for j in range(left, right):
                #if an index has a flag, then remove it
                if [i,j] in self.flags:
                    self.flags.remove([i,j])
                    self.no_of_flags+=1
                    label = Label(text="Flags left "+ str(self.no_of_flags))
                    label.grid(row = self.row, column = self.col-4, columnspan=4)
                if [i,j] == index:
                    continue
                #if the nearby element is a blank space, and it was not already visited:
                elif self.mine_probablity[i][j] == 0 and self.button[i][j].cget("state") not in "disabled":
                    #A recursive call with the adjescent index as argument
                    self.show_spaces([i,j])
                elif self.mine_probablity != 0 and self.button[i][j].cget("state") not in "disabled":
                    self.show_num([i,j])

    #To create the base layout of grid of buttons
    def init_buttons(self):
    
        for r in range(self.row):
            #br contains a row of buttons
            br = []
            for c in range(self.col):
                #When user hits a bomb 
                if [r, c] in self.mines:
                    b = Button(root, text ="   ", width = 3, height = 2, command = lambda index=[r, c] : self.explode(index))
                elif self.mine_probablity[r][c] != 0:
                    b = Button(root, text = "   ", width = 3, height = 2, 
                    command = lambda index=[r, c] : self.show_num(index))
                else:
                    b = Button(root, text ="   ", width = 3, height = 2, 
                    command = lambda index=[r, c] : self.show_spaces(index))
                #To mark a button
                b.bind("<Button-3>", lambda event, index=[r, c] : self.mark(index))
                b.grid(row = r, column = c)
                br.append(b)
            #Appending each row to the grid of buttons
            self.button.append(br)

if __name__ == "__main__":
    root = Tk()
    root.geometry("470x560")
    root.title("Minesweeper")

    app = Mines(root)   #app is an object for the window

    root.mainloop()