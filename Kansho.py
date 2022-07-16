"""
SCRIPT NAME:
    Kansho_Script.py

DESCRIPTION:
    Creates Kansho board and allows two human players to play,
    forces players to keep to Kansho rules, automatically removes nessessary markers,
    keeps track of scores and player markers.

FUNCTIONS:
    Remove_old_files() - Deletes non-required board and scores from directory (this has been disabled, remove "#" to enable)
    Calculate_Scores() - Calculates each players score and remaining markers
    Show_Board() - Displays the current board to the user
    Save_Scores() and Save_Board() - Outputs the current turns board and scores to a .csv file in the current directroy
    Input_x() and Input_y() - Allows user to input  x and y co-ordinates and checks if input is integer
    Define_Neighbour_Index() - Calculates the index of current markers neighbours
    Define_Neighbour_States() - Calculates the state of current markers neighbours
    Take_Turn() - Sets up a loop to allow players to take turns

UPDATE RECORD:
Date          Version     Author         Description
11/06/2020    v1.0        Pete Sanders   Created
12/06/2020    v1.1        Pete Sanders   Bug fixes
                                         Minor alterations to board display
                                         Prints board images to files
20/05/2022    v2.0        Pete Sanders   Included some basic front end.   
24/05/2022    v2.1        Pete Sanders   Re-ordering of code to work better with front end commands.                                      
                                         
RECOMMENDED FUTURE IMPROVEMENTS:
    Make one neighboured tokens and enclosed areas loops more efficient.
    Mark placed marker as red when players last go to make it easier to know where to place other markers
    Allow user to input a precice location on the chart, could use a conversion table to do this.

Bugs:
                       
"""
#%% Import nessessary modules
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sys import exit
import os
from pathlib import Path
import tkinter as tk
import time
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import *
from PIL import ImageTk, Image

#%%###########################################################################
#   1. Print instructions, define initial conditions
#   2. Define board and scores
#   3. Make a move:
#           3.1. Place marker:
#                   3.111. Determine if this is the players last move.
#                   3.1.2. If so, allow them to keep placing markers until they are done.
#           3.2. Place surrounding markers,
#           3.3. Remove opponents markers.
#   4. Calculate scores and save board.
#   5. Determine if the game is over:
#           5.1. If so calculate the result.
###############################################################################

#%% 1. Print instructions, define initial conditions
global Turn_No
global Total_Markers
global Markers_P1
global Markers_P2
global Used_P1
global Used_P2
global P1_Used
global P2_Used
global Turn_No
global Last_Turn

# Print instrustions
print ('Instructions:', '\n',
       'These will need changing based on the changes made.',)

# Define initial condtions
Markers_P1 = 123
Markers_P2 = 123
Used_P1 = 0
Used_P2 = 0
P1_Used = 0
P2_Used = 0
Turn_No = 0
Total_Markers = Markers_P1 + Markers_P2
Player = 1
Last_Turn = 0

#%%  2. Define board and scores
# This should be done using code up front, instead of reading a csv file like it is currently.


Board_0 = pd.read_csv ('Board_0.csv', header = 0)

