#!/usr/bin/python

import wx
import os
import random

class MinesweeperGame():

    board = []

            
    def __init__(self, num_rows, num_cols, num_mines):
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.num_mines = num_mines
        
        for i in range(num_rows):
            for j in range(num_cols):
                self.board.append(0)
                
        nums = [x for x in range(self.num_rows * self.num_cols )]
        random.shuffle(nums)
        mine_locations = nums[:num_mines]
        
        for i in mine_locations:
           self.board[i] = -1
           
        self.calc_neighbours()
            
    def calc_neighbours(self):
        for i in range(self.num_rows * self.num_cols):
            if self.board[i] == -1:
                continue
                
            neighbours = []
            neighbours += self.get_above_indices(i)
            neighbours += self.get_below_indices(i)
            neighbours += self.get_left_index(i)
            neighbours += self.get_right_index(i)
            
            count =0
            for n in neighbours:
                if self.board[n] == -1:
                    count += 1
            self.board[i] = count
            
            
    def get_above_indices(self, num):
        if num < self.num_cols:     # Top Row                     
            return []
            
        aboveLeft = num-self.num_cols - 1
        above = num-self.num_cols
        aboveRight = num-self.num_cols + 1
        
        if num % self.num_cols == 0:          # Left Column
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

        
        
class MainWindow(wx.Frame):

    def onButtonClick(self, event):
        button = event.GetEventObject()
        
        id = int(button.GetId())
        if self.checkLoss(id):
            dlg = wx.MessageDialog(self, "You Lost", "You Lost", wx.OK)
            dlg.ShowModal()
            dlg.Destroy()
            exit()
        else:
            button.SetLabel(str(self.game.board[id]))
            button.Disable()
            if self.checkWin():
                dlg = wx.MessageDialog(self, "You Win!", "You Win!", wx.OK)
                dlg.ShowModal()
                dlg.Destroy()
                exit()
        
        
    def __init__(self, parent, title, game):
        self.game = game
        self.buttonList = []
    
        wx.Frame.__init__(self, parent, title=title, size= (500,500))
        
        gs = wx.GridSizer(10,10) # 10 rows and 10 columns
        
        num_rows = 10
        num_cols = 10
        
        for i in range(0, num_rows):
            for j in range(0, num_cols):
                button = wx.Button(self, id = i*10+j, label = " ")
                button.Bind(wx.EVT_BUTTON, self.onButtonClick)  
                gs.Add(button, 0, wx.ALL|wx.EXPAND)
                self.buttonList.append(button)

        self.SetSizer(gs)
        self.Centre()
        
        self.Show(True)
    def checkLoss(self, id):
        if self.game.board[id] == -1:
            return True
        return False
        
    def checkWin(self):
        for b in self.buttonList:
            id = int(b.GetId())
            if b.IsEnabled() and self.game.board[id] != -1:
                return False
        return True
        
#Main
game = MinesweeperGame(10,10, 10)
app = wx.App(False)
frame = MainWindow(None, "MineSweeper", game)
app.MainLoop()


# ToDo
# Automatic expansion when clicking 0
# Never lose on first click