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
    Save_Scores() and Save_Board() - Outputs the current turns board and scores
    Input_x() and Input_y() - Allows user to input  x and y co-ordinates and checks if input is integer
    Define_Neighbour_Index() - Calculates the index of current markers neighbours
    Define_Neighbour_States() - Calculates the state of current markers neighbours
    Take_Turn() - Sets up a loop to allow players to take turns
    Go_To() - Allows the player to select a previous turn or 'load' a saved game.
    Update_FE() - Allows the updating of the front end following resize or changes to Game_Notes

UPDATE RECORD:
Date          Version     Author          Description
11/06/2020    v1.0        Pete Sanders    Created
12/06/2020    v1.1        Pete Sanders    Bug fixes
                                          Minor alterations to board display
                                          Prints board images to files
20/05/2022    v2.0        Pete Sanders    Included some basic front end.   
24/05/2022    v2.1        Pete Sanders    Re-ordering of code to work better with front end commands.                                      
16/06/2022    v2.3        Pete Sanders    Fixed issues with turn ordering and endgame.
17/06/2022    v2.4        Pete Sanders    Made some improvements.
19/06/2022    v2.5        Pete Sanders    Added Game_Notes and side pannel.
19/06/2022    v2.6        Pete Sanders    Add 'Working on it...' to Game_Notes after completing a move.
                                          Allowed entry using ENTER key.
14/07/2022    v2.7        Pete Sanders    Updated front end, changed so that nothing saves to file,
                                          used pickle to store data locally.
16/07/2022    v2.8        Pete Sanders    Another go at trying to get the damned exe to work!.
19/07/2022    v2.9        Pete Sanders    Spme efficiencies in coding made.
                                        
RECOMMENDED FUTURE IMPROVEMENTS:
    Make one neighboured tokens and enclosed areas loops more efficient.
    Mark placed marker as red when players last go to make it easier to know where to place other markers
    Allow game saving and sub-directories for saved games.
    Find a better way to resize the FE.
    Allow entering of location from clicking on board.
    
Bugs:

