#!/usr/bin/env python

"""
Minesweeper the Game

ToDo's
- Colourful numbers (ie, 1 is blue)
- Add a graphic for flagged mines.
- Double click to clear neighbours automatically (all unflagged neighbours)
"""

__author__ = "Nathan Bryans"
import wx
import os
import random

class MinesweeperGame():

    board = []
            
    def __init__(self, num_rows, num_cols, num_mines):
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.num_mines = num_mines

        if num_mines > num_rows*num_cols-1:
            self.num_mines = num_rows*num_cols-1
        
        for i in range(num_rows):
            for j in range(num_cols):
                self.board.append(0)
                
        nums = [x for x in range(self.num_rows * self.num_cols )]
        random.shuffle(nums)
        mine_locations = nums[:num_mines]
        
        for i in mine_locations:
           self.board[i] = -1
        print mine_locations
           
        self.calc_neighbours_mines()
    
    def swap_mine_for_first_click(self, id):
        print "Swapping"
        listOfNoMines = []
        for i in range(self.num_rows * self.num_cols):
            if self.board[i] != -1:
                listOfNoMines.append(i)
        random.shuffle(listOfNoMines)

        self.board[id] = 0
        self.board[listOfNoMines[0]] = -1
        self.calc_neighbours_mines()

    def get_neighbours(self, i):
            neighbours = []
            neighbours += self.get_above_indices(i)
            neighbours += self.get_below_indices(i)
            neighbours += self.get_left_index(i)
            neighbours += self.get_right_index(i)
            
            return neighbours
    
    def calc_neighbours_mines(self):
        for i in range(self.num_rows * self.num_cols):
            if self.board[i] == -1:
                continue
                
            neighbours = self.get_neighbours(i)
            
            count = 0
            for n in neighbours:
                if self.board[n] == -1:
                    count += 1
            self.board[i] = count
            
            
    def get_above_indices(self, num):
        if num < self.num_cols:             # Top Row                     
            return []
            
        aboveLeft = num-self.num_cols - 1
        above = num-self.num_cols
        aboveRight = num-self.num_cols + 1
        
        if num % self.num_cols == 0:        # Left Column
            return [above, aboveRight]
        if (num+1) % self.num_cols == 0:    # Right Column
            return [aboveLeft, above]

        return [aboveLeft, above, aboveRight]
        
    def get_below_indices(self, num):
        if num >= (self.num_rows-1)*self.num_cols:      #Bottom Row
            return []
            
        belowLeft = num+self.num_cols - 1
        below = num+self.num_cols
        belowRight = num+self.num_cols + 1
        
        if num % self.num_cols == 0:            # Left Column
            return [below, belowRight]
        if (num+1) % self.num_cols == 0:      # Right Column
            return [belowLeft, below]
        
        return [belowLeft, below, belowRight]
    
    def get_left_index(self, num):
        if num % self.num_cols == 0:
            return []
            
        return [num-1]
    
    def get_right_index(self, num):
        if (num+1) % self.num_cols == 0:
            return []
            
        return [num+1]
        
    def find_neighbouring_zeros(self, id, explored):
        explored.append(id)
        if self.board[id] != 0:
            return []
        neighbours = self.get_neighbours(id)
        toOpen = list(neighbours[:])
        
        for n in neighbours:
            if n not in explored:
                explored.append(n)
                if self.board[n] == 0:
                    toOpen.extend(self.find_neighbouring_zeros(n, explored))
                    
        return toOpen

    def checkLoss(self, id):
        return self.board[id] == -1     #return True is mine clicked, False otherwise   
        
class MainWindow(wx.Frame):

    flag = "%"
    firstClick = True
    
    def onButtonClick(self, event):
        button = event.GetEventObject()
        
        # We don't allow the button to be clicked if it is flagged
        if not self.isFlagged(button):
            id = int(button.GetId())
            if self.game.checkLoss(id) and not self.firstClick:
                self.lose_actions()
            else:
                if self.game.checkLoss(id):
                    self.game.swap_mine_for_first_click(id)
                button.SetLabel(str(self.game.board[id]))
                button.Disable()
                if self.checkWin():
                    self.win_actions()
                self.expand_zeros(id)
                self.firstClick = False

    def win_actions(self):
        dlg = wx.MessageDialog(self, "You Win!", "You Win!", wx.OK)
        dlg.ShowModal()
        dlg.Destroy()
        exit()

    def lose_actions(self):
        dlg = wx.MessageDialog(self, "You Lost", "You Lost", wx.OK)
        dlg.ShowModal()
        dlg.Destroy()
        exit()

    def onRightClick(self, event):
        button = event.GetEventObject()

        id = int(button.GetId())
        if button.IsEnabled():
            if self.isFlagged(button):
                button.SetLabel("")
            else:
                button.SetLabel(self.flag) # Put '%' for flagged
          
    def __init__(self, parent, title, game):
        self.game = game
        self.buttonList = []
        
        num_rows = game.num_rows
        num_cols = game.num_cols
        square_size_px = 35

        wx.Frame.__init__(self, parent, title=title, size= (square_size_px*num_rows,square_size_px*num_cols))
        
        gs = wx.GridSizer(num_rows,num_cols) # 10 rows and 10 columns
        
        for i in range(0, num_rows):
            for j in range(0, num_cols):
                button = wx.Button(self, id = i*10+j, label = " ")
                button.Bind(wx.EVT_BUTTON, self.onButtonClick)
                button.Bind(wx.EVT_RIGHT_DOWN, self.onRightClick)
                gs.Add(button, 0, wx.ALL|wx.EXPAND)
                self.buttonList.append(button)

        self.SetSizer(gs)
        self.Centre()
        
        self.Show(True)
    
    def expand_zeros(self, id):
        if self.game.board[id] == 0:
            toOpen = self.game.find_neighbouring_zeros(id, [])
            
            for id in toOpen:
                if not self.isFlagged(self.buttonList[id]): #Don't want to open flagged squares
                    self.buttonList[id].SetLabel(str(self.game.board[id]))
                    self.buttonList[id].Disable()
        
    def checkWin(self):
        for b in self.buttonList:
            id = int(b.GetId())
            if b.IsEnabled() and self.game.board[id] != -1:
                return False
        return True
        
    def isFlagged(self, button):
        if self.flag in button.GetLabel():
            return True
        else:
            return False
        
#Main
game = MinesweeperGame(10,10, 10)
app = wx.App(False)
frame = MainWindow(None, "MineSweeper", game)
app.MainLoop()