Board_0_data = {'x': [11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,
                      10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,
                      9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,
                      8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,
                      7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,
                      6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,
                      5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,
                      4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,
                      3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,
                      2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,
                      1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,
                      0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
                      -1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,
                      -2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,
                      -3,-3,-3,-3,-3,-3,-3,-3,-3,-3,-3,-3,-3,-3,-3,-3,-3,-3,-3,-3,-3,-3,-3,
                      -4,-4,-4,-4,-4,-4,-4,-4,-4,-4,-4,-4,-4,-4,-4,-4,-4,-4,-4,-4,-4,-4,-4,
                      -5,-5,-5,-5,-5,-5,-5,-5,-5,-5,-5,-5,-5,-5,-5,-5,-5,-5,-5,-5,-5,-5,-5,
                      -6,-6,-6,-6,-6,-6,-6,-6,-6,-6,-6,-6,-6,-6,-6,-6,-6,-6,-6,-6,-6,-6,-6,
                      -7,-7,-7,-7,-7,-7,-7,-7,-7,-7,-7,-7,-7,-7,-7,-7,-7,-7,-7,-7,-7,-7,-7,
                      -8,-8,-8,-8,-8,-8,-8,-8,-8,-8,-8,-8,-8,-8,-8,-8,-8,-8,-8,-8,-8,-8,-8,
                      -9,-9,-9,-9,-9,-9,-9,-9,-9,-9,-9,-9,-9,-9,-9,-9,-9,-9,-9,-9,-9,-9,-9,
                      -10,-10,-10,-10,-10,-10,-10,-10,-10,-10,-10,-10,-10,-10,-10,-10,-10,-10,-10,-10,-10,-10,-10,
                      -11,-11,-11,-11,-11,-11,-11,-11,-11,-11,-11,-11,-11,-11,-11,-11,-11,-11,-11,-11,-11,-11,-11],
                'y': [11,10,9,8,7,6,5,4,3,2,1,0,-1,-2,-3,-4,-5,-6,-7,-8,-9,-10,-11,
                      11,10,9,8,7,6,5,4,3,2,1,0,-1,-2,-3,-4,-5,-6,-7,-8,-9,-10,-11,
                      11,10,9,8,7,6,5,4,3,2,1,0,-1,-2,-3,-4,-5,-6,-7,-8,-9,-10,-11,
                      11,10,9,8,7,6,5,4,3,2,1,0,-1,-2,-3,-4,-5,-6,-7,-8,-9,-10,-11,
                      11,10,9,8,7,6,5,4,3,2,1,0,-1,-2,-3,-4,-5,-6,-7,-8,-9,-10,-11,
                      11,10,9,8,7,6,5,4,3,2,1,0,-1,-2,-3,-4,-5,-6,-7,-8,-9,-10,-11,
                      11,10,9,8,7,6,5,4,3,2,1,0,-1,-2,-3,-4,-5,-6,-7,-8,-9,-10,-11,
                      11,10,9,8,7,6,5,4,3,2,1,0,-1,-2,-3,-4,-5,-6,-7,-8,-9,-10,-11,
                      11,10,9,8,7,6,5,4,3,2,1,0,-1,-2,-3,-4,-5,-6,-7,-8,-9,-10,-11,
                      11,10,9,8,7,6,5,4,3,2,1,0,-1,-2,-3,-4,-5,-6,-7,-8,-9,-10,-11,
                      11,10,9,8,7,6,5,4,3,2,1,0,-1,-2,-3,-4,-5,-6,-7,-8,-9,-10,-11,
                      11,10,9,8,7,6,5,4,3,2,1,0,-1,-2,-3,-4,-5,-6,-7,-8,-9,-10,-11,
                      11,10,9,8,7,6,5,4,3,2,1,0,-1,-2,-3,-4,-5,-6,-7,-8,-9,-10,-11,
                      11,10,9,8,7,6,5,4,3,2,1,0,-1,-2,-3,-4,-5,-6,-7,-8,-9,-10,-11,
                      11,10,9,8,7,6,5,4,3,2,1,0,-1,-2,-3,-4,-5,-6,-7,-8,-9,-10,-11,
                      11,10,9,8,7,6,5,4,3,2,1,0,-1,-2,-3,-4,-5,-6,-7,-8,-9,-10,-11,
                      11,10,9,8,7,6,5,4,3,2,1,0,-1,-2,-3,-4,-5,-6,-7,-8,-9,-10,-11,
                      11,10,9,8,7,6,5,4,3,2,1,0,-1,-2,-3,-4,-5,-6,-7,-8,-9,-10,-11,
                      11,10,9,8,7,6,5,4,3,2,1,0,-1,-2,-3,-4,-5,-6,-7,-8,-9,-10,-11,
                      11,10,9,8,7,6,5,4,3,2,1,0,-1,-2,-3,-4,-5,-6,-7,-8,-9,-10,-11,
                      11,10,9,8,7,6,5,4,3,2,1,0,-1,-2,-3,-4,-5,-6,-7,-8,-9,-10,-11,
                      11,10,9,8,7,6,5,4,3,2,1,0,-1,-2,-3,-4,-5,-6,-7,-8,-9,-10,-11,
                      11,10,9,8,7,6,5,4,3,2,1,0,-1,-2,-3,-4,-5,-6,-7,-8,-9,-10,-11],
                'y_display': [11.5,10.5,9.5,8.5,7.5,6.5,5.5,4.5,3.5,2.5,1.5,0.5,-0.5,-1.5,-2.5,-3.5,-4.5,-5.5,-6.5,-7.5,-8.5,-9.5,-10.5,
                              11,10,9,8,7,6,5,4,3,2,1,0,-1,-2,-3,-4,-5,-6,-7,-8,-9,-10,-11,
                              11.5,10.5,9.5,8.5,7.5,6.5,5.5,4.5,3.5,2.5,1.5,0.5,-0.5,-1.5,-2.5,-3.5,-4.5,-5.5,-6.5,-7.5,-8.5,-9.5,-10.5,
                              11,10,9,8,7,6,5,4,3,2,1,0,-1,-2,-3,-4,-5,-6,-7,-8,-9,-10,-11,
                              11.5,10.5,9.5,8.5,7.5,6.5,5.5,4.5,3.5,2.5,1.5,0.5,-0.5,-1.5,-2.5,-3.5,-4.5,-5.5,-6.5,-7.5,-8.5,-9.5,-10.5,
                              11,10,9,8,7,6,5,4,3,2,1,0,-1,-2,-3,-4,-5,-6,-7,-8,-9,-10,-11,
                              11.5,10.5,9.5,8.5,7.5,6.5,5.5,4.5,3.5,2.5,1.5,0.5,-0.5,-1.5,-2.5,-3.5,-4.5,-5.5,-6.5,-7.5,-8.5,-9.5,-10.5,
                              11,10,9,8,7,6,5,4,3,2,1,0,-1,-2,-3,-4,-5,-6,-7,-8,-9,-10,-11,
                              11.5,10.5,9.5,8.5,7.5,6.5,5.5,4.5,3.5,2.5,1.5,0.5,-0.5,-1.5,-2.5,-3.5,-4.5,-5.5,-6.5,-7.5,-8.5,-9.5,-10.5,
                              11,10,9,8,7,6,5,4,3,2,1,0,-1,-2,-3,-4,-5,-6,-7,-8,-9,-10,-11,
                              11.5,10.5,9.5,8.5,7.5,6.5,5.5,4.5,3.5,2.5,1.5,0.5,-0.5,-1.5,-2.5,-3.5,-4.5,-5.5,-6.5,-7.5,-8.5,-9.5,-10.5,
                              11,10,9,8,7,6,5,4,3,2,1,0,-1,-2,-3,-4,-5,-6,-7,-8,-9,-10,-11,
                              11.5,10.5,9.5,8.5,7.5,6.5,5.5,4.5,3.5,2.5,1.5,0.5,-0.5,-1.5,-2.5,-3.5,-4.5,-5.5,-6.5,-7.5,-8.5,-9.5,-10.5,
                              11,10,9,8,7,6,5,4,3,2,1,0,-1,-2,-3,-4,-5,-6,-7,-8,-9,-10,-11,
                              11.5,10.5,9.5,8.5,7.5,6.5,5.5,4.5,3.5,2.5,1.5,0.5,-0.5,-1.5,-2.5,-3.5,-4.5,-5.5,-6.5,-7.5,-8.5,-9.5,-10.5,
                              11,10,9,8,7,6,5,4,3,2,1,0,-1,-2,-3,-4,-5,-6,-7,-8,-9,-10,-11,
                              11.5,10.5,9.5,8.5,7.5,6.5,5.5,4.5,3.5,2.5,1.5,0.5,-0.5,-1.5,-2.5,-3.5,-4.5,-5.5,-6.5,-7.5,-8.5,-9.5,-10.5,
                              11,10,9,8,7,6,5,4,3,2,1,0,-1,-2,-3,-4,-5,-6,-7,-8,-9,-10,-11,
                              11.5,10.5,9.5,8.5,7.5,6.5,5.5,4.5,3.5,2.5,1.5,0.5,-0.5,-1.5,-2.5,-3.5,-4.5,-5.5,-6.5,-7.5,-8.5,-9.5,-10.5,
                              11,10,9,8,7,6,5,4,3,2,1,0,-1,-2,-3,-4,-5,-6,-7,-8,-9,-10,-11,
                              11.5,10.5,9.5,8.5,7.5,6.5,5.5,4.5,3.5,2.5,1.5,0.5,-0.5,-1.5,-2.5,-3.5,-4.5,-5.5,-6.5,-7.5,-8.5,-9.5,-10.5,
                              11,10,9,8,7,6,5,4,3,2,1,0,-1,-2,-3,-4,-5,-6,-7,-8,-9,-10,-11,
                              11.5,10.5,9.5,8.5,7.5,6.5,5.5,4.5,3.5,2.5,1.5,0.5,-0.5,-1.5,-2.5,-3.5,-4.5,-5.5,-6.5,-7.5,-8.5,-9.5,-10.5,],
                'x,y': [3, 4],
                'Value': [3, 4]}
