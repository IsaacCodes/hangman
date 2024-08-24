#Imports + setup
import pygame as pg
import random

import settings
import words
import object

pg.init()

#The letter objects on the keyboard
class Letter(object.Rectangle):
  #Creates letter
  def __init__(self, pos: "tuple[int, int]", letter: str, keyboard, answer, man):
    #Parent rectangle
    super().__init__(pos, (40, 40), color="white", border_size=3, border_color="black", corner_rounding=20, text=letter, text_size=24, text_color="black", group=False)

    #Constants
    self.keyboard = keyboard
    self.answer = answer
    self.man = man
    self.letter = letter
    self.revealed = False

  #When letter is clicked or pressed by 
  def on_click(self):
    #Don't run this function if the letter has already been revealed
    if self.revealed:
      return

    #If letter is in word, display it and set keyboard color to green
    if self.letter in self.answer.word.lower():
      color = "green"
      self.answer.reveal(self.letter)
    #Otherwise, set red and reveal one of man's ligaments
    else:
      color = "red"
      self.man.reveal()

    #Set bool, change color
    self.revealed = True
    self.image.fill(color, special_flags=pg.BLEND_ADD)
  

#Keyboard used to type guess letters / display them
class Keyboard(dict):
  #Creates an array (dict) of letters
  def __init__(self, answer, man):
    self_dict = {}
    for i, letter in enumerate("qwertyuiopasdfghjklzxcvbnm"):
      buff = 50 #Buffer amount
      lpr = 10 #Letters per row
      x = (i % lpr - lpr//2 + .5)*buff + settings.width/2
      y = (i//lpr)*buff + settings.width/2 - 10
      
      self_dict[letter] = Letter((x, y), letter, self, answer, man)
  
    super().__init__(self_dict)


#The answer/word you are guessing
class Answer(object.Text):
  def __init__(self):    
    #The word, its blanks, then create parent text
    self.word = random.choice(words.word_list)
    self.blanks = ["_"]*len(self.word)
    super().__init__((settings.width/2, 30), " ".join(self.blanks), group=False)

  #Reveals a letter
  def reveal(self, letter):
    for i in range(len(self.word)):
      if self.word[i].lower() == letter:
        self.blanks[i] = self.word[i]
        self.update(" ".join(self.blanks))
    #If you find the whole word
    if "_" not in self.blanks:
      settings.won = True


#The actual hangman
class Man(list):
  def __init__(self):
    #Max amount of limbs and how many are revealed
    self.max_guesses = 6
    self.revealed = 0

    #List to be self init
    self_list = []
    #Creates the self list from the body parts
    body_pos = (100, settings.height/2-60)
    body_size = (100, 130)
    body_parts = ["head", "body", "left_arm", "right_arm", "left_leg", "right_leg"]
    for body_part in body_parts:
      self_list.append(object.Image(body_pos, f"{body_part}.png", body_size, group=False))
    
    self.gallows = object.Image(body_pos, "gallows.png", body_size, group=False)
    
    super().__init__(self_list)

  #Reveals a ligament
  def reveal(self):
    #Display a body part and update vars
    object.objects.add(self[self.revealed])
    self.revealed += 1
    if self.revealed == self.max_guesses:
      settings.lost = True
    