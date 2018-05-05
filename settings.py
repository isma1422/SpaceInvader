class Settings():
	"""A class to store all settings for Alien Invasion"""
	
	
	def __init__(self):
		"""Initialize the game's settings"""
		#Screen settings
		self.screen_width = 1200
		self.screen_height = 800
		self.bg_color = (255,255,255)
		
		#Bullet settings
		self.bullet_speed_factor = 1
		self.bullet_width = 3
		self.bullet_heigth = 15
		self.bullet_color = (60,60,60)
		self.bullets_allowed = 3
		
		#Aliens settings
		self.alien_speed_factor = 1
		self.fleet_drop_speed = 10
		self.fleet_direction = 1