Board_0 = pd.DataFrame(data = Board_0_data)

This_Turn = pd.read_csv ('Board_0.csv', header = 0)
These_Scores =pd.read_csv ('Scores_0.csv', header = 0)


#%% Step 3, Setup the initial part of the front end
# This has to happen before Show_Board() is called because Show_Board() uses the panel.
# Assignes some function within tk to root
root = tk.Tk()
root.title('Kansho')
root.geometry('500x600')
root.resizable(0,0)

img = ImageTk.PhotoImage(Image.open('Kansho - Logo.jpg'))
panel = Label(root, image = img)
panel.pack_propagate(0)
panel.pack(side = "left", fill = "both", expand = 1)

#%% Remove_old_files()
def Remove_old_files():
    file_no = 1

    while file_no < 246:
        Scores = Path('Scores_' + str(file_no) + '.csv')
        Boards = Path('Board_' + str(file_no) + '.csv')
        Turns = Path('Turn_' + str(file_no) + '.jpg')
        
        if Scores.exists():
            os.remove('Scores_' + str(file_no) + '.csv')
        else:
            pass
    
        if Boards.exists():
            os.remove('Board_' + str(file_no) + '.csv')
        else:
            pass
        
        if Turns.exists():
            os.remove('Turn_' + str(file_no) + '.jpg')
        else:
            pass

        file_no = file_no +1
        
