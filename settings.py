#Game info used across files
#Imports + Setup
import os

#Window size
size = width, height = (550, 400)

#Finds current directory
dir = os.path.dirname(os.path.realpath(__file__))

#Global vars
playing_game = False
lost = False
won = False
points = 0