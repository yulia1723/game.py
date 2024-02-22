from pygame import *

#buat background biasa
window_width = 800
window_height = 600
window = display.set_mode((window_width, window_height))
window.fill((198, 157, 218))
display.set_caption('my first game')
#buat background pakai picture
bg_image = image.load('download (3).jpeg') 
bg_image = transform.scale(bg_image, (window_width, window_height)) 

#buat objek berbentuk kotak-kotak
class Rectangle(sprite.Sprite):
    def __init__(self, width, height, x, y, color):
        super().__init__()
        self.rect = Rect(x, y, width, height) #buat titik koordinat x dan y dan buat ukuran kotaknya
        self.fill_color = color #nambahin warna
    def display(self):
        draw.rect(window, self.fill_color, self.rect) #untuk nampilin kotak nya
        
class Circle(sprite.Sprite): #buat objek berbentuk lingkaran
    def __init__(self, radius, x, y, color):
        super().__init__()
        self.center = (x, y) #letak lingkarannya
        self.radius = radius #jari-jari
        self.fill_color = color # ngisi warnanya

    def display(self):
        draw.circle(window, self.fill_color, self.center, self.radius)

#buat objek pakai gambar pahlawan
class GameSprite(sprite.Sprite):
     def __init__(self, picture, x, y, width, height):
       sprite.Sprite.__init__(self)
       picture = image.load(picture) #variabel gambar
       self.image = transform.scale(picture, (width, height))
       # posisi gambarnya
       self.rect = self.image.get_rect()
       self.rect.x = x
       self.rect.y = y
   # nampilin gambar
     def display(self):
       window.blit(self.image, (self.rect.x, self.rect.y))
       
#buat objeknya pahlawan biasa bisa gerak
class Player(GameSprite):
    #fungsi untuk objeknya diatur keyboard
   def __init__(self, picture, x, y, width, height, x_speed, y_speed):
       GameSprite.__init__(self, picture, x, y, width, height)
       self.x_speed = x_speed
       self.y_speed = y_speed
    #untuk update gerak objek
   def update(self):
        # self.rect.x += self.x_speed
        # self.rect.y += self.y_speed 
        if player1.rect.x <= window_width-80 and player1.x_speed > 0 or player1.rect.x >= 0 and player1.x_speed < 0:
            self.rect.x += self.x_speed
          
        #membuat dinding    
        platforms_touched = sprite.spritecollide(self, walls, False) # tidak dapat menyentuh dinding
        # dinding kanan dan kiri
        if self.x_speed > 0: #gerak ke kanan
            for p in platforms_touched:
                self.rect.right = min(self.rect.right, p.rect.left) #if several walls were touched at once, then the right edge is the minimum possible
        elif self.x_speed < 0: #gerak ke kiri 
            for p in platforms_touched:
                self.rect.left = max(self.rect.left, p.rect.right) #if several walls have been touched, then the left edge is the maximum
        
        # atas bawah
        if player1.rect.y <= window_height-80 and player1.y_speed > 0 or player1.rect.y >= 0 and player1.y_speed < 0:
            self.rect.y += self.y_speed
        
        # nyentuh dinding atas bawah
        platforms_touched = sprite.spritecollide(self, walls, False)
        
        if self.y_speed > 0: # keatas 
            for p in platforms_touched:
                self.rect.bottom = min(self.rect.bottom, p.rect.top)
        elif self.y_speed < 0: # kebawah
            for p in platforms_touched:
                self.rect.top = max(self.rect.top, p.rect.bottom) 
    #buat peluru
   def shoot(self):
        bullet = Bullet(picture='pngegg.png', x=self.rect.right, y=self.rect.centery, width=15, height=20, speed=15)
        bullets.add(bullet)
        
# class enemy / musuh
class Enemy(GameSprite):
    side = 'left' # menentukan sekarang gerak ke kanan atau kiri

    # constructor
    def __init__(self, picture, x, y, width, height, speed):
        GameSprite.__init__(self, picture, x, y, width, height)
        self.speed = speed # untuk geraknya musuh

    # untuk gerak kanan - kiri
    def update(self): # bisanya update
        # dia gerak ke kanan kalo udah natap tembok
        if self.rect.x <= 390 : # jarak x wall + width wall
            self.side = 'right'
        # gerak ke kiri kalo udah sampe edge
        if self.rect.x >= window_width - 85:
            self.side = 'left'
        
        # untuk gerak sesuai side
        if self.side == 'left': # side kiri --> gerak ke kiri
            self.rect.x -= self.speed
        else: # side kanan --> gerak ke kanan
            self.rect.x += self.speed
                