#Remove_old_files()       

#%% Show Board
def Show_Board():
    global panel
    global img
    global Player
    
    plt.figure(figsize=(10,10))

# Define x, y co-ordinates and values (z)        
    x_board = This_Turn['x']
    y_board = This_Turn['y_display']
    z_board = This_Turn['Value']

# Define x and y co-ordinates for z values = 1, 2 and 3 respectively        
    x_1 = x_board[z_board == 1]
    y_1 = y_board[z_board == 1]    
    x_2 = x_board[z_board == 2]
    y_2 = y_board[z_board == 2]
    x_3 = x_board[z_board == 3]
    y_3 = y_board[z_board == 3]

# Define chart parameters        
    plt.axis([-11,11,-9,9]) 
    major_ticksx = np.arange(-10, 11, 1)
    major_ticksy = np.arange(-9, 9, 1)
    plt.tick_params(axis = 'both', labeltop=True, labelright=True)
    plt.xticks(major_ticksx, fontsize=16)
    plt.yticks(major_ticksy, fontsize=16)
    plt.grid(axis = 'both', color = (0.4,0.4,0.4), linewidth = 1.5)        
    plt.scatter(x_board,y_board, marker = 'H', s = 1300, color = (0.74,0.47,0.34), edgecolor = 'k')
    plt.scatter(x_3,y_3, marker = 'H', s = 1350, color = 'w')
    plt.scatter(x_1,y_1, marker = 'o', s = 500, color = 'w', edgecolor = 'k')
    plt.scatter(x_2,y_2, marker = 'o', s = 500, color = 'k', edgecolor = 'k')
    plt.tight_layout()
    
    #Chart annotations
    props = dict(boxstyle='round', facecolor=(0,0.6,0.6), alpha=0.7)
    
    if Player == 1:
        plt.text(-10.5, -8.5, "White, it's your go", fontsize=18, verticalalignment='center', bbox=props)
    else:
        plt.text(-10.5, -8.5, "Black, it's your go", fontsize=18, verticalalignment='center', bbox=props)
    
    plt.text(-10.5, 8, 'White Score = ' + str("%.0f" % float(These_Scores['InPlay_P1'].loc[0])) +
                        '\n' + 'Black Score = ' + str("%.0f" % float(These_Scores['InPlay_P2'].loc[0])),
                        fontsize=18, verticalalignment='center', bbox=props)
    
    plt.text(10.5, -8, 'White Left = ' + str("%.0f" % float(These_Scores['Markers_P1'].loc[0])) +
                          '\n' + 'Black Left = ' + str("%.0f" % float(These_Scores['Markers_P2'].loc[0])),
                          fontsize=18, verticalalignment='center', horizontalalignment='right', bbox=props)
    
    plt.text(0, 0, 'Turn' + '\n' + str("%.0f" % float(Turn_No)), fontsize=18, verticalalignment='center', horizontalalignment='center', bbox=props)
    
    
# Pause chart to display during loops    
    plt.savefig('Turn_{}'.format(Turn_No) +'.jpg')
    plt.pause(0.1)
    
    panel.destroy()
    
    img = Image.open('Turn_{}'.format(Turn_No) +'.jpg')
    img = img.resize((450, 450), Image.ANTIALIAS)
    img = ImageTk.PhotoImage(img)
    panel = Label(root, image = img)
    panel.pack_propagate(0)
    panel.pack(side = "left", fill = tk.BOTH, expand = True)

    
#%% Calculate score
def Calculate_Scores():
    global Turn_No
    
    # Makes sure code doesn't crash during Turn 0
    if Turn_No == 0:
        Turn_No = 1
        # Pull in scores from previous turn file    
        Scores = pd.read_csv ('Scores_' + str(Turn_No - 1) + '.csv', header = 0)
        Turn_No = 0
    else:
        Scores = pd.read_csv ('Scores_' + str(Turn_No - 1) + '.csv', header = 0)    
 
# Define scores for this turn based on 'Scores' and current markers used    
    These_Scores['InPlay_P1'].loc[0] = This_Turn[This_Turn.Value == 1].sum().loc['Value']
    These_Scores['InPlay_P2'].loc[0] = int(This_Turn[This_Turn.Value == 2].sum().loc['Value'] / 2)  
    These_Scores['Markers_P1'].loc[0] = Scores['Markers_P1'].loc[0] - P1_Used
    These_Scores['Markers_P2'].loc[0] = Scores['Markers_P2'].loc[0] - P2_Used

#%% Print scores and board
def Save_Scores():
    globals()['Scores_{}'.format(Turn_No)] = These_Scores
    globals()['Scores_{}'.format(Turn_No)].to_csv('Scores_'+str(Turn_No)+'.csv',index=False)
            
