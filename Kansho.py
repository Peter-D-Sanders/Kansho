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
    Go_To() - Allows the player to select a previous turn or 'load' a saved game.

UPDATE RECORD:
Date          Version     Author         Description
11/06/2020    v1.0        Pete Sanders   Created
12/06/2020    v1.1        Pete Sanders   Bug fixes
                                         Minor alterations to board display
                                         Prints board images to files
20/05/2022    v2.0        Pete Sanders   Included some basic front end.   
24/05/2022    v2.1        Pete Sanders   Re-ordering of code to work better with front end commands.                                      
16/06/2022    v2.3        Pete Sanders   Fixed issues with turn ordering and endgame.
17/06/2022    v2.4        Pete Sanders   Made some improvements.
                                        
RECOMMENDED FUTURE IMPROVEMENTS:
    Make one neighboured tokens and enclosed areas loops more efficient.
    Mark placed marker as red when players last go to make it easier to know where to place other markers
    Allow game saving and sub-directories for saved games.
    Add a turn by turn commentary.
    Include a side pannel for commentary so that the console is not needed.
    Change board co-ordinates to start at 0,0 in the bottom left corner.    

Bugs:
    Player not remembered using Go_To(): e.g. if white played turn 3, black would play when go back to t3 is active, needs changing.
    Issue with endgame if player has more than one go in a row to end.    

