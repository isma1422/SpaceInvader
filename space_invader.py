import sys
import pygame
from ship import Ship
from settings import Settings
from pygame.sprite import Group
import game_functions as gf
from game_stats import GameStats

def run_game():
	#Initialize game and create a screen object
	pygame.init()
	ai_settings = Settings()
	
	screen = pygame.display.set_mode((ai_settings.screen_width,ai_settings.screen_height))
	pygame.display.set_caption("Alien invasion")
		
	#Create an instance of game stats
	stats = GameStats(ai_settings)
	
	#Make a ship
	ship = Ship(screen)
			
	#Make a group to store bullets in.
	bullets = Group()
	
	#Group of aliens
	aliens = Group()
	
	gf.create_fleet(ai_settings, screen, ship, aliens)
	
	#Start the main loop for the game
	while True:
		
		gf.check_events(ai_settings, screen, ship, bullets)
		ship.update()
		gf.update_bullets(ai_settings, screen, ship, aliens, bullets)	
		gf.update_aliens(ai_settings, stats, screen, ship, aliens, bullets)
		gf.update_screen(ai_settings,screen,ship, aliens, bullets)
		

run_game()