def Save_Board():
    globals()['Board_{}'.format(Turn_No)] = This_Turn
    globals()['Board_{}'.format(Turn_No)].to_csv('Board_'+str(Turn_No)+'.csv',index=False)
#%% Player_Check() Check if player 1 or 2 is playing based on turn no. or number of markers
def Player_Check():
    global Player
    global Opponent
    global Turn_No
    
    if Markers_P1 <= 0:
        Player = 2
        Opponent = 1
        print('Black player...your turn')
    elif Markers_P2 <= 0:
        Player = 1
        Opponent = 2
        print('White player...your turn')
    else:
        if Turn_No % 2 == 0:
            Player = 1
            Opponent = 2
            print('White player...your turn')
        else:
            Player = 2
            Opponent = 1
            print('Black player...your turn')    

#%% Input co-ordinates, checks that inputted co-ordinates match the entry requirements.
# If so, passes to Take_Turn(), If not, displays error message.
def Input():      
    global Place_x
    global Place_y 
    global entry1
    global coords
    global Last_Turn
       
    # The entry requirements are that:
    # 1. Integers between -10 and 10 must be used.
    # 2. They must be seperated by a single comma.
    # 3. They must represent a location on the board.
    # 4. The location must be unoccupied by another piece.
    
    Pass = 0
    
    # 1. Check that there is text in input1 and that it has at least one comma.
    if (str(entry1.get()) != '') and (',' in str(entry1.get())):
        coords = list(entry1.get().split(','))
        Place_x = int(coords[0])
        Place_y = int(coords[1])
        entry1.delete(0, END)
        Pass = Pass + 1
    else:
        entry1.delete(0, END)
        
        
    # 2. Check to see if Place_x and Place_y are integers between -10 and 10
    if (-10 <= Place_x <= 10) and (-10 <= Place_y <= 10):
        Pass = Pass + 1        
    else:
        pass
    
    # Check to see if co-ordinate is on board
    while (sum(1 for item in This_Turn['x'] if item==(Place_x)) == 0) and (sum(1 for item in This_Turn['y'] if item==(Place_y)) == 0):
        pass
    else:
        Pass = Pass + 1
    
    # 4. Check to see if required space is occupied
    # Find the row relating to the place location
    Place_index = Board_0[Board_0['x,y']==str(str(Place_x) + ',' + str(Place_y))].index.values

    Place_State = int(This_Turn['Value'].loc[Place_index])
    if Place_State > 0:
        pass
    else:
        Pass = Pass + 1
    
    # Check to see if all stages passed, if so contunue, if not pass
    if Pass == 4:
        if Last_Turn == 0:
            Take_Turn()
        else:
            pass
        #check to see if the space is correct regarding the last go rules.
    else:
        print('Entered co-ordinate is incorrect, please try again')
        
        
        
#%% Define neighbour index
def Define_Neighbour_Index():   
# Define variables used in function     
    global a_index
    global b_index
    global c_index
    global d_index
    global e_index
    global f_index
    global Place_index

# Defines different e and f indexes if x value is odd or even   
    Place_index = Board_0[Board_0['x,y']==str(str(lookup_x) + ',' + str(lookup_y))].index.values
    
    if int(lookup_x) % 2 == 0:
        e_index = Place_index - 22
        f_index = Place_index + 24
   
    else:
        e_index = Place_index + 22
        f_index = Place_index - 24    
    a_index = Place_index - 23
    b_index = Place_index + 23
    c_index = Place_index - 1
    d_index = Place_index + 1
    
#%% Define_Neighbour_States
def Define_Neighbour_States():    
# Define variables used in function 
    global a_index
    global b_index
    global c_index
    global d_index
    global e_index
    global f_index
    global a_state
    global b_state
    global c_state
    global d_state
    global e_state
    global f_state
    global Neighbour_vals
    global This_Turn
       
    a_state = int(This_Turn['Value'].loc[int(a_index)])
    b_state = int(This_Turn['Value'].loc[int(b_index)])
    c_state = int(This_Turn['Value'].loc[int(c_index)])
    d_state = int(This_Turn['Value'].loc[int(d_index)])
    e_state = int(This_Turn['Value'].loc[int(e_index)])
    f_state = int(This_Turn['Value'].loc[int(f_index)])
    
# Create a list of neighbour vals to be interrogated later
    Neighbour_vals = [int(a_state), int(b_state), int(c_state),
                      int(d_state), int(e_state), int(f_state)]

