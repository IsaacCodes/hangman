#Imports and setup
import pygame as pg

import settings
import object
import game

pg.init()

#Creates screen/window
screen = pg.display.set_mode(settings.size)
pg.display.set_caption("Hangman")


#Main function
def main(skip_menu: bool) -> tuple[bool, bool]:
  #Creates menu objects
  title = object.Text((settings.width/2, 35), "Hangman", text_size=48)
  desc = object.MultiText((settings.width/2, 100), "Hit \"Play!\",\n Then guess the word by clicking one letter at a time.\n After six wrong guesses, you lose, so be careful!", text_size=20, text_color="gray30", line_buffer = 5)
  play_button = object.Rectangle((settings.width/2, settings.height/2-10), (150, 75), color="gray60", border_size=2, border_color="black", corner_rounding=15, text="Play!", text_size=36, text_color="black")
  menu_man = [object.Image((settings.width/2, settings.height-80), f"{body_part}.png", (100, 130)) for body_part in ("gallows", "head", "body", "left_arm", "right_arm", "left_leg", "right_leg")]
  #Stores all menu objects in the menu group
  menu_objects = pg.sprite.Group(title, desc, play_button, menu_man)
  
  #Creates game objects
  answer = game.Answer()
  man = game.Man()
  keyboard = game.Keyboard(answer, man)
  restart_button = object.Image((settings.width - 45, 17), "restart.png", group=False)
  menu_button = object.Image((settings.width - 15, 15), "house.png", group=False)
  points_display = object.Text((0, 0), f"Points: {settings.points}", 22, group=False)
  points_display.rect.topleft = (5, 5)
  #Stores all game objects in the game group
  game_objects = pg.sprite.Group(answer, man.gallows, [keyboard[key] for key in keyboard], restart_button, menu_button, points_display)

  #Post-game objects
  lose_text = object.MultiText((350, settings.height/2-60), f"You Lose!\nThe Word Was: {answer.word}", 24, "red", group=False)
  win_text = object.Text((350, settings.height/2-60), "You Win!", 32, "green", group=False)

  #Hide menu_objects and add game_objects, skipping the menu
  if skip_menu:
    object.objects.remove(menu_objects)
    object.objects.add(game_objects)
    settings.playing_game = True
  
  #Loop variables
  clock = pg.time.Clock()
  while True:
    #Max 60 fps
    clock.tick(60)

    #Event loop
    for event in pg.event.get():
      #Quit
      if event.type == pg.QUIT:
        return False, False
      #Left click
      left_click = event.type == pg.MOUSEBUTTONDOWN and event.button == 1
      key_press = event.type == pg.KEYDOWN
      mouse_pos = pg.mouse.get_pos()
      #On menu
      if not settings.playing_game:
        #If play button clicked
        if left_click and play_button.rect.collidepoint(mouse_pos):
          #Hide menu_objects and add game_objects
          object.objects.remove(menu_objects)
          object.objects.add(game_objects)
          settings.playing_game = True
      #In game
      elif not settings.lost:
        #If a digital keyboard button is clicked
        for key in keyboard:
          if left_click and keyboard[key].rect.collidepoint(mouse_pos):
            keyboard[key].on_click()
        #If a physical keyboard button in pressed 
        if key_press and pg.K_a <= event.key <= pg.K_z:
          keyboard[event.unicode].on_click()
      #Regardless of state
      #Restart game
      if left_click and restart_button.rect.collidepoint(mouse_pos):
        #Updates points
        if settings.won:
          settings.points += man.max_guesses - man.revealed
        else:
          settings.points = 0
        #Restart, skip_menu
        return True, True
      #Menu button
      if left_click and menu_button.rect.collidepoint(mouse_pos):
        #Reset points
        settings.points = 0
        #Restart, skip_menu
        return True, False
          
    #One time game over modifications
    #Loss
    if settings.playing_game and settings.lost:
      settings.playing_game = False
      object.objects.add(lose_text)
    #Win
    elif settings.playing_game and settings.won:
      settings.playing_game = False
      object.objects.add(win_text)
        

    #Background
    screen.fill("white")
    #Draw all game objects
    object.objects.draw(screen)
    #Updates screen
    pg.display.update()


#Runs the game
restart, skip_menu = main(False)
while restart:
  #Reset vars and clear groups
  settings.playing_game = False
  settings.lost = False
  settings.won = False
  object.objects = pg.sprite.LayeredUpdates()
  
  restart, skip_menu = main(skip_menu)