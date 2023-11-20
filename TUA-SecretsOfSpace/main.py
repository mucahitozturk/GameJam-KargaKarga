import pygame
import sys
import random

# Pygame'ı başlat
pygame.init()

# Ekran boyutları
screen_width = 990
screen_height = 540

# Arkaplan boyutları
background_width = 1885
background_height = 3651

# Renkler
white = (255, 255, 255)
red = (255, 0, 0)

# Oyun ekranını oluştur
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("SECRETS OF SPACE")

# Uzay gemisi
spaceship_image = pygame.image.load("assets/gemi.png")
spaceship_rect = spaceship_image.get_rect()
spaceship_rect.center = (screen_width // 2, screen_height - 50)

# Düşmanlar (gezegenleri düşman olarak kullanalım)
enemy_image_1 = pygame.image.load("assets/dusman.png")
enemy_image_2 = pygame.image.load("assets/dusman_2.png")
enemy_image_3 = pygame.image.load("assets/dusman_3.png")
meteor_image = pygame.image.load("demir.png")

rehber_image = pygame.image.load("assets/interface/rehber/rehber (1).jpg")

# Arkaplan
background_start = pygame.image.load("assets/start.png")

background_image = pygame.image.load("assets/space_background.jpg")
background_y = 0

class Enemy:
    def __init__(self, x, y,speed=0):
        self.rect = pygame.Rect(x, y, 50, 50)
        self.health = 5
        self.destroy_timer = 0
        self.explosion_timer = 0
        self.exterminate=False
        if speed==0:
            self.speed = random.randrange(2, 4)  # Düşman hızı
        else:
            self.speed=speed
        self.fire_chance = 0.01  # Ateş etme olasılığı
        self.bullets = []  # Düşman ateşleri

    def update(self):
        global aldigimizGezegenler
        if self.destroy_timer == 0:
            self.rect.y += self.speed
            if  self.rect.y > screen_height: 
                if self.exterminate:
                    enemies.remove(self)
                else:
                    self.rect.y = random.randint(-200, -50)
                    self.rect.x = random.randint(0, screen_width - 50)
                    if len(aldigimizGezegenler)<=1:
                        self.health = 5
                        self.fire_chance += 0.00001
                    elif len(aldigimizGezegenler)<=4:
                        self.health = 8
                        self.fire_chance += 0.00005
                    elif len(aldigimizGezegenler)<=10:
                        self.health = 10
                        self.fire_chance += 0.0001
                    
                    self.fire_chance += 0.001
        else:
            self.destroy_timer -= 1
            if self.destroy_timer == 0:
                enemies.remove(self)

        # Rastgele ateş etme kontrolü
        if random.random() < self.fire_chance:
            if self.speed<=7:
                self.fire_bullet() 

    def fire_bullet(self):
        bullet_rect = pygame.Rect(self.rect.centerx, self.rect.bottom, 10, 20)
        self.bullets.append(bullet_rect)


class Gezegen:
    def __init__(self, x, y, gezegen_adi):
        self.rect = pygame.Rect(x, y, 50, 50)
        self.gezegen_adi = gezegen_adi

    def update(self):
        self.rect.y += 2  # Gezegenlerin hareket hızı
        if self.rect.y > screen_height: 
            gezeneler.remove(self)
            print(f"{self.gezegen_adi} geldi!")

gezegenKusat=False
class Menu:
    def __init__(self): 
        self.font = pygame.font.Font(None, 36)
        self.menu_active = False
        self.menu_options = []
        self.selected_option = 0 
        self.startMenu=True
    def display_menu(self,):
        if self.startMenu:
            self.menu_options = [
            {"text": "Başla", "image": pygame.image.load("assets/interface/startBtn.jpg")}, 
            {"text": "Rehber", "image": pygame.image.load("assets/interface/rehberBtn.jpg")}
            ]
        else:
            self.menu_options =  [
            {"text": "Ele Geçir", "image": pygame.image.load("assets/interface/eleGecirBtn.jpg")},
            {"text": "Maden Topla", "image": pygame.image.load("assets/interface/madenToplaBtn.jpg")},
            {"text": "Çıkış", "image": pygame.image.load("assets/interface/cikisBtn.jpg")}
        ]
        menu_height = len(self.menu_options) * 90
        menu_y = screen_height // 2 - menu_height // 2

        for i, option in enumerate(self.menu_options):
            image = option["image"]
            option_rect = image.get_rect(center=(screen_width // 2, menu_y + i * 90))
            screen.blit(image, option_rect)
            # Seçilen opsiyonu vurgula
            if i == self.selected_option:
                pygame.draw.rect(screen, red, option_rect, 1)
    
    def handle_menu_input(self):
        global gezegenKusat, stage, backgroundSpeed
        if self.menu_active == True:
            
            keys = pygame.key.get_pressed()
            mouse_x, mouse_y = pygame.mouse.get_pos()
            
            mouse_click, _, _ = pygame.mouse.get_pressed()        
            if keys[pygame.K_UP] and self.selected_option > 0:
                self.selected_option -= 1
            elif keys[pygame.K_DOWN] and self.selected_option < len(self.menu_options) - 1:
                self.selected_option += 1
            elif keys[pygame.K_RETURN] or (mouse_click and self.is_mouse_over_option(mouse_x, mouse_y)):
                selected_text = self.menu_options[self.selected_option]["text"]
                if selected_text == "Maden Topla":
                    print("Maden Toplama işlemi başlatıldı.")
                    # Buraya maden toplama işlemleri ekleyebilirsiniz.
                    self.menu_active = False
                elif selected_text == "Ele Geçir":
                    print("Gezegen Ele Geçiriliyor..")
                    gezegenKusat=True
                    self.menu_active = False
                elif selected_text == "Çıkış":
                    self.menu_active = False
                elif selected_text == "Başla":
                    stage=0 
                    self.menu_active = False
                elif selected_text == "Rehber":
                    guide_images = [
                        pygame.image.load("assets/interface/rehber/rehber (1).jpg"),
                        pygame.image.load("assets/interface/rehber/rehber (2).jpg"),
                        pygame.image.load("assets/interface/rehber/rehber (3).jpg"),
                        pygame.image.load("assets/interface/rehber/rehber (4).jpg"),
                        pygame.image.load("assets/interface/rehber/rehber (5).jpg"),
                        pygame.image.load("assets/interface/rehber/rehber (6).jpg"),
                        pygame.image.load("assets/interface/rehber/rehber (7).jpg"),
                        pygame.image.load("assets/interface/rehber/rehber (8).jpg")
                    ]
                    current_image_index = 0
                    screen.blit(guide_images[current_image_index], (0, 0))
                    pygame.display.flip()  # Update the display to show the guide image  
                    while True:
                        for event in pygame.event.get():
                            if event.type == pygame.MOUSEBUTTONDOWN:
                                current_image_index += 1
                                if current_image_index >= len(guide_images):
                                    self.menu_active = False
                                    return
                                screen.blit(guide_images[current_image_index], (0, 0))
                                pygame.display.flip()  # Update the display to show the next guide image
                
            elif self.is_mouse_over_option(mouse_x, mouse_y):
                pass
            else:
                self.selected_option = -1
            #mouse üzerine gelince border çizdirme
        

    def is_mouse_over_option(self, mouse_x, mouse_y):
        for i, option in enumerate(self.menu_options):
            image = option["image"]
            option_rect = image.get_rect(center=(screen_width // 2, screen_height // 2 - len(self.menu_options) * 50 + i * 100)) 
            if option_rect.collidepoint(mouse_x, mouse_y):  
                self.selected_option = i
                return True
        return False



menu = Menu()
# Sadece bir gezegen olsun

# Ateş topu
bullet_image = pygame.image.load("assets/kursun.png")
bullet_rects = []
bullet_speed = 5

# Düşman ateş topu
enemy_bullet_image = pygame.image.load("assets/dusman_kursun.png")
enemy_bullet_rects = []
enemy_bullet_speed = 5

# Can sistemi
max_health = 30
current_health = max_health

# Font
font = pygame.font.Font(None, 36)

# Düşmanlara ateş etme fonksiyonu
def fire_bullet(x, y):
    bullet_rects.append(pygame.Rect(x, y, 10, 20))

def draw_text(text, color, x, y):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

def spriteLoad(spriteDir, spriteCount):
    sprites = [pygame.image.load(f"{spriteDir}/img_{i}.png") for i in range(spriteCount)]
    return sprites

def effect(sprites, x, y, duration):
    if duration > 0:
        original_surface = sprites[len(sprites) - duration]
        scaled_surface = pygame.transform.scale(original_surface, (350, 350))
        screen.blit(scaled_surface, (x - 130, y - 100))
        duration -= 1
    return duration

# Zamanlayıcı için değişkenler
bullet_timer = 0
bullet_cooldown = 10  # FPS'e bağlı olarak belirli aralıklarla ateş etmek için kullanılır (60 FPS'de 1 saniye)

# Patlama efekti için değişkenler
spaceship_explosion_timer = 0
explosion = spriteLoad("assets/patlama", 32)

# Ana oyun döngüsü
# Ana oyun döngüsü
clock = pygame.time.Clock()

enemies = []
gezeneler = []

gezegen_isimleri = ["venus", "mars", "ay", "merkür", "saturn", "jupiter", "neptune", "uranus"]

gezegen_adi = random.choice(gezegen_isimleri)
gezegen_gorsel = pygame.image.load(f"assets/{gezegen_adi}.png")
 
geciciGezegen=None
aldigimizGezegenler=[]

stage = -1
backgroundSpeed = 1.9
background_wait = 0


    
while True:

    if len(enemies) == 0 or stage==7:
        if stage == 0:  
            backgroundSpeed += 0.2
            background_wait += 1
            if background_wait >= 100:
                background_start=background_image
            if background_wait >= 200:
                backgroundSpeed = 1.9
                background_wait = 0
                stage = 1
        elif stage == 1:
            stage += 1
            enemies = [Enemy(random.randint(0, screen_width - 50), random.randint(-200, -50)) for _ in range(2*(len(aldigimizGezegenler)+1))]
        elif stage == 2:
            backgroundSpeed = 30
            background_wait += 1
            if background_wait >= 150:
                backgroundSpeed = 1.9
                background_wait = 0
                stage += 1
        elif stage == 3:
            gezegen_adi = random.choice(gezegen_isimleri)
            gezegen_gorsel = pygame.image.load(f"assets/{gezegen_adi}.png")
            print(gezegen_adi, stage)
            gezeneler = [Gezegen(random.randint(0, screen_width - 50), random.randint(-200, -50), gezegen_adi)]
            stage = 4
        elif stage == 4:
            if gezeneler == []:
                stage = 2
                gezeneler.clear()
            if gezegenKusat:
                geciciGezegen = gezeneler 
                gezeneler=[]
                gezegenKusat=False
                
                stage = 5
        elif stage == 5:
            enemies = [Enemy(random.randint(0, screen_width - 100), random.randint(-200, -50)) for _ in range(2*(len(aldigimizGezegenler)+1))]
            stage=6
        elif stage == 6:
            aldigimizGezegenler.append(geciciGezegen[0])
            gezegen_isimleri.remove(geciciGezegen[0].gezegen_adi)
            geciciGezegen=[]
            gezegenKusat=False
            collided_gezegen = None 
            enemies = [Enemy(random.randint(0, screen_width - 100), random.randint(-400, -50),10) for _ in range(10)]
            
            stage=7
        elif stage == 7: 
            backgroundSpeed = 30
            background_wait += 1
            if background_wait >= 500:
                backgroundSpeed = 1.9
                background_wait = 0
                stage = 3
            elif background_wait>=430:
                for enemy in enemies:
                    enemy.exterminate=True
            
            pass
            
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Menüyü kontrol et
    menu.handle_menu_input()
    if menu.menu_active:
        menu.display_menu()
        pygame.display.flip()  # Ekranı güncelle
        continue

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and spaceship_rect.top > 0:
        spaceship_rect.y -= 5
    if keys[pygame.K_s] and spaceship_rect.bottom < screen_height:
        spaceship_rect.y += 5
    if keys[pygame.K_a] and spaceship_rect.left > 0:
        spaceship_rect.x -= 5
    if keys[pygame.K_d] and spaceship_rect.right < screen_width:
        spaceship_rect.x += 5

    # Arkaplanı hareket ettir
    background_y += backgroundSpeed
    if background_y >= background_height:
        background_y = 0

    # Ateş topunu gönderme kontrolü
    bullet_timer += 1
    if keys[pygame.K_SPACE] and bullet_timer >= bullet_cooldown:
        fire_bullet(spaceship_rect.centerx, spaceship_rect.top)
        bullet_timer = 0  # Zamanlayıcıyı sıfırla

    # Düşmanların hareketi, ateş etmeleri ve sınır kontrolü
    for enemy in enemies:
        enemy.update()
        enemy.explosion_timer = effect(explosion, enemy.rect.x, enemy.rect.y, enemy.explosion_timer)

    # Gezegenlerin hareketi
    if gezeneler != []:
        for gezegen in gezeneler:
            gezegen.update()
            if spaceship_rect.colliderect(gezegen.rect):
                if collided_gezegen != gezegen:
                    menu.menu_active = True
                    print("Gezegen çarptı!")
                    collided_gezegen = gezegen
            else:
                collided_gezegen = None

    if menu.menu_active:
        menu.display_menu()
        menu.handle_menu_input()
    else:
        pass

    # Ateş topu hareketi ve çarpışma kontrolü
    for bullet_rect in bullet_rects:
        bullet_rect.y -= bullet_speed
        if bullet_rect.y < 0:
            bullet_rects.remove(bullet_rect)
        for enemy in enemies:
            if bullet_rect.colliderect(enemy.rect):
                enemy.health -= 1
                try:
                    bullet_rects.remove(bullet_rect)
                except:
                    pass
                if enemy.health <= 0:
                    enemy.destroy_timer = 15  # 3 saniye (60 FPS * 3 saniye)
                    enemy.explosion_timer = 31  # Patlama animasyonu süresi (60 FPS * 0.53 saniye)

    # Düşman ateş topu hareketi ve çarpışma kontrolü
    for enemy in enemies:
        for enemy_bullet_rect in enemy.bullets:
            enemy_bullet_rect.y += enemy_bullet_speed
            if enemy_bullet_rect.colliderect(spaceship_rect):
                current_health -= 1
                enemy.bullets.remove(enemy_bullet_rect)
                if current_health <= 0:
                    pygame.quit()
                    sys.exit()
            if enemy_bullet_rect.y > screen_height:
                try:
                    enemy.bullets.remove(enemy_bullet_rect)
                except:
                    pass
        #çarpışırsak canımız azalacak
        if spaceship_rect.colliderect(enemy.rect):
            current_health -= 1 
            enemy.health =-2
            enemy.rect.y -=60
            enemy.destroy_timer = 15
            enemy.explosion_timer = 31 
            if current_health <= 0:
                pygame.quit()
                sys.exit()
            

    # Ekranı temizle
    screen.fill((0, 0, 0))

    # Arkaplanı çiz
    screen.blit(background_image, (0, background_y - background_height))
    screen.blit(background_start, (0, background_y))

    # Uzay gemisini, düşmanları, gezegenleri ve ateş topunu ekrana çiz
    screen.blit(spaceship_image, spaceship_rect)
    for enemy in enemies:
        if stage==7:
            screen.blit(meteor_image, enemy.rect)
        else:
            if len(aldigimizGezegenler)<=1:
                screen.blit(enemy_image_1, enemy.rect)
            elif len(aldigimizGezegenler)<=4:
                screen.blit(enemy_image_2, enemy.rect)
            elif len(aldigimizGezegenler)<=10:
                screen.blit(enemy_image_3, enemy.rect)
            
        for enemy_bullet_rect in enemy.bullets:
            screen.blit(enemy_bullet_image, enemy_bullet_rect)
        enemy.explosion_timer = effect(explosion, enemy.rect.x, enemy.rect.y, enemy.explosion_timer)

    for bullet_rect in bullet_rects:
        screen.blit(bullet_image, bullet_rect)

    for gezegen in gezeneler:
        screen.blit(gezegen_gorsel, gezegen.rect)

    # Can miktarını ekrana yazdır
    draw_text(f"Can: {current_health}/{max_health}", white, 10, 10)
    draw_text(f"Gezegenlerimiz: {(len(aldigimizGezegenler))} Adet", white, 10, 40)
    # Ekranı güncelle
    pygame.display.flip()
    
    if  stage==-1:
        backgroundSpeed=0
        menu.menu_active = True 
        menu.startMenu=True
    else:
        menu.startMenu=False
    # FPS ayarı
    clock.tick(60)