#%% Last_Go()
def Last_Go():
    global Player_Markers
    
    Last_Turn = 1
            
    if Player == 2:
        print('Black player, this is your last go, good luck!')
                
    else:
        print('White player, this is your last go, good luck!')
            
    Calculate_Scores()
    Save_Scores()
    Save_Board()
    Show_Board()
            
    if Player_Markers > 0:
            
        if Player == 2:
            print('Black player its still your turn')
                
        else:
            print('White player its still your turn')
                    
        # Here we need to trigger Input() but in a way that it wouldn't
        # trigger Take_Turn() aftter.
                                                     
        Place_index = Board_0[Board_0['x,y']==str(str(Place_x) + ',' + str(Place_y))].index.values
        Place_State = int(This_Turn['Value'].loc[Place_index])
                
        # Check to see if required space is neighbour
        Neighbour_index = [int(a_index), int(b_index), int(c_index),
                           int(d_index), int(e_index), int(f_index)]
                
        if sum(1 for item in Neighbour_index if item==(int(Place_index))) == 0:
            print('You cant go there, try again')
            Player_Markers = Player_Markers + 1
        else:            
            # Check to see if required space is occupied
            if Place_State == int(Player):
                print('You have already gone there, try again')
                Player_Markers = Player_Markers + 1
                    
            else:                                 
                Place_index = Board_0[Board_0['x,y']==str(str(Place_x) + ',' + str(Place_y))].index.values
                This_Turn['Value'].loc[Place_index] = int(Player)
                        
                if int(Player) == 1:
                    P1_Used = P1_Used + 1
                
                else:
                    P2_Used = P2_Used + 1
                
            Calculate_Scores()
            Save_Scores()
            Save_Board() 
            Show_Board()
                
            Player_Markers = int(These_Scores[str('Markers_P' + str(Player))].loc[0])
                
            Last_Turn = 0
                
            Turn_No = Turn_no - 1
                    

#%% Step 3, Set turn number and place a token
def Take_Turn():
# Define variables used in function    
    global Turn_No
    global Markers_P1
    global Markers_P2
    global Used_P1
    global Used_P2
    global a_index
    global b_index
    global c_index
    global d_index
    global e_index
    global f_index
    global a_state
    global b_state
    global c_state
    global d_state
    global e_state
    global f_state
    global These_Scores
    global This_Turn
    global P1_Used
    global P2_Used
    global place_state
    global lookup_x
    global lookup_y
    global Place_x
    global Place_y
    global Neighbour_vals
    global Player
    global Last_Turn
    
    # Increase turn number and reset numbers used
    Turn_No =  Turn_No + 1
    P1_Used = 0
    P2_Used = 0
    
    # Define this turn board and scores state
    variables = globals()
    This_Turn = pd.read_csv ('Board_' + str(Turn_No - 1) + '.csv', header = 0)
    These_Scores = pd.read_csv ('Scores_' + str(Turn_No - 1) + '.csv', header = 0)

    # Find the row relating to the place location
    Place_index = Board_0[Board_0['x,y']==str(str(Place_x) + ',' + str(Place_y))].index.values
    
    #Define new board state as new df (allowing for backtracking)
    This_Turn['Value'].loc[Place_index] = int(Player)
    
    if int(Player) == 1:
        P1_Used = P1_Used + 1

    else:
        P2_Used = P2_Used + 1

    Calculate_Scores()
    Save_Scores()
    Save_Board()
    Show_Board()
       
# Step 4, Calculate markers required for go, and fill neighbours
    # Rename Place_x and Place_y as lookups to work with Define_Neighbour_Index
    lookup_x = Place_x
    lookup_y = Place_y
        
    Define_Neighbour_Index()
    Define_Neighbour_States()
    
    # Need some game state identifier
                                          
    # Identify if this is the players last go or not.
    # Check if the number of markers required to play is greater than those available
    Req_Markers = sum(1 for item in Neighbour_vals if item==(0)) + 1
    Player_Markers = int(These_Scores[str('Markers_P' + str(Player))].loc[0])
      
    # If so then keep player playing until they run out of markers
    # This ends up in a death loop, needs sorting out. I wonder if we can deal with this during the 
    if Req_Markers >= Player_Markers:
        Last_Go()
     
    # If not then fill neighbours
    elif Req_Markers < Player_Markers:
        Neighbour_No = 1
    
        Neighbours = dict([(1, 'a'), (2, 'b'), (3, 'c'), (4, 'd'), (5, 'e'), (6, 'f')])
            
        while Neighbour_No <= 6:
            if variables['{}_state'.format(Neighbours[Neighbour_No])] == int(Player):
                This_Turn['Value'].loc[variables['{}_index'.format(Neighbours[Neighbour_No])]] = int(Player)

            elif variables['{}_state'.format(Neighbours[Neighbour_No])] == 3:
                This_Turn['Value'].loc[variables['{}_index'.format(Neighbours[Neighbour_No])]] = 3 
    
            else:
                This_Turn['Value'].loc[variables['{}_index'.format(Neighbours[Neighbour_No])]] = int(Player)
                if int(Player) == 1:
                    P1_Used = P1_Used + 1
                    
                else:
                    P2_Used = P2_Used + 1                    
    
            Neighbour_No = Neighbour_No + 1
                
        Calculate_Scores()
        Save_Scores()
        Save_Board()
        Show_Board()
            
    else:
        pass
                                           
