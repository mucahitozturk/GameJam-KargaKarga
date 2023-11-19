import pygame
import sys
import random

# Pygame'ı başlat
pygame.init()

# Ekran boyutları
screen_width = 800
screen_height = 600

# Arkaplan boyutları
background_width = 1885
background_height = 3651

# Renkler
white = (255, 255, 255)
red = (255, 0, 0)

# Oyun ekranını oluştur
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Uzay Gemisi Oyunu")

# Uzay gemisi
spaceship_image = pygame.image.load("assets/gemi.png")
spaceship_rect = spaceship_image.get_rect()
spaceship_rect.center = (screen_width // 2, screen_height - 50)

# Düşmanlar (gezegenleri düşman olarak kullanalım)
enemy_image = pygame.image.load("assets/dusman.png")

# Arkaplan
background_image = pygame.image.load("assets/space_background.jpg")
background_y = 0

gezegen_image = pygame.image.load("assets/gezegen.png")

# Düşman sınıfı
class Enemy:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 50, 50)
        self.health = 5
        self.destroy_timer = 0
        self.explosion_timer = 0
        self.speed = random.randint(1, 3)  # Düşman hızı
        self.fire_chance = 0.005  # Ateş etme olasılığı
        self.bullets = []  # Düşman ateşleri

    def update(self):
        if self.destroy_timer == 0:
            self.rect.y += self.speed
            if self.rect.y > screen_height:
                self.rect.y = random.randint(-200, -50)
                self.rect.x = random.randint(0, screen_width - 50)
                self.health = 5
                self.fire_chance = 0.005
        else:
            self.destroy_timer -= 1
            if self.destroy_timer == 0:
                enemies.remove(self)

        # Rastgele ateş etme kontrolü
        if random.random() < self.fire_chance:
            self.fire_bullet()

    def fire_bullet(self):
        bullet_rect = pygame.Rect(self.rect.centerx, self.rect.bottom, 10, 20)
        self.bullets.append(bullet_rect)


# Gezegen sınıfı
class Gezegen:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 50, 50)
        # Diğer gezegen özelliklerini ekleyebilirsiniz.

    def update(self):
        self.rect.y += 2  # Gezegenlerin hareket hızı
        if self.rect.y > screen_height:
            self.rect.y = random.randint(-200, -50)
            self.rect.x = random.randint(0, screen_width - 50)


# Düşmanlar ve gezegenler listesi
enemies = [Enemy(random.randint(0, screen_width - 50), random.randint(-200, -50)) for _ in range(3)]
gezeneler = []

# Ateş topu
bullet_image = pygame.image.load("assets/kursun.png")
bullet_rects = []
bullet_speed = 5

# Düşman ateş topu
enemy_bullet_image = pygame.image.load("assets/dusman_kursun.png")
enemy_bullet_rects = []
enemy_bullet_speed = 5

# Can sistemi
max_health = 10
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

# Harita butonu sınıfı
class MapButton:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.image.load("bos.jpg")  # Harita butonu resmi

    def draw(self):
        screen.blit(self.image, self.rect)

# Harita görüntüsü
map_image = pygame.image.load("bos.jpg")

# Harita butonu oluştur
map_button = MapButton(screen_width - 480, 100, 20, 10)  # Konumu ve boyutu değiştirildi



# Zamanlayıcı için değişkenler
bullet_timer = 0
bullet_cooldown = 10  # FPS'e bağlı olarak belirli aralıklarla ateş etmek için kullanılır (60 FPS'de 1 saniye)

# Patlama efekti için değişkenler
spaceship_explosion_timer = 0
explosion = spriteLoad("assets/patlama", 32)

# Ana oyun döngüsü
clock = pygame.time.Clock()

stage = 0
backgroundSpeed = 2
background_wait = 0
while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Sol fare tuşuna basıldığını kontrol et
                if map_button.rect.collidepoint(event.pos):  # Eğer fare tıklaması harita butonuna denk geliyorsa
                    # Harita görüntüsünü ekrana çiz
                    screen.fill((0, 0, 0))
                    screen.blit(map_image, (0, 0))
                    pygame.display.flip()
                    pygame.time.delay(3000)  # Harita görüntüsünü 3 saniye boyunca göster (isteğe bağlı)


    if len(enemies) == 0:
        if stage == 0:
            stage += 1
            enemies = [Enemy(random.randint(0, screen_width - 50), random.randint(-200, -50)) for _ in range(3)]
        elif stage == 1:
            stage += 1
            enemies = [Enemy(random.randint(0, screen_width - 50), random.randint(-200, -50)) for _ in range(2)]
        elif stage == 2:
            backgroundSpeed = 30
            background_wait += 1
            if background_wait >= 150:
                backgroundSpeed = 2
                stage += 1
        elif stage == 3:
            # Bu kısımda gezegenler gelmeye başlayacak ve artık düşman olmayacak
            gezeneler = [Gezegen(random.randint(0, screen_width - 50), random.randint(-200, -50)) for _ in range(3)]

    for gezegen in gezeneler:
        screen.blit(gezegen_image, gezegen.rect)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

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
    for gezegen in gezeneler:
        gezegen.update()

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

    # Ekranı temizle
    screen.fill((0, 0, 0))

    # Arkaplanı çiz
    screen.blit(background_image, (0, background_y - background_height))
    screen.blit(background_image, (0, background_y))

    # Uzay gemisini, düşmanları, gezegenleri ve ateş topunu ekrana çiz
    screen.blit(spaceship_image, spaceship_rect)
    for enemy in enemies:
        screen.blit(enemy_image, enemy.rect)
        for enemy_bullet_rect in enemy.bullets:
            screen.blit(enemy_bullet_image, enemy_bullet_rect)
        enemy.explosion_timer = effect(explosion, enemy.rect.x, enemy.rect.y, enemy.explosion_timer)

    for bullet_rect in bullet_rects:
        screen.blit(bullet_image, bullet_rect)

    for gezegen in gezeneler:
        screen.blit(enemy_image, gezegen.rect)

    # Can miktarını ekrana yazdır
    draw_text(f"Can: {current_health}/{max_health}", red, 10, 10)

    # Harita butonunu çiz
    map_button.draw()

    # Ekranı güncelle
    pygame.display.flip()

    # FPS ayarı
    clock.tick(60)