"""
#%% Import nessessary modules
import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np
from pathlib import Path
import tkinter as tk
from tkinter import *
from PIL import ImageTk, Image
import math
import warnings

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
global Last_Turn_Count
global Opponent

warnings.filterwarnings('ignore')

# Print instrustions
print ('Instructions:', '\n',
       'The input boxes will be used to input your moves and commands.', '\n',
       'When making a move enter the x and y co-ordinates for the move you want to make in the upper box.', '\n',
       "Then click on the 'Take Turn' button", '\n',
       'Co-ordinates can be entered using a decimal point e.g. (1 , 1.5)', '\n',
       "If you want to go back to a particular move or 'load a saved game' enter the number of the turn into the bottom box.", '\n',
       "Then click on the 'Go To' button and the game can contunue from that move", '\n',
       'Have fun!', '\n',)

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
Opponent = 2
Last_Turn = 0
Last_Turn_Count = 0

#%%  2. Define board and scores
# This should be done using code up front, instead of reading a csv file like it is currently.
Board_0_data = {'x': [11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,
                      8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,
                      5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,
                      2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
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
                'y': [11,10,9,8,7,6,5,4,3,2,1,0,-1,-2,-3,-4,-5,-6,-7,-8,-9,-10,-11,11,10,9,8,7,6,5,4,3,2,1,0,-1,-2,-3,-4,-5,-6,-7,-8,-9,-10,-11,
                      11,10,9,8,7,6,5,4,3,2,1,0,-1,-2,-3,-4,-5,-6,-7,-8,-9,-10,-11,11,10,9,8,7,6,5,4,3,2,1,0,-1,-2,-3,-4,-5,-6,-7,-8,-9,-10,-11,
                      11,10,9,8,7,6,5,4,3,2,1,0,-1,-2,-3,-4,-5,-6,-7,-8,-9,-10,-11,11,10,9,8,7,6,5,4,3,2,1,0,-1,-2,-3,-4,-5,-6,-7,-8,-9,-10,-11,
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
                'x,y': ['11,11','11,10','11,9','11,8','11,7','11,6','11,5','11,4','11,3','11,2','11,1','11,0','11,-1','11,-2','11,-3','11,-4','11,-5','11,-6','11,-7','11,-8','11,-9','11,-10','11,-11',
                        '10,11','10,10','10,9','10,8','10,7','10,6','10,5','10,4','10,3','10,2','10,1','10,0','10,-1','10,-2','10,-3','10,-4','10,-5','10,-6','10,-7','10,-8','10,-9','10,-10','10,-11',
                        '9,11','9,10','9,9','9,8','9,7','9,6','9,5','9,4','9,3','9,2','9,1','9,0','9,-1','9,-2','9,-3','9,-4','9,-5','9,-6','9,-7','9,-8','9,-9','9,-10','9,-11',
                        '8,11','8,10','8,9','8,8','8,7','8,6','8,5','8,4','8,3','8,2','8,1','8,0','8,-1','8,-2','8,-3','8,-4','8,-5','8,-6','8,-7','8,-8','8,-9','8,-10','8,-11',
                        '7,11','7,10','7,9','7,8','7,7','7,6','7,5','7,4','7,3','7,2','7,1','7,0','7,-1','7,-2','7,-3','7,-4','7,-5','7,-6','7,-7','7,-8','7,-9','7,-10','7,-11',
                        '6,11','6,10','6,9','6,8','6,7','6,6','6,5','6,4','6,3','6,2','6,1','6,0','6,-1','6,-2','6,-3','6,-4','6,-5','6,-6','6,-7','6,-8','6,-9','6,-10','6,-11',
                        '5,11','5,10','5,9','5,8','5,7','5,6','5,5','5,4','5,3','5,2','5,1','5,0','5,-1','5,-2','5,-3','5,-4','5,-5','5,-6','5,-7','5,-8','5,-9','5,-10','5,-11',
                        '4,11','4,10','4,9','4,8','4,7','4,6','4,5','4,4','4,3','4,2','4,1','4,0','4,-1','4,-2','4,-3','4,-4','4,-5','4,-6','4,-7','4,-8','4,-9','4,-10','4,-11',
                        '3,11','3,10','3,9','3,8','3,7','3,6','3,5','3,4','3,3','3,2','3,1','3,0','3,-1','3,-2','3,-3','3,-4','3,-5','3,-6','3,-7','3,-8','3,-9','3,-10','3,-11',
                        '2,11','2,10','2,9','2,8','2,7','2,6','2,5','2,4','2,3','2,2','2,1','2,0','2,-1','2,-2','2,-3','2,-4','2,-5','2,-6','2,-7','2,-8','2,-9','2,-10','2,-11',
                        '1,11','1,10','1,9','1,8','1,7','1,6','1,5','1,4','1,3','1,2','1,1','1,0','1,-1','1,-2','1,-3','1,-4','1,-5','1,-6','1,-7','1,-8','1,-9','1,-10','1,-11',
                        '0,11','0,10','0,9','0,8','0,7','0,6','0,5','0,4','0,3','0,2','0,1','0,0','0,-1','0,-2','0,-3','0,-4','0,-5','0,-6','0,-7','0,-8','0,-9','0,-10','0,-11',
                        '-1,11','-1,10','-1,9','-1,8','-1,7','-1,6','-1,5','-1,4','-1,3','-1,2','-1,1','-1,0','-1,-1','-1,-2','-1,-3','-1,-4','-1,-5','-1,-6','-1,-7','-1,-8','-1,-9','-1,-10','-1,-11',
                        '-2,11','-2,10','-2,9','-2,8','-2,7','-2,6','-2,5','-2,4','-2,3','-2,2','-2,1','-2,0','-2,-1','-2,-2','-2,-3','-2,-4','-2,-5','-2,-6','-2,-7','-2,-8','-2,-9','-2,-10','-2,-11',
                        '-3,11','-3,10','-3,9','-3,8','-3,7','-3,6','-3,5','-3,4','-3,3','-3,2','-3,1','-3,0','-3,-1','-3,-2','-3,-3','-3,-4','-3,-5','-3,-6','-3,-7','-3,-8','-3,-9','-3,-10','-3,-11',
                        '-4,11','-4,10','-4,9','-4,8','-4,7','-4,6','-4,5','-4,4','-4,3','-4,2','-4,1','-4,0','-4,-1','-4,-2','-4,-3','-4,-4','-4,-5','-4,-6','-4,-7','-4,-8','-4,-9','-4,-10','-4,-11',
                        '-5,11','-5,10','-5,9','-5,8','-5,7','-5,6','-5,5','-5,4','-5,3','-5,2','-5,1','-5,0','-5,-1','-5,-2','-5,-3','-5,-4','-5,-5','-5,-6','-5,-7','-5,-8','-5,-9','-5,-10','-5,-11',
                        '-6,11','-6,10','-6,9','-6,8','-6,7','-6,6','-6,5','-6,4','-6,3','-6,2','-6,1','-6,0','-6,-1','-6,-2','-6,-3','-6,-4','-6,-5','-6,-6','-6,-7','-6,-8','-6,-9','-6,-10','-6,-11',
                        '-7,11','-7,10','-7,9','-7,8','-7,7','-7,6','-7,5','-7,4','-7,3','-7,2','-7,1','-7,0','-7,-1','-7,-2','-7,-3','-7,-4','-7,-5','-7,-6','-7,-7','-7,-8','-7,-9','-7,-10','-7,-11',
                        '-8,11','-8,10','-8,9','-8,8','-8,7','-8,6','-8,5','-8,4','-8,3','-8,2','-8,1','-8,0','-8,-1','-8,-2','-8,-3','-8,-4','-8,-5','-8,-6','-8,-7','-8,-8','-8,-9','-8,-10','-8,-11',
                        '-9,11','-9,10','-9,9','-9,8','-9,7','-9,6','-9,5','-9,4','-9,3','-9,2','-9,1','-9,0','-9,-1','-9,-2','-9,-3','-9,-4','-9,-5','-9,-6','-9,-7','-9,-8','-9,-9','-9,-10','-9,-11',
                        '-10,11','-10,10','-10,9','-10,8','-10,7','-10,6','-10,5','-10,4','-10,3','-10,2','-10,1','-10,0','-10,-1','-10,-2','-10,-3','-10,-4','-10,-5','-10,-6','-10,-7','-10,-8','-10,-9','-10,-10','-10,-11',
                        '-11,11','-11,10','-11,9','-11,8','-11,7','-11,6','-11,5','-11,4','-11,3','-11,2','-11,1','-11,0','-11,-1','-11,-2','-11,-3','-11,-4','-11,-5','-11,-6','-11,-7','-11,-8','-11,-9','-11,-10','-11,-11'],
                'Value': [3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,0,0,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,0,0,0,0,0,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,
                          0,0,0,0,0,0,0,0,0,3,3,3,3,3,3,3,3,3,3,3,3,0,0,0,0,0,0,0,0,0,0,0,0,3,3,3,3,3,3,3,3,3,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,3,3,3,3,3,3,3,3,3,0,0,0,0,0,0,0,0,
                          0,0,0,0,0,0,3,3,3,3,3,3,3,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,3,3,3,3,3,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,3,3,3,3,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
                          3,3,3,3,3,3,3,0,0,0,0,0,0,0,3,3,0,0,0,0,0,0,0,3,3,3,3,3,3,0,0,0,0,0,0,0,3,3,3,0,0,0,0,0,0,0,3,3,3,3,3,3,3,0,0,0,0,0,0,0,3,3,0,0,0,0,0,0,0,3,3,3,3,3,3,0,
                          0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,3,3,3,3,3,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,3,3,3,3,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,3,3,3,3,3,3,3,3,0,0,0,0,0,0,
                          0,0,0,0,0,0,0,0,3,3,3,3,3,3,3,3,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,3,3,3,3,3,3,3,3,3,3,0,0,0,0,0,0,0,0,0,0,0,0,3,3,3,3,3,3,3,3,3,3,3,0,0,0,0,0,0,0,0,0,3,3,
                          3,3,3,3,3,3,3,3,3,3,3,3,3,3,0,0,0,0,0,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,0,0,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3]}

# Set Board_0_data to datframe
Board_0 = pd.DataFrame(data = Board_0_data)
This_Turn = Board_0
This_Turn.to_csv('Board_'+str(Turn_No) +'.csv',index=False)

Scores_0_data = {'InPlay_P1': [0],
                'InPlay_P2': [0],
                'Markers_P1': [Markers_P1],
                'Markers_P2': [Markers_P2]}
Scores_0 = pd.DataFrame(data = Scores_0_data)
These_Scores = Scores_0
These_Scores.to_csv('Scores_'+str(Turn_No) +'.csv',index=False)

#%% Step 3, Setup the initial part of the front end
# This has to happen before Show_Board() is called because Show_Board() uses the panel.
# Assignes some function within tk to root
root = tk.Tk()
root.title('Kansho')
root.geometry('666x800')

panel = Label(root)
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

        file_no = file_no + 1

#%% Show Board
def Show_Board():
    global panel
    global img
    global Player
    global height
    global imgsize
    
    # turn interactive plotting off
    plt.ioff()
    
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
    plt.scatter(x_board,y_board, marker = 'H', s = 1300, color = (0.74,0.47,0.34), edgecolor = 'k', linewidth = 1)
    plt.scatter(x_3,y_3, marker = 'H', s = 1500, color = 'w')
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
    plt.close()
    plt.pause(0.1)
    
    root.update()
    height = root.winfo_height()
    imgsize = int(math.floor(height * (5/6)))
    
    panel.destroy()
    
    img = Image.open('Turn_{}'.format(Turn_No) +'.jpg')
    img = img.resize((imgsize, imgsize), Image.ANTIALIAS)
    img = ImageTk.PhotoImage(img)
    panel = Label(root, image = img)
    panel.pack_propagate(0)
    panel.pack(side = "bottom", fill = tk.BOTH, expand = True)
    
#%% Calculate score
def Calculate_Scores():
    global Turn_No
    global P1_Used
    global P2_Used
    global Last_Turn
    global Player
    
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
    
    if Last_Turn == 1 and Player == 2:
        pass
    else:
        These_Scores['Markers_P1'].loc[0] = Scores['Markers_P1'].loc[0] - P1_Used
        
    if Last_Turn == 1 and Player == 1:
        pass
    else:
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
    global Markers_P1
    global Markers_P2
    
    if Markers_P1 <= 0 and Markers_P2 > 0:
        Player = 2
        Opponent = 1
    elif Markers_P2 <= 0 and Markers_P1 > 0:
        Player = 1
        Opponent = 2
    else:
        pass
    
    if Last_Turn == 0 and Player == 1 and Markers_P1 > 0:
        print('White player...your turn','\n',)
    elif Last_Turn == 0 and Player == 2 and Markers_P2 > 0:
        print('Black player...your turn','\n',)
    else:
        pass
        
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
    global lookup_x
    global lookup_y

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
    global Player_Markers
    global Req_Markers
    global Neighbour_index
    global Last_Turn_Count
    global Total_Markers
    global Opponent
    
    # Increase turn number and reset numbers used
    Turn_No = Turn_No + 1
    
    P1_Used = 0
    P2_Used = 0

    Calculate_Scores()
    
    # Define this turn board and scores state
    variables = globals()
    This_Turn = pd.read_csv ('Board_' + str(Turn_No - 1) + '.csv', header = 0)
    These_Scores = pd.read_csv ('Scores_' + str(Turn_No - 1) + '.csv', header = 0)

    # Find the row relating to the place location
    Place_index = Board_0[Board_0['x,y']==str(str(Place_x) + ',' + str(Place_y))].index.values
    
    # Define new board state as new df (allowing for backtracking)
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
                                          
    # Identify if this is the players last go or not.
    # Check if the number of markers required to play is greater than those available
    if Last_Turn == 1:
        pass
    else:
        Req_Markers = sum(1 for item in Neighbour_vals if item != 3) - sum(1 for item in Neighbour_vals if item == Player)
        
    Player_Markers = int(These_Scores[str('Markers_P' + str(Player))].loc[0])
     
    # If so then fill neighbours
    if Req_Markers <= Player_Markers:
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
        
    # If not then perform last go procedures
    elif Req_Markers > Player_Markers:
        Last_Turn_Count = Last_Turn_Count + 1
        
        # Sets the condition for the last go, enabling code below to be skipped until the last go is over.
        if Player_Markers > 0:
            Last_Turn = 1
        else:
            Last_Turn = 0
    
        if Player == 2 and Last_Turn_Count == 1:
            print('Black player, this is your last go, good luck!','\n',)
        elif Player == 1 and Last_Turn_Count == 1:
            print('White player, this is your last go, good luck!','\n',)
        else:
            pass
                
        if Player_Markers > 0:
            if Player == 2:
                print('Black player its still your turn','\n',)
            elif Player == 1:
                print('White player its still your turn','\n',)
            else:
                Last_Turn_Count == 0
                    
            # Define Neighbour_index and make sure that only these spaces are used for future moves   
            if Last_Turn_Count == 1:
                Neighbour_index = [int(a_index), int(b_index), int(c_index), int(d_index), int(e_index), int(f_index)]
            else:
                pass                    
                    
        Player_Markers = int(These_Scores[str('Markers_P' + str(Player))].loc[0])
                
       # Req_Markers = Req_Markers - 1
            
        Calculate_Scores()
        Save_Scores()
        Save_Board()
        Show_Board()
            
    else:
        Calculate_Scores()
        Save_Scores()
        Save_Board()
        Show_Board()
                                           
    if Last_Turn == 1 and ((Player == 1 and Markers_P1 > 0) or (Player == 2 and Markers_P2 > 0)):
        pass
    else:
        # Reset Last_Turn and Last_Turn_Count == 0
        Last_Turn == 0
        Last_Turn_Count == 0
        
        # Step 5, Search for and remove enclosed areas, starts with opposing player no.
        # Maybe this could be a seperate function
        No_Rotations = 0
        InPlay_P1 = This_Turn[This_Turn.Value == 1].sum().loc['Value']
        InPlay_P2 = int(This_Turn[This_Turn.Value == 2].sum().loc['Value'] / 2)
            
        # Setup loop to repeat until each piece is assessed
        while No_Rotations <= (InPlay_P1 + InPlay_P2):        
            This_Turn_index = 0
            
            # Setup loop to run through each 'row' of board
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
            No_Rotations = No_Rotations + 1
            InPlay_P2 = int(This_Turn[This_Turn.Value == 2].sum().loc['Value'] / 2)
            
        # Mark all remaining opponent as "0"
        This_Turn.loc[(This_Turn.Value == int(Opponent)),'Value'] = 0
                
        # Mark all 4s as Opponent no
        This_Turn.loc[(This_Turn.Value == 4),'Value'] = int(Opponent)
    
        # Repeat for player
        No_Rotations = 0
            
        while No_Rotations <= (InPlay_P1 + InPlay_P2):        
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
            No_Rotations = No_Rotations + 1
            InPlay_P1 = This_Turn[This_Turn.Value == 1].sum().loc['Value']
            InPlay_P2 = int(This_Turn[This_Turn.Value == 2].sum().loc['Value'] / 2)
                    
        # Mark all remaining player as "0"
        This_Turn['Value'] = np.where((This_Turn.Value == int(Player)), 0, This_Turn.Value)
        
        # Mark all 4s as player no
        This_Turn['Value'] = np.where((This_Turn.Value == 4), int(Player), This_Turn.Value)
    
        # Step 6, Search for and remove one-neighboured tokens
        # Maybe this could be a seperate function
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
    Calculate_Scores()
    
    Markers_P1 = int(These_Scores['Markers_P1'].loc[0])
    Markers_P2 = int(These_Scores['Markers_P2'].loc[0])
    
    Save_Scores()
    Save_Board()
        
    Total_Markers = Markers_P1 + Markers_P2
    
    Show_Board()
    
    # if not a last go then swap player
    if Last_Turn == 0:
        Calculate_Scores()
        Save_Scores()
        Save_Board()
        Show_Board()
        
        #Swap player
        if Player == 1 and Opponent == 2:
            Player = 2
            Opponent = 1
        elif Player == 2 and Opponent == 1:
            Player = 1
            Opponent = 2
        else:
            pass
        
        Player_Check()
    
    else:
        pass
    
    Show_Board()
    
    # Sort out endgame
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
        else:
            winner = 'Black'
            
        # Print outcome
        if InPlay_P1 == InPlay_P2:
            print('End of game, A Draw? How did that happen?',)
        else:
            print('End of game, congratulations ' + str(winner) + ', you acheived ' + str(outcome))
            
        #Remove_old_files()
    
#%% Input co-ordinates, checks that inputted co-ordinates match the entry requirements.
# If so, passes to Take_Turn(), If not, displays error message.
def Input():      
    global Place_x
    global Place_y 
    global entry1
    global coords
    global Last_Turn
    global Neighbour_index
       
    # The entry requirements are that:
    # 1. Integers between -10 and 10 must be used.
    # 2. They must be seperated by a single comma.
    # 3. They must represent a location on the board.
    # 4. The location must be unoccupied by another piece
    #    (unless its the last go in which case it can be occupied by the opponents piece).
    
    Pass = 0
    
    # 1. Check that there is text in input1, that it has at least one comma, and that numbers are either side of the comma.
    if (str(entry1.get()) != '') and (',' in str(entry1.get())):
        coords = list(entry1.get().split(','))
        Place_x = float(coords[0])
        Place_y = float(coords[1])
        
        # Round down to floor and convert to integer
        Place_x = int(math.floor(Place_x))
        Place_y = int(math.floor(Place_y))
        
        entry1.delete(0, END)
        Pass = Pass + 1
    else:
        entry1.delete(0, END)
        
    # 2. Check to see if Place_x and Place_y are integers between -10 and 10
    if (-10 <= Place_x <= 10) and (-10 <= Place_y <= 10):
        Pass = Pass + 1
    else:
        pass
    
    # 3. Check to see if co-ordinate is on board
    while (sum(1 for item in This_Turn['x'] if item==(Place_x)) == 0) and (sum(1 for item in This_Turn['y'] if item==(Place_y)) == 0):
        pass
    else:
        Pass = Pass + 1
    
    # 4. Check to see if required space is occupied
    # Find the row relating to the place location
    Place_index = Board_0[Board_0['x,y']==str(str(Place_x) + ',' + str(Place_y))].index.values
    Place_State = int(This_Turn['Value'].loc[Place_index])
    
    if Last_Turn == 0 and Place_State > 0:
        pass
    elif Last_Turn == 1 and Place_State != Player:
        Pass = Pass + 1
    elif Last_Turn == 1 and Place_State == Player:
        pass
    else:
        Pass = Pass + 1
    
    # Check to see if all stages passed, if so contunue, if not pass
    if Pass == 4 and Last_Turn == 0:
        Take_Turn()
    elif Pass == 4 and Last_Turn == 1 and ((sum(1 for item in Neighbour_index if item == Place_index)) > 0): 
        Take_Turn()
    else:
        print('Entered co-ordinate is incorrect, please try again','\n',)
        
#%% What the buttons do
def Go_To():
    global This_Turn
    global Markers_P1
    global Markers_P2
    global These_Scores
    global Turn_No
                   
    Turn = str(entry2.get())
    
    # The entry requirements are that:
    # 1. Integers between 1 and 246 must be used.
    
    Pass = 0
    
    # 1. Check that there is text in input2 and that it is an integer between 1 and 246 incl.
    if (int(Turn) >= 1) and (int(Turn) <= 246):
        entry2.delete(0, END)
        Pass = Pass + 1
    else:
        entry2.delete(0, END)
            
    # Check to see if all stages passed, if so contunue, if not pass
    if Pass == 1:
        Turn_No = int(Turn)
        This_Turn = pd.read_csv ('Board_' + str(Turn_No) + '.csv', header = 0) 
        These_Scores = pd.read_csv ('Scores_' + str(Turn_No) + '.csv', header = 0)    
        Markers_P1 = int(These_Scores['Markers_P1'].loc[0])
        Markers_P2 = int(These_Scores['Markers_P2'].loc[0])

    else:
        print('Not a valid turn number, please try again','\n',)
    
    Show_Board()

#%% Create and show board to players  
Calculate_Scores()
Player_Check()
Show_Board()
               
#%% Some other front end stuff
canwidth = imgsize
canheight = int(math.floor(height * (1/6)))
butheight = canheight / 5
fontsize = int(math.floor(butheight * 0.5))

canvas1 = tk.Canvas(root, width = canwidth, height = canheight)
BTT = tk.Button(canvas1, text = 'Take Turn', font = ('Arial', fontsize), command = Input, bg='brown',fg='white')
BGB = tk.Button(canvas1, text = 'Go To', font = ('Arial', fontsize), command = Go_To, bg='brown',fg='white')
entry1 = tk.Entry(canvas1, font = ('Arial', fontsize))
entry2 = tk.Entry(canvas1, font = ('Arial', fontsize))

canvas1.pack()
BTT.place(height = butheight, width = 100, x = (canwidth / 2) + 70, y = butheight)
BGB.place(height = butheight, width = 100, x = (canwidth / 2) + 70, y = butheight * 3)
entry1.place(height = butheight, width = 100, x = (canwidth / 2) - 50, y = butheight)
entry2.place(height = butheight, width = 100, x = (canwidth / 2) - 50, y = butheight * 3)
text1 = canvas1.create_text((canwidth / 2) - 60, butheight + (butheight / 2), anchor = "e")
canvas1.itemconfig(text1, text="Enter co-ordinates here (x,y):", font = ('Arial', fontsize))
text2 = canvas1.create_text((canwidth / 2) - 60, butheight * 3 + (butheight / 2), anchor = "e")
canvas1.itemconfig(text2, text="Enter turn number here:", font = ('Arial', fontsize))

# No idea what this does but its  important.
root.mainloop()    
