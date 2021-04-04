import pygame
import time

from pygame.locals import*
from time import sleep

class Sprite():
	def __init__(self, x, y):
	   self.x = x
	   self.y = y
	   self.vert_velocity = -12

	def update(self):
		return

	def drawYourself(self, screen):
		return

	def isTube(self):
		return False
	def isMario(self):
		return False
	def isGoomba(self):
		return False
	def isFireball(self):
		return False
	def isBrick(self):
		return False

	def hasItCollide(self, a):
		if self.x+self.w <= a.x:
			return False
		elif self.x >= a.x+a.w:
			return False
		elif self.y+self.h <= a.y:
			return False
		elif self.y >= a.y+a.h:
			return False
		else:
			return True

class Tube (Sprite):
	def __init__(self, x, y):
		super().__init__(x, y)
		self.x = x
		self.y = y
		self.w = 55
		self.h = 400
		self.tube_image = pygame.image.load("tube.png")

	def update(self):
		return

	def isTube(self):
		return True


class Mario (Sprite):
	def __init__(self, x, y):
		super().__init__(x, y)
		self.countFrames = 0
		self.x = x
		self.marioViewLocation = self.x
		self.y = y
		self.w = 60
		self.h = 95
		self.marioImageNum = 0
		self.marioTop = False
		self.flip = False
		self.px = x
		self.py = y

		self.mario_images = []
		self.image1 = pygame.image.load("mario1.png")
		self.mario_images.append(self.image1)
		self.image2 = pygame.image.load("mario2.png")
		self.mario_images.append(self.image2)
		self.image3 = pygame.image.load("mario3.png")
		self.mario_images.append(self.image3)
		self.image4 = pygame.image.load("mario4.png")
		self.mario_images.append(self.image4)
		self.image5 = pygame.image.load("mario5.png")
		self.mario_images.append(self.image5)

	def update(self):
		self.countFrames+=1
		if not self.marioTop:
			self.vert_velocity += 0.9
			self.y += self.vert_velocity
		if self.y > 400-self.h:
			self.vert_velocity = 0
			self.y = 400-self.h
			self.countFrames = 0
		if self.y < -50:
			self.y = -50

	def jump(self):
		if self.countFrames < 5:
			self.vert_velocity -= 5
		self.marioTop = False


	def isMario(self):
		return True


	def savePreviousCoordinate(self):
		self.px = self.x
		self.py = self.y

	def updateImage(self):
		self.marioImageNum+=1
		if self.marioImageNum > 4:
			self.marioImageNum = 0

	def getOutOfTube(self, t):
		if self.x+self.w >= t.x and self.px + self.w <= t.x:
			self.x = t.x - self.w
		if self.x <= t.x + t.w and self.px >= t.x + t.w:
			self.x = t.x + t.w
		if self.y + self.h >= t.y and self.py + self.h <= t.y:
			self.y = t.y - self.h
			self.countFrames = 0
			self.vert_velocity = 0
		if self.y <= t.h + t.y and self.py >= t.y + t.h:
			self.y = t.y + t.h


class Goomba (Sprite):

	def __init__(self, x, y, model):
		super().__init__(x, y)
		self.x = x
		self.y = y
		self.px = x
		self.py = y

		self.w = 48
		self.h = 57

		self.model = model
		self.goombaTop = False
		self.direction = 1
		self.fireballSpeed = 5
		self.goombaFrames = 0
		self.isBurning = False
		self.goombaImageNum = 0

		self.goomba_image = pygame.image.load("goomba1.png")
		self.goomba_fire = pygame.image.load("goomba_fire.png")


	def update(self):
		self.savePreviousCoordinate()

		if not self.goombaTop:
			self.vert_velocity += 0.9
			self.y += self.vert_velocity
		if self.y > 400-self.h:
				self.vert_velocity = 0
				self.y = 400-self.h
		if self.y < -50:
				self.y = -50

		self.x+=self.fireballSpeed*self.direction

		for i in range(len(self.model.sprites)):
			isTube = isinstance(self.model.sprites[i], Tube)
			if self.model.sprites[i].isTube() and self.hasItCollide(self.model.sprites[i]):
					self.getOutOfTube(self.model.sprites[i])

		if self.isBurning is True:
			self.goombaFrames+=1

	def savePreviousCoordinate(self):
		self.px = self.x
		self.py = self.y

	def goombaBurning(self):
		self.isBurning = True
		self.fireballSpeed = 0

	def getOutOfTube(self, t):
		if self.x+self.w >= t.x and self.px + self.w <= t.x:
			self.x = t.x - self.w
			self.direction = self.direction*-1

		if self.x <= t.x + t.w and self.px >= t.x + t.w:
			self.x = t.x + t.w
			self.direction = self.direction*-1

	def isGoomba(self):
		return True

class Fireball (Sprite):

	def __init__(self, x, y, m):
		super().__init__(x, y)
		self.x = x
		self.y = y
		self.px = x
		self.py = y
		self.w = 47
		self.h = 47
		self.model = m
		self.direction = 1
		self.fireballSpeed = 10
		self.fireball_image = pygame.image.load("fireball.png")


	def update(self):
		self.x+=self.fireballSpeed*self.direction
		self.vert_velocity+= 5
		self.y += self.vert_velocity
		self.savePreviousCoordinate()

		if self.y > 400-self.h:
			self.vert_velocity = -38
			self.y = 400-self.h

		for i in range(len(self.model.sprites)):
			if self.model.sprites[i].isGoomba() and self.hasItCollide(self.model.sprites[i]) and not self.model.sprites[i].isBurning:
				self.model.sprites[i].goombaBurning()

	def savePreviousCoordinate(self):
		self.px = self.x
		self.py = self.y

	def isFireball(self):
		return true

	def drawYourself(self, screen):
		# self.screen.blit.drawImage(self.fireball_image, self.x-self.model.mario.x +self.model.mario.marioViewLocation -self.w/2, self.y)
		screen.blit(self.fireball_image, (self.x-self.model.mario.x +self.model.mario.marioViewLocation -self.w/2, self.y))