"""
#%% Import nessessary modules
import pandas as pd
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import *
from PIL import ImageTk
import math
import io
from PIL import Image
import numpy as np

#%% Setu initial front end stuff
root = tk.Tk()
root.title('Kansho v2.7')
root.geometry('875x500')

panel = Label(root)
panel.pack_propagate(0)
panel.pack(side = "left", fill = "both", expand = 1)

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
global Game_Notes

# Setup Game_Notes
Game_Notes = """Instructions:
       The input boxes will be used to input your moves and commands.
       When making a move enter the x and y co-ordinates for the move you want to make in the upper box.
       Then click on the 'Take Turn' button or press the ENTER key.
       Co-ordinates can be entered using a decimal point e.g. (1 , 1.5).
       If you want to go back to a particular move or 'load a saved game' enter the number of the turn into the bottom box.
       Then click on the 'Go To' button, or press the ENTER key, and the game can contunue from that move. \n \n"""
       
Game_Notes =  Game_Notes + 'Have fun! \n \n'

# Define initial condtions
Markers_P1 = 12
Markers_P2 = 12
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

# 2. Define board and scores
Board_0_data = {'x': [22,22,22,22,22,22,22,22,22,22,22,22,22,22,22,22,22,22,22,22,22,22,22,
                      21,21,21,21,21,21,21,21,21,21,21,21,21,21,21,21,21,21,21,21,21,21,21,
                      20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,
                      19,19,19,19,19,19,19,19,19,19,19,19,19,19,19,19,19,19,19,19,19,19,19,
                      18,18,18,18,18,18,18,18,18,18,18,18,18,18,18,18,18,18,18,18,18,18,18,
                      17,17,17,17,17,17,17,17,17,17,17,17,17,17,17,17,17,17,17,17,17,17,17,
                      16,16,16,16,16,16,16,16,16,16,16,16,16,16,16,16,16,16,16,16,16,16,16,
                      15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,
                      14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,
                      13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,
                      12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,
                      11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,
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
                      0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                'y': [22,21,20,19,18,17,16,15,14,13,12,11,10,9,8,7,6,5,4,3,2,1,0,
                      22,21,20,19,18,17,16,15,14,13,12,11,10,9,8,7,6,5,4,3,2,1,0,
                      22,21,20,19,18,17,16,15,14,13,12,11,10,9,8,7,6,5,4,3,2,1,0,
                      22,21,20,19,18,17,16,15,14,13,12,11,10,9,8,7,6,5,4,3,2,1,0,
                      22,21,20,19,18,17,16,15,14,13,12,11,10,9,8,7,6,5,4,3,2,1,0,
                      22,21,20,19,18,17,16,15,14,13,12,11,10,9,8,7,6,5,4,3,2,1,0,
                      22,21,20,19,18,17,16,15,14,13,12,11,10,9,8,7,6,5,4,3,2,1,0,
                      22,21,20,19,18,17,16,15,14,13,12,11,10,9,8,7,6,5,4,3,2,1,0,
                      22,21,20,19,18,17,16,15,14,13,12,11,10,9,8,7,6,5,4,3,2,1,0,
                      22,21,20,19,18,17,16,15,14,13,12,11,10,9,8,7,6,5,4,3,2,1,0,
                      22,21,20,19,18,17,16,15,14,13,12,11,10,9,8,7,6,5,4,3,2,1,0,
                      22,21,20,19,18,17,16,15,14,13,12,11,10,9,8,7,6,5,4,3,2,1,0,
                      22,21,20,19,18,17,16,15,14,13,12,11,10,9,8,7,6,5,4,3,2,1,0,
                      22,21,20,19,18,17,16,15,14,13,12,11,10,9,8,7,6,5,4,3,2,1,0,
                      22,21,20,19,18,17,16,15,14,13,12,11,10,9,8,7,6,5,4,3,2,1,0,
                      22,21,20,19,18,17,16,15,14,13,12,11,10,9,8,7,6,5,4,3,2,1,0,
                      22,21,20,19,18,17,16,15,14,13,12,11,10,9,8,7,6,5,4,3,2,1,0,
                      22,21,20,19,18,17,16,15,14,13,12,11,10,9,8,7,6,5,4,3,2,1,0,
                      22,21,20,19,18,17,16,15,14,13,12,11,10,9,8,7,6,5,4,3,2,1,0,
                      22,21,20,19,18,17,16,15,14,13,12,11,10,9,8,7,6,5,4,3,2,1,0,
                      22,21,20,19,18,17,16,15,14,13,12,11,10,9,8,7,6,5,4,3,2,1,0,
                      22,21,20,19,18,17,16,15,14,13,12,11,10,9,8,7,6,5,4,3,2,1,0,
                      22,21,20,19,18,17,16,15,14,13,12,11,10,9,8,7,6,5,4,3,2,1,0],
                'y_display': [22.5,21.5,20.5,19.5,18.5,17.5,16.5,15.5,14.5,13.5,12.5,11.5,10.5,9.5,8.5,7.5,6.5,5.5,4.5,3.5,2.5,1.5,0.5,
                              22,21,20,19,18,17,16,15,14,13,12,11,10,9,8,7,6,5,4,3,2,1,0,
                              22.5,21.5,20.5,19.5,18.5,17.5,16.5,15.5,14.5,13.5,12.5,11.5,10.5,9.5,8.5,7.5,6.5,5.5,4.5,3.5,2.5,1.5,0.5,
                              22,21,20,19,18,17,16,15,14,13,12,11,10,9,8,7,6,5,4,3,2,1,0,
                              22.5,21.5,20.5,19.5,18.5,17.5,16.5,15.5,14.5,13.5,12.5,11.5,10.5,9.5,8.5,7.5,6.5,5.5,4.5,3.5,2.5,1.5,0.5,
                              22,21,20,19,18,17,16,15,14,13,12,11,10,9,8,7,6,5,4,3,2,1,0,
                              22.5,21.5,20.5,19.5,18.5,17.5,16.5,15.5,14.5,13.5,12.5,11.5,10.5,9.5,8.5,7.5,6.5,5.5,4.5,3.5,2.5,1.5,0.5,
                              22,21,20,19,18,17,16,15,14,13,12,11,10,9,8,7,6,5,4,3,2,1,0,
                              22.5,21.5,20.5,19.5,18.5,17.5,16.5,15.5,14.5,13.5,12.5,11.5,10.5,9.5,8.5,7.5,6.5,5.5,4.5,3.5,2.5,1.5,0.5,
                              22,21,20,19,18,17,16,15,14,13,12,11,10,9,8,7,6,5,4,3,2,1,0,
                              22.5,21.5,20.5,19.5,18.5,17.5,16.5,15.5,14.5,13.5,12.5,11.5,10.5,9.5,8.5,7.5,6.5,5.5,4.5,3.5,2.5,1.5,0.5,
                              22,21,20,19,18,17,16,15,14,13,12,11,10,9,8,7,6,5,4,3,2,1,0,
                              22.5,21.5,20.5,19.5,18.5,17.5,16.5,15.5,14.5,13.5,12.5,11.5,10.5,9.5,8.5,7.5,6.5,5.5,4.5,3.5,2.5,1.5,0.5,
                              22,21,20,19,18,17,16,15,14,13,12,11,10,9,8,7,6,5,4,3,2,1,0,
                              22.5,21.5,20.5,19.5,18.5,17.5,16.5,15.5,14.5,13.5,12.5,11.5,10.5,9.5,8.5,7.5,6.5,5.5,4.5,3.5,2.5,1.5,0.5,
                              22,21,20,19,18,17,16,15,14,13,12,11,10,9,8,7,6,5,4,3,2,1,0,
                              22.5,21.5,20.5,19.5,18.5,17.5,16.5,15.5,14.5,13.5,12.5,11.5,10.5,9.5,8.5,7.5,6.5,5.5,4.5,3.5,2.5,1.5,0.5,
                              22,21,20,19,18,17,16,15,14,13,12,11,10,9,8,7,6,5,4,3,2,1,0,
                              22.5,21.5,20.5,19.5,18.5,17.5,16.5,15.5,14.5,13.5,12.5,11.5,10.5,9.5,8.5,7.5,6.5,5.5,4.5,3.5,2.5,1.5,0.5,
                              22,21,20,19,18,17,16,15,14,13,12,11,10,9,8,7,6,5,4,3,2,1,0,
                              22.5,21.5,20.5,19.5,18.5,17.5,16.5,15.5,14.5,13.5,12.5,11.5,10.5,9.5,8.5,7.5,6.5,5.5,4.5,3.5,2.5,1.5,0.5,
                              22,21,20,19,18,17,16,15,14,13,12,11,10,9,8,7,6,5,4,3,2,1,0,
                              22.5,21.5,20.5,19.5,18.5,17.5,16.5,15.5,14.5,13.5,12.5,11.5,10.5,9.5,8.5,7.5,6.5,5.5,4.5,3.5,2.5,1.5,0.5],
                'x,y': ['22,22','22,21','22,20','22,19','22,18','22,17','22,16','22,15','22,14','22,13','22,12','22,11','22,10','22,9','22,8','22,7','22,6','22,5','22,4','22,3','22,2','22,1','22,0',
                        '21,22','21,21','21,20','21,19','21,18','21,17','21,16','21,15','21,14','21,13','21,12','21,11','21,10','21,9','21,8','21,7','21,6','21,5','21,4','21,3','21,2','21,1','21,0',
                        '20,22','20,21','20,20','20,19','20,18','20,17','20,16','20,15','20,14','20,13','20,12','20,11','20,10','20,9','20,8','20,7','20,6','20,5','20,4','20,3','20,2','20,1','20,0',
                        '19,22','19,21','19,20','19,19','19,18','19,17','19,16','19,15','19,14','19,13','19,12','19,11','19,10','19,9','19,8','19,7','19,6','19,5','19,4','19,3','19,2','19,1','19,0',
                        '18,22','18,21','18,20','18,19','18,18','18,17','18,16','18,15','18,14','18,13','18,12','18,11','18,10','18,9','18,8','18,7','18,6','18,5','18,4','18,3','18,2','18,1','18,0',
                        '17,22','17,21','17,20','17,19','17,18','17,17','17,16','17,15','17,14','17,13','17,12','17,11','17,10','17,9','17,8','17,7','17,6','17,5','17,4','17,3','17,2','17,1','17,0',
                        '16,22','16,21','16,20','16,19','16,18','16,17','16,16','16,15','16,14','16,13','16,12','16,11','16,10','16,9','16,8','16,7','16,6','16,5','16,4','16,3','16,2','16,1','16,0',
                        '15,22','15,21','15,20','15,19','15,18','15,17','15,16','15,15','15,14','15,13','15,12','15,11','15,10','15,9','15,8','15,7','15,6','15,5','15,4','15,3','15,2','15,1','15,0',
                        '14,22','14,21','14,20','14,19','14,18','14,17','14,16','14,15','14,14','14,13','14,12','14,11','14,10','14,9','14,8','14,7','14,6','14,5','14,4','14,3','14,2','14,1','14,0',
                        '13,22','13,21','13,20','13,19','13,18','13,17','13,16','13,15','13,14','13,13','13,12','13,11','13,10','13,9','13,8','13,7','13,6','13,5','13,4','13,3','13,2','13,1','13,0',
                        '12,22','12,21','12,20','12,19','12,18','12,17','12,16','12,15','12,14','12,13','12,12','12,11','12,10','12,9','12,8','12,7','12,6','12,5','12,4','12,3','12,2','12,1','12,0',
                        '11,22','11,21','11,20','11,19','11,18','11,17','11,16','11,15','11,14','11,13','11,12','11,11','11,10','11,9','11,8','11,7','11,6','11,5','11,4','11,3','11,2','11,1','11,0',
                        '10,22','10,21','10,20','10,19','10,18','10,17','10,16','10,15','10,14','10,13','10,12','10,11','10,10','10,9','10,8','10,7','10,6','10,5','10,4','10,3','10,2','10,1','10,0',
                        '9,22','9,21','9,20','9,19','9,18','9,17','9,16','9,15','9,14','9,13','9,12','9,11','9,10','9,9','9,8','9,7','9,6','9,5','9,4','9,3','9,2','9,1','9,0',
                        '8,22','8,21','8,20','8,19','8,18','8,17','8,16','8,15','8,14','8,13','8,12','8,11','8,10','8,9','8,8','8,7','8,6','8,5','8,4','8,3','8,2','8,1','8,0',
                        '7,22','7,21','7,20','7,19','7,18','7,17','7,16','7,15','7,14','7,13','7,12','7,11','7,10','7,9','7,8','7,7','7,6','7,5','7,4','7,3','7,2','7,1','7,0',
                        '6,22','6,21','6,20','6,19','6,18','6,17','6,16','6,15','6,14','6,13','6,12','6,11','6,10','6,9','6,8','6,7','6,6','6,5','6,4','6,3','6,2','6,1','6,0',
                        '5,22','5,21','5,20','5,19','5,18','5,17','5,16','5,15','5,14','5,13','5,12','5,11','5,10','5,9','5,8','5,7','5,6','5,5','5,4','5,3','5,2','5,1','5,0',
                        '4,22','4,21','4,20','4,19','4,18','4,17','4,16','4,15','4,14','4,13','4,12','4,11','4,10','4,9','4,8','4,7','4,6','4,5','4,4','4,3','4,2','4,1','4,0',
                        '3,22','3,21','3,20','3,19','3,18','3,17','3,16','3,15','3,14','3,13','3,12','3,11','3,10','3,9','3,8','3,7','3,6','3,5','3,4','3,3','3,2','3,1','3,0',
                        '2,22','2,21','2,20','2,19','2,18','2,17','2,16','2,15','2,14','2,13','2,12','2,11','2,10','2,9','2,8','2,7','2,6','2,5','2,4','2,3','2,2','2,1','2,0',
                        '1,22','1,21','1,20','1,19','1,18','1,17','1,16','1,15','1,14','1,13','1,12','1,11','1,10','1,9','1,8','1,7','1,6','1,5','1,4','1,3','1,2','1,1','1,0',
                        '0,22','0,21','0,20','0,19','0,18','0,17','0,16','0,15','0,14','0,13','0,12','0,11','0,10','0,9','0,8','0,7','0,6','0,5','0,4','0,3','0,2','0,1','0,0'],
                'Value': [3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,
                          3,3,3,3,3,3,3,3,3,3,3,3,3,0,0,3,3,3,3,3,3,3,3,
                          3,3,3,3,3,3,3,3,3,3,3,0,0,0,0,0,3,3,3,3,3,3,3,
                          3,3,3,3,3,3,3,3,0,0,0,0,0,0,0,0,0,3,3,3,3,3,3,
                          3,3,3,3,3,3,0,0,0,0,0,0,0,0,0,0,0,0,3,3,3,3,3,
                          3,3,3,3,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,3,3,3,
                          3,3,3,3,3,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,3,3,
                          3,3,3,3,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,3,
                          3,3,3,3,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,
                          3,3,3,3,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,3,
                          3,3,3,3,3,0,0,0,0,0,0,0,3,3,0,0,0,0,0,0,0,3,3,
                          3,3,3,3,0,0,0,0,0,0,0,3,3,3,0,0,0,0,0,0,0,3,3,
                          3,3,3,3,3,0,0,0,0,0,0,0,3,3,0,0,0,0,0,0,0,3,3,
                          3,3,3,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,3,3,
                          3,3,3,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,3,
                          3,3,3,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,3,3,
                          3,3,3,3,3,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,3,3,
                          3,3,3,3,3,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,3,3,
                          3,3,3,3,3,3,3,3,0,0,0,0,0,0,0,0,0,0,0,0,3,3,3,
                          3,3,3,3,3,3,3,3,0,0,0,0,0,0,0,0,0,3,3,3,3,3,3,
                          3,3,3,3,3,3,3,3,3,3,0,0,0,0,0,3,3,3,3,3,3,3,3,
                          3,3,3,3,3,3,3,3,3,3,0,0,3,3,3,3,3,3,3,3,3,3,3,
                          3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3]}

# Set Board_0_data to datframe
Board_0 = pd.DataFrame(data = Board_0_data)
This_Turn = Board_0

# Pickles board for go back to use
globals()['Board_0' + '_io'] = io.StringIO()
This_Turn.to_csv(globals()['Board_0' + '_io'])

Scores_0_data = {'InPlay_P1': [0],
                'InPlay_P2': [0],
                'Markers_P1': [Markers_P1],
                'Markers_P2': [Markers_P2],
                'Player_No': [2],
                'Player': ['Black'],
                'Last turn': [0],
                'Last_Turn_Count': [0]}

Scores_0 = pd.DataFrame(data = Scores_0_data)
These_Scores = Scores_0
Game_Notes = (Game_Notes + 'Turn 0: \n     ' +
              'White has ' + str(Markers_P1) + ' markers, \n     ' +
              'Black has ' + str(Markers_P2) + ' markers, \n     ' +
              'Score: White = 0,  Black = 0.\n \n')

# Pickles scores for go back to use
globals()['Scores_0' + '_io'] = io.StringIO()
These_Scores.to_csv(globals()['Scores_0' + '_io'])

#%% Calculate_FE_sizes
def Calculate_FE_sizes():
    global height
    global width
    global imgsize
    global mid
    global canvas_height
    global button_height
    global button_width
    global fontsize
    global canvas_width
    global canvas1_height
    global canvas1_x
    global canvas2_height
    global canvas2_x
    global text_width
    global text1_height
    global text2_height
    global BTT_x
    global BTT_y
    global BGB_x
    global BGB_y
    global entry_x
    global entry1_y
    global entry2_y    
    
    root.update()
    height = root.winfo_height()
    width = root.winfo_width()
    imgsize = int(math.floor(height * (5/6)))
    mid = width / 2
    
    canvas_height = int(math.floor(height * (1/6)))
    button_height = int(canvas_height / 5)
    button_width = int(math.floor(imgsize / 6.5))
    
    fontsize = int(math.floor(button_height * 0.5))
    
    canvas_width = int(imgsize - button_height)
    canvas1_height = int(math.floor(height * (1/6)))
    canvas1_x = mid - imgsize + button_height
    canvas2_height = height - button_height
    canvas2_x = mid + button_height
    
    text_width = (imgsize / 2) - (button_width * 0.6)
    text1_height = button_height + (button_height / 2)
    text2_height = button_height * 3 + (button_height / 2)
    
    BTT_x = (imgsize / 2) + (button_width * 0.7)
    BTT_y = button_height
    BGB_x = (imgsize / 2) + (button_width * 0.7)
    BGB_y = button_height * 3
    
    entry_x = (imgsize / 2) - (button_width * 0.5)
    entry1_y = button_height
    entry2_y = button_height * 3

#%% Show Board
def Show_Board():
    global panel
    global img
    global Player
    global plt
    global This_Turn
    global Markers_P1
    global Markers_P2
    global These_Scores
    global Turn_No
    global Player
    global Game_Notes
    global Opponent
    global Last_Turn_Count
    global Last_Turn
    global panel
    global entry2
    
    # turn interactive plotting off
    plt.ioff()
    
    plt.figure(figsize=(10.4,10.9))

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
    plt.axis([0,22,0,20]) 
    major_ticksx = np.arange(0, 22, 1)
    major_ticksy = np.arange(0, 20, 1)
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
        plt.text(11,19.5, "White, it's your go", fontsize=18, verticalalignment='center', horizontalalignment='center', bbox=props)
    else:
        plt.text(11, 19.5, "Black, it's your go", fontsize=18, verticalalignment='center', horizontalalignment='center', bbox=props)
    
    plt.text(0.5, 1, 'White Score = ' + str("%.0f" % float(These_Scores.loc[0,'InPlay_P1'])) +
                        '\n' + 'Black Score = ' + str("%.0f" % float(These_Scores.loc[0,'InPlay_P2'])),
                        fontsize=18, verticalalignment='center', bbox=props)
    
    plt.text(21.5, 1, 'White Left = ' + str("%.0f" % float(These_Scores.loc[0,'Markers_P1'])) +
                          '\n' + 'Black Left = ' + str("%.0f" % float(These_Scores.loc[0,'Markers_P2'])),
                          fontsize=18, verticalalignment='center', horizontalalignment='right', bbox=props)
    
    plt.text(11, 10, 'Turn' + '\n' + str("%.0f" % float(Turn_No)), fontsize=18, verticalalignment='center', horizontalalignment='center', bbox=props)


    # Pause chart to display during loops   
    img_buf = io.BytesIO()
    
    plt.savefig(img_buf, format = 'png')
    plt.close()
    plt.pause(0.1)
        
    Calculate_FE_sizes()
    canvas1_height = int(math.floor(height * (1/5.8)))

    panel.destroy()
    img = Image.open(img_buf)
    img = img.resize((canvas_width, canvas_width), Image.ANTIALIAS)
    img = ImageTk.PhotoImage(img)
    panel = Label(root, image = img)
    panel.place(width = canvas_width, height = canvas_width, x = (width / 2) - canvas_width, y = canvas1_height)

#%% Calculate score
def Calculate_Scores():
    global Turn_No
    global P1_Used
    global P2_Used
    global Last_Turn
    global Player
    global Last_Turn
    global Last_Turn_Count
    
    # Makes sure code doesn't crash during Turn 0
    if Turn_No == 0:
        Turn_No = 1    
        # Unpickle the scores and board
        globals()['Scores_' + str(Turn_No - 1) + '_io'].seek(0)
        Scores = pd.read_csv(globals()['Scores_' + str(Turn_No - 1) + '_io'], header = 0)
        
        Turn_No = 0
    else:
        globals()['Scores_' + str(Turn_No - 1) + '_io'].seek(0)
        Scores = pd.read_csv(globals()['Scores_' + str(Turn_No - 1) + '_io'], header = 0)

    # Define scores for this turn based on 'Scores' and current markers used    
    These_Scores.loc[0,'InPlay_P1'] = This_Turn[This_Turn.Value == 1].sum().loc['Value']
    These_Scores.loc[0,'InPlay_P2'] = int(This_Turn[This_Turn.Value == 2].sum().loc['Value'] / 2)
    
    if Last_Turn == 1 and Player == 2:
        pass
    else:
        These_Scores.loc[0,'Markers_P1'] = Scores.loc[0,'Markers_P1'] - P1_Used
        
    if Last_Turn == 1 and Player == 1:
        pass
    else:
        These_Scores.loc[0,'Markers_P2'] = Scores.loc[0,'Markers_P2'] - P2_Used
        
    # Player
    These_Scores.loc[0,'Player_No'] = Player

    if Player == 1 :
        These_Scores.loc[0,'Player'] = 'White'
    elif Player == 2:
        These_Scores.loc[0,'Player'] = 'Black'  
    else:
        pass
    
    # Last turn
    These_Scores.loc[0,'Last turn'] = Last_Turn
    These_Scores.loc[0,'Last_Turn_Count'] = Last_Turn_Count
        
#%% Print scores and board
def Save_Scores():
    Scores_Turn = 'Scores_' + str(Turn_No)
    
    # Pickles scores for go back to use
    globals()[Scores_Turn + '_io'] = io.StringIO()
    These_Scores.to_csv(globals()[Scores_Turn + '_io'])
    
def Save_Board():
    Board_Turn = 'Board_' + str(Turn_No)

    # Pickles board for go back to use    
    globals()[Board_Turn + '_io'] = io.StringIO()
    This_Turn.to_csv(globals()[Board_Turn + '_io'])
    
#%% Player_Check() Check if player 1 or 2 is playing based on turn no. or number of markers
def Player_Check():
    global Player
    global Opponent
    global Markers_P1
    global Markers_P2
    global Game_Notes
    
    if Markers_P1 <= 0 and Markers_P2 > 0:
        Player = 2
        Opponent = 1
    elif Markers_P2 <= 0 and Markers_P1 > 0:
        Player = 1
        Opponent = 2
    else:
        pass
    
    if Last_Turn == 0 and Player == 1 and Markers_P1 > 0:
        Game_Notes = Game_Notes + 'White player...your turn. \n \n'
    elif Last_Turn == 0 and Player == 2 and Markers_P2 > 0:
        Game_Notes = Game_Notes + 'Black player...your turn. \n \n'
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
    global Neighbour_index


    if Last_Turn == 0:
        # Defines different e and f indexes if x value is odd or even   
        Place_index = Board_0[Board_0['x,y']==str(str(lookup_x) + ',' + str(lookup_y))].index.values
        
        if int(lookup_x) % 2 != 0:
            e_index = Place_index - 22
            f_index = Place_index + 24
        else:
            e_index = Place_index + 22
            f_index = Place_index - 24
            
        a_index = Place_index - 23
        b_index = Place_index + 23
        c_index = Place_index - 1
        d_index = Place_index + 1
        
        Neighbour_index = [int(a_index), int(b_index), int(c_index), int(d_index), int(e_index), int(f_index)]
    else:
        pass
    
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
       
    a_state = int(This_Turn.loc[int(a_index),'Value'])
    b_state = int(This_Turn.loc[int(b_index),'Value'])
    c_state = int(This_Turn.loc[int(c_index),'Value'])
    d_state = int(This_Turn.loc[int(d_index),'Value'])
    e_state = int(This_Turn.loc[int(e_index),'Value'])
    f_state = int(This_Turn.loc[int(f_index),'Value'])
    
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
    global Game_Notes
    
    # Increase turn number and reset markers used
    Turn_No = Turn_No + 1
    P1_Used = 0
    P2_Used = 0

    # Calculate_Scores()
    
    # Define this turn board and scores state
    variables = globals()
    
    # Unpickle the scores and board
    globals()['Board_' + str(Turn_No - 1) + '_io'].seek(0)
    globals()['Scores_' + str(Turn_No - 1) + '_io'].seek(0)
    
    This_Turn = pd.read_csv(globals()['Board_' + str(Turn_No - 1) + '_io'], header = 0)
    These_Scores = pd.read_csv(globals()['Scores_' + str(Turn_No - 1) + '_io'], header = 0)

    # Find the row relating to the place location
    Place_index = Board_0[Board_0['x,y']==str(str(Place_x) + ',' + str(Place_y))].index.values
    
    # Define new board state as new df (allowing for backtracking)
    This_Turn.loc[Place_index,'Value'] = int(Player)
    
    if int(Player) == 1:
        P1_Used = P1_Used + 1
    else:
        P2_Used = P2_Used + 1

    Calculate_Scores()
    Save_Scores()
    # Save_Board()
    # Show_Board()
       
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
        
    Player_Markers = int(These_Scores.loc[0,str('Markers_P' + str(Player))])
     
    # If so then fill neighbours
    if Req_Markers <= Player_Markers:
        Neighbour_No = 1
    
        Neighbours = dict([(1, 'a'), (2, 'b'), (3, 'c'), (4, 'd'), (5, 'e'), (6, 'f')])
            
        while Neighbour_No <= 6:
            if variables['{}_state'.format(Neighbours[Neighbour_No])] == int(Player):
                This_Turn.loc[variables['{}_index'.format(Neighbours[Neighbour_No])],'Value'] = int(Player)

            elif variables['{}_state'.format(Neighbours[Neighbour_No])] == 3:
                This_Turn.loc[variables['{}_index'.format(Neighbours[Neighbour_No])],'Value'] = 3 
    
            else:
                This_Turn.loc[variables['{}_index'.format(Neighbours[Neighbour_No])],'Value'] = int(Player)
                if int(Player) == 1:
                    P1_Used = P1_Used + 1
                else:
                    P2_Used = P2_Used + 1                    
    
            Neighbour_No = Neighbour_No + 1
                
        # Calculate_Scores()
        # Save_Scores()
        # Save_Board()
        # Show_Board()
        
    # If not then perform last go procedures
    elif Req_Markers > Player_Markers:
        Last_Turn_Count = Last_Turn_Count + 1
        
        # Sets the condition for the last go, enabling code below to be skipped until the last go is over.
        if Player_Markers > 0:
            Last_Turn = 1
        else:
            Last_Turn = 0
    
        if Player == 2 and Last_Turn_Count == 1:
            Game_Notes = Game_Notes + 'Black player, this is your last go, good luck! \n \n'
        elif Player == 1 and Last_Turn_Count == 1:
            Game_Notes = Game_Notes + 'White player, this is your last go, good luck! \n \n'
        else:
            pass
                    
        # Define Neighbour_index and make sure that only these spaces are used for future moves   
        if Last_Turn_Count == 1:
            Neighbour_index = [int(a_index), int(b_index), int(c_index), int(d_index), int(e_index), int(f_index)]
        else:
            pass                    
                    
        Player_Markers = int(These_Scores.loc[0,str('Markers_P' + str(Player))])
        
        Update_FE()
            
       # Calculate_Scores()
       # Save_Scores()
       # Save_Board()
       # Show_Board()
            
   # else:
        # Update_FE()
        
        # Calculate_Scores()
        # Save_Scores()
        # Save_Board()
        # Show_Board()
                                           
    if Last_Turn == 1 and ((Player == 1 and Markers_P1 > 0) or (Player == 2 and Markers_P2 > 0)):
        pass
    else:
        # Reset Last_Turn and Last_Turn_Count == 0
        Last_Turn = 0
        Last_Turn_Count = 0
        
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
                if int(This_Turn.loc[int(This_Turn_index),'Value']) == int(Opponent):
                    lookup_x = This_Turn.loc[int(This_Turn_index),'x']
                    lookup_y = This_Turn.loc[int(This_Turn_index),'y']
    
                    Define_Neighbour_Index()
                    Define_Neighbour_States() 
    
                    # Mark anything with "0" neighbours as "4"
                    if sum(1 for item in Neighbour_vals if item==(0)) > 0:
                        This_Turn.loc[This_Turn_index,'Value'] = 4
    
                    # Mark anything with "4" neighbours as "4"
                    if sum(1 for item in Neighbour_vals if item==(4)) > 0:
                        This_Turn.loc[This_Turn_index,'Value'] = 4
                
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
                if int(This_Turn.loc[int(This_Turn_index),'Value']) == int(Player):
    
                    lookup_x = This_Turn.loc[int(This_Turn_index),'x']
                    lookup_y = This_Turn.loc[int(This_Turn_index),'y']
                        
                    Define_Neighbour_Index()
                    Define_Neighbour_States()
                        
                    # Mark anything with "0" neighbours as "4"
                    if sum(1 for item in Neighbour_vals if item==(0)) > 0:
                        This_Turn.loc[This_Turn_index,'Value'] = 4
    
                    # Mark anything with "4" neighbours as "4"
                    if sum(1 for item in Neighbour_vals if item==(4)) > 0:
                        This_Turn.loc[This_Turn_index,'Value'] = 4
                
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
                if int(This_Turn.loc[int(This_Turn_index),'Value']) == 1:
                    lookup_x = This_Turn.loc[int(This_Turn_index),'x']
                    lookup_y = This_Turn.loc[int(This_Turn_index),'y']
            
                    Define_Neighbour_Index()
                    Define_Neighbour_States()
                    
                    if sum(1 for item in Neighbour_vals if item==(1)) <= 1:
                        This_Turn.loc[This_Turn_index,'Value'] = 0
                
                    else:
                        pass
        
                elif int(This_Turn.loc[int(This_Turn_index),'Value']) == 2:
                    lookup_x = This_Turn.loc[int(This_Turn_index),'x']
                    lookup_y = This_Turn.loc[int(This_Turn_index),'y'] 
    
                    Define_Neighbour_Index()
                    Define_Neighbour_States()
           
                    if sum(1 for item in Neighbour_vals if item==(2)) <= 1:
                        This_Turn.loc[This_Turn_index,'Value'] = 0  
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
    
    Markers_P1 = int(These_Scores.loc[0,'Markers_P1'])
    Markers_P2 = int(These_Scores.loc[0,'Markers_P2'])
    
    Save_Scores()
    # Save_Board()
        
    Total_Markers = Markers_P1 + Markers_P2
    
    # Show_Board()
    
    # Update the game notes
    if Player == 1:
        Color = 'White'
        x = str(P1_Used)
        y = str(These_Scores.loc[0,'Markers_P1'])
    
    else:
        Color = 'Black'
        x = str(P2_Used)
        y = str(These_Scores.loc[0,'Markers_P2'])
    
    Game_Notes = (Game_Notes + 'Turn ' + str(Turn_No) + ': \n     ' +
                  Color + ' played ' + '(' + str(Place_x) + ',' + str(Place_y) + '),' + '\n     ' +
                  'Placing '+ x + ' markers,' + '\n     ' +
                  Color + ' has ' + y + ' markers left,' + '\n     ' +
                  'Score: ' + 'White = ' + str(int(These_Scores.loc[0,'InPlay_P1'])) + ', Black = ' + str(int(These_Scores.loc[0,'InPlay_P2'])) + ',\n \n')
    
    if Player_Markers > 0 and Req_Markers > Player_Markers:
        if Player == 2:
            Game_Notes = Game_Notes + 'Black player its still your turn. \n \n'
        elif Player == 1:
            Game_Notes = Game_Notes + 'White player its still your turn. \n \n'
        else:
            Last_Turn_Count = 0    
    
    # if not a last go then swap player
    if Last_Turn == 0:
        Calculate_Scores()
        Save_Scores()
        # Save_Board()
        # Show_Board()
        
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
    
    Save_Board()
    Show_Board()
    
    # Sort out endgame
    if Markers_P1 <= 0 and Markers_P2 <= 0:
        # End Game and display winner!
        InPlay_P1 = These_Scores.loc[0,'InPlay_P1']
        InPlay_P2 = These_Scores.loc[0,'InPlay_P2']
        
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
        if These_Scores.loc[0,'InPlay_P1'] > These_Scores.loc[0,'InPlay_P2']:
            winner = 'White'
        else:
            winner = 'Black'

        # Print outcome
        if InPlay_P1 == InPlay_P2:
            Game_Notes = Game_Notes + 'End of game, A Draw? How did that happen? \n \n'
        else:
            Game_Notes = Game_Notes + 'End of game, congratulations ' + str(winner) + ', you acheived ' + str(outcome) + '\n \n'
    
    # Remove 'Working on it...'
    Game_Notes = Game_Notes.replace("Working on it... \n \n", "")
    Update_FE()
    
#%% Input co-ordinates, checks that inputted co-ordinates match the entry requirements.
# If so, passes to Take_Turn(), If not, displays error message.
def Input():      
    global Place_x
    global Place_y 
    global entry1
    global coords
    global Last_Turn
    global Neighbour_index
    global lookup_x
    global lookup_y
    global Game_Notes
    
    
    # The entry requirements are that:
    # 1. Integers between 0 and 22 must be used.
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
        
        lookup_x = Place_x
        lookup_y = Place_x
        
        entry1.delete(0, END)
        Pass = Pass + 1
    else:
        entry1.delete(0, END)
        
    Game_Notes = Game_Notes + 'Working on it... \n \n'
    Update_FE()
        
    # 2. Check to see if Place_x and Place_y are integers between 0 and 22
    if (0 <= Place_x <= 22) and (0 <= Place_y <= 22):
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
    Place_State = int(This_Turn.loc[Place_index,'Value'])
    
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
        Game_Notes = Game_Notes + 'Entered co-ordinate ' + '(' + str(Place_x) + ',' + str(Place_y) + ')' + ' is incorrect, please try again \n \n'
        
    Update_FE()
        
#%% What the buttons do
def Go_To():
    global This_Turn
    global Markers_P1
    global Markers_P2
    global These_Scores
    global Turn_No
    global Player
    global Game_Notes
    global Opponent
    global Last_Turn_Count
    global Last_Turn
    global panel
    global entry2
       
    # Issue with last go in that, the player swap is fucking things up.
                   
    Turn = str(entry2.get())
    
    # The entry requirements are that:
    # 1. Integers between 1 and 246 must be used.
    
    Pass = 0
    
    # 1. Check that there is text in input2 and that it is an integer between 1 and 246 incl.
    if (int(Turn) >= 0) and (int(Turn) <= 246):
        entry2.delete(0, END)
        Pass = Pass + 1
    else:
        entry2.delete(0, END)
            
    # Check to see if all stages passed, if so contunue, if not pass
    if Pass == 1:
        Turn_No = int(Turn)
        
        # Unpickle the scores and board 
        globals()['Board_' + str(Turn_No ) + '_io'].seek(0)
        globals()['Scores_' + str(Turn_No) + '_io'].seek(0)
        
        This_Turn = pd.read_csv(globals()['Board_' + str(Turn_No) + '_io'], header = 0)
        These_Scores = pd.read_csv(globals()['Scores_' + str(Turn_No) + '_io'], header = 0)   

        Markers_P1 = int(These_Scores.loc[0,'Markers_P1'])
        Markers_P2 = int(These_Scores.loc[0,'Markers_P2'])
        Player = int(These_Scores.loc[0,'Player_No'])
        Last_Turn_Count = int(These_Scores.loc[0,'Last_Turn_Count'])
        Last_Turn = int(These_Scores.loc[0,'Last turn'])
       
        # If not last go flip player to allow opponent to play 
        if Last_Turn == 0:
            if Player == 1:
                Player = 2
                Opponent = 1
            elif Player == 2:
               Player = 1
               Opponent = 2 
            else:
                pass
        else:
            pass
        
        Game_Notes = Game_Notes + 'Went to turn number ' + Turn + '.\n \n'
        
        if Last_Turn == 1:
            if Player == 1:
                Game_Notes = Game_Notes + 'White player its still your turn.\n \n'
            elif Player == 2:
                  Game_Notes = Game_Notes + 'Black player its still your turn.\n \n'
            else:
                pass
        else:
            pass

        Update_FE()
        
        Player_Check()
        
        Update_FE()
        
    else:
        Game_Notes = Game_Notes + 'Not a valid turn number, please try again. \n \n'
        
        Update_FE()


#%% Create and show board to players  
Calculate_Scores()
Player_Check()
Show_Board()
               
#%% Some other front end stuff

Calculate_FE_sizes()

def Setup_FE_Features():
    global canvas1
    global canvas2
    global BTT
    global BGB
    global entry1
    global entry2
    global side_pannel
    global Game_Notes    
    
    # Setup all the front end features
    canvas1 = tk.Canvas(root, width = canvas_width, height = canvas1_height)
    canvas2 = tk.Canvas(root, width = canvas_width, height = canvas2_height)
    BTT = tk.Button(canvas1, text = 'Take Turn', font = ('Arial', fontsize), command = Input, bg='brown',fg='white')
    BGB = tk.Button(canvas1, text = 'Go To', font = ('Arial', fontsize), command = Go_To, bg='brown',fg='white')
    entry1 = tk.Entry(canvas1, font = ('Arial', fontsize))
    entry2 = tk.Entry(canvas1, font = ('Arial', fontsize))
    text1 = canvas1.create_text(text_width, text1_height, anchor = "e")
    text2 = canvas1.create_text(text_width, text2_height, anchor = "e")
    side_pannel = tk.Text(canvas2, font = ('Arial', fontsize), wrap=WORD)
    side_pannel.insert(tk.END, Game_Notes)

    canvas1.place(x = canvas1_x, y = 0)
    canvas2.place(x = canvas2_x, y = 0)
    BTT.place(height = button_height, width = button_width, x = BTT_x, y = BTT_y)
    BGB.place(height = button_height, width = button_width, x = BGB_x, y = BGB_y)
    entry1.place(height = button_height, width = button_width, x = entry_x, y = entry1_y)
    entry2.place(height = button_height, width = button_width, x = entry_x, y = entry2_y)
    canvas1.itemconfig(text1, text="Enter co-ordinates here (x,y):", font = ('Arial', fontsize))
    canvas1.itemconfig(text2, text="Enter turn number here:", font = ('Arial', fontsize))
    side_pannel.place(x = 1, y = button_height, relwidth = 1, height = canvas2_height - button_height)
    side_pannel.see("end")
    entry1.bind('<Return>', lambda x: Input ())
    entry1.focus()
    entry2.bind('<Return>', lambda x: Go_To ())

Setup_FE_Features()

#%% Update_FE()
def Update_FE():
    global canvas1
    global canvas2
    global BTT
    global BGB
    global entry1
    global entry2
    global side_pannel
    global Game_Notes

    Calculate_FE_sizes()
    
    # Destroy and re-set up front end features
    canvas1.destroy()
    canvas2.destroy()
    BTT.destroy()
    BGB.destroy()
    entry1.destroy()
    entry2.destroy()
    side_pannel.destroy()
    
    Setup_FE_Features()
    
    Show_Board()

Update_FE()
root.mainloop()    
