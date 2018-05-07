import sys
import pygame
from bullet import Bullet
from alien import Alien
from time import sleep

def check_events(ai_settings, screen, ship, bullets):
	"""Respond to keypresses and mouse events."""
	#Wactch for keyboard and mouse events
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
		elif event.type == pygame.KEYDOWN:
			check_keydown_events(event, ai_settings, screen, ship, bullets)
		elif event.type == pygame.KEYUP:
			check_keyup_events(event,ship)
					

def check_keydown_events(event, ai_settings, screen, ship, bullets):
	"""Respond to keypresses"""			
	if event.key == pygame.K_RIGHT:
		#Move the ship to the right
		ship.moving_right = True
	elif event.key == pygame.K_LEFT:
		ship.moving_left = True
	elif event.key == pygame.K_SPACE:
		fire_bullet(ai_settings, screen, ship, bullets)
	elif event.key == pygame.K_q:
		sys.exit()

def check_keyup_events(event,ship):
	if event.key == pygame.K_RIGHT:
		ship.moving_right = False
	elif event.key == pygame.K_LEFT:
		ship.moving_left = False


def update_screen(ai_settings, screen, ship, aliens, bullets):
	"""Update images on the screen and flip to new screen"""
	screen.fill(ai_settings.bg_color)
	#Redraw all the bullets behind ship and aliens
	for bullet in bullets.sprites():
		bullet.draw_bullet()
	ship.blitme()
	aliens.draw(screen)
	#Make the most recently drawn screen visible
	pygame.display.flip()


def update_bullets(ai_settings, screen, ship, aliens, bullets):
	"""Update the position of bullets and get rid of old bullets."""
	bullets.update()
	#Get rid of bullets
	for bullet in bullets.copy():
		if bullet.rect.bottom <= 0:
			bullets.remove(bullet)
	
	check_alien_bullet_collision(ai_settings, screen, ship, aliens, bullets)
	
	
def check_alien_bullet_collision(ai_settings, screen, ship, aliens, bullets):
	
	#Check for bullets hiting aliens
	collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
	
	if len(aliens) == 0:
		#Destroy existing bullets and create new fleet.
		bullets.empty()
		create_fleet(ai_settings, screen, ship, aliens)
	
	
def update_aliens(ai_settings, stats, screen, ship, aliens, bullets):
	"""Update the position of all the aliens"""
	check_fleet_edges(ai_settings, aliens)
	aliens.update()
	
	#Look alien ship collision
	if pygame.sprite.spritecollideany(ship, aliens):
		ship_hit(ai_settings, stats, screen, ship, aliens, bullets)
			
			
def fire_bullet(ai_settings, screen, ship, bullets):
	"""Fire a bullet if limit not reached yet"""
	#Create a new bullet and add it to the bullets group.
	if len(bullets) < ai_settings.bullets_allowed:
		new_bullet = Bullet(ai_settings, screen, ship)
		bullets.add(new_bullet)
		

def create_fleet(ai_settings, screen, ship, aliens):
	"""Create a full fleet of aliens."""
	
	#Create an alien and find the number of aliens in a row
	#Spacing between each alien is equal to one alien width
	alien = Alien(ai_settings, screen)
	number_aliens_x = get_number_aliens(ai_settings, alien.rect.width)
	
	number_of_rows = get_row_number(ai_settings, ship.rect.height, alien.rect.height)
	
	for row_number in range(number_of_rows):
		for alien_number in range(number_aliens_x):
			create_alien(ai_settings, screen, aliens, alien_number, row_number)
		
		
def get_number_aliens(ai_settings, alien_width):
	"""Determine the number of aliens that fit in a row"""
	available_space_x = ai_settings.screen_width - 2 * alien_width
	number_aliens_x = int(available_space_x / (2 * alien_width))
	return number_aliens_x
	
def get_row_number(ai_settings, ship_height, alien_height):
	"""Determine the number of rows of aliens that fit in the screen"""
	available_space_y = (ai_settings.screen_height - (3 * alien_height) - ship_height)
	number_of_rows = int(available_space_y / (2 * alien_height) )
	return number_of_rows
	
def create_alien(ai_settings, screen, aliens, alien_number, row_number):
	alien = Alien(ai_settings, screen)
	alien_width = alien.rect.width
	alien.x = alien_width + 2 * alien_width * alien_number
	alien.rect.x = alien.x
	alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
	aliens.add(alien)


def check_fleet_edges(ai_settings, aliens):
	for alien in aliens.sprites():
		if alien.check_edges():
			change_fleet_direction(ai_settings, aliens)
			break


def change_fleet_direction(ai_settings, aliens):
	
	for alien in aliens.sprites():
		alien.rect.y += ai_settings.fleet_drop_speed
	ai_settings.fleet_direction *= -1



def ship_hit(ai_settings, stats, screen, ship, aliens, bullets):
	"""Respond to ship being hit by alien"""
	#Decrement ships_left
	stats.ships_left -= 1
	
	#Empty the list of aliens and bullets
	aliens.empty()
	bullets.empty()
	
	#Create a new fleet and center the ship
	create_fleet(ai_settings, screen, ship, aliens)
	ship.center_ship()
	
	#Pause
	sleep(0.5)
	
	