class Model():
	def __init__(self):
		self.x = 0
		self.y = 0

		self.sprites = []
		self.mario = Mario(100, 200)
		self.sprites.append(self.mario)
		self.tube1 = Tube(350, 300)
		self.sprites.append(self.tube1)
		self.tube2 = Tube(700, 200)
		self.sprites.append(self.tube2)

		self.goomba1 = Goomba(500, 300, self)
		self.sprites.append(self.goomba1)

	def update(self):
		for i in range(len(self.sprites)):
			self.sprites[i].update()
			isMario = isinstance(self.sprites[i], Mario)
			if isMario is True:
				m = self.sprites[i]
				for j in range(len(self.sprites)):
					isTube = isinstance(self.sprites[j], Tube)
					t = 0
					if isTube is True:
						t = self.sprites[j]
						if self.hasItCollide(m, t) is True:
							self.mario.getOutOfTube(t)

		for r in self.sprites:
			isGoomba = isinstance(r, Goomba)
			if isGoomba is True:
				g = r
				if g.isBurning is True:
					if g.goombaFrames > 20:
						self.sprites.remove(g)

		for k in self.sprites:
			isFireball = isinstance(k, Fireball)
			if isFireball is True:
					f = k
					if f.x> 2500:
						self.sprites.remove(f)
						# print ("Fireball has been removed")

	def hasItCollide(self, a, b):
		if a.x+a.w <= b.x:
			return False
		elif a.x >= b.x+b.w:
			return False
		elif a.y+a.h <= b.y:
			return False
		elif a.y >= b.y+b.h:
			return False
		else:
			return True

	def addFireball(self):
		fireballLocation = self.mario.x+self.mario.w
		fireball = Fireball(fireballLocation,self.mario.y + self.mario.h/2, self)
		self.sprites.append(fireball)

class View():
	def __init__(self, model):
		screen_size = (800,600)
		self.screen = pygame.display.set_mode(screen_size, 32)
		self.model = model

	def update(self):
		self.screen.fill([153,255,255])
		pygame.draw.rect(self.screen, (0,255,0), (0,400,100000,500), 0)

		for i in self.model.sprites:
			sprite = i
			if isinstance(i, Mario):
				self.screen.blit(self.model.mario.mario_images[self.model.mario.marioImageNum], (self.model.mario.marioViewLocation, self.model.mario.y, self.model.mario.w, self.model.mario.h))
			if isinstance(i, Tube):
				self.screen.blit(self.model.tube1.tube_image, (self.model.tube1.x - self.model.mario.x + self.model.mario.marioViewLocation, self.model.tube1.y))
				self.screen.blit(self.model.tube2.tube_image, (self.model.tube2.x - self.model.mario.x + self.model.mario.marioViewLocation, self.model.tube2.y))
			if isinstance(i, Goomba):
				if self.model.goomba1.isBurning is True:
					self.screen.blit(self.model.goomba1.goomba_fire, (self.model.goomba1.x - self.model.mario.x + self.model.mario.marioViewLocation, self.model.goomba1.y, -self.model.goomba1.w, self.model.goomba1.h))
				else:
					self.screen.blit(self.model.goomba1.goomba_image, (self.model.goomba1.x - self.model.mario.x + self.model.mario.marioViewLocation, self.model.goomba1.y))
			if isinstance (i, Fireball):
				sprite.drawYourself(self.screen)
				# self.screen.blit(self.model.fireball.fireball_image, (self.model.fireball.x-self.model.mario.x +self.model.mario.marioViewLocation -self.model.fireball.w/2, self.model.fireball.y))
		pygame.display.flip()

class Controller():
	def __init__(self, model, view):
		self.model = model
		self.view = view
		self.keep_going = True

	def update(self):
		self.model.mario.savePreviousCoordinate()
		for event in pygame.event.get():
			if event.type == QUIT:
				self.keep_going = False
			elif event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					self.keep_going = False
				if event.key == K_RIGHT:
					return True
				if event.key == K_LEFT:
					return True
				if event.key == K_UP:
					return True
				if event.key == K_LCTRL:
					return True
			elif event.type == KEYUP:
				if event.key == K_RIGHT:
					return False
				if event.key == K_LEFT:
					return False
				if event.key == K_UP:
					return False
				if event.key == K_LCTRL:
					return False
		keys = pygame.key.get_pressed()
		if keys[K_LEFT]:
			self.model.mario.x-=10
			self.model.mario.updateImage()
		if keys[K_RIGHT]:
			self.model.mario.x+=10
			self.model.mario.updateImage()
		if keys[K_UP]:
			self.model.mario.jump()
		if keys[K_DOWN]:
			self.model.mario.y += 10
		if keys[K_LCTRL]:
			# print("control key pressed")
			self.model.addFireball()

print("Use the arrow keys to move. Press Esc to quit.")
pygame.init()
m = Model()
v = View(m)
c = Controller(m, v)
while c.keep_going:
	c.update()
	m.update()
	v.update()
	sleep(0.04)
print("Goodbye")