# class bullet / peluru
class Bullet(GameSprite):
    # constructor
    def __init__(self, picture, x, y, width, height, speed):
        GameSprite.__init__(self, picture, x, y, width, height)
        self.speed = speed

    # buat dia gerak
    def update(self):
        self.rect.x += self.speed
        # kalo sampe edge dia hilang
        if self.rect.x > window_width:
            self.kill() # biar dia hilang

        
#nambahin warna untuk kotaknya
warna =(161, 73, 133)

run = True
finish = False 

rect1 = Rectangle(color=warna, x=230, y=150, width=300, height=50)
rect2 = Rectangle(color=warna, x=350, y=150, width=60, height=320)
walls = sprite.Group()
#dinding agar tidak keluar dari background
walls.add(rect1)
walls.add(rect2)
circle1 = Circle(color=warna , radius=40, x=400, y=100)
player1 = Player(picture='Pacman 2 Icon - Classic Games Icons.jpg', height=80, width=80, x=20, y=380, x_speed=0, y_speed=0)
#buat karakter jahat
obs1 = GameSprite(height=200, width=70, picture='packman_icon-icons.com_54382.png', x=100, y=100)
#untuk mengakhiri game 

finish_obj = GameSprite(picture='pngwing.com.png', height=80, width=80, x=window_width-100, y=window_height-100)
#musuh
enemy1 = Enemy(picture='packman_icon-icons.com_54382.png', height=70, width=70, x=window_width-80, y=200, speed=5)
enemy2 = Enemy(picture='packman_icon-icons.com_54382.png', height=70, width=70, x=window_width-80, y=280, speed=5)

# group musuh
enemies = sprite.Group()
enemies.add(enemy1)
enemies.add(enemy2)

# peluru
bullets = sprite.Group()
#enemy_obj = GameSprite(picture='packman_icon-icons.com_54382.png', height=70, width=70, x=300, y=300)

#untuk bisa keluar
while run:
    #untuk peluru dan lawan melambat
    time.delay(50)
    for e in event.get():
        if e.type == QUIT:
            run = False
            
        #untuk gerakin objeknya  
        elif e.type == KEYDOWN:
        
            if e.key == K_UP: #atas
                player1.y_speed -= 8
            elif e.key == K_DOWN: #bawah
                player1.y_speed += 8
            elif e.key == K_RIGHT: #kanan
                player1.x_speed += 8
            elif e.key == K_LEFT: #kiri
                player1.x_speed -= 8
            elif e.key == K_SPACE:
                player1.shoot()
        elif e.type == KEYUP:
           if e.key == K_LEFT:
               player1.x_speed = 0
           elif e.key == K_RIGHT:
               player1.x_speed = 0
           elif e.key == K_UP:
               player1.y_speed = 0
           elif e.key == K_DOWN:
               player1.y_speed = 0
               
    if not finish:
        # nampilin gambarnya sebagai background
        window.blit(bg_image, (0,0))  
#nampilin kotaknya
        rect1.display()    
        rect2.display()
        bullets.update() # buat nampilin pelurunya 
        bullets.draw(window) # buat nampilin semua pelurunya
        circle1.display()
        
        #enemy1.display()
        finish_obj.display()
        
        player1.display()
        player1.update()
        
        enemies.update()
        enemies.draw(window) # untuk nampilin semua enemies
        
        # peluru nyentuh musuh
        sprite.groupcollide(enemies, bullets, True, True) # True --> hilang
        # peluru nyentuh dinding
        sprite.groupcollide(bullets, walls, True, False)
    
    # nyentuh musuh
        if sprite.spritecollide(player1, enemies, False): # kalah 
            finish = True
            img = image.load('gallery.jpg')
            window.fill((255, 255, 255))
            window.blit(transform.scale(img, (window_width, window_height)), (0, 0))

        # nyentuh finish
    if sprite.collide_rect(player1, finish_obj): # menang
            finish = True
            img = image.load('30073178_1385272921579182_5253827170990513237_o.jpg')
            window.fill((255, 255, 255))
            window.blit(transform.scale(img, (window_width, window_height)), (0, 0))


    display.update()