# Step 5, Search for and remove enclosed areas
    # Start with opposing player no
    No_Rotations = 0
    InPlay_P1 = This_Turn[This_Turn.Value == 1].sum().loc['Value']
    InPlay_P2 = int(This_Turn[This_Turn.Value == 2].sum().loc['Value'] / 2)
        
    # Setup loop to repeat until each piece is assessed
    while No_Rotations <= max(InPlay_P1,InPlay_P2):        
        This_Turn_index = 0
        # Setup loop to run through each row of board
        while This_Turn_index <= 528:
            if int(This_Turn['Value'].loc[int(This_Turn_index)]) == int(Opponent):
                lookup_x = This_Turn['x'].loc[int(This_Turn_index)]
                lookup_y = This_Turn['y'].loc[int(This_Turn_index)]

                Define_Neighbour_Index()
                    
                Define_Neighbour_States() 

                # Mark anything with "0" neighbours as "4"
                if sum(1 for item in Neighbour_vals if item==(0)) > 0:
                    This_Turn['Value'].loc[This_Turn_index] = 4

                # Mark anything with "4" neighbours as "4"
                if sum(1 for item in Neighbour_vals if item==(4)) > 0:
                    This_Turn['Value'].loc[This_Turn_index] = 4
            
                This_Turn_index = This_Turn_index + 1
                    
            else:
                This_Turn_index = This_Turn_index + 1
        
        # Repeat for every board Rotation
        No_Rotations = No_Rotations + max(1, (max(InPlay_P1,InPlay_P2) - max(This_Turn[This_Turn.Value == 1].sum().loc['Value'], int(This_Turn[This_Turn.Value == 2].sum().loc['Value'] / 2))))
        InPlay_P1 = This_Turn[This_Turn.Value == 1].sum().loc['Value']
        InPlay_P2 = int(This_Turn[This_Turn.Value == 2].sum().loc['Value'] / 2)
        
    # Mark all remaining opponent as "0"
    This_Turn.loc[(This_Turn.Value == int(Opponent)),'Value'] = 0
            
    # Mark all 4s as Opponent no
    This_Turn.loc[(This_Turn.Value == 4),'Value'] = int(Opponent)

    # Repeat for player
    No_Rotations = 0
    InPlay_P1 = This_Turn[This_Turn.Value == 1].sum().loc['Value']
    InPlay_P2 = int(This_Turn[This_Turn.Value == 2].sum().loc['Value'] / 2)
        
    while No_Rotations <= max(InPlay_P1,InPlay_P2):        
        This_Turn_index = 0
        while This_Turn_index <= 528:
            if int(This_Turn['Value'].loc[int(This_Turn_index)]) == int(Player):

                lookup_x = This_Turn['x'].loc[int(This_Turn_index)]
                lookup_y = This_Turn['y'].loc[int(This_Turn_index)]
                    
                Define_Neighbour_Index()
                    
                Define_Neighbour_States()
                    
                # Mark anything with "0" neighbours as "4"
                if sum(1 for item in Neighbour_vals if item==(0)) > 0:
                    This_Turn['Value'].loc[This_Turn_index] = 4

                # Mark anything with "4" neighbours as "4"
                if sum(1 for item in Neighbour_vals if item==(4)) > 0:
                    This_Turn['Value'].loc[This_Turn_index] = 4
            
                This_Turn_index = This_Turn_index + 1
                    
            else:
                This_Turn_index = This_Turn_index + 1
        
        # Repeat for every board Rotation
        No_Rotations = No_Rotations + max(1, (max(InPlay_P1,InPlay_P2) - max(This_Turn[This_Turn.Value == 1].sum().loc['Value'], int(This_Turn[This_Turn.Value == 2].sum().loc['Value'] / 2))))
        InPlay_P1 = This_Turn[This_Turn.Value == 1].sum().loc['Value']
        InPlay_P2 = int(This_Turn[This_Turn.Value == 2].sum().loc['Value'] / 2)
                
    # Mark all remaining player as "0"
    This_Turn['Value'] = np.where((This_Turn.Value == int(Player)), 0, This_Turn.Value)
            
    # Mark all 4s as player no
    This_Turn['Value'] = np.where((This_Turn.Value == 4), int(Player), This_Turn.Value)

    # Step 6, Search for and remove one-neighboured tokens 
    No_Rotations = 0
    InPlay_P1 = This_Turn[This_Turn.Value == 1].sum().loc['Value']
    InPlay_P2 = int(This_Turn[This_Turn.Value == 2].sum().loc['Value'] / 2)
        
    while No_Rotations <= max(InPlay_P1,InPlay_P2):
        This_Turn_index = 0
        while This_Turn_index <= 528:
            if int(This_Turn['Value'].loc[int(This_Turn_index)]) == 1:
                lookup_x = This_Turn['x'].loc[int(This_Turn_index)]
                lookup_y = This_Turn['y'].loc[int(This_Turn_index)]
        
                Define_Neighbour_Index()
                Define_Neighbour_States()
                
                if sum(1 for item in Neighbour_vals if item==(1)) <= 1:
                    This_Turn['Value'].loc[This_Turn_index] = 0
            
                else:
                    pass
    
            elif int(This_Turn['Value'].loc[int(This_Turn_index)]) == 2:
                lookup_x = This_Turn['x'].loc[int(This_Turn_index)]
                lookup_y = This_Turn['y'].loc[int(This_Turn_index)] 

                Define_Neighbour_Index()
                Define_Neighbour_States()
       
                if sum(1 for item in Neighbour_vals if item==(2)) <= 1:
                    This_Turn['Value'].loc[This_Turn_index] = 0
                    
                else:
                    pass
            
            else:
                pass
                
            This_Turn_index = This_Turn_index + 1

        No_Rotations = No_Rotations + max(1, (max(InPlay_P1,InPlay_P2) - max(This_Turn[This_Turn.Value == 1].sum().loc['Value'], int(This_Turn[This_Turn.Value == 2].sum().loc['Value'] / 2))))
        InPlay_P1 = This_Turn[This_Turn.Value == 1].sum().loc['Value']
        InPlay_P2 = int(This_Turn[This_Turn.Value == 2].sum().loc['Value'] / 2)
                    
    Calculate_Scores()
        
    Show_Board()

    # End the go and the formation of a new board
    Markers_P1 = int(These_Scores['Markers_P1'].loc[0])
    Markers_P2 = int(These_Scores['Markers_P2'].loc[0])
    Save_Scores()
    Save_Board()
        
    Total_Markers = Markers_P1 + Markers_P2
            
    Player_Check()    
    Show_Board()
        
#%% What the buttons do
def Go_Back():
    to_turn = int(input('To turn: '))
                
    Turn_No = int(to_turn)
               
    This_Turn = pd.read_csv ('Board_' + str(Turn_No) + '.csv', header = 0) 
    These_Scores = pd.read_csv ('Scores_' + str(Turn_No) + '.csv', header = 0)    
    Markers_P1 = int(These_Scores['Markers_P1'].loc[0])
    Markers_P2 = int(These_Scores['Markers_P2'].loc[0])
                
    Show_Board()

#%% Create and show board to players
Calculate_Scores()

Player_Check()

Show_Board()
               
#%% Some other front end stuff
                
# Describes the button and what function it runs
canvas = tk.Canvas(root, width = 40, height = 30)
BTT = tk.Button(root, text = 'Take Turn', command = Input, bg='brown',fg='white')
BGB = tk.Button(root, text = 'Go Back', command = Go_Back, bg='brown',fg='white')

BTT.pack(); canvas.pack()
BGB.pack()

entry1 = tk.Entry (root) 
canvas.create_window(20, 15, window=entry1)

#%% Sort out engame
if Markers_P1 <= 0 and Markers_P2 <= 0:
    # End Game and display winner!
    InPlay_P1 = These_Scores['InPlay_P1'].loc[0]
    InPlay_P2 = These_Scores['InPlay_P2'].loc[0]
    
    # Calculate margin percentage
    Margin_Of_Victory = ((InPlay_P1 - InPlay_P2)**2)**(0.5)
    Total_InPlay = InPlay_P1 + InPlay_P2
    Margin_Percentage = (100 * int(Margin_Of_Victory))/Total_InPlay
        
    # Determine outcome based on margin percentage
    if Margin_Percentage < 5:
        outcome = 'a Hollow Victory'
          
    elif 6 <=Margin_Percentage <= 15:
        outcome = 'a Technical Victory'
            
    elif 16 <= Margin_Percentage <= 30:
        outcome = 'an Outright Victory'    
        
    elif 31 <= Margin_Percentage <= 50:
        outcome = 'DOMINATION'
        
    elif Margin_Percentage > 50:
        outcome = 'an ANNIHILATION'
            
    else:
        pass    
        
    # Define winner
    if These_Scores['InPlay_P1'].loc[0] > These_Scores['InPlay_P2'].loc[0]:
        winner = 'White'
        winner_no = entry1
    else:
        winner = 'Black'
        winner_no = 2
        
    # Print outcome
    if InPlay_P1 == InPlay_P2:
        print('End of game, A Draw? How did that happen?')
    else:
        print('End of game, congratulations ' + str(winner) + ', you acheived ' + str(outcome))
        
    #Remove_old_files()

# No idea what this does but its  important.
root.mainloop